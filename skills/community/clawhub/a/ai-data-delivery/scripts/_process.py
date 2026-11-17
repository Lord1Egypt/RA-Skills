"""Local process identity checks, not a boundary against same-user tampering.

Windows termination uses the queried process handle. Linux requires a pidfd;
there is no fallback from a stale identity to a numeric-PID signal.
"""
from contextlib import contextmanager
import json
import os
from pathlib import Path
import re
import select
import shlex
import shutil
import signal
import sys
import uuid

from _contract import minimal_env

OWNER = 'ai-data-delivery/rebuild'
SHELLS = {'cmd', 'powershell', 'pwsh', 'sh', 'bash', 'dash', 'ash', 'zsh',
          'ksh', 'fish', 'csh', 'tcsh', 'wscript', 'cscript', 'mshta'}


def canonical(path):
    return os.path.normcase(os.path.realpath(os.fspath(path)))


def child_env(pass_names=()):
    extra = {}
    for name in pass_names:
        if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', name):
            raise ValueError('pass-env must contain environment variable names only')
        if name not in os.environ:
            raise ValueError('requested environment variable is absent: ' + name)
        extra[name] = os.environ[name]
    return minimal_env(extra)


def parse_argv(command=None, json_argv=None):
    if json_argv is not None:
        try:
            result = json.loads(json_argv)
        except (ValueError, TypeError) as exc:
            raise ValueError('argv must be a JSON array of strings') from exc
    elif isinstance(command, str) and command.strip():
        if os.name == 'nt':
            import ctypes
            from ctypes import wintypes
            shell32 = ctypes.WinDLL('shell32', use_last_error=True)
            shell32.CommandLineToArgvW.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(ctypes.c_int)]
            shell32.CommandLineToArgvW.restype = ctypes.POINTER(wintypes.LPWSTR)
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LocalFree.argtypes = [wintypes.HLOCAL]
            kernel32.LocalFree.restype = wintypes.HLOCAL
            count = ctypes.c_int()
            pointer = shell32.CommandLineToArgvW(command, ctypes.byref(count))
            if not pointer:
                raise ValueError('cannot parse command; use JSON argv')
            try:
                result = [pointer[i] for i in range(count.value)]
            finally:
                kernel32.LocalFree(pointer)
        else:
            result = shlex.split(command)
    else:
        raise ValueError('a command or JSON argv is required')
    if not isinstance(result, list) or not result or any(not isinstance(x, str) or '\0' in x for x in result) or not result[0]:
        raise ValueError('argv must be a nonempty string array without NUL')
    return result


def validate_argv(argv, project, env):
    candidate = argv[0]
    name = Path(candidate).name.lower()
    if Path(name).stem in SHELLS or Path(name).suffix in {'.cmd', '.bat'}:
        raise ValueError('shell interpreters and .cmd/.bat launchers are not supported; provide an executable argv')
    if os.path.dirname(candidate):
        executable = Path(candidate) if os.path.isabs(candidate) else Path(project) / candidate
        resolved = str(executable.resolve()) if executable.is_file() else None
    else:
        resolved = shutil.which(candidate, path=env.get('PATH', ''))
    if not resolved or not Path(resolved).is_file():
        raise ValueError('command executable is unavailable')
    resolved = canonical(resolved)
    if Path(resolved).stem.lower() in SHELLS or Path(resolved).suffix.lower() in {'.cmd', '.bat'}:
        raise ValueError('resolved command is a shell or batch launcher')
    if os.name != 'nt' and not os.access(resolved, os.X_OK):
        raise ValueError('command executable is not executable')
    return [resolved, *argv[1:]]


def require_process_support():
    if os.name == 'nt':
        return
    if sys.platform.startswith('linux') and hasattr(os, 'pidfd_open') and hasattr(signal, 'pidfd_send_signal'):
        try:
            probe = os.pidfd_open(os.getpid(), 0)
            os.close(probe)
        except OSError as exc:
            raise ValueError('Linux pidfd is unavailable; no process was started') from exc
        return
    raise ValueError('safe process management requires Windows handles or Linux pidfd; no PID-only fallback')


def _windows():
    import ctypes
    from ctypes import wintypes
    api = ctypes.WinDLL('kernel32', use_last_error=True)
    api.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    api.OpenProcess.restype = wintypes.HANDLE
    api.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    api.GetProcessTimes.restype = wintypes.BOOL
    api.QueryFullProcessImageNameW.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
    api.QueryFullProcessImageNameW.restype = wintypes.BOOL
    api.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
    api.TerminateProcess.restype = wintypes.BOOL
    api.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    api.WaitForSingleObject.restype = wintypes.DWORD
    api.CloseHandle.argtypes = [wintypes.HANDLE]
    api.CloseHandle.restype = wintypes.BOOL
    return ctypes, wintypes, api


