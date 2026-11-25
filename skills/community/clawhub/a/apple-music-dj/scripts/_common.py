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
import signal
import stat
import subprocess
import sys
import tempfile
import time
from typing import Any, Literal, overload
from datetime import datetime, UTC
from pathlib import Path
import contextlib

# ── Python version guard ──────────────────────────────────────────
_MIN_PYTHON = (3, 11)
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
# Names follow Apple Music's genre list. A name not listed here falls back to the
# listed genre it ends with (see base_genre): "Garage Rock" → Rock.
GENRE_ENERGY = {
    # rock / metal / punk
    "Metal": 0.95, "Hardcore": 0.95, "Punk": 0.9, "Grunge": 0.8, "Hard Rock": 0.85, "Emo": 0.75,
    "Rock": 0.7, "Alternative": 0.6, "Indie Rock": 0.6, "Prog-Rock/Art Rock": 0.6, "Psychedelic": 0.55,
    "Indie": 0.5, "Soft Rock": 0.4, "Pop/Rock": 0.65, "Adult Alternative": 0.5, "College Rock": 0.6,
    # electronic
    "Dance": 0.85, "Electronic": 0.8, "House": 0.8, "Techno": 0.85, "Trance": 0.85, "Dubstep": 0.9,
    "Drum & Bass": 0.9, "Hardstyle": 0.95, "Electronica": 0.65, "IDM": 0.55, "Downtempo": 0.3,
    "Lo-Fi": 0.2, "Ambient": 0.1, "Chill": 0.25,
    # hip-hop / r&b
    "Hip-Hop/Rap": 0.75, "Trap": 0.8, "Drill": 0.8, "Alternative Rap": 0.65, "Grime": 0.8,
    "R&B/Soul": 0.5, "Contemporary R&B": 0.5, "Neo-Soul": 0.4, "Soul": 0.5, "Funk": 0.65,
    "Disco": 0.75, "Motown": 0.6,
    # pop
    "Pop": 0.7, "K-Pop": 0.75, "J-Pop": 0.7, "Synth Pop": 0.65, "Indie Pop": 0.45, "Teen Pop": 0.7,
    "Dance Pop": 0.8, "Anime": 0.65,
    # country / folk
    "Country": 0.45, "Contemporary Country": 0.55, "Americana": 0.4, "Bluegrass": 0.45, "Folk": 0.3,
    "Singer/Songwriter": 0.3, "Acoustic": 0.35,
    # jazz / blues
    "Jazz": 0.3, "Smooth Jazz": 0.25, "Big Band": 0.55, "Bebop": 0.45, "Blues": 0.45, "Bossa Nova": 0.35,
    "Lounge": 0.25,
    # latin / world / reggae
    "Latin": 0.7, "Reggaeton": 0.8, "Urbano latino": 0.8, "Salsa y Tropical": 0.75, "Afrobeats": 0.75,
    "Afro-Beat": 0.75, "Reggae": 0.5, "Dancehall": 0.75, "World": 0.5,
    # classical / quiet
    "Classical": 0.2, "Opera": 0.35, "Baroque": 0.3, "Chamber Music": 0.2, "Soundtrack": 0.4,
    "Easy Listening": 0.25, "Vocal": 0.3, "New Age": 0.1, "Meditation": 0.05,
    # other
    "Christian & Gospel": 0.55, "Gospel": 0.6, "Fitness & Workout": 0.9, "Holiday": 0.5,
    "Christmas": 0.5, "Children's Music": 0.55,
}
# Short names inside compound genres that stand for a listed genre ("Underground Rap" → Hip-Hop/Rap)
GENRE_ALIASES = {"rap": "Hip-Hop/Rap", "hip-hop": "Hip-Hop/Rap", "hip hop": "Hip-Hop/Rap",
                 "r&b": "R&B/Soul", "edm": "Dance", "lofi": "Lo-Fi", "christian": "Christian & Gospel"}
HIGH_ENERGY = 0.7
LOW_ENERGY = 0.3

