"""Own command lifetimes with POSIX process groups or Windows Job Objects.

The caller owns the output file. Windows 10+ targets are created inside their
private job and remain suspended until launch setup completes; only explicitly
duplicated standard handles are inherited. Neither backend adds a wrapper
process to command timings.
"""

from __future__ import annotations

import ctypes
import errno
import math
import os
import signal
import subprocess
import time
from pathlib import Path
from typing import BinaryIO

_CLEANUP_TIMEOUT = 10.0
_WAIT_INTERVAL = 0.05


def _duration(value: float, name: str) -> float:
    """Reject unbounded cleanup intervals while allowing immediate deadlines."""
    value = float(value)
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be a finite nonnegative number")
    return value


class _PosixProcess:
    """Keep cleanup scoped to the process group created for one command."""

    def __init__(self, process: subprocess.Popen) -> None:
        """Remember the process group leader without taking ownership of output."""
        self._process = process
        self.pid = process.pid
        self._closed = False

    @property
    def returncode(self) -> int | None:
        """Expose the direct child's observed exit status."""
        return self._process.returncode

    def wait(self, timeout: float | None = None) -> int:
        """Wait for the direct child using subprocess's interruptible wait."""
        return self._process.wait(timeout=timeout)

    def _signal_group(self, number: int) -> None:
        """Signal the owned group even when its original leader has exited."""
        try:
            os.killpg(self.pid, number)
        except ProcessLookupError:
            pass

    def stop(self, grace: float = 0) -> None:
        """Request group termination, force it after grace, and reap the child."""
        if self._closed:
            return
        grace = _duration(grace, "grace")
        if grace:
            self._signal_group(signal.SIGTERM)
            try:
                self.wait(timeout=grace)
            except subprocess.TimeoutExpired:
                pass
        # A successful wait only reaps the leader; surviving group members
        # must still receive SIGKILL. Escaped sessions are outside this group.
        self._signal_group(signal.SIGKILL)
        try:
            self.wait(timeout=_CLEANUP_TIMEOUT)
        except subprocess.TimeoutExpired as error:
            raise OSError(errno.ETIMEDOUT, "command did not exit after SIGKILL") from error

    def close(self) -> None:
        """Stop remaining group members on every exit and make cleanup idempotent."""
        if self._closed:
            return
        try:
            self.stop()
        finally:
            self._closed = True


