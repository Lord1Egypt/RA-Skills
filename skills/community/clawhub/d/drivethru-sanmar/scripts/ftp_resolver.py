"""Resolve marketing color names to SanMar mainframe color codes.

SanMar's web-service inventory and pricing endpoints query against
the *mainframe* color (an abbreviated code such as ``BLACK`` or
``ATHHTHR``). The mainframe code often differs from the marketing
``COLOR_NAME`` shown in catalogs (``Athletic Heather``). When a tool
queries with the marketing name SanMar returns ``Invalid style
specified`` or an empty result.

The mapping lives in ``SanMarPDD/SanMar_SDL_N.csv`` on SanMar's SFTP
server. This module downloads that CSV (with on-disk caching since it
only changes daily), then looks up rows by ``STYLE#`` plus a fuzzy
match on ``COLOR_NAME`` and an optional ``SIZE`` filter, and returns
the ``SANMAR_MAINFRAME_COLOR`` value (along with ``INVENTORY_KEY`` /
``SIZE_INDEX`` / ``UNIQUE_KEY`` so callers can skip a follow-up
pricing call).

Connection details from the SanMar FTP Integration Guide v23.1:
``Host: ftp.sanmar.com``, ``Port: 2200``, protocol ``SFTP``. The
username is your SanMar customer number; the password is FTP-specific
(NOT the SanMar.com web-services password).
"""

from __future__ import annotations