# Genres in the same family get half credit when tastes and tracks are compared.
# A genre not listed here is placed by its base_genre.
GENRE_ADJACENCY = {
    "rock_family": {"Rock", "Alternative", "Indie", "Punk", "Metal", "Grunge", "Hard Rock", "Indie Rock",
                    "Emo", "Hardcore", "Soft Rock", "Pop/Rock", "Prog-Rock/Art Rock", "Psychedelic",
                    "Adult Alternative", "College Rock"},
    "electronic_family": {"Electronic", "Dance", "House", "Techno", "Ambient", "IDM", "Trance", "Dubstep",
                          "Drum & Bass", "Hardstyle", "Electronica", "Downtempo", "Lo-Fi", "Chill"},
    "hiphop_family": {"Hip-Hop/Rap", "R&B/Soul", "Funk", "Trap", "Drill", "Alternative Rap", "Grime",
                      "Contemporary R&B", "Neo-Soul"},
    "folk_family": {"Folk", "Singer/Songwriter", "Country", "Americana", "Bluegrass", "Acoustic",
                    "Contemporary Country"},
    "jazz_family": {"Jazz", "Blues", "Bossa Nova", "Soul", "Smooth Jazz", "Big Band", "Bebop", "Lounge",
                    "Motown"},
    "classical_family": {"Classical", "Soundtrack", "New Age", "Opera", "Baroque", "Chamber Music",
                         "Easy Listening", "Meditation"},
    "pop_family": {"Pop", "Synth Pop", "Indie Pop", "K-Pop", "J-Pop", "Teen Pop", "Dance Pop", "Disco",
                   "Anime"},
    "latin_family": {"Latin", "Reggaeton", "Urbano latino", "Salsa y Tropical", "Bossa Nova"},
    "caribbean_african_family": {"Reggae", "Dancehall", "Afrobeats", "Afro-Beat", "World"},
}
_GENRE_FAMILIES = [{g.lower() for g in family} for family in GENRE_ADJACENCY.values()]
_KNOWN_GENRES = {g.lower(): g for g in GENRE_ENERGY} | GENRE_ALIASES
_KNOWN_GENRE_PATTERNS = [
    (re.compile(rf"(?<![a-z0-9]){re.escape(name)}(?![a-z0-9])"), canonical)
    for name, canonical in sorted(_KNOWN_GENRES.items(), key=lambda kv: -len(kv[0]))
]
SUBGENRE_PROXIMITY = 0.75  # "Garage Rock" vs "Rock": closer than a family match, short of exact
# Listed genres that are scenes of their own, not a sub-genre of the word they end with
SELF_ROOTED_GENRES = {"K-Pop", "J-Pop", "Afro-Beat"}

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
    "avoid_repeat_days": 30,
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


def _stream_target(path: Path) -> Path | None:
    """The device `path` stands for if it is (or links to) a stream; None for ordinary paths.

    A symlink to anything else is refused: we never write through one.
    """
    if path.is_symlink():
        target = path.resolve()
        if _is_stream(target):
            return target
        raise OSError(errno.ELOOP, f"Refusing to write through the symlink {path}; pass the real path instead.")
    return path if _is_stream(path) else None


