#!/usr/bin/env python3
"""
_common.py — Shared utilities for Apple Music DJ scripts.

Provides call_api(), load_profile(), search helpers, and token utilities
used across all scripts.
"""

import base64
import hashlib
import errno
import json
import os
import re
import stat
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
import contextlib

# ── Python version guard ──────────────────────────────────────────
_MIN_PYTHON = (3, 10)
if sys.version_info < _MIN_PYTHON:
    sys.exit(
        f"ERROR: Python {_MIN_PYTHON[0]}.{_MIN_PYTHON[1]}+ is required "
        f"(you have {sys.version_info.major}.{sys.version_info.minor}). "
        f"Please upgrade Python."
    )

# Genres that Apple Music puts on everything — filter these out of scoring
GENERIC_GENRES = {"music"}

# Rough 0-1 energy per genre. >=0.7 counts as high-energy, <=0.3 as low-energy
# (see taste_profiler.infer_energy_profile); everything else is mid-range.
GENRE_ENERGY = {
    "Metal": 0.95, "Punk": 0.9, "Dance": 0.85, "Electronic": 0.8, "House": 0.8,
    "Techno": 0.85, "Grunge": 0.8, "Hip-Hop/Rap": 0.75, "Rock": 0.7, "Pop": 0.7,
    "K-Pop": 0.75, "J-Pop": 0.7, "Synth Pop": 0.65, "Funk": 0.65, "Alternative": 0.6,
    "IDM": 0.55, "Indie": 0.5, "R&B/Soul": 0.5, "Soul": 0.5, "Blues": 0.45,
    "Country": 0.45, "Indie Pop": 0.45, "Americana": 0.4, "Bluegrass": 0.45,
    "Soundtrack": 0.4, "Bossa Nova": 0.35, "Acoustic": 0.35,
    "Jazz": 0.3, "Folk": 0.3, "Singer/Songwriter": 0.3, "Classical": 0.2,
    "Ambient": 0.1, "New Age": 0.1,
}
HIGH_ENERGY = 0.7
LOW_ENERGY = 0.3

SCRIPT_DIR = Path(__file__).parent
API_SCRIPT = SCRIPT_DIR / "apple_music_api.sh"

APP_DIR = Path.home() / ".apple-music-dj"
DEFAULT_CONFIG_PATH = APP_DIR / "config.json"

SNAPSHOT_DIR = Path.home() / ".apple-music-dj" / "snapshots"
MAX_SNAPSHOTS = 52

DEFAULT_CONFIG = {
    "default_storefront": "auto",
    "preferred_genres": [],
    "excluded_artists": [],
    "playlist_size": 30,
    "cache_ttl_hours": 168,
}


def load_config(path: str | None = None) -> dict:
    """Load user configuration from JSON, falling back to defaults.

    If no path is given, looks at ~/.apple-music-dj/config.json.
    Missing keys are filled with defaults; missing file returns all defaults.
    """
    config = dict(DEFAULT_CONFIG)
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
    if not config_path.exists():
        return config
    try:
        with open(config_path) as f:
            user_config = json.load(f)
        if not isinstance(user_config, dict):
            print(f"WARN: Config is not a JSON object: {config_path}", file=sys.stderr)
            return config
        config.update(user_config)
        return config
    except json.JSONDecodeError as e:
        print(f"WARN: Invalid JSON in config: {config_path} (line {e.lineno})", file=sys.stderr)
        return config
    except OSError as e:
        print(f"WARN: Could not read config: {e}", file=sys.stderr)
        return config


def ensure_private_dir(path, tighten: bool = False) -> Path:
    """Create `path` and any missing parents as 0700 directories.

    mkdir's `mode` only applies to the leaf (and is masked by the umask), so each missing
    level is created and chmod'ed individually. Directories that already exist are left
    alone unless `tighten` is set, and then only if we own them — we never loosen or
    chmod somebody else's directory (e.g. a user's ~/Documents).
    """
    path = Path(path)
    missing = []
    p = path
    while not p.exists() and p != p.parent:
        missing.append(p)
        p = p.parent
    for d in reversed(missing):
        try:
            d.mkdir(mode=0o700)
        except FileExistsError:
            continue
        os.chmod(d, 0o700)
    if tighten and path.is_dir() and not path.is_symlink() and path.stat().st_uid == os.getuid():
        os.chmod(path, 0o700)
    return path


