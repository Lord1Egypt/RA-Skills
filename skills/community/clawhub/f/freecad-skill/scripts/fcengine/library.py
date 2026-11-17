"""Parts from the official FreeCAD library (https://github.com/FreeCAD/FreeCAD-library).

Pure Python (stdlib), run by the launcher: FreeCAD's own Python may lack SSL
(the snap has no _ssl module), so the engine never touches the network.

- Search uses an index of the repository (one GitHub API call), cached in the
  workspace for a week.
- Parts are downloaded on demand into <workspace>/.fcskill/library/parts/,
  mirroring the repository layout; each file is checked against its git blob
  hash from the index, so a tampered or truncated download is rejected.
- Network goes only to api.github.com and raw.githubusercontent.com for this
  repository. FCSKILL_OFFLINE=1 disables it; FCSKILL_LIBRARY may point at a
  local clone instead (no network at all). The launcher reads these two
  settings and passes them in as a Source: this module reads no environment
  variable, and a request is built from constants and a library path only.
- Cache files are reached from the workspace folder one path component at a
  time, without following links (see _open_dir).
- Parts are CC-BY 3.0: every import carries an attribution.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import stat
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Dict, List, Optional, Tuple

from . import __version__, errors

REPO = "FreeCAD/FreeCAD-library"
BRANCH = "master"
API_TREE = f"https://api.github.com/repos/{REPO}/git/trees/{BRANCH}?recursive=1"
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/"
WEB = f"https://github.com/{REPO}/blob/{BRANCH}/"
HISTORY = f"https://github.com/{REPO}/commits/{BRANCH}/"
LICENSE = "CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)"
INDEX_TTL_S = 7 * 24 * 3600
MAX_DOWNLOAD = 60 * 1024 * 1024
# Import preference: exact B-rep exchange formats first; FCStd when nothing else exists. STL is a mesh, not a solid.
FORMATS = ("step", "stp", "brep", "brp", "iges", "igs", "fcstd")
LISTED = FORMATS + ("stl",)
CACHE_DIR = Path(".fcskill") / "library"
ENV_LOCAL = "FCSKILL_LIBRARY"
ENV_OFFLINE = "FCSKILL_OFFLINE"
# The only URLs ever fetched: this repository's index and its raw files. Nothing is sent but the request itself.
ALLOWED_PREFIXES = (f"https://api.github.com/repos/{REPO}/", RAW)
ALLOWED_HOSTS = ("api.github.com", "raw.githubusercontent.com")


def _err(code: str, msg: str, hint: str = "") -> errors.SkillError:
    return errors.SkillError(code, msg, hint=hint or None)


def _ext(path: str) -> str:
    return path.rsplit(".", 1)[-1].lower() if "." in path.rsplit("/", 1)[-1] else ""


def _safe_rel(path: str) -> str:
    p = PurePosixPath(path)
    if p.is_absolute() or any(part in ("", ".", "..") for part in p.parts):
        raise _err(errors.INVALID_PARAM, f"Invalid library path '{path}'")
    return str(p)


# ------------------------------------------------------------------ index


@dataclass(frozen=True)
class Source:
    """Where parts come from: a local clone of the library, or GitHub unless ``offline``."""

    local: Optional[Path] = None
    offline: bool = False


GITHUB = Source()


def source(local: Optional[str], offline: bool) -> Source:
    """The Source for the launcher's settings (the values of FCSKILL_LIBRARY and FCSKILL_OFFLINE)."""
    if not local:
        return Source(None, offline)
    root = Path(local).expanduser()
    if not root.is_dir():
        raise _err(
            errors.LIBRARY_UNAVAILABLE,
            f"{ENV_LOCAL} points to '{local}', which is not a folder",
            hint="Point it at a clone of https://github.com/FreeCAD/FreeCAD-library, or unset it to download parts.",
        )
    return Source(root, offline)