def write_private(path, text: str) -> None:
    """Write `text` to `path` readable by the owner only, replacing it atomically.

    - The text goes to an owner-only temp file in the same directory, is fsync'ed, then
      `os.replace`d over the target, so a crash or a concurrent run never leaves a truncated
      file: readers see the old content or the new, never half of either.
    - New parent directories are 0700, and our own ~/.apple-music-dj directories are
      tightened to 0700.
    - The target is validated *before* anything is written: a symlink (or a file owned by
      someone else) is refused rather than replaced.
    - Stream devices are the one exception, since `/dev/stdout` is itself a symlink on Linux;
      they are written directly and left untouched (no replace, no chmod).
    """
    path = Path(path)
    tighten_app_dir(path)
    ensure_private_dir(path.parent, tighten=path.parent == APP_DIR or APP_DIR in path.parent.parents)
    stream = _stream_target(path)
    if stream is not None:
        # No O_TRUNC and O_NOFOLLOW, then check what we really opened: if the device was swapped for
        # a regular file or symlink after _stream_target looked, refuse instead of truncating it.
        fd = os.open(str(stream), os.O_WRONLY | os.O_NOFOLLOW)
        try:
            if stat.S_ISREG(os.fstat(fd).st_mode) or stat.S_ISDIR(os.fstat(fd).st_mode):
                raise OSError(errno.ELOOP, f"{path} changed while opening it; refusing to write to it.")
            with os.fdopen(fd, "w") as f:
                fd = -1
                f.write(text)
        finally:
            if fd != -1:
                os.close(fd)
        return
    with contextlib.suppress(FileNotFoundError):
        if os.lstat(path).st_uid != os.getuid():
            raise PermissionError(errno.EPERM, f"{path} is owned by another user; refusing to overwrite it.")
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")  # created 0600
    try:
        with os.fdopen(fd, "w") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(tmp_name)
        raise


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


def _signal_group(proc: subprocess.Popen, sig: int) -> None:
    """Send `sig` to the child's whole process group (the script, its pipelines and its curl)."""
    with contextlib.suppress(ProcessLookupError, PermissionError):
        os.killpg(proc.pid, sig)


def _run_with_term_grace(cmd: list[str], timeout: float, grace: float = 5) -> subprocess.CompletedProcess:
    """Like subprocess.run(timeout=...), but ends a stuck child with SIGTERM before SIGKILL.

    subprocess.run kills with SIGKILL, which bash can't trap, so apple_music_api.sh would
    leave its token-bearing temp files behind. SIGTERM lets its cleanup trap run first.

    The child runs in its own process group and the signals go to the whole group: killing
    only the shell would leave a curl or a sibling script holding the output pipes open, and
    the final read would block past the timeout. That read is bounded too.
    """
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                            start_new_session=True)
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except BaseException as e:  # a timeout, or Ctrl-C: the child is in another group and won't see it
        _signal_group(proc, signal.SIGTERM)
        try:
            proc.communicate(timeout=grace)
        except subprocess.TimeoutExpired:
            _signal_group(proc, signal.SIGKILL)
            with contextlib.suppress(subprocess.TimeoutExpired):  # a process outside the group holds the pipes
                proc.communicate(timeout=grace)
        if isinstance(e, subprocess.TimeoutExpired):
            raise subprocess.TimeoutExpired(cmd, timeout) from None
        raise
    return subprocess.CompletedProcess(cmd, proc.returncode, stdout, stderr)


def run_script(script: str, *args: str, timeout: float = 30) -> subprocess.CompletedProcess:
    """Run a sibling shell script from scripts/ and capture its output.

    The one place the Python scripts shell out: SIGTERM-first timeouts (see _run_with_term_grace),
    stdout/stderr captured as text, tokens never on the command line (the shell scripts read them
    from the environment). Writes still need the caller's explicit `--yes` argument. Raises
    subprocess.TimeoutExpired on timeout and OSError if the script can't be run.
    """
    if Path(script).name != script:
        raise ValueError(f"run_script takes a bare script name from scripts/, not {script!r}")
    return _run_with_term_grace([str(SCRIPT_DIR / script), *args], timeout=timeout)


@overload
def call_api(command: str, *args: str, raw: Literal[True]) -> str | None:
    """With raw=True: stdout as a stripped string (None on failure)."""
@overload
def call_api(command: str, *args: str, raw: Literal[False] = False) -> Any:
    """Otherwise: the parsed JSON (None on failure)."""
def call_api(command: str, *args: str, raw: bool = False) -> Any:
    """Call apple_music_api.sh and parse JSON output.

    If raw=True, return stdout as a stripped string instead of parsing JSON.
    """
    try:
        result = run_script(API_SCRIPT.name, command, *args)
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
    when = when or datetime.now(UTC)
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
    today = datetime.now(UTC).date()
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