class OwnedProcess:
    def __init__(self, pid):
        require_process_support()
        if isinstance(pid, bool) or not isinstance(pid, int) or pid <= 0 or pid == os.getpid():
            raise ValueError('invalid managed process ID')
        self.pid, self.handle = pid, None
        if os.name == 'nt':
            ctypes, _, api = _windows()
            self.handle = api.OpenProcess(0x1000 | 0x0001 | 0x00100000, False, pid)
            if not self.handle:
                raise ValueError('recorded process is absent or cannot be inspected')
        else:
            try:
                self.handle = os.pidfd_open(pid, 0)
            except OSError as exc:
                raise ValueError('recorded process is absent or pidfd is unavailable') from exc

    def alive(self):
        if self.handle is None:
            return False
        if os.name == 'nt':
            result = _windows()[2].WaitForSingleObject(self.handle, 0)
            if result == 0xFFFFFFFF:
                raise ValueError('cannot inspect process handle')
            return result == 0x102
        return not select.select([self.handle], [], [], 0)[0]

    def identity(self):
        if not self.alive():
            raise ValueError('recorded process has exited; stale record is not a stop target')
        if os.name == 'nt':
            ctypes, wt, api = _windows()
            creation, exit_time, kernel, user = (wt.FILETIME() for _ in range(4))
            if not api.GetProcessTimes(self.handle, *(ctypes.byref(x) for x in (creation, exit_time, kernel, user))):
                raise ValueError('cannot read process creation time')
            size = wt.DWORD(32768)
            image = ctypes.create_unicode_buffer(size.value)
            if not api.QueryFullProcessImageNameW(self.handle, 0, image, ctypes.byref(size)):
                raise ValueError('cannot read process executable')
            start = str((creation.dwHighDateTime << 32) | creation.dwLowDateTime)
            executable = canonical(image.value)
        else:
            try:
                stat = Path(f'/proc/{self.pid}/stat').read_text()
                start = Path('/proc/sys/kernel/random/boot_id').read_text().strip() + ':' + stat[stat.rfind(')') + 2:].split()[19]
                executable = canonical(os.readlink(f'/proc/{self.pid}/exe'))
            except (OSError, IndexError) as exc:
                raise ValueError('cannot read process identity') from exc
        if not self.alive():
            raise ValueError('process exited during identity inspection')
        return {'pid': self.pid, 'start_time': start, 'executable': executable}

    def record(self, project, launch_executable):
        return {'schema_version': 1, 'owner': OWNER, **self.identity(),
                'project': canonical(project), 'launch_executable': canonical(launch_executable),
                'instance_id': uuid.uuid4().hex}

    def verify(self, record, project):
        validate_record(record, project)
        actual = self.identity()
        if any(actual[key] != record[key] for key in ('pid', 'start_time', 'executable')):
            raise ValueError('process identity mismatch; no process was stopped')

    def stop(self, timeout=5):
        if not self.alive():
            return
        if os.name == 'nt':
            api = _windows()[2]
            if not api.TerminateProcess(self.handle, 1) and self.alive():
                raise ValueError('owned process termination failed')
            if api.WaitForSingleObject(self.handle, int(timeout * 1000)) != 0:
                raise ValueError('owned process did not exit within cleanup timeout')
        else:
            signal.pidfd_send_signal(self.handle, signal.SIGTERM)
            if not select.select([self.handle], [], [], timeout)[0]:
                signal.pidfd_send_signal(self.handle, signal.SIGKILL)
                if not select.select([self.handle], [], [], timeout)[0]:
                    raise ValueError('owned process did not exit within cleanup timeout')

    def close(self):
        if self.handle is not None:
            if os.name == 'nt':
                _windows()[2].CloseHandle(self.handle)
            else:
                os.close(self.handle)
            self.handle = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


def validate_record(record, project):
    if not isinstance(record, dict) or record.get('schema_version') != 1 or record.get('owner') != OWNER:
        raise ValueError('unrecognized process record; legacy integer PID files are refused')
    if not isinstance(record.get('project'), str) or not record['project'] or canonical(record['project']) != canonical(project):
        raise ValueError('process record belongs to another project')
    if isinstance(record.get('pid'), bool) or not isinstance(record.get('pid'), int) or record['pid'] <= 0:
        raise ValueError('invalid process record PID')
    for name in ('start_time', 'executable', 'launch_executable', 'instance_id'):
        if not isinstance(record.get(name), str) or not record[name]:
            raise ValueError('incomplete process identity record')
    if not os.path.isabs(record['executable']) or not os.path.isabs(record['launch_executable']):
        raise ValueError('process executable identity must be absolute')
    port = record.get('local_port')
    if port is not None and (isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535):
        raise ValueError('invalid recorded service port')


def read_record(path, project):
    if not Path(path).exists():
        return None
    try:
        record = json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise ValueError('cannot read managed process record') from exc
    validate_record(record, project)
    return record


def write_record(path, record):
    path = Path(path)
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        with temporary.open('x', encoding='utf-8') as stream:
            json.dump(record, stream, sort_keys=True)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def remove_record(path, record):
    """Do not erase a concurrently replaced or externally changed identity."""
    path = Path(path)
    if path.exists():
        try:
            current = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc:
            raise ValueError('process stopped but changed record was retained') from exc
        if current != record:
            raise ValueError('process stopped but replacement record was retained')
        path.unlink()


@contextmanager
def process_lock(path):
    """An OS lock serializes replacements; the empty lock file is not identity."""
    with open(str(path) + '.lock', 'a+b') as stream:
        stream.seek(0, 2)
        if not stream.tell():
            stream.write(b'0'); stream.flush()
        stream.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise ValueError('another rebuild manages this record; no replacement performed') from exc
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == 'nt':
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)
