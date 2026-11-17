"""Create and read private signing keys with native file access controls."""

from __future__ import annotations

import ctypes
import errno
import os
import stat
from pathlib import Path
from typing import Any, NoReturn

_READ_LIMIT = 33
_DWORD = ctypes.c_uint32
_BOOL = ctypes.c_int32
_HANDLE = ctypes.c_void_p
_POINTER = ctypes.c_void_p
_INVALID_HANDLE = ctypes.c_void_p(-1).value


class KeyFileCreationError(OSError):
    """A creation guard failed and cleanup also needs caller review."""

    def __init__(self, error: Exception, path: Path, cleanup_errors: list[str]) -> None:
        super().__init__(str(error))
        self.outputs_requiring_review = [str(path)]
        self.cleanup_errors = cleanup_errors


class _SecurityAttributes(ctypes.Structure):
    _fields_ = [
        ("nLength", _DWORD),
        ("lpSecurityDescriptor", _POINTER),
        ("bInheritHandle", _BOOL),
    ]


class _SidAndAttributes(ctypes.Structure):
    _fields_ = [("Sid", _POINTER), ("Attributes", _DWORD)]


class _FileTime(ctypes.Structure):
    _fields_ = [("low", _DWORD), ("high", _DWORD)]


class _FileInformation(ctypes.Structure):
    _fields_ = [
        ("attributes", _DWORD),
        ("creation", _FileTime),
        ("access", _FileTime),
        ("write", _FileTime),
        ("volume", _DWORD),
        ("size_high", _DWORD),
        ("size_low", _DWORD),
        ("links", _DWORD),
        ("index_high", _DWORD),
        ("index_low", _DWORD),
    ]


class _Acl(ctypes.Structure):
    _fields_ = [
        ("revision", ctypes.c_ubyte),
        ("reserved", ctypes.c_ubyte),
        ("size", ctypes.c_uint16),
        ("count", ctypes.c_uint16),
        ("reserved2", ctypes.c_uint16),
    ]


class _AceHeader(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ubyte),
        ("flags", ctypes.c_ubyte),
        ("size", ctypes.c_uint16),
    ]


class _FileDisposition(ctypes.Structure):
    _fields_ = [("delete", ctypes.c_ubyte)]


def _raise_windows_error(action: str, code: int | None = None) -> NoReturn:
    error = ctypes.get_last_error() if code is None else code
    raise OSError(error, f"{action} failed (Windows error {error})")