def _rightmost_genre(name: str, skip_whole: bool) -> str | None:
    """The listed genre whose whole-word match ends furthest right in `name` (longest on a tie)."""
    best: tuple[int, int, str] | None = None
    for pattern, canonical in _KNOWN_GENRE_PATTERNS:
        for m in pattern.finditer(name):
            if skip_whole and m.start() == 0 and m.end() == len(name):
                continue
            key = (m.end(), m.end() - m.start(), canonical)
            if best is None or key[:2] > best[:2]:
                best = key
    return best[2] if best else None


def base_genre(genre: str) -> str | None:
    """The listed genre a name is or ends with: "Rock" → Rock, "Garage Rock" → Rock,
    "Underground Rap" → Hip-Hop/Rap. In English compounds the last word names the kind,
    so the match ending furthest right wins. None if nothing matches."""
    name = genre.strip().lower()
    return _KNOWN_GENRES.get(name) or _rightmost_genre(name, skip_whole=False)


def root_genre(genre: str) -> str | None:
    """Like base_genre, but reduced until it stops changing: "Hard Rock" → Rock,
    "Modern Hard Rock" → Hard Rock → Rock, "Contemporary R&B" → R&B/Soul → Soul.
    A plain listed genre and SELF_ROOTED_GENRES are their own roots."""
    root = base_genre(genre)
    seen: set[str] = set()
    while root and root not in SELF_ROOTED_GENRES and root not in seen:
        seen.add(root)
        parent = _rightmost_genre(root.lower(), skip_whole=True)
        if not parent:
            break
        root = parent
    return root


def genre_energy(genre: str) -> float | None:
    """0-1 energy for one genre, via base_genre for names GENRE_ENERGY doesn't list."""
    base = base_genre(genre)
    return GENRE_ENERGY.get(base) if base else None


def track_energy(genres: list[str]) -> float:
    """Average 0-1 energy of a track's genres (0.5 when none are recognised)."""
    known = [e for e in (genre_energy(g) for g in genres) if e is not None]
    return sum(known) / len(known) if known else 0.5


def _families(genre: str) -> list[int]:
    """Indexes of the families a genre belongs to (directly, else through its base genre)."""
    name = genre.lower()
    found = [i for i, family in enumerate(_GENRE_FAMILIES) if name in family]
    if not found and (base := base_genre(genre)):
        found = [i for i, family in enumerate(_GENRE_FAMILIES) if base.lower() in family]
    return found


def genre_proximity(genre_a: str, genre_b: str) -> float:
    """Score genre proximity: 1.0 exact, 0.75 same root genre ("Hard Rock" / "Rock" /
    "Garage Rock"), 0.5 same family, 0.0 different."""
    a, b = genre_a.lower(), genre_b.lower()
    if a == b:
        return 1.0
    root_a, root_b = root_genre(genre_a), root_genre(genre_b)
    if root_a and root_a == root_b:
        return SUBGENRE_PROXIMITY
    if set(_families(genre_a)) & set(_families(genre_b)):
        return 0.5
    return 0.0


def best_genre_match(track_genres: list[str], target_genres: list[str]) -> float:
    """Best proximity score between any track genre and any target genre."""
    return max((genre_proximity(tg, target) for tg in track_genres for target in target_genres), default=0.0)


def taste_affinity(track_genres: list[str], genre_distribution: list[dict]) -> float:
    """How much a listener likes a track's sound, 0-1.

    The best proximity between any of the track's genres and any of the listener's,
    scaled by that genre's weight relative to their top genre. So an exact match on
    the top genre is 1.0, while an exact match on a genre at 2% of the listening (top
    genre 40%) is only 0.05. `best_genre_match` treats both the same. A profile without
    weights counts every genre equally.
    """
    weights = [(g["genre"], max(g.get("weight") or 0, 0)) for g in genre_distribution if g.get("genre")]
    if not any(w for _, w in weights):
        weights = [(name, 1.0) for name, _ in weights]
    top = max((w for _, w in weights), default=0)
    if top <= 0:
        return 0.0
    return max((genre_proximity(t, name) * w / top for t in track_genres for name, w in weights), default=0.0)


# ── User preferences applied to every playlist ───────────────────

