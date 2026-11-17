"""
state.py

Daemon 运行状态持久化（JSON 文件）。
CLI 通过读取这个文件定位 daemon 的 socket 端口。
"""

import json
import os
import tempfile
from pathlib import Path

_STATE_FILE = Path(__file__).parent / ".clawtrader_state.json"
_RUNTIME_FILE = Path(__file__).parent.parent / ".clawtrader_runtime.json"


def configure(state_file: Path, runtime_file: Path) -> None:
    """Select the files for one account instance before any I/O occurs."""
    global _STATE_FILE, _RUNTIME_FILE
    _STATE_FILE = Path(state_file)
    _RUNTIME_FILE = Path(runtime_file)


def _read_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, ValueError, TypeError):
        return {}
    return data if isinstance(data, dict) else {}


def _atomic_write(path: Path, data: dict) -> None:
    """Write JSON without exposing a partially-written state file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=str(path.parent),
    )
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass


def read() -> dict:
    return _read_json(_STATE_FILE)


def read_path(path: Path) -> dict:
    return _read_json(Path(path))


def write(data: dict) -> None:
    _atomic_write(_STATE_FILE, data)


def clear() -> None:
    if _STATE_FILE.exists():
        _STATE_FILE.unlink()


def get_port() -> int | None:
    return read().get("port")


def is_running() -> bool:
    return is_running_path(_STATE_FILE)


def is_running_path(path: Path) -> bool:
    st = _read_json(Path(path))
    if not st.get("port"):
        return False
    pid = st.get("pid")
    if not pid:
        return False
    if os.name == "nt":
        # Windows: os.kill(pid, 0) 的 0 == CTRL_C_EVENT，不能探活（会抛 OSError）
        # 改用 OpenProcess + GetExitCodeProcess 判断进程是否存活
        import ctypes
        _PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        _STILL_ACTIVE = 259
        handle = ctypes.windll.kernel32.OpenProcess(
            _PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not handle:
            return False
        try:
            code = ctypes.c_ulong()
            if not ctypes.windll.kernel32.GetExitCodeProcess(
                    handle, ctypes.byref(code)):
                return False
            return code.value == _STILL_ACTIVE
        finally:
            ctypes.windll.kernel32.CloseHandle(handle)
    try:
        os.kill(pid, 0)   # POSIX: 发信号 0 探活
        return True
    except OSError:
        return False


def read_runtime() -> dict:
    """Read persistent local conditions and schedules."""
    return _read_json(_RUNTIME_FILE)


def write_runtime(data: dict) -> None:
    """Persist local conditions and schedules atomically."""
    _atomic_write(_RUNTIME_FILE, data)