def _check_url(url: str) -> None:
    parts = urllib.parse.urlsplit(url)
    if not url.startswith(ALLOWED_PREFIXES) or parts.scheme != "https" or parts.hostname not in ALLOWED_HOSTS:
        raise _err(
            errors.LIBRARY_UNAVAILABLE, f"Refused to contact '{url}': only the FreeCAD library on GitHub is used"
        )


class _SameHostRedirect(urllib.request.HTTPRedirectHandler):
    """Follow redirects only to the allowed GitHub URLs."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        _check_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


USER_AGENT = f"fcskill/{__version__}"


def _get(url: str, limit: int, offline: bool) -> bytes:
    _check_url(url)
    if offline:
        raise _err(
            errors.LIBRARY_UNAVAILABLE,
            "Network access is disabled (FCSKILL_OFFLINE=1)",
            hint=f"Ask the user to unset FCSKILL_OFFLINE, or to set {ENV_LOCAL} to a local clone of the FreeCAD library.",
        )
    # No cookies, credentials or other headers: a bare anonymous GET of a fixed, allow-listed URL.
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    opener = urllib.request.build_opener(_SameHostRedirect)
    try:
        with opener.open(req, timeout=60) as resp:  # noqa: S310 - allow-listed https URLs only
            data = resp.read(limit + 1)
    except urllib.error.HTTPError as e:
        hint = (
            (
                "GitHub's anonymous API limit (60 requests/hour) may be exhausted; the index is cached for a week, so "
                "retry later or set FCSKILL_LIBRARY to a local clone."
            )
            if e.code in (403, 429)
            else ""
        )
        raise _err(errors.LIBRARY_UNAVAILABLE, f"Download failed: HTTP {e.code} for {url}", hint=hint) from None
    except (urllib.error.URLError, OSError) as e:
        raise _err(
            errors.LIBRARY_UNAVAILABLE,
            f"Cannot reach GitHub: {getattr(e, 'reason', e)}",
            hint=f"Check the network, or set {ENV_LOCAL} to a local clone of the FreeCAD library.",
        ) from None
    if len(data) > limit:
        raise _err(errors.LIBRARY_UNAVAILABLE, f"Download larger than {limit // (1024 * 1024)} MB refused: {url}")
    return data


def load_index(root: Path, refresh: bool = False, src: Source = GITHUB) -> Dict[str, Any]:
    """{"source": ..., "files": {path: {"size": n, "sha": git blob sha or None}}}."""
    local = src.local
    if local is not None:
        files = {}
        for dirpath, _dirs, names in os.walk(local):
            if ".git" in Path(dirpath).parts:
                continue
            for n in names:
                if _ext(n) in LISTED:
                    full = Path(dirpath) / n
                    files[full.relative_to(local).as_posix()] = {"size": full.stat().st_size, "sha": None}
        return {"source": str(local), "files": files}
    cache = root / CACHE_DIR / "index.json"
    cached = None if refresh else _read_cached(root, cache)
    if cached is not None and time.time() - cached[1] < INDEX_TTL_S:
        try:
            return json.loads(cached[0].decode("utf-8"))
        except ValueError:
            pass
    tree = json.loads(_get(API_TREE, 50 * 1024 * 1024, src.offline).decode("utf-8"))
    if tree.get("truncated"):
        raise _err(
            errors.LIBRARY_UNAVAILABLE,
            "GitHub returned a truncated index of the FreeCAD library",
            hint=f"Set {ENV_LOCAL} to a local clone of the library.",
        )
    files = {
        e["path"]: {"size": e.get("size", 0), "sha": e["sha"]}
        for e in tree.get("tree", [])
        if e.get("type") == "blob" and _ext(e["path"]) in LISTED
    }
    index = {"source": f"https://github.com/{REPO}", "files": files}
    _write_cached(root, cache, json.dumps(index).encode("utf-8"))
    return index


# ------------------------------------------------------------------ search


def _parts(index: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    """Part path without extension -> {format: file path}."""
    out: Dict[str, Dict[str, str]] = {}
    for path in index["files"]:
        stem = path.rsplit(".", 1)[0]
        out.setdefault(stem, {})[_ext(path)] = path
    return out


def _tokens(text: str) -> List[str]:
    return [t for t in re.split(r"[^a-z0-9]+", text.lower()) if t]


def search(index: Dict[str, Any], query: str, limit: int = 10) -> List[Dict[str, Any]]:
    words = _tokens(query)
    if not words:
        raise _err(errors.INVALID_PARAM, "Empty search", hint='Give keywords, e.g. "608 bearing" or "nema 17 motor".')
    scored = []
    for part, fmts in _parts(index).items():
        name = part.rsplit("/", 1)[-1].lower()
        hay = part.lower()
        if not all(w in hay for w in words):
            continue
        score = sum(3 if w in name else 1 for w in words) + sum(2 for w in words if w in _tokens(name))
        # A number should match as a whole number: "608" means 608ZZ, not 6082.
        score += sum(2 for w in words if w.isdigit() and re.search(r"(?<![0-9])" + w + r"(?![0-9])", name))
        importable = [f for f in FORMATS if f in fmts]
        score += 1 if "step" in fmts or "stp" in fmts else 0
        if not importable:
            score -= 5  # STL only: listed, but cannot be imported as a solid
        scored.append((-score, len(part), part, fmts, importable))
    scored.sort()
    out = []
    for _s, _l, part, fmts, importable in scored[:limit]:
        best = importable[0] if importable else None
        entry: Dict[str, Any] = {"part": part, "formats": sorted(fmts), "importable": bool(importable)}
        if best:
            entry["size_kb"] = round(index["files"][fmts[best]]["size"] / 1024)
        entry["url"] = WEB + urllib.parse.quote(fmts[best or sorted(fmts)[0]])
        out.append(entry)
    return out


# ------------------------------------------------------------------ fetch


def resolve(index: Dict[str, Any], ref: str) -> str:
    """Repository path of the file to import for a part reference (with or without extension)."""
    ref = _safe_rel(ref.strip().strip("/"))
    if ref in index["files"] and _ext(ref) in FORMATS:
        return ref
    if ref in index["files"]:
        raise _err(
            errors.UNSUPPORTED,
            f"'{ref}' is an STL mesh, not a solid",
            hint="Pick a part with a STEP, BREP, IGES or FCStd file (see 'formats' in the search results).",
        )
    fmts = _parts(index).get(ref.rsplit(".", 1)[0] if _ext(ref) in LISTED else ref)
    if not fmts:
        raise _err(
            errors.OBJECT_NOT_FOUND,
            f"No part '{ref}' in the FreeCAD library",
            hint="Use the 'part' value from 'fcskill.py library <keywords>'.",
        )
    for f in FORMATS:
        if f in fmts:
            return fmts[f]
    raise _err(
        errors.UNSUPPORTED, f"'{ref}' exists only as an STL mesh, not a solid", hint="Pick another part, or model it."
    )


def local_path(root: Path, repo_path: str) -> Path:
    return root / CACHE_DIR / "parts" / _safe_rel(repo_path)


# Cache files are read and written without following links. Checking a resolved path first is not enough:
# a link planted at .fcskill, at .fcskill/library or at any folder below would resolve consistently for the
# cache root and the file alike, and a folder can be swapped between the check and the write. So where the
# platform has descriptor-relative calls (Linux, macOS), each component is opened from its parent's
# descriptor with O_NOFOLLOW, and the file is created and renamed relative to the last descriptor.
_DIR_FD = (
    {os.open, os.mkdir, os.rename, os.unlink} <= os.supports_dir_fd
    and hasattr(os, "O_NOFOLLOW")
    and hasattr(os, "O_DIRECTORY")
)
_CLOEXEC = getattr(os, "O_CLOEXEC", 0)


def _cache_parts(root: Path, path: Path) -> Tuple[str, ...]:
    """Components of a cache path below the workspace: always .fcskill/library/..."""
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        parts = ()
    if parts[: len(CACHE_DIR.parts)] != CACHE_DIR.parts or any(p in ("", ".", "..") for p in parts):
        raise _err(errors.LIBRARY_UNAVAILABLE, f"'{path}' is not inside the library cache of {root}")
    return parts


def _link_error(root: Path, names: Tuple[str, ...]) -> errors.SkillError:
    where = Path(*names).as_posix()
    return _err(
        errors.LIBRARY_UNAVAILABLE,
        f"'{where}' in the workspace is a link or not a folder: the library cache is not used through links",
        hint=f"Remove '{root / where}' (the cache is rebuilt on demand).",
    )


def _open_dir(root: Path, names: Tuple[str, ...], create: bool) -> Optional[int]:
    """Descriptor of the folder root/names..., or None if it does not exist (and ``create`` is false).

    Each component is opened relative to its parent's descriptor and must be a real folder."""
    fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | _CLOEXEC)
    try:
        for i, name in enumerate(names):
            if create:
                try:
                    os.mkdir(name, 0o777, dir_fd=fd)
                except FileExistsError:
                    pass  # whatever is there is verified by the open below
            try:
                nxt = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | _CLOEXEC, dir_fd=fd)
            except FileNotFoundError:
                if create:
                    raise
                os.close(fd)
                return None
            except OSError:  # ELOOP or ENOTDIR: a link, or a file where a folder belongs
                raise _link_error(root, names[: i + 1]) from None
            os.close(fd)
            fd = nxt
        return fd
    except BaseException:
        os.close(fd)
        raise