PREFERRED_GENRE_BOOST = 0.1


def _rater(profile: dict, who: str) -> dict:
    """One listener's ratings and play weights, as the filters use them."""
    return {
        "who": who,
        "signals": profile.get("rating_signals") or {},
        "play_weights": {a["name"].lower(): a.get("play_weight", 0) for a in profile.get("top_artists", [])
                         if a.get("name")},
    }


CLEAN_LOOKUP_LIMIT = 15  # catalog searches per run spent looking for clean versions of explicit songs


def user_filters(config: dict, recent_track_ids: set[str] | None = None, profile: dict | None = None,
                 profile_b: dict | None = None, *, clean_only: bool | None = None,
                 storefront: str | None = None, include_library: bool = False) -> dict:
    """The parts of config.json, recent playlist history and ratings that every strategy honours.

    `profile_b` is the second listener of a blend: both listeners' ratings count.
    `clean_only` (default: config.json's `clean_only`) keeps explicit songs out; it needs
    `storefront` to look up clean versions.
    """
    raters = [_rater(p, who) for p, who in ((profile, "you"), (profile_b, "they")) if p]
    excluded = {a.lower() for a in config.get("excluded_artists") or [] if isinstance(a, str)}
    # An artist a listener disliked enough is left out, like excluded_artists, unless that
    # listener plays them a lot or the other listener likes them (then they're only scored
    # down, in apply_user_filters)
    for rater in raters:
        others = [r for r in raters if r is not rater]
        for key in rating_summary_keys(rater["signals"])["demoted"]:
            liked_elsewhere = any((r["signals"].get("artists") or {}).get(key, {}).get("likes") for r in others)
            if rater["play_weights"].get(key, 0) < FAVOURITE_PLAY_WEIGHT and not liked_elsewhere:
                excluded.add(key)
    return {
        "excluded_artists": excluded,
        "preferred_genres": [g for g in config.get("preferred_genres") or [] if isinstance(g, str)],
        "recent_track_ids": set(recent_track_ids or ()),
        "raters": raters,
        # ids a clean-version swap must not introduce: dislikes (either listener) and, unless the run
        # allows them, songs already in the library. Strategies add their own (the seed, a playlist's tracks).
        "blocked_ids": {tid for p in (profile, profile_b) if p
                        for tid in (p.get("disliked_song_ids") or []) + ([] if include_library
                                                                          else p.get("library_song_ids") or [])},
        "clean_only": config.get("clean_only") is True if clean_only is None else clean_only,
        "storefront": storefront,
        "clean_lookups_left": CLEAN_LOOKUP_LIMIT,
        "clean_cache": {},
    }


def passes_user_filters(candidate: dict, filters: dict | None) -> bool:
    """False for an excluded artist, a track used in a recent DJ playlist, or (clean mode) an explicit song."""
    if not filters:
        return True
    if filters.get("clean_only") and candidate.get("explicit"):
        return False
    return (candidate.get("artist", "").lower() not in (filters.get("excluded_artists") or set())
            and candidate.get("id") not in (filters.get("recent_track_ids") or set()))


def swap_explicit_for_clean(candidate: dict, filters: dict | None) -> dict:
    """In clean mode, replace an explicit song with its clean version when the catalog has one.

    The clean version is the same title by the same artist whose `contentRating` isn't explicit.
    One catalog search per distinct song, at most CLEAN_LOOKUP_LIMIT per run; anything not
    swapped stays explicit and is dropped by passes_user_filters.
    """
    if not filters or not filters.get("clean_only") or not candidate.get("explicit") or not filters.get("storefront"):
        return candidate
    name, artist = candidate.get("name", ""), candidate.get("artist", "")
    key = (name.lower(), artist.lower())
    cache: dict = filters.setdefault("clean_cache", {})
    if key not in cache:
        if filters.get("clean_lookups_left", 0) <= 0 or not name or not artist:
            return candidate
        filters["clean_lookups_left"] -= 1
        found = call_api("search", filters["storefront"], f"{name} {artist}", "songs")
        cache[key] = next((s for s in ((found or {}).get("results", {}).get("songs", {}) or {}).get("data", [])
                           if s.get("attributes", {}).get("name", "").lower() == key[0]
                           and s.get("attributes", {}).get("artistName", "").lower() == key[1]
                           and s.get("attributes", {}).get("contentRating") != "explicit"), None)
    clean = cache[key]
    blocked = (filters.get("blocked_ids") or set()) | (filters.get("recent_track_ids") or set())
    if not clean or clean.get("id") in blocked:
        return candidate
    attrs = clean.get("attributes", {})
    return {**candidate, "id": clean.get("id", candidate.get("id")), "explicit": False,
            "album": attrs.get("albumName", candidate.get("album", "")),
            "duration_ms": attrs.get("durationInMillis", candidate.get("duration_ms")),
            "reason": f"{candidate.get('reason', '')} (clean version)".strip()}