def tighten_app_dir(path) -> None:
    """If `path` is inside ~/.apple-music-dj, make that directory (if we own it) owner-only too."""
    path = Path(path)
    if path == APP_DIR or APP_DIR in path.parents:
        ensure_private_dir(APP_DIR, tighten=True)


def _is_stream(path: Path) -> bool:
    """Character device, FIFO or socket (e.g. /dev/stdout resolves to one)."""
    try:
        mode = os.stat(path).st_mode
    except OSError:
        return False
    return stat.S_ISCHR(mode) or stat.S_ISFIFO(mode) or stat.S_ISSOCK(mode)


def write_private(path, text: str) -> None:
    """Write `text` to `path` readable by the owner only.

    - `os.open(..., 0o600)` only applies when a file is *created*, so a pre-existing file is
      fchmod'ed too. New parent directories are 0700, and our own ~/.apple-music-dj
      directories are tightened to 0700.
    - The target is validated *before* anything destructive happens: it is opened without
      O_TRUNC and with O_NOFOLLOW, and only truncated once fstat shows a regular file we own.
      A symlink (or a file owned by someone else) is refused rather than truncated/chmod'ed.
    - Stream devices are the one exception, since `/dev/stdout` is itself a symlink on Linux;
      they are opened directly and left untouched (no truncate, no chmod).
    """
    path = Path(path)
    tighten_app_dir(path)
    ensure_private_dir(path.parent, tighten=path.parent == APP_DIR or APP_DIR in path.parent.parents)
    try:
        fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    except OSError as e:
        if e.errno != errno.ELOOP:
            raise
        target = path.resolve()
        if not _is_stream(target):
            raise OSError(errno.ELOOP, f"Refusing to write through the symlink {path}; "
                                       f"pass the real path instead.") from e
        fd = os.open(str(target), os.O_WRONLY)
    try:
        st = os.fstat(fd)
        if stat.S_ISREG(st.st_mode):
            if st.st_uid != os.getuid():
                raise PermissionError(errno.EPERM, f"{path} is owned by another user; refusing to overwrite it.")
            os.fchmod(fd, 0o600)
            os.ftruncate(fd, 0)
        with os.fdopen(fd, "w") as f:
            fd = -1  # now owned by the file object
            f.write(text)
    finally:
        if fd != -1:
            os.close(fd)


def save_config(config: dict, path: str | None = None):
    """Write config to JSON with restrictive permissions."""
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
    write_private(config_path, json.dumps(config, indent=2) + "\n")


def require_env_tokens():
    """Verify Apple Music tokens are set. Call before any API usage."""
    import os
    missing = []
    if not os.environ.get("APPLE_MUSIC_DEV_TOKEN"):
        missing.append("APPLE_MUSIC_DEV_TOKEN")
    if not os.environ.get("APPLE_MUSIC_USER_TOKEN"):
        missing.append("APPLE_MUSIC_USER_TOKEN")
    if missing:
        print(f"ERROR: Missing env vars: {', '.join(missing)}", file=sys.stderr)
        print("  Set them up in one step: python3 scripts/setup_auth.py (see references/auth-setup.md)", file=sys.stderr)
        print("  Or try it first with no tokens: python3 scripts/demo.py tour", file=sys.stderr)
        sys.exit(1)


