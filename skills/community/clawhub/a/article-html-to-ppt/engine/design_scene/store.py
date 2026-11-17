"""No-follow task I/O, bounded decoding, and content-addressed assets."""
from __future__ import annotations

import hashlib
import io
import json
import os
import stat
import uuid
from contextlib import contextmanager
from pathlib import Path, PurePosixPath

from PIL import Image

MAX_JSON = 8 * 1024 * 1024
MAX_IMAGE = 25 * 1024 * 1024
MAX_PIXELS = 32_000_000
MAX_FILE = 128 * 1024 * 1024


class DesignError(ValueError):
    """An actionable input, capability, integrity, or acceptance failure."""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def json_bytes(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False).encode("utf-8") + b"\n"


def parse_json(data: bytes):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise DesignError(f"DUPLICATE_JSON_KEY: {key}")
            result[key] = value
        return result

    def nonfinite(value):
        raise DesignError(f"NONFINITE_NUMBER: {value}")

    if len(data) > MAX_JSON:
        raise DesignError("JSON_TOO_LARGE")
    try:
        return json.loads(data, object_pairs_hook=pairs, parse_constant=nonfinite)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise DesignError(f"INVALID_JSON: {exc}") from exc


def _parts(relative: str):
    p = PurePosixPath(relative)
    if (p.is_absolute() or not p.parts or any(x in {".", ".."} for x in p.parts)
            or "\\" in relative or "\x00" in relative or ":" in relative):
        raise DesignError("UNSAFE_RELATIVE_PATH")
    return p.parts


class Store:
    """No symlink traversal, including ancestors, for reads or writes.

    Parent directories remain open across atomic writes. Temporary names are
    unpredictable, exclusive, and never reused. This is an I/O boundary, not
    an OS sandbox against arbitrary code execution.
    """

    def __init__(self, root: str | Path, *, create=False):
        self.root = Path(os.path.abspath(root))
        self._windows = None
        if os.name == "nt":
            from .windows_io import WindowsIO
            self._windows = WindowsIO(self.root, create=create)
            return
        fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
        try:
            for part in self.root.parts[1:]:
                if create:
                    try:
                        os.mkdir(part, 0o700, dir_fd=fd)
                    except FileExistsError:
                        pass
                new = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                os.close(fd)
                fd = new
            self.fd = fd
        except OSError as exc:
            os.close(fd)
            raise DesignError(f"UNSAFE_TASK_DIRECTORY: {exc}") from exc

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self._windows is not None:
            self._windows.close()
        else:
            os.close(self.fd)

    @contextmanager
    def parent(self, relative: str, *, create=False):
        parts = _parts(relative)
        fd = os.dup(self.fd)
        try:
            for part in parts[:-1]:
                if create:
                    try:
                        os.mkdir(part, 0o700, dir_fd=fd)
                    except FileExistsError:
                        pass
                new = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                os.close(fd)
                fd = new
            yield fd, parts[-1]
        except OSError as exc:
            raise DesignError(f"UNSAFE_TASK_IO: {relative}: {exc}") from exc
        finally:
            os.close(fd)

    def read(self, relative: str, limit=MAX_FILE) -> bytes:
        if self._windows is not None:
            return self._windows.read(relative, limit)
        with self.parent(relative) as (fd, name):
            src = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
            with os.fdopen(src, "rb") as f:
                meta = os.fstat(f.fileno())
                if not stat.S_ISREG(meta.st_mode) or meta.st_size > limit:
                    raise DesignError(f"INVALID_FILE_SIZE_OR_TYPE: {relative}")
                data = f.read(limit + 1)
                if len(data) > limit:
                    raise DesignError("FILE_TOO_LARGE")
                return data

    def write(self, relative: str, data: bytes, *, exclusive=False):
        if self._windows is not None:
            return self._windows.write(relative, data, exclusive=exclusive)
        if len(data) > MAX_FILE:
            raise DesignError("OUTPUT_TOO_LARGE")
        with self.parent(relative, create=True) as (fd, name):
            try:
                dest = os.stat(name, dir_fd=fd, follow_symlinks=False)
            except FileNotFoundError:
                dest = None
            if dest and (exclusive or not stat.S_ISREG(dest.st_mode) or dest.st_nlink != 1):
                raise DesignError(f"OUTPUT_EXISTS_OR_UNSAFE: {relative}")
            temp = ".write-" + uuid.uuid4().hex
            tmpfd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=fd)
            try:
                with os.fdopen(tmpfd, "wb") as f:
                    f.write(data)
                    f.flush()
                    os.fsync(f.fileno())
                if exclusive:
                    os.link(temp, name, src_dir_fd=fd, dst_dir_fd=fd, follow_symlinks=False)
                    os.unlink(temp, dir_fd=fd)
                else:
                    os.replace(temp, name, src_dir_fd=fd, dst_dir_fd=fd)
            finally:
                try:
                    os.unlink(temp, dir_fd=fd)
                except FileNotFoundError:
                    pass

    def json(self, relative: str):
        return parse_json(self.read(relative, MAX_JSON))

    def put_json(self, relative: str, value, *, exclusive=False):
        self.write(relative, json_bytes(value), exclusive=exclusive)


def external_bytes(path: str | Path, limit=MAX_IMAGE):
    """Only the explicit ingestion boundary reads a caller-specified file."""
    path = Path(os.path.abspath(path))
    with Store(path.parent) as store:
        return store.read(path.name, limit)


def decode_image(data: bytes):
    if len(data) > MAX_IMAGE:
        raise DesignError("IMAGE_TOO_LARGE")
    try:
        with Image.open(io.BytesIO(data)) as im:
            if im.format not in {"PNG", "JPEG"}:
                raise DesignError("IMAGE_FORMAT_UNSUPPORTED: only PNG/JPEG")
            if im.width * im.height > MAX_PIXELS or getattr(im, "n_frames", 1) != 1:
                raise DesignError("IMAGE_RESOURCE_LIMIT")
            im.load()
            return im.convert("RGBA")
    except (OSError, ValueError, Image.DecompressionBombError) as exc:
        raise DesignError(f"INVALID_IMAGE: {exc}") from exc


def normalized_png(data: bytes, crop=None) -> tuple[bytes, tuple[int, int]]:
    im = decode_image(data)
    if crop is not None:
        if (len(crop) != 4 or any(type(x) is not int for x in crop)
                or crop[0] < 0 or crop[1] < 0 or crop[2] <= 0 or crop[3] <= 0
                or crop[0] + crop[2] > im.width or crop[1] + crop[3] > im.height):
            raise DesignError("INVALID_SOURCE_CROP")
        x, y, w, h = crop
        im = im.crop((x, y, x + w, y + h))
    out = io.BytesIO()
    im.save(out, format="PNG")
    if out.tell() > MAX_IMAGE:
        raise DesignError("NORMALIZED_IMAGE_TOO_LARGE")
    return out.getvalue(), im.size
