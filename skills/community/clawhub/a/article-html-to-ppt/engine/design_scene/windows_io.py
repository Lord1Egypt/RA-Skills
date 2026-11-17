"""Windows task I/O: hold directory handles and reject reparse points.

Loaded only on Windows. Directory handles omit FILE_SHARE_DELETE so ancestors
cannot be renamed while path-based child operations are in progress. This is
an I/O boundary for the fixed worker, not a sandbox for arbitrary programs.
"""
from __future__ import annotations

import ctypes
import os
import stat
import uuid
from contextlib import ExitStack, contextmanager
from ctypes import wintypes
from pathlib import Path, PureWindowsPath

from .store import DesignError, MAX_FILE, _parts


class FileInfo(ctypes.Structure):
    _fields_ = [("attributes", wintypes.DWORD), ("created", wintypes.FILETIME),
                ("accessed", wintypes.FILETIME), ("written", wintypes.FILETIME),
                ("volume", wintypes.DWORD), ("size_high", wintypes.DWORD),
                ("size_low", wintypes.DWORD), ("links", wintypes.DWORD),
                ("index_high", wintypes.DWORD), ("index_low", wintypes.DWORD)]


def _component(name):
    if (PureWindowsPath(name).is_reserved() or name.endswith((".", " "))
            or any(c in name for c in '<>:"/\\|?*') or any(ord(c) < 32 for c in name)):
        raise DesignError("UNSAFE_WINDOWS_PATH_COMPONENT")
    return name


class WindowsIO:
    def __init__(self, root: Path, *, create=False):
        if not root.drive or root.drive.startswith("\\\\"):
            raise DesignError("WINDOWS_LOCAL_DRIVE_REQUIRED")
        self.root = root
        self.api = ctypes.WinDLL("kernel32", use_last_error=True)
        self.api.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                                        wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
        self.api.CreateFileW.restype = wintypes.HANDLE
        self.api.GetFileInformationByHandle.argtypes = [wintypes.HANDLE, ctypes.POINTER(FileInfo)]
        self.api.GetFileInformationByHandle.restype = wintypes.BOOL
        self.api.CloseHandle.argtypes = [wintypes.HANDLE]
        self.api.CloseHandle.restype = wintypes.BOOL
        self.stack = ExitStack()
        try:
            current = Path(root.anchor)
            self.stack.enter_context(self._directory(current))
            for name in root.parts[1:]:
                current /= _component(name)
                if create:
                    try:
                        current.mkdir(mode=0o700)
                    except FileExistsError:
                        pass
                self.stack.enter_context(self._directory(current))
        except (OSError, DesignError) as exc:
            self.close()
            raise DesignError(f"UNSAFE_TASK_DIRECTORY: {exc}") from exc

    def close(self):
        self.stack.close()

    def _open(self, path, *, directory=False):
        # OPEN_EXISTING, OPEN_REPARSE_POINT, BACKUP_SEMANTICS. Never follow a
        # junction/symlink, including when opening the final file itself.
        flags = 0x00200000 | 0x02000000
        access = 0x80 if directory else 0x80000000  # READ_ATTRIBUTES / GENERIC_READ
        handle = self.api.CreateFileW(str(path), access, 0x1 | 0x2, None, 3, flags, None)
        if handle == ctypes.c_void_p(-1).value:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            info = FileInfo()
            if not self.api.GetFileInformationByHandle(handle, ctypes.byref(info)):
                raise ctypes.WinError(ctypes.get_last_error())
            if info.attributes & 0x400 or bool(info.attributes & 0x10) != directory:
                raise DesignError("WINDOWS_REPARSE_POINT_OR_WRONG_FILE_TYPE")
            return handle
        except BaseException:
            self.api.CloseHandle(handle)
            raise

    @contextmanager
    def _directory(self, path):
        handle = self._open(path, directory=True)
        try:
            yield
        finally:
            self.api.CloseHandle(handle)

    @contextmanager
    def parent(self, relative, *, create=False):
        parts = [_component(p) for p in _parts(relative)]
        with ExitStack() as stack:
            current = self.root
            try:
                for part in parts[:-1]:
                    current /= part
                    if create:
                        try:
                            current.mkdir(mode=0o700)
                        except FileExistsError:
                            pass
                    stack.enter_context(self._directory(current))
                yield current / parts[-1]
            except OSError as exc:
                raise DesignError(f"UNSAFE_TASK_IO: {relative}: {exc}") from exc

    def read(self, relative, limit=MAX_FILE):
        import msvcrt
        with self.parent(relative) as path:
            handle = self._open(path)
            try:
                fd = msvcrt.open_osfhandle(handle, os.O_RDONLY | os.O_BINARY)
            except BaseException:
                self.api.CloseHandle(handle)
                raise
            with os.fdopen(fd, "rb") as f:
                meta = os.fstat(f.fileno())
                if not stat.S_ISREG(meta.st_mode) or meta.st_size > limit:
                    raise DesignError(f"INVALID_FILE_SIZE_OR_TYPE: {relative}")
                data = f.read(limit + 1)
                if len(data) > limit:
                    raise DesignError("FILE_TOO_LARGE")
                return data

    def write(self, relative, data, *, exclusive=False):
        if len(data) > MAX_FILE:
            raise DesignError("OUTPUT_TOO_LARGE")
        with self.parent(relative, create=True) as path:
            try:
                meta = path.lstat()
            except FileNotFoundError:
                meta = None
            if meta and (exclusive or not stat.S_ISREG(meta.st_mode) or meta.st_nlink != 1
                         or meta.st_file_attributes & 0x400):
                raise DesignError(f"OUTPUT_EXISTS_OR_UNSAFE: {relative}")
            temp = path.parent / (".write-" + uuid.uuid4().hex)
            fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_BINARY, 0o600)
            try:
                with os.fdopen(fd, "wb") as f:
                    f.write(data)
                    f.flush()
                    os.fsync(f.fileno())
                # On Windows rename fails if the destination already exists.
                (os.rename if exclusive else os.replace)(temp, path)
            finally:
                try:
                    temp.unlink()
                except FileNotFoundError:
                    pass