def _plain_dir(root: Path, names: Tuple[str, ...], create: bool) -> Optional[Path]:
    """The same walk for platforms without descriptor-relative calls (Windows): every component is checked
    to be a real folder, not a symbolic link or junction, before the next one is entered."""
    folder = root
    for i, name in enumerate(names):
        folder = folder / name
        if create and not os.path.lexists(folder):
            folder.mkdir(exist_ok=True)
        if folder.is_symlink() or folder.is_junction():
            raise _link_error(root, names[: i + 1])
        if not os.path.lexists(folder):
            return None
        if not folder.is_dir():
            raise _link_error(root, names[: i + 1])
    return folder


def _read_cached(root: Path, path: Path) -> Optional[Tuple[bytes, float]]:
    """(content, modification time) of a cache file; None if it is absent or not a regular file (a link
    is not followed: the entry counts as missing and is rewritten)."""
    *dirs, name = _cache_parts(root, path)
    try:
        if not _DIR_FD:
            folder = _plain_dir(root, tuple(dirs), create=False)
            if folder is None or (folder / name).is_symlink() or not (folder / name).is_file():
                return None
            return (folder / name).read_bytes(), (folder / name).stat().st_mtime
        fd = _open_dir(root, tuple(dirs), create=False)
        if fd is None:
            return None
        try:
            file_fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | _CLOEXEC, dir_fd=fd)
        finally:
            os.close(fd)
        with os.fdopen(file_fd, "rb") as fh:
            info = os.fstat(fh.fileno())
            if not stat.S_ISREG(info.st_mode):
                return None
            return fh.read(), info.st_mtime
    except OSError:
        return None