class _WindowsAPI:
    """Small, lazy Win32 binding; DLL lookup is restricted to System32."""

    def __init__(self) -> None:
        kernel = ctypes.WinDLL("kernel32.dll", use_last_error=True, winmode=0x800)
        security = ctypes.WinDLL("advapi32.dll", use_last_error=True, winmode=0x800)
        pointer_out = ctypes.POINTER(_POINTER)
        dword_out = ctypes.POINTER(_DWORD)
        self.get_current_process = self._bind(kernel, "GetCurrentProcess", [], _HANDLE)
        self.close_handle = self._bind(kernel, "CloseHandle", [_HANDLE], _BOOL)
        self.local_free = self._bind(kernel, "LocalFree", [_POINTER], _POINTER)
        self.create_file = self._bind(kernel, "CreateFileW", [
            ctypes.c_wchar_p, _DWORD, _DWORD, ctypes.POINTER(_SecurityAttributes),
            _DWORD, _DWORD, _HANDLE,
        ], _HANDLE)
        self.get_file_type = self._bind(kernel, "GetFileType", [_HANDLE], _DWORD)
        self.get_file_information = self._bind(kernel, "GetFileInformationByHandle", [
            _HANDLE, ctypes.POINTER(_FileInformation),
        ], _BOOL)
        self.set_file_information = self._bind(kernel, "SetFileInformationByHandle", [
            _HANDLE, ctypes.c_int, _POINTER, _DWORD,
        ], _BOOL)
        self.open_process_token = self._bind(security, "OpenProcessToken", [
            _HANDLE, _DWORD, ctypes.POINTER(_HANDLE),
        ], _BOOL)
        self.get_token_information = self._bind(security, "GetTokenInformation", [
            _HANDLE, ctypes.c_int, _POINTER, _DWORD, dword_out,
        ], _BOOL)
        self.sid_to_string = self._bind(security, "ConvertSidToStringSidW", [
            _POINTER, pointer_out,
        ], _BOOL)
        self.descriptor_from_string = self._bind(security, "ConvertStringSecurityDescriptorToSecurityDescriptorW", [
            ctypes.c_wchar_p, _DWORD, pointer_out, dword_out,
        ], _BOOL)
        self.get_security_information = self._bind(security, "GetSecurityInfo", [
            _HANDLE, ctypes.c_int, _DWORD, pointer_out, pointer_out,
            pointer_out, pointer_out, pointer_out,
        ], _DWORD)
        self.get_security_control = self._bind(security, "GetSecurityDescriptorControl", [
            _POINTER, ctypes.POINTER(ctypes.c_uint16), dword_out,
        ], _BOOL)
        self.get_ace = self._bind(security, "GetAce", [_POINTER, _DWORD, pointer_out], _BOOL)
        self.equal_sid = self._bind(security, "EqualSid", [_POINTER, _POINTER], _BOOL)
        self.valid_sid = self._bind(security, "IsValidSid", [_POINTER], _BOOL)

    @staticmethod
    def _bind(library: Any, name: str, arguments: list[Any], result: Any) -> Any:
        function = getattr(library, name)
        function.argtypes = arguments
        function.restype = result
        return function

    def current_user(self) -> tuple[Any, int, str]:
        """Return the SID's owning buffer as well as its pointer and SDDL form."""
        token = _HANDLE()
        if not self.open_process_token(self.get_current_process(), 0x0008, ctypes.byref(token)):
            _raise_windows_error("querying the current user")
        try:
            size = _DWORD()
            self.get_token_information(token, 1, None, 0, ctypes.byref(size))
            if ctypes.get_last_error() != 122 or size.value < ctypes.sizeof(_SidAndAttributes):
                _raise_windows_error("querying the current user SID")
            buffer = ctypes.create_string_buffer(size.value)
            if not self.get_token_information(token, 1, buffer, size, ctypes.byref(size)):
                _raise_windows_error("reading the current user SID")
            sid = ctypes.cast(buffer, ctypes.POINTER(_SidAndAttributes)).contents.Sid
            if not sid or not self.valid_sid(sid):
                raise ValueError("the current user SID is invalid")
            text = _POINTER()
            if not self.sid_to_string(sid, ctypes.byref(text)):
                _raise_windows_error("encoding the current user SID")
            try:
                return buffer, sid, ctypes.wstring_at(text)
            finally:
                self.local_free(text)
        finally:
            self.close_handle(token)

    def private_descriptor(self, user_sid: str) -> _POINTER:
        descriptor = _POINTER()
        if not self.descriptor_from_string(
            f"O:{user_sid}D:P(A;;FA;;;{user_sid})", 1, ctypes.byref(descriptor), None,
        ):
            _raise_windows_error("creating a protected owner-only ACL")
        return descriptor

    def open_key(self, path: Path, *, create: bool, descriptor: _POINTER | None = None) -> int:
        attributes = (
            _SecurityAttributes(ctypes.sizeof(_SecurityAttributes), descriptor, False)
            if descriptor is not None else None
        )
        # CREATE_NEW / OPEN_EXISTING; share mode 0 blocks concurrent data
        # read/write/delete opens. OPEN_REPARSE_POINT exposes the link itself.
        access = 0x80000000 | 0x00020000
        if create:
            access |= 0x40000000 | 0x00010000  # write / delete-on-failure
        handle = self.create_file(
            str(path), access, 0, ctypes.byref(attributes) if attributes is not None else None,
            1 if create else 3, 0x00200000 | 0x80, None,
        )
        if handle in (None, _INVALID_HANDLE):
            error = ctypes.get_last_error()
            if create and error in (80, 183):
                raise FileExistsError(errno.EEXIST, "key file already exists")
            _raise_windows_error("opening the private signing key", error)
        return handle

    def assert_regular_handle(self, handle: int) -> None:
        if self.get_file_type(handle) != 1:  # FILE_TYPE_DISK
            raise ValueError("private signing key must be a regular disk file")
        information = _FileInformation()
        if not self.get_file_information(handle, ctypes.byref(information)):
            _raise_windows_error("checking the private signing key file type")
        if information.attributes & (0x10 | 0x40 | 0x400):  # directory / device / reparse point
            raise ValueError("private signing key must not be a directory, device or reparse point")

    def assert_private_handle(self, handle: int, user_sid: int) -> None:
        owner, dacl, descriptor = _POINTER(), _POINTER(), _POINTER()
        result = self.get_security_information(
            handle, 1, 0x1 | 0x4, ctypes.byref(owner), None,
            ctypes.byref(dacl), None, ctypes.byref(descriptor),
        )
        if result:
            _raise_windows_error("reading the private signing key ACL", result)
        try:
            if not owner or not self.valid_sid(owner) or not self.equal_sid(owner, user_sid):
                raise ValueError("private signing key requires a protected owner-only ACL owned by the current user")
            control, revision = ctypes.c_uint16(), _DWORD()
            if not descriptor or not self.get_security_control(descriptor, ctypes.byref(control), ctypes.byref(revision)):
                _raise_windows_error("checking the private signing key ACL controls")
            if not dacl or control.value & (0x4 | 0x1000) != (0x4 | 0x1000):
                raise ValueError("private signing key requires a non-null protected owner-only ACL")
            acl = ctypes.cast(dacl, ctypes.POINTER(_Acl)).contents
            owner_can_read = False
            for index in range(acl.count):
                ace = _POINTER()
                if not self.get_ace(dacl, index, ctypes.byref(ace)):
                    _raise_windows_error("checking a private signing key ACL entry")
                header = ctypes.cast(ace, ctypes.POINTER(_AceHeader)).contents
                # Accept ordinary owner-only allow entries. Unknown ACE forms
                # fail closed rather than guessing where their SID is stored.
                if header.type != 0 or header.size < 16:
                    raise ValueError("private signing key requires a protected owner-only ACL with supported allow entries")
                entry_sid = ace.value + 8  # ACE_HEADER + ACCESS_MASK
                if not self.valid_sid(entry_sid) or not self.equal_sid(entry_sid, user_sid):
                    raise ValueError("private signing key requires a protected owner-only ACL; another principal has access")
                mask = _DWORD.from_address(ace.value + 4).value
                if not header.flags & 0x8 and mask & (0x1 | 0x80000000 | 0x10000000):
                    owner_can_read = True
            if not owner_can_read:
                raise ValueError("private signing key requires a protected owner-only ACL that permits owner reading")
        finally:
            if descriptor:
                self.local_free(descriptor)

    def delete_created_handle(self, handle: int) -> None:
        disposition = _FileDisposition(True)
        if not self.set_file_information(handle, 4, ctypes.byref(disposition), ctypes.sizeof(disposition)):
            _raise_windows_error("removing a created signing key after generation failed")