import csv
import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from schemas import (  # noqa: E402  (sibling module, scripts dir on sys.path)
    MainframeColorMatch,
    MainframeColorResolution,
    SanMarFTPCredentials,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class SanMarFTPError(Exception):
    """Raised when the SanMar FTP server cannot be reached or read."""


class SanMarFTPConfigError(SanMarFTPError):
    """Missing or invalid FTP credentials."""


# ---------------------------------------------------------------------------
# Paths / config
# ---------------------------------------------------------------------------


SDL_REMOTE_PATH = "/SanMarPDD/SanMar_SDL_N.csv"
DEFAULT_CACHE_DIR = Path(os.environ.get("SANMAR_FTP_CACHE_DIR") or "/tmp/sme-sanmar-cache")
DEFAULT_CACHE_TTL_SECONDS = 24 * 60 * 60  # SanMar refreshes the SDL nightly.


def ftp_credentials_from_env() -> SanMarFTPCredentials:
    """Optional fallback: load FTP credentials from environment variables.

    The supported runtime pattern is for the agent to collect FTP
    credentials from the user and pass an explicit
    :class:`SanMarFTPCredentials` object into every tool call. This
    helper is the optional cache layer — used only when the caller
    did not pass credentials directly. Raises
    :class:`SanMarFTPConfigError` if no env-var fallback is
    configured; the agent should treat that error as a signal to ask
    the user for the FTP password (which is distinct from the
    sanmar.com / web-services password).

    Recognized vars (all optional):
      ``SANMAR_FTP_USERNAME`` — defaults to ``SANMAR_CUSTOMER_NUMBER``.
      ``SANMAR_FTP_PASSWORD``
      ``SANMAR_FTP_HOST`` — defaults to ``ftp.sanmar.com``.
      ``SANMAR_FTP_PORT`` — defaults to ``2200``.
    """

    username = (
        os.getenv("SANMAR_FTP_USERNAME", "").strip()
        or os.getenv("SANMAR_CUSTOMER_NUMBER", "").strip()
    )
    password = os.getenv("SANMAR_FTP_PASSWORD", "").strip()
    host = os.getenv("SANMAR_FTP_HOST", "ftp.sanmar.com").strip() or "ftp.sanmar.com"
    port_raw = os.getenv("SANMAR_FTP_PORT", "2200").strip() or "2200"
    try:
        port = int(port_raw)
    except ValueError as exc:
        raise SanMarFTPConfigError(f"SANMAR_FTP_PORT must be an integer, got {port_raw!r}") from exc

    missing: list[str] = []
    if not username:
        missing.append("FTP username (SanMar customer number)")
    if not password:
        missing.append("FTP password (separate from the web-services password)")
    if missing:
        raise SanMarFTPConfigError(
            "SanMar FTP credentials were not provided. Ask the user for "
            + " and ".join(missing)
            + " and supply them either via the SANMAR_FTP_USERNAME / "
            "SANMAR_FTP_PASSWORD environment variables or as the "
            "customer_number / ftp_password fields in the tool's stdin JSON."
        )
    return SanMarFTPCredentials(username=username, password=password, host=host, port=port)


# ---------------------------------------------------------------------------
# CSV download + cache
# ---------------------------------------------------------------------------


@dataclass
class _CachedFile:
    path: Path
    fetched_at: float


def _cache_path(cache_dir: Path) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / "SanMar_SDL_N.csv"


def _is_cache_fresh(path: Path, ttl: int) -> bool:
    if not path.is_file():
        return False
    age = time.time() - path.stat().st_mtime
    return age < ttl


def _download_sdl(
    credentials: SanMarFTPCredentials,
    dest: Path,
    *,
    timeout: int = 60,
) -> None:
    """Download ``SanMar_SDL_N.csv`` over SFTP into ``dest`` atomically."""

    try:
        import paramiko
    except ImportError as exc:  # pragma: no cover — runtime guard
        raise SanMarFTPError(
            "paramiko is required for SanMar SFTP access. "
            "Install it with `pip install paramiko`."
        ) from exc

    logger.info(
        "Connecting to SanMar SFTP %s:%s as %s",
        credentials.host,
        credentials.port,
        credentials.username,
    )
    transport = paramiko.Transport((credentials.host, credentials.port))
    try:
        transport.connect(username=credentials.username, password=credentials.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        if sftp is None:
            raise SanMarFTPError("Could not open SFTP channel after authenticating")
        try:
            sftp.get_channel().settimeout(timeout)
            tmp = dest.with_suffix(dest.suffix + ".part")
            sftp.get(SDL_REMOTE_PATH, str(tmp))
            tmp.replace(dest)
        finally:
            sftp.close()
    except paramiko.SSHException as exc:
        raise SanMarFTPError(f"SanMar SFTP error: {exc}") from exc
    except OSError as exc:
        raise SanMarFTPError(f"Failed to download {SDL_REMOTE_PATH}: {exc}") from exc
    finally:
        transport.close()


def fetch_sdl_csv(
    credentials: SanMarFTPCredentials | None = None,
    *,
    cache_dir: Path | str | None = None,
    cache_ttl_seconds: int = DEFAULT_CACHE_TTL_SECONDS,
    force_refresh: bool = False,
) -> Path:
    """Return a local path to a fresh copy of ``SanMar_SDL_N.csv``.

    Downloads via SFTP if the on-disk cache is missing or stale.
    Idempotent: callers may invoke this repeatedly. Set
    ``force_refresh=True`` to bypass the cache.
    """

    creds = credentials or ftp_credentials_from_env()
    cache_root = Path(cache_dir) if cache_dir else DEFAULT_CACHE_DIR
    target = _cache_path(cache_root)

    if not force_refresh and _is_cache_fresh(target, cache_ttl_seconds):
        return target

    _download_sdl(creds, target)
    return target


# ---------------------------------------------------------------------------
# Lookup
# ---------------------------------------------------------------------------


def _normalize(value: str | None) -> str:
    if not value:
        return ""
    return "".join(ch for ch in value.lower() if ch.isalnum())


def _row_color_matches(row_color: str, requested_color: str) -> bool:
    """Match policy: case/whitespace-insensitive equality, then containment.

    SanMar's COLOR_NAME column uses title-cased marketing names like
    "Athletic Heather"; the user may type "athletic heather", "ATHLETIC
    HEATHER", or even "Athletic-Heather". Containment fallback handles
    minor variations like "Heather Black" vs "Black Heather".
    """

    a = _normalize(row_color)
    b = _normalize(requested_color)
    if not a or not b:
        return False
    if a == b:
        return True
    return a in b or b in a


def _row_size_matches(row_size: str, requested_size: str | None) -> bool:
    if not requested_size:
        return True
    return _normalize(row_size) == _normalize(requested_size)


def lookup_mainframe_color(
    style: str,
    color: str,
    size: str | None = None,
    *,
    credentials: SanMarFTPCredentials | None = None,
    csv_path: Path | str | None = None,
    cache_dir: Path | str | None = None,
    cache_ttl_seconds: int = DEFAULT_CACHE_TTL_SECONDS,
    force_refresh: bool = False,
) -> MainframeColorResolution:
    """Resolve a marketing color to its SanMar mainframe color code.

    Returns a :class:`MainframeColorResolution` with status:

    - ``"matched"``: exactly one mainframe color found.
    - ``"ambiguous"``: multiple mainframe colors match — caller should
      ask the user to disambiguate. ``matches`` is populated.
    - ``"not_found"``: nothing matched. The caller should surface this
      to the user verbatim.
    """

    if not style:
        raise ValueError("style is required")
    if not color:
        raise ValueError("color is required")

    if csv_path is None:
        path = fetch_sdl_csv(
            credentials=credentials,
            cache_dir=cache_dir,
            cache_ttl_seconds=cache_ttl_seconds,
            force_refresh=force_refresh,
        )
    else:
        path = Path(csv_path)
        if not path.is_file():
            raise SanMarFTPError(f"SDL CSV not found at {path}")

    style_norm = _normalize(style)
    matches: list[MainframeColorMatch] = []
    seen: set[tuple[str, str]] = set()

    with path.open("r", encoding="utf-8", errors="replace", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            row_style = row.get("STYLE#") or row.get("STYLE")
            if not row_style or _normalize(row_style) != style_norm:
                continue
            row_color_name = (row.get("COLOR_NAME") or "").strip()
            mainframe_color = (row.get("SANMAR_MAINFRAME_COLOR") or "").strip()
            if not mainframe_color:
                continue
            if not _row_color_matches(row_color_name, color):
                continue
            row_size = (row.get("SIZE") or "").strip()
            if not _row_size_matches(row_size, size):
                continue
            key = (mainframe_color, row_size)
            if key in seen:
                continue
            seen.add(key)
            matches.append(
                MainframeColorMatch(
                    style=row_style.strip(),
                    requested_color=color,
                    size=row_size or None,
                    mainframe_color=mainframe_color,
                    color_name=row_color_name,
                    inventory_key=(row.get("INVENTORY_KEY") or "").strip() or None,
                    size_index=(row.get("SIZE_INDEX") or "").strip() or None,
                    unique_key=(row.get("UNIQUE_KEY") or "").strip() or None,
                )
            )

    distinct_colors = {m.mainframe_color for m in matches}
    if not matches:
        status = "not_found"
    elif len(distinct_colors) == 1:
        status = "matched"
    else:
        status = "ambiguous"

    as_of = (
        datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()
        if path.is_file()
        else None
    )
    return MainframeColorResolution(
        status=status,
        style=style,
        requested_color=color,
        size=size,
        matches=matches,
        as_of=as_of,
    )


__all__ = (
    "DEFAULT_CACHE_DIR",
    "DEFAULT_CACHE_TTL_SECONDS",
    "SDL_REMOTE_PATH",
    "SanMarFTPError",
    "SanMarFTPConfigError",
    "fetch_sdl_csv",
    "ftp_credentials_from_env",
    "lookup_mainframe_color",
)