def call_api(command: str, *args, raw: bool = False) -> dict | list | str | None:
    """Call apple_music_api.sh and parse JSON output.

    If raw=True, return stdout as a stripped string instead of parsing JSON.
    """
    cmd = [str(API_SCRIPT), command] + list(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            stderr_msg = result.stderr.strip()
            if stderr_msg:
                print(f"WARN: API call '{command}' failed: {stderr_msg}", file=sys.stderr)
            return None
        if raw:
            return result.stdout.strip()
        return json.loads(result.stdout)
    except FileNotFoundError:
        print(f"ERROR: API script not found: {API_SCRIPT}", file=sys.stderr)
        print("  Ensure apple_music_api.sh is in the scripts/ directory.", file=sys.stderr)
        return None
    except subprocess.TimeoutExpired:
        print(f"WARN: API call timed out: {command} {' '.join(args)}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print(f"WARN: Malformed JSON from API call: {command}", file=sys.stderr)
        return None


def load_profile(path: str) -> dict:
    """Load a taste profile JSON with user-friendly error handling."""
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Profile not found: {path}", file=sys.stderr)
        print("  Run the taste profiler first: python3 scripts/taste_profiler.py", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in profile: {path}", file=sys.stderr)
        print(f"  Parse error at line {e.lineno}, column {e.colno}", file=sys.stderr)
        print("  Try regenerating: python3 scripts/taste_profiler.py --max-age 0", file=sys.stderr)
        sys.exit(1)


def search_artist(sf: str, name: str) -> dict | None:
    """Search for an artist by name and return the top match."""
    result = call_api("search", sf, name, "artists")
    if not result:
        return None
    artists = result.get("results", {}).get("artists", {}).get("data", [])
    return artists[0] if artists else None


def search_album(sf: str, query: str) -> dict | None:
    """Search for an album by name and return the top match."""
    result = call_api("search", sf, query, "albums")
    if not result:
        return None
    albums = result.get("results", {}).get("albums", {}).get("data", [])
    return albums[0] if albums else None


def filter_generic_genres(genres: list[str]) -> list[str]:
    """Remove generic genres like 'Music' that Apple puts on everything."""
    return [g for g in genres if g.lower() not in GENERIC_GENRES]


def check_token_expiry(warn_days: int = 14) -> dict | None:
    """Check the dev token JWT exp claim and return status.

    Returns a dict with keys: expired (bool), days_remaining (int|None),
    warning (bool), message (str). Returns None if token is not set or
    cannot be decoded.
    """
    token = os.environ.get("APPLE_MUSIC_DEV_TOKEN", "")
    if not token:
        return None

    try:
        # JWT is header.payload.signature — decode the payload (middle segment)
        parts = token.split(".")
        if len(parts) != 3:
            return None
        # Add padding for base64
        payload_b64 = parts[1]
        padding = 4 - len(payload_b64) % 4
        if padding != 4:
            payload_b64 += "=" * padding
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        exp = payload.get("exp")
        if exp is None:
            return None

        now = time.time()
        remaining_secs = exp - now
        days_remaining = int(remaining_secs / 86400)

        if remaining_secs <= 0:
            return {
                "expired": True,
                "days_remaining": 0,
                "warning": True,
                "message": "⛔ Dev token has EXPIRED. Regenerate with: python3 scripts/setup_auth.py --new-dev-token",
            }
        elif days_remaining <= warn_days:
            return {
                "expired": False,
                "days_remaining": days_remaining,
                "warning": True,
                "message": f"⚠️  Dev token expires in {days_remaining} day(s). Regenerate: python3 scripts/setup_auth.py --new-dev-token",
            }
        else:
            return {
                "expired": False,
                "days_remaining": days_remaining,
                "warning": False,
                "message": f"✅ Dev token valid for {days_remaining} more day(s).",
            }
    except Exception:
        return None


# ── Music User Token age ─────────────────────────────────────────
# The user token is opaque (no expiry inside it) and Apple doesn't say when it lapses, so we note
# when we first saw it — by a short SHA-256 fingerprint, never the token itself — and warn as it
# nears the ~6 months these tokens usually last.

USER_TOKEN_SEEN = APP_DIR / "user_token_seen.json"
USER_TOKEN_LIFETIME_DAYS = 180


def user_token_fingerprint(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()[:16]


def record_user_token(token: str, path: Path | None = None, when: datetime | None = None) -> None:
    """Remember today (or `when`) as the day this user token was issued or first seen."""
    when = when or datetime.now(timezone.utc)
    write_private(Path(path) if path else USER_TOKEN_SEEN,
                  json.dumps({"fingerprint": user_token_fingerprint(token),
                              "first_seen": when.date().isoformat()}) + "\n")


def check_user_token_age(warn_days: int = 14, path: Path | None = None) -> dict | None:
    """Estimate how long the current APPLE_MUSIC_USER_TOKEN has left.

    Returns {age_days, days_left, warning, message}, or None when there is no token, in demo
    mode, or the record can't be read or written. A token we haven't seen before is recorded
    as new today.
    """
    token = os.environ.get("APPLE_MUSIC_USER_TOKEN", "")
    if not token or os.environ.get("APPLE_MUSIC_DJ_DEMO"):
        return None
    path = Path(path) if path else USER_TOKEN_SEEN
    today = datetime.now(timezone.utc).date()
    try:
        seen = json.loads(path.read_text()) if path.is_file() else {}
        if not isinstance(seen, dict) or seen.get("fingerprint") != user_token_fingerprint(token):
            record_user_token(token, path)
            seen = {"first_seen": today.isoformat()}
        first = datetime.strptime(seen["first_seen"], "%Y-%m-%d").date()
    except (OSError, ValueError, KeyError, TypeError):
        return None
    age = max((today - first).days, 0)
    left = USER_TOKEN_LIFETIME_DAYS - age
    if left <= warn_days:
        message = (f"⚠️  Your Apple Music user token is about {age} days old and these usually last ~6 months. "
                   f"If requests start failing with HTTP 403, renew it: python3 scripts/setup_auth.py")
    else:
        message = f"✅ User token first seen {age} day(s) ago (roughly {left} days left)."
    return {"age_days": age, "days_left": left, "warning": left <= warn_days, "message": message}


STOREFRONT_CACHE = Path.home() / ".apple-music-dj" / "storefront.cache"


def get_storefront(override: str | None = None) -> str:
    """Get storefront code with auto-detection and caching.

    Priority: explicit override > env var > cache > API detection > 'us' fallback.
    """
    if override and override != "auto":
        return override

    # Check env var
    env_sf = os.environ.get("APPLE_MUSIC_STOREFRONT", "")
    if env_sf:
        return env_sf

    # Check cache (an unreadable cache just means we detect from the API below)
    with contextlib.suppress(OSError):
        if STOREFRONT_CACHE.exists():
            cached = STOREFRONT_CACHE.read_text().strip()
            if len(cached) == 2 and cached.isalpha():
                return cached

    # Auto-detect from API
    result = call_api("user-storefront", raw=True)
    if isinstance(result, str) and len(result) == 2 and result.isalpha():
        # Cache the result
        with contextlib.suppress(OSError):
            write_private(STOREFRONT_CACHE, result + "\n")
        return result

    print(
        "⚠ Could not detect storefront, defaulting to 'us'. "
        "Set APPLE_MUSIC_STOREFRONT or use --storefront to override.",
        file=sys.stderr,
    )
    return "us"


def get_album_tracks(sf: str, album_id: str) -> list:
    """Fetch tracks for an album, returning a flat list of track dicts."""
    detail = call_api("album-tracks", sf, album_id)
    if not detail or "data" not in detail:
        return []
    tracks = []
    for album_data in detail.get("data", []):
        track_rel = album_data.get("relationships", {}).get("tracks", {}).get("data", [])
        tracks.extend(track_rel)
    return tracks


def track_energy(genres: list[str]) -> float:
    """Average 0-1 energy of a track's genres (0.5 when none are recognised)."""
    known = [GENRE_ENERGY[g] for g in genres if g in GENRE_ENERGY]
    return sum(known) / len(known) if known else 0.5


# ── Taste snapshots (for drift tracking) ─────────────────────────

def make_snapshot(profile: dict) -> dict:
    """Compact, ID-free copy of a profile that is safe to keep long-term."""
    return {
        "top_artists": [
            {"name": a.get("name", ""), "weight": a.get("play_weight", a.get("count", 0))}
            for a in profile.get("top_artists", [])[:20]
        ],
        "genre_distribution": [
            {"genre": g.get("genre", ""), "weight": g.get("weight", 0)}
            for g in profile.get("genre_distribution", [])
        ],
        "era_distribution": [
            {"decade": e.get("decade", ""), "weight": e.get("weight", 0)}
            for e in profile.get("era_distribution", [])
        ],
        "energy_profile": profile.get("energy_profile", "balanced"),
        "variety_score": profile.get("variety_score", 0.5),
        "mainstream_score": profile.get("mainstream_score", 0.5),
        "generated_at": profile.get("generated_at") or datetime.now(timezone.utc).isoformat(),
    }


def save_snapshot(profile: dict, directory: Path | None = None) -> Path:
    """Write today's snapshot (one per day) with 0600 perms, keeping the newest MAX_SNAPSHOTS."""
    directory = Path(directory) if directory else SNAPSHOT_DIR
    snap = make_snapshot(profile)
    path = directory / f"{snap['generated_at'][:10]}.json"
    write_private(path, json.dumps(snap, indent=2))
    for old in sorted(directory.glob("????-??-??.json"))[:-MAX_SNAPSHOTS]:
        old.unlink(missing_ok=True)
    return path


def list_snapshots(directory: Path | None = None) -> list[tuple[str, Path]]:
    """All snapshots as (YYYY-MM-DD, path), oldest first."""
    directory = Path(directory) if directory else SNAPSHOT_DIR
    return [(p.stem, p) for p in sorted(directory.glob("????-??-??.json"))
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.stem)]