def apply_user_filters(candidates: list[dict], filters: dict | None) -> list[dict]:
    """Drop excluded artists and recently used tracks; nudge preferred genres up; let your
    likes and dislikes steer.

    Candidates with a ``_score`` get ``PREFERRED_GENRE_BOOST`` scaled by how well they
    match a preferred genre (half for a family match), plus ``rating_adjustment`` for the
    artist and genres each listener has rated (summed), noted in the track's ``reason``.
    """
    if not filters:
        return candidates
    preferred = filters.get("preferred_genres") or []
    raters = filters.get("raters") or []
    kept = []
    seen_ids: set[str] = set()
    for c in candidates:
        c = swap_explicit_for_clean(c, filters)
        if not passes_user_filters(c, filters):
            continue
        if filters.get("clean_only") and c.get("id"):  # an explicit song and its clean twin become one entry
            if c["id"] in seen_ids:
                continue
            seen_ids.add(c["id"])
        if "_score" in c:
            if preferred:
                c["_score"] += PREFERRED_GENRE_BOOST * best_genre_match(c.get("genre", []), preferred)
            artist = c.get("artist", "")
            notes = []
            for rater in raters:
                adjustment, note = rating_adjustment(artist, c.get("genre", []), rater["signals"],
                                                     rater["play_weights"].get(artist.lower(), 0), rater["who"])
                c["_score"] += adjustment
                notes += [note] if note else []
            if notes:
                c["reason"] = f"{c.get('reason', '')} ({'; '.join(notes)})".strip()
        kept.append(c)
    return kept


# ── Rating signals: likes and dislikes steer every strategy ──────
# A dislike always removes that one song. These act on the artist and genres around it,
# and stay bounded: one dislike changes nothing at artist level. An artist with
# DISLIKES_TO_DEMOTE dislikes and no likes is left out of playlists, unless you play them
# a lot (play weight >= FAVOURITE_PLAY_WEIGHT): then they're only scored down.

DISLIKES_TO_DEMOTE = 2            # dislikes (and no likes) before an artist is demoted
ARTIST_DISLIKE_PENALTY = 0.5      # larger than most score gaps, so a demoted artist rarely makes the cut
FAVOURITE_PLAY_WEIGHT = 0.05      # artists at or above this play weight ...
FAVOURITE_PENALTY_FACTOR = 0.5    # ... get only this share of the penalty
LIKE_BOOST_PER_SONG, LIKE_BOOST_MAX = 0.05, 0.15          # per net like for the artist
GENRE_LIKE_BOOST_PER_SONG, GENRE_LIKE_BOOST_MAX = 0.02, 0.1  # per net like for the genre


def _plural(n: int, word: str) -> str:
    return f"{n} {word}" + ("" if n == 1 else "s")


def _recount(signals: dict) -> dict:
    """Rebuild the artist and genre counts from the per-song ratings (returns the same dict)."""
    artists: dict = {}
    genres: dict = {}
    for song in (signals.get("songs") or {}).values():
        field = {1: "likes", -1: "dislikes"}.get(song.get("value"))
        if not field:
            continue
        if song.get("artist"):
            entry = artists.setdefault(song["artist"].lower(), {"name": song["artist"], "likes": 0, "dislikes": 0})
            entry[field] += 1
        for genre in song.get("genres", []):
            genres.setdefault(genre, {"likes": 0, "dislikes": 0})[field] += 1
    signals["artists"], signals["genres"] = artists, genres
    return signals