def _write_cached(root: Path, dest: Path, data: bytes) -> None:
    """Write a cache file without following links, at any level: see _open_dir. The data goes to a new
    file (O_EXCL), which then replaces the directory entry itself, so a link planted at ``dest`` is replaced,
    not written through."""
    *dirs, name = _cache_parts(root, dest)
    try:
        if not _DIR_FD:
            folder = _plain_dir(root, tuple(dirs), create=True)
            assert folder is not None
            file_fd, tmp = tempfile.mkstemp(dir=folder, prefix=f".{name}.", suffix=".part")  # new file, never a link
            try:
                with os.fdopen(file_fd, "wb") as fh:
                    fh.write(data)
                os.replace(tmp, folder / name)
            except BaseException:
                Path(tmp).unlink(missing_ok=True)
                raise
            return
        fd = _open_dir(root, tuple(dirs), create=True)
        assert fd is not None
        tmp = f".{name}.{secrets.token_hex(8)}.part"
        try:
            file_fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | _CLOEXEC, 0o644, dir_fd=fd)
            try:
                with os.fdopen(file_fd, "wb") as fh:
                    fh.write(data)
                os.replace(tmp, name, src_dir_fd=fd, dst_dir_fd=fd)
            except BaseException:
                try:
                    os.unlink(tmp, dir_fd=fd)
                except OSError:
                    pass
                raise
        finally:
            os.close(fd)
    except OSError as e:
        raise _err(errors.LIBRARY_UNAVAILABLE, f"Cannot write the library cache file '{dest}': {e}") from None