def _read_limited(descriptor: int) -> bytes:
    data = bytearray()
    while len(data) < _READ_LIMIT:
        chunk = os.read(descriptor, _READ_LIMIT - len(data))
        if not chunk:
            break
        data.extend(chunk)
    return bytes(data)


def create_key_file(path: Path) -> int:
    """Create a new owner-private file and return a non-inheritable write FD."""
    if os.name != "nt":
        return os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    import msvcrt

    api = _WindowsAPI()
    user_buffer, user_sid, user_text = api.current_user()
    descriptor = api.private_descriptor(user_text)
    handle = None
    file_descriptor = None
    try:
        handle = api.open_key(path, create=True, descriptor=descriptor)
        api.assert_regular_handle(handle)
        api.assert_private_handle(handle, user_sid)
        file_descriptor = msvcrt.open_osfhandle(handle, os.O_WRONLY | os.O_BINARY)
        os.set_inheritable(file_descriptor, False)
        return file_descriptor
    except BaseException as error:
        cleanup_errors: list[str] = []
        if handle is not None:
            try:
                api.delete_created_handle(handle)
            except Exception as cleanup_error:
                cleanup_errors.append(str(cleanup_error))
            try:
                if file_descriptor is not None:
                    os.close(file_descriptor)
                elif not api.close_handle(handle):
                    _raise_windows_error("closing a created signing key handle")
            except Exception as cleanup_error:
                cleanup_errors.append(str(cleanup_error))
        if cleanup_errors and isinstance(error, Exception):
            raise KeyFileCreationError(error, path, cleanup_errors) from error
        raise
    finally:
        # user_buffer keeps the SID pointer alive until every ACL check ends.
        del user_buffer
        api.local_free(descriptor)