def set_song_rating(signals: dict, song_id: str, value: int, attrs: dict | None = None) -> dict:
    """Set one song's rating (1 like, -1 dislike, 0 cleared) and recount. Returns the same dict.

    Each song keeps its own artist and genres under ``songs``, and the counts are always
    rebuilt from those, so clearing a song removes exactly what it contributed. A song
    whose details aren't known (`attrs` None and never seen) can't contribute and is skipped.
    """
    songs = signals.setdefault("songs", {})
    if value == 0:
        songs.pop(song_id, None)
    elif attrs and attrs.get("artistName"):
        songs[song_id] = {"value": value, "artist": attrs["artistName"],
                          "genres": filter_generic_genres(attrs.get("genreNames", []))}
    elif song_id in songs:
        songs[song_id]["value"] = value
    return _recount(signals)


def rating_signals_from(rated: list[tuple[str, int, dict]]) -> dict:
    """Ratings signals from (song ID, value, song attributes) triples."""
    signals: dict = {"songs": {}, "artists": {}, "genres": {}}
    for song_id, value, attrs in rated:
        set_song_rating(signals, song_id, value, attrs)
    return signals


def rating_adjustment(artist: str, genres: list[str], signals: dict,
                      play_weight: float = 0.0, who: str = "you") -> tuple[float, str | None]:
    """Score change from one listener's ratings, and a note for the track's reason (None if nothing applies)."""
    adjustment, note = 0.0, None
    entry = (signals.get("artists") or {}).get(artist.lower())
    if entry:
        likes, dislikes = entry.get("likes", 0), entry.get("dislikes", 0)
        if dislikes >= DISLIKES_TO_DEMOTE and not likes:
            factor = FAVOURITE_PENALTY_FACTOR if play_weight >= FAVOURITE_PLAY_WEIGHT else 1.0
            adjustment -= ARTIST_DISLIKE_PENALTY * factor
            note = f"demoted: {who} disliked {_plural(dislikes, 'song')} by {entry.get('name', artist)}"
        elif likes > dislikes:
            adjustment += min(LIKE_BOOST_PER_SONG * (likes - dislikes), LIKE_BOOST_MAX)
            note = f"boosted: {who} liked {_plural(likes, 'song')} by {entry.get('name', artist)}"
    genre_table = signals.get("genres") or {}
    net = max((genre_table[g].get("likes", 0) - genre_table[g].get("dislikes", 0) for g in genres if g in genre_table),
              default=0)
    if net > 0:
        adjustment += min(GENRE_LIKE_BOOST_PER_SONG * net, GENRE_LIKE_BOOST_MAX)
    return adjustment, note


def rating_summary_keys(signals: dict) -> dict[str, list[str]]:
    """Lower-cased artist keys your ratings boost or demote."""
    boosted, demoted = [], []
    for key, entry in (signals.get("artists") or {}).items():
        likes, dislikes = entry.get("likes", 0), entry.get("dislikes", 0)
        if dislikes >= DISLIKES_TO_DEMOTE and not likes:
            demoted.append(key)
        elif likes > dislikes:
            boosted.append(key)
    return {"boosted": boosted, "demoted": demoted}


def rating_summary(*all_signals: dict) -> dict:
    """Artists the ratings currently boost or demote (any listener's), for a playlist's summary."""
    summary: dict[str, set[str]] = {"boosted_artists": set(), "demoted_artists": set()}
    for signals in all_signals:
        artists = signals.get("artists") or {}
        for kind, keys in rating_summary_keys(signals).items():
            summary[f"{kind}_artists"] |= {artists[k].get("name", k) for k in keys}
    return {kind: sorted(names) for kind, names in summary.items()}


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
        "generated_at": profile.get("generated_at") or datetime.now(UTC).isoformat(),
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