def parts_folder(root: Path) -> Optional[Path]:
    """The folder of downloaded parts if it exists; refused if it is reached through a link."""
    names = _cache_parts(root, root / CACHE_DIR / "parts")
    if not _DIR_FD:
        return _plain_dir(root, names, create=False)
    try:
        fd = _open_dir(root, names, create=False)
    except OSError:
        return None
    if fd is None:
        return None
    os.close(fd)
    return root.joinpath(*names)


def attribution(repo_path: str) -> Dict[str, str]:
    name = repo_path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    return {
        "part": name,
        "source": WEB + urllib.parse.quote(repo_path),
        "license": LICENSE,
        "authors": HISTORY + urllib.parse.quote(repo_path),
        "text": f"'{name}' from the FreeCAD library ({WEB + urllib.parse.quote(repo_path)}), licensed {LICENSE}; "
        f"authors: see {HISTORY + urllib.parse.quote(repo_path)}",
    }


def _blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()  # noqa: S324 - git object id, not security


def fetch(
    root: Path, ref: str, index: Optional[Dict[str, Any]] = None, src: Source = GITHUB
) -> Tuple[Path, Dict[str, Any]]:
    """Make the part available in the workspace; returns its path and metadata (also written next to it)."""
    index = index or load_index(root, src=src)
    repo_path = resolve(index, ref)
    dest = local_path(root, repo_path)
    meta = {"library": repo_path, **attribution(repo_path)}
    entry = index["files"][repo_path]
    local = src.local
    cached = _read_cached(root, dest)
    if cached is not None and (entry["sha"] is None or _blob_sha(cached[0]) == entry["sha"]):
        pass  # cached and intact
    elif local is not None:
        part = (local / repo_path).resolve()
        if not part.is_file() or not part.is_relative_to(local.resolve()):
            raise _err(errors.LIBRARY_UNAVAILABLE, f"'{repo_path}' is not a file inside {ENV_LOCAL} ({local})")
        _write_cached(root, dest, part.read_bytes())
    else:
        if entry.get("size", 0) > MAX_DOWNLOAD:
            raise _err(
                errors.LIBRARY_UNAVAILABLE,
                f"'{repo_path}' is {entry['size'] // (1024 * 1024)} MB; the limit is "
                f"{MAX_DOWNLOAD // (1024 * 1024)} MB",
                hint="Pick a lighter variant, or download it yourself and import the file.",
            )
        data = _get(RAW + urllib.parse.quote(repo_path), MAX_DOWNLOAD, src.offline)
        if _blob_sha(data) != entry["sha"]:
            raise _err(
                errors.LIBRARY_UNAVAILABLE,
                f"Downloaded '{repo_path}' does not match the library index",
                hint="The library changed since the index was cached: retry with 'fcskill.py library --refresh'.",
            )
        _write_cached(root, dest, data)
    _write_cached(root, dest.with_name(dest.name + ".json"), json.dumps(meta).encode("utf-8"))
    return dest, meta


def library_refs(request: Any) -> List[str]:
    """Library parts named by the 'import' steps of a v2 request."""
    steps = request.get("steps") if isinstance(request, dict) else None
    if not isinstance(steps, list) and isinstance(request, dict) and request.get("op") == "import":
        steps = [request]
    refs = []
    for s in steps or []:
        if isinstance(s, dict) and s.get("op") == "import" and isinstance(s.get("library"), str):
            refs.append(s["library"])
    return refs