if os.name == "nt":
    from ctypes import wintypes

    import msvcrt

    _HANDLE = wintypes.HANDLE
    _DWORD = wintypes.DWORD
    _SIZE_T = ctypes.c_size_t
    _LPVOID = wintypes.LPVOID
    _INVALID_HANDLE = ctypes.c_void_p(-1).value
    _WAIT_OBJECT_0 = 0
    _WAIT_TIMEOUT = 258
    _WAIT_FAILED = 0xFFFFFFFF
    _ERROR_INSUFFICIENT_BUFFER = 122
    _ERROR_INVALID_HANDLE = 6
    _CONTROL_C_EXIT = 0xC000013A
    _CREATE_SUSPENDED = 0x00000004
    _CREATE_UNICODE_ENVIRONMENT = 0x00000400
    _EXTENDED_STARTUPINFO_PRESENT = 0x00080000
    _STARTF_USESTDHANDLES = 0x00000100
    _PROC_THREAD_ATTRIBUTE_HANDLE_LIST = 0x00020002
    _PROC_THREAD_ATTRIBUTE_JOB_LIST = 0x0002000D
    _JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
    _JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION = 1
    _JOB_OBJECT_EXTENDED_LIMIT_INFORMATION = 9

    class _STARTUPINFOW(ctypes.Structure):
        _fields_ = [
            ("cb", _DWORD),
            ("lpReserved", wintypes.LPWSTR),
            ("lpDesktop", wintypes.LPWSTR),
            ("lpTitle", wintypes.LPWSTR),
            ("dwX", _DWORD),
            ("dwY", _DWORD),
            ("dwXSize", _DWORD),
            ("dwYSize", _DWORD),
            ("dwXCountChars", _DWORD),
            ("dwYCountChars", _DWORD),
            ("dwFillAttribute", _DWORD),
            ("dwFlags", _DWORD),
            ("wShowWindow", wintypes.WORD),
            ("cbReserved2", wintypes.WORD),
            ("lpReserved2", ctypes.POINTER(wintypes.BYTE)),
            ("hStdInput", _HANDLE),
            ("hStdOutput", _HANDLE),
            ("hStdError", _HANDLE),
        ]

    class _STARTUPINFOEXW(ctypes.Structure):
        _fields_ = [("StartupInfo", _STARTUPINFOW), ("lpAttributeList", _LPVOID)]

    class _PROCESS_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("hProcess", _HANDLE),
            ("hThread", _HANDLE),
            ("dwProcessId", _DWORD),
            ("dwThreadId", _DWORD),
        ]

    class _BASIC_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", ctypes.c_longlong),
            ("PerJobUserTimeLimit", ctypes.c_longlong),
            ("LimitFlags", _DWORD),
            ("MinimumWorkingSetSize", _SIZE_T),
            ("MaximumWorkingSetSize", _SIZE_T),
            ("ActiveProcessLimit", _DWORD),
            ("Affinity", _SIZE_T),
            ("PriorityClass", _DWORD),
            ("SchedulingClass", _DWORD),
        ]

    class _IO_COUNTERS(ctypes.Structure):
        _fields_ = [
            (name, ctypes.c_ulonglong)
            for name in (
                "ReadOperationCount",
                "WriteOperationCount",
                "OtherOperationCount",
                "ReadTransferCount",
                "WriteTransferCount",
                "OtherTransferCount",
            )
        ]

    class _EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("BasicLimitInformation", _BASIC_LIMIT_INFORMATION),
            ("IoInfo", _IO_COUNTERS),
            ("ProcessMemoryLimit", _SIZE_T),
            ("JobMemoryLimit", _SIZE_T),
            ("PeakProcessMemoryUsed", _SIZE_T),
            ("PeakJobMemoryUsed", _SIZE_T),
        ]

    class _BASIC_ACCOUNTING_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("TotalUserTime", ctypes.c_longlong),
            ("TotalKernelTime", ctypes.c_longlong),
            ("ThisPeriodTotalUserTime", ctypes.c_longlong),
            ("ThisPeriodTotalKernelTime", ctypes.c_longlong),
            ("TotalPageFaultCount", _DWORD),
            ("TotalProcesses", _DWORD),
            ("ActiveProcesses", _DWORD),
            ("TotalTerminatedProcesses", _DWORD),
        ]

    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    def _bind(name: str, arguments: list, result: object) -> object:
        """Declare each Win32 ABI explicitly, including pointer-sized handles."""
        function = getattr(_kernel32, name)
        function.argtypes = arguments
        function.restype = result
        return function

    _CloseHandle = _bind("CloseHandle", [_HANDLE], wintypes.BOOL)
    _GetCurrentProcess = _bind("GetCurrentProcess", [], _HANDLE)
    _GetStdHandle = _bind("GetStdHandle", [_DWORD], _HANDLE)
    _DuplicateHandle = _bind(
        "DuplicateHandle",
        [_HANDLE, _HANDLE, _HANDLE, ctypes.POINTER(_HANDLE), _DWORD, wintypes.BOOL, _DWORD],
        wintypes.BOOL,
    )
    _CreateFileW = _bind(
        "CreateFileW",
        [wintypes.LPCWSTR, _DWORD, _DWORD, _LPVOID, _DWORD, _DWORD, _HANDLE],
        _HANDLE,
    )
    _InitializeProcThreadAttributeList = _bind(
        "InitializeProcThreadAttributeList",
        [_LPVOID, _DWORD, _DWORD, ctypes.POINTER(_SIZE_T)],
        wintypes.BOOL,
    )
    _UpdateProcThreadAttribute = _bind(
        "UpdateProcThreadAttribute",
        [_LPVOID, _DWORD, _SIZE_T, _LPVOID, _SIZE_T, _LPVOID, ctypes.POINTER(_SIZE_T)],
        wintypes.BOOL,
    )
    _DeleteProcThreadAttributeList = _bind("DeleteProcThreadAttributeList", [_LPVOID], None)
    _CreateProcessW = _bind(
        "CreateProcessW",
        [
            wintypes.LPCWSTR,
            wintypes.LPWSTR,
            _LPVOID,
            _LPVOID,
            wintypes.BOOL,
            _DWORD,
            _LPVOID,
            wintypes.LPCWSTR,
            ctypes.POINTER(_STARTUPINFOW),
            ctypes.POINTER(_PROCESS_INFORMATION),
        ],
        wintypes.BOOL,
    )
    _CreateJobObjectW = _bind("CreateJobObjectW", [_LPVOID, wintypes.LPCWSTR], _HANDLE)
    _SetInformationJobObject = _bind(
        "SetInformationJobObject", [_HANDLE, ctypes.c_int, _LPVOID, _DWORD], wintypes.BOOL
    )
    _QueryInformationJobObject = _bind(
        "QueryInformationJobObject",
        [_HANDLE, ctypes.c_int, _LPVOID, _DWORD, ctypes.POINTER(_DWORD)],
        wintypes.BOOL,
    )
    _ResumeThread = _bind("ResumeThread", [_HANDLE], _DWORD)
    _WaitForSingleObject = _bind("WaitForSingleObject", [_HANDLE, _DWORD], _DWORD)
    _GetExitCodeProcess = _bind("GetExitCodeProcess", [_HANDLE, ctypes.POINTER(_DWORD)], wintypes.BOOL)
    _TerminateJobObject = _bind("TerminateJobObject", [_HANDLE, wintypes.UINT], wintypes.BOOL)

    def _win_error() -> OSError:
        """Capture the calling thread's Win32 error before another API changes it."""
        return ctypes.WinError(ctypes.get_last_error())

    def _close_handles(handles: list[int]) -> None:
        """Attempt every owned close exactly once and preserve any cleanup failure."""
        first_error = None
        while handles:
            handle = handles.pop()
            try:
                if handle and handle != _INVALID_HANDLE and not _CloseHandle(handle):
                    raise _win_error()
            except BaseException as error:
                if first_error is None:
                    first_error = error
        if first_error is not None:
            raise first_error

    def _duplicate(handle: int, owned: list[int]) -> int:
        """Make one inheritable standard handle and register its local ownership."""
        duplicate = _HANDLE()
        current = _GetCurrentProcess()
        if not _DuplicateHandle(current, handle, current, ctypes.byref(duplicate), 0, True, 2):
            raise _win_error()
        owned.append(duplicate.value)
        return duplicate.value

    def _stdin_handle(owned: list[int]) -> int:
        """Preserve usable process stdin, substituting NUL for a missing handle."""
        source = _GetStdHandle(0xFFFFFFF6)  # STD_INPUT_HANDLE (-10 as DWORD).
        if source and source != _INVALID_HANDLE:
            try:
                return _duplicate(source, owned)
            except OSError as error:
                if error.winerror != _ERROR_INVALID_HANDLE:
                    raise
        source = _CreateFileW("NUL", 0x80000000, 3, None, 3, 0x80, None)
        if not source or source == _INVALID_HANDLE:
            raise _win_error()
        owned.append(source)
        return _duplicate(source, owned)

    def _wait_process(handle: int, argv: list[str], timeout: float | None) -> int:
        """Poll a native process handle in short waits so Ctrl-C reaches Python."""
        deadline = None if timeout is None else time.monotonic() + _duration(timeout, "timeout")
        while True:
            remaining = _WAIT_INTERVAL if deadline is None else max(0, deadline - time.monotonic())
            milliseconds = min(50, math.ceil(remaining * 1000))
            result = _WaitForSingleObject(handle, milliseconds)
            if result == _WAIT_OBJECT_0:
                code = _DWORD()
                if not _GetExitCodeProcess(handle, ctypes.byref(code)):
                    raise _win_error()
                return code.value
            if result == _WAIT_FAILED:
                raise _win_error()
            if result != _WAIT_TIMEOUT:
                raise OSError(f"unexpected process wait result: {result}")
            if deadline is not None and time.monotonic() >= deadline:
                raise subprocess.TimeoutExpired(argv, timeout)

    def _active_processes(job: int) -> int:
        """Query job membership independently of the original command's status."""
        info = _BASIC_ACCOUNTING_INFORMATION()
        if not _QueryInformationJobObject(
            job, _JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION, ctypes.byref(info), ctypes.sizeof(info), None
        ):
            raise _win_error()
        return info.ActiveProcesses

    def _wait_job_empty(job: int, deadline: float) -> None:
        """Require job membership to reach zero before declaring cleanup complete."""
        while True:
            active = _active_processes(job)
            if active == 0:
                return
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise OSError(errno.ETIMEDOUT, f"job still contains {active} processes after termination")
            time.sleep(min(_WAIT_INTERVAL, remaining))

    class _WindowsProcess:
        """Own a non-inherited job and the direct command's native process handle."""

        def __init__(self, pid: int, process: int, job: int, argv: list[str]) -> None:
            """Take ownership only after the suspended target is safely assigned."""
            self.pid = pid
            self.returncode = None
            self._process = process
            self._job = job
            self._argv = argv
            self._closed = False

        def wait(self, timeout: float | None = None) -> int:
            """Wait interruptibly for the root process without mistaking it for the whole job."""
            if self.returncode is not None:
                return self.returncode
            if self._closed:
                raise OSError(errno.EBADF, "process handle has been closed")
            self.returncode = _wait_process(self._process, self._argv, timeout)
            return self.returncode

        def stop(self, grace: float = 0) -> None:
            """Allow an inherited Ctrl-C grace period, then terminate every job member."""
            if self._closed:
                return
            grace = _duration(grace, "grace")
            if grace:
                try:
                    self.wait(timeout=grace)
                except subprocess.TimeoutExpired:
                    pass
            if _active_processes(self._job):
                if not _TerminateJobObject(self._job, _CONTROL_C_EXIT):
                    error = _win_error()
                    if _active_processes(self._job):
                        raise error
            deadline = time.monotonic() + _CLEANUP_TIMEOUT
            try:
                self.wait(timeout=max(0, deadline - time.monotonic()))
            except subprocess.TimeoutExpired as error:
                raise OSError(errno.ETIMEDOUT, "command did not exit after job termination") from error
            _wait_job_empty(self._job, deadline)

        def close(self) -> None:
            """Terminate leftovers, verify the job is empty, and release both handles once."""
            if self._closed:
                return
            primary_error = None
            try:
                self.stop()
            except BaseException as error:
                primary_error = error
                raise
            finally:
                handles = [self._process, self._job]
                self._process = self._job = None
                self._closed = True
                try:
                    _close_handles(handles)
                except BaseException as error:
                    if primary_error is None:
                        raise
                    primary_error.add_note(f"closing native process resources also failed: {error}")

    def _environment_block(env: dict) -> ctypes.Array:
        """Build a sorted Unicode environment with case-insensitive last-write-wins keys."""
        entries = {}
        for key, value in env.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise TypeError("Windows environment names and values must be strings")
            if not key or "\0" in key or "\0" in value or "=" in key[1:]:
                raise ValueError("invalid Windows environment entry")
            # Explicit overlays must replace inherited names regardless of casing.
            entries[key.upper()] = (key, value)
        ordered = [entries[key] for key in sorted(entries)]
        return ctypes.create_unicode_buffer("\0".join(f"{key}={value}" for key, value in ordered) + "\0\0")

    def _spawn_windows(
        argv: list[str], root: Path, env: dict, output: BinaryIO, command_line: str | None
    ) -> _WindowsProcess:
        """Create a suspended target already in its job, then complete setup and resume it."""
        handles = []
        info = _PROCESS_INFORMATION()
        attribute_list = None
        job = None
        transferred = False
        primary_error = None
        try:
            job = _CreateJobObjectW(None, None)
            if not job:
                raise _win_error()
            limits = _EXTENDED_LIMIT_INFORMATION()
            # Neither BREAKAWAY_OK nor SILENT_BREAKAWAY_OK is enabled.
            limits.BasicLimitInformation.LimitFlags = _JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            if not _SetInformationJobObject(
                job, _JOB_OBJECT_EXTENDED_LIMIT_INFORMATION, ctypes.byref(limits), ctypes.sizeof(limits)
            ):
                raise _win_error()
            stdin = _stdin_handle(handles)
            stdout = _duplicate(msvcrt.get_osfhandle(output.fileno()), handles)
            inherited = (_HANDLE * 2)(stdin, stdout)
            jobs = (_HANDLE * 1)(job)
            size = _SIZE_T()
            if not _InitializeProcThreadAttributeList(None, 2, 0, ctypes.byref(size)):
                if ctypes.get_last_error() != _ERROR_INSUFFICIENT_BUFFER:
                    raise _win_error()
            if not size.value:
                raise OSError("Windows returned an empty process attribute list")
            attributes = ctypes.create_string_buffer(size.value)
            attribute_pointer = ctypes.cast(attributes, _LPVOID)
            if not _InitializeProcThreadAttributeList(attribute_pointer, 2, 0, ctypes.byref(size)):
                raise _win_error()
            attribute_list = attribute_pointer
            if not _UpdateProcThreadAttribute(
                attribute_list, 0, _PROC_THREAD_ATTRIBUTE_HANDLE_LIST,
                ctypes.cast(inherited, _LPVOID), ctypes.sizeof(inherited), None, None
            ):
                raise _win_error()
            # JOB_LIST assigns membership during creation, closing the window
            # in which a killed launcher could leave an unassigned suspended root.
            # The job handle is an attribute value, never an inherited handle.
            if not _UpdateProcThreadAttribute(
                attribute_list, 0, _PROC_THREAD_ATTRIBUTE_JOB_LIST,
                ctypes.cast(jobs, _LPVOID), ctypes.sizeof(jobs), None, None
            ):
                raise _win_error()
            startup = _STARTUPINFOEXW()
            startup.StartupInfo.cb = ctypes.sizeof(startup)
            startup.StartupInfo.dwFlags = _STARTF_USESTDHANDLES
            startup.StartupInfo.hStdInput = stdin
            startup.StartupInfo.hStdOutput = startup.StartupInfo.hStdError = stdout
            startup.lpAttributeList = attribute_list
            command = ctypes.create_unicode_buffer(
                command_line if command_line is not None else subprocess.list2cmdline(argv)
            )
            environment = _environment_block(env)
            flags = _CREATE_SUSPENDED | _CREATE_UNICODE_ENVIRONMENT | _EXTENDED_STARTUPINFO_PRESENT
            if not _CreateProcessW(
                None, command, None, None, True, flags, ctypes.cast(environment, _LPVOID),
                str(root), ctypes.byref(startup.StartupInfo), ctypes.byref(info)
            ):
                raise _win_error()
            # Drop local launch-only resources before the target can execute.
            _DeleteProcThreadAttributeList(attribute_list)
            attribute_list = None
            _close_handles(handles)
            if _ResumeThread(info.hThread) == 0xFFFFFFFF:
                raise _win_error()
            thread = info.hThread
            info.hThread = None
            _close_handles([thread])
            process = _WindowsProcess(info.dwProcessId, info.hProcess, job, list(argv))
            transferred = True
            return process
        except BaseException as error:
            primary_error = error
            if info.hProcess:
                try:
                    # Any successfully created root is already owned by this job.
                    if not _TerminateJobObject(job, _CONTROL_C_EXIT):
                        raise _win_error()
                    deadline = time.monotonic() + _CLEANUP_TIMEOUT
                    _wait_process(info.hProcess, argv, _CLEANUP_TIMEOUT)
                    _wait_job_empty(job, deadline)
                except BaseException as cleanup_error:
                    error.add_note(f"failed launch cleanup also failed: {cleanup_error}")
            raise
        finally:
            if attribute_list is not None:
                _DeleteProcThreadAttributeList(attribute_list)
            if info.hThread:
                handles.append(info.hThread)
            if not transferred:
                handles.extend([info.hProcess, job])
            try:
                _close_handles(handles)
            except BaseException as error:
                if primary_error is None:
                    raise
                primary_error.add_note(f"closing launch resources also failed: {error}")


def spawn_process(
    argv: list[str], root: Path, env: dict, output: BinaryIO,
    *, windows_command_line: str | None = None
) -> object:
    """Launch one owned command without taking ownership of the output file.

    windows_command_line is reserved for fixed internal batch adapters whose
    cmd.exe quoting differs from MSVCRT argv quoting. Ordinary commands use
    list2cmdline on Windows; POSIX always executes the original argv directly.
    """
    if not argv or not argv[0]:
        raise ValueError("command must not be empty")
    if any(not isinstance(value, str) or "\0" in value for value in argv):
        raise ValueError("command arguments must be strings without NUL characters")
    if windows_command_line is not None and (
        not isinstance(windows_command_line, str)
        or not windows_command_line.strip()
        or "\0" in windows_command_line
    ):
        raise ValueError("Windows command line must be a nonempty string without NUL characters")
    output.flush()
    if os.name == "nt":
        return _spawn_windows(argv, root, env, output, windows_command_line)
    return _PosixProcess(
        subprocess.Popen(
            argv, cwd=root, env=env, stdout=output, stderr=subprocess.STDOUT, start_new_session=True
        )
    )