def assert_created_key_file(path: Path, descriptor: int) -> None:
    """Check a generated output while its original creation FD is still held."""
    if os.name != "nt":
        original = os.fstat(descriptor)
        current = path.lstat()
        if (
            not stat.S_ISREG(current.st_mode)
            or (current.st_dev, current.st_ino) != (original.st_dev, original.st_ino)
        ):
            raise ValueError("created key output path changed during key generation")
        if stat.S_IMODE(original.st_mode) & 0o077:
            raise ValueError("created key output became group/world accessible")
        return
    import msvcrt

    api = _WindowsAPI()
    user_buffer, user_sid, _ = api.current_user()
    try:
        handle = msvcrt.get_osfhandle(descriptor)
        api.assert_regular_handle(handle)
        api.assert_private_handle(handle, user_sid)
    finally:
        del user_buffer


def discard_created_key_file(descriptor: int) -> bool:
    """Delete through a held Windows handle; preserve POSIX outputs for review.

    POSIX cannot atomically bind path-based unlink to the creating descriptor.
    Comparing an inode before unlink would still allow replacement in between.
    """
    if os.name != "nt":
        return False
    import msvcrt

    _WindowsAPI().delete_created_handle(msvcrt.get_osfhandle(descriptor))
    return True


def read_private_file(path: Path) -> bytes:
    """Verify the opened file's private permissions before reading at most 33 bytes."""
    if os.name != "nt":
        if not stat.S_ISREG(path.lstat().st_mode):
            raise ValueError("private signing key must be a regular file")
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        descriptor = os.open(path, flags)
        try:
            information = os.fstat(descriptor)
            if not stat.S_ISREG(information.st_mode):
                raise ValueError("private signing key must be a regular file")
            if stat.S_IMODE(information.st_mode) & 0o077:
                raise ValueError("private signing key is group/world accessible; chmod 600 before use")
            return _read_limited(descriptor)
        finally:
            os.close(descriptor)
    import msvcrt

    api = _WindowsAPI()
    user_buffer, user_sid, _ = api.current_user()
    handle = api.open_key(path, create=False)
    descriptor = None
    try:
        api.assert_regular_handle(handle)
        api.assert_private_handle(handle, user_sid)
        descriptor = msvcrt.open_osfhandle(handle, os.O_RDONLY | os.O_BINARY)
        os.set_inheritable(descriptor, False)
        return _read_limited(descriptor)
    finally:
        del user_buffer
        if descriptor is not None:
            os.close(descriptor)
        else:
            api.close_handle(handle)
