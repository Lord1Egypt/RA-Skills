"""Account registry and fully isolated runtime paths."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY_FILE = PROJECT_ROOT / "accounts.json"
_ACCOUNT_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,31}$")


class AccountRegistryError(ValueError):
    pass


def validate_account_id(account_id: str) -> str:
    account_id = str(account_id or "").strip()
    if not _ACCOUNT_ID_RE.fullmatch(account_id):
        raise AccountRegistryError(
            "账户别名只能包含字母、数字、下划线和连字符，长度 1-32"
        )
    return account_id


def _atomic_write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".tmp", dir=str(path.parent)
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


@dataclass(frozen=True)
class AccountPaths:
    account_id: str
    display_name: str
    root: Path
    config_file: Path
    state_file: Path
    runtime_file: Path
    idempotency_file: Path
    start_lock_file: Path
    log_file: Path
    md_flow_dir: Path
    td_flow_dir: Path
    daemon_port: Optional[int]
    legacy: bool = False

    def ensure_layout(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self.md_flow_dir.mkdir(parents=True, exist_ok=True)
        self.td_flow_dir.mkdir(parents=True, exist_ok=True)


class AccountRegistry:
    """Load aliases while keeping credentials inside each instance directory."""

    def __init__(self, registry_file: Optional[Path] = None):
        configured = os.environ.get("CLAW_ACCOUNTS_FILE", "").strip()
        self.path = Path(registry_file or configured or DEFAULT_REGISTRY_FILE).resolve()
        self.project_root = PROJECT_ROOT
        self._data = self._load()

    @property
    def is_legacy(self) -> bool:
        return bool(self._data.get("legacy"))

    def _load(self) -> Dict[str, Any]:
        if not self.path.exists():
            return {
                "version": 1,
                "legacy": True,
                "default_account": "default",
                "accounts": {
                    "default": {
                        "display_name": "默认账户",
                        "path": ".",
                        "enabled": True,
                    }
                },
            }
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError) as exc:
            raise AccountRegistryError(f"账户注册表无法读取: {self.path}") from exc
        if not isinstance(data, dict) or not isinstance(data.get("accounts"), dict):
            raise AccountRegistryError(f"账户注册表格式无效: {self.path}")
        for account_id, entry in data["accounts"].items():
            validate_account_id(account_id)
            if not isinstance(entry, dict):
                raise AccountRegistryError(f"账户 {account_id} 配置必须是对象")
        ports = []
        for account_id, entry in data["accounts"].items():
            if not entry.get("enabled", True) or entry.get("daemon_port") is None:
                continue
            try:
                ports.append(int(entry["daemon_port"]))
            except (TypeError, ValueError) as exc:
                raise AccountRegistryError(
                    f"账户 {account_id} daemon_port 无效"
                ) from exc
        if len(ports) != len(set(ports)):
            raise AccountRegistryError("启用账户的 daemon_port 不能重复")
        return data

    def account_ids(self, include_disabled: bool = False) -> list[str]:
        result = []
        for account_id, entry in self._data["accounts"].items():
            if include_disabled or entry.get("enabled", True):
                result.append(account_id)
        return sorted(result)

    def default_account(self) -> str:
        explicit = os.environ.get("CLAW_ACCOUNT", "").strip()
        if explicit:
            return validate_account_id(explicit)
        configured = str(self._data.get("default_account") or "").strip()
        if configured:
            return validate_account_id(configured)
        accounts = self.account_ids()
        if len(accounts) == 1:
            return accounts[0]
        raise AccountRegistryError("存在多个账户，请明确指定 --account")

    def resolve(self, account_id: Optional[str] = None) -> AccountPaths:
        account_id = validate_account_id(account_id or self.default_account())
        entry = self._data["accounts"].get(account_id)
        if not isinstance(entry, dict):
            raise AccountRegistryError(f"账户不存在: {account_id}")
        if not entry.get("enabled", True):
            raise AccountRegistryError(f"账户已停用: {account_id}")

        relative = Path(str(entry.get("path") or f"accounts/{account_id}"))
        root = (self.project_root / relative).resolve() if not relative.is_absolute() else relative.resolve()
        try:
            root.relative_to(self.project_root)
        except ValueError as exc:
            raise AccountRegistryError("账户运行目录必须位于项目目录内") from exc

        legacy = self.is_legacy and account_id == "default"
        state_file = (
            PROJECT_ROOT / "scripts" / ".clawtrader_state.json"
            if legacy
            else root / ".clawtrader_state.json"
        )
        configured_port = entry.get("daemon_port")
        if configured_port is None and not legacy:
            configured_port = 17771 + self.account_ids().index(account_id)
        if configured_port is not None:
            try:
                configured_port = int(configured_port)
            except (TypeError, ValueError) as exc:
                raise AccountRegistryError(f"账户 {account_id} daemon_port 无效") from exc
            if not 1024 <= configured_port <= 65535:
                raise AccountRegistryError(f"账户 {account_id} daemon_port 超出范围")

        return AccountPaths(
            account_id=account_id,
            display_name=str(entry.get("display_name") or account_id),
            root=root,
            config_file=root / "config.json",
            state_file=state_file,
            runtime_file=root / ".clawtrader_runtime.json",
            idempotency_file=root / ".clawtrader_idempotency.json",
            start_lock_file=root / ".clawtrader_start.lock",
            log_file=root / "clawtrader.log",
            md_flow_dir=root / "flow" / "md",
            td_flow_dir=root / "flow" / "td",
            daemon_port=configured_port,
            legacy=legacy,
        )

    def public_accounts(self) -> list[Dict[str, Any]]:
        result = []
        for account_id in self.account_ids(include_disabled=True):
            entry = self._data["accounts"][account_id]
            paths = self.resolve(account_id) if entry.get("enabled", True) else None
            result.append({
                "account_id": account_id,
                "display_name": str(entry.get("display_name") or account_id),
                "enabled": bool(entry.get("enabled", True)),
                "configured": bool(paths and paths.config_file.exists()),
                "daemon_port": paths.daemon_port if paths else entry.get("daemon_port"),
            })
        return result

    def write_example(self, target: Optional[Path] = None) -> Path:
        target = Path(target or self.path)
        if target.exists():
            return target
        _atomic_write_json(target, {
            "version": 1,
            "default_account": "A",
            "accounts": {
                name: {
                    "display_name": f"账户 {name}",
                    "path": f"accounts/{name}",
                    "enabled": True,
                    "daemon_port": 17770 + index,
                }
                for index, name in enumerate("ABCDE", start=1)
            },
        })
        return target


def _pid_alive(pid: int) -> bool:
    """跨平台探活：Windows 上 os.kill(pid, 0) 的 0 == CTRL_C_EVENT 不能探活，
    改用 OpenProcess + GetExitCodeProcess 判断进程是否存活。"""
    if os.name == "nt":
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
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:      # 进程存在但无权限探测 → 视为存活
        return True


class AccountLease:
    """Process-lifetime lock preventing duplicate sessions for one real account."""

    def __init__(self, broker_id: str, user_id: str):
        identity = f"{broker_id}\0{user_id}".encode("utf-8")
        digest = hashlib.sha256(identity).hexdigest()[:24]
        self.path = PROJECT_ROOT / ".run" / f"account-{digest}.lock"
        self.acquired = False

    def acquire(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        for _ in range(2):
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            except FileExistsError:
                try:
                    pid = int(self.path.read_text(encoding="ascii").strip())
                    if _pid_alive(pid):
                        raise RuntimeError("该期货账户已有一个交易实例正在运行")
                    # 旧进程已退出，删除残留锁后重试一次
                    try:
                        self.path.unlink()
                    except FileNotFoundError:
                        pass
                    continue
                except (FileNotFoundError, ValueError):
                    raise RuntimeError("账户独占锁状态未知，拒绝启动第二个交易实例")
            else:
                try:
                    os.write(fd, str(os.getpid()).encode("ascii"))
                finally:
                    os.close(fd)
                self.acquired = True
                return
        raise RuntimeError("无法取得账户独占锁")

    def release(self) -> None:
        if not self.acquired:
            return
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass
        self.acquired = False
