"""
core/keychain.py — 跨平台密钥管理
支持：macOS / Windows / Linux

存储策略：
- macOS:     security 命令（Keychain）
- Windows:   cmdkey（凭据管理器）
- Linux:     secret-tool（libsecret/GNOME Keyring）
- Fallback:  config.json（仅限 api_token，master_password 必须用系统密钥链）
"""
from __future__ import annotations

import os, json, subprocess, sys
from pathlib import Path

HOME = Path.home()
CONFIG_PATH = HOME / ".amber-hunter" / "config.json"
SERVICE_NAME = "com.huper.amber-hunter"


def _detect_os():
    if sys.platform == "darwin":
        return "macos"
    elif sys.platform == "win32":
        return "windows"
    else:
        return "linux"


OS = _detect_os()


# ── macOS ────────────────────────────────────────────────
def _macos_get(account: str) -> str | None:
    try:
        r = subprocess.run(
            ["security", "find-generic-password", "-s", SERVICE_NAME, "-a", account, "-w"],
            capture_output=True, text=True, timeout=3
        )
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def _macos_set(account: str, password: str) -> bool:
    try:
        subprocess.run(
            ["security", "delete-generic-password", "-s", SERVICE_NAME, "-a", account],
            capture_output=True
        )
        r = subprocess.run(
            ["security", "add-generic-password",
             "-s", SERVICE_NAME, "-a", account, "-w", password, "-U"],
            capture_output=True, text=True
        )
        return r.returncode == 0
    except Exception:
        return False


# ── Windows ─────────────────────────────────────────────
def _windows_get(account: str) -> str | None:
    """从 Windows 凭据管理器读取密码（需要 pywin32）。
    未安装 pywin32 时返回 None；调用方（get_master_password）会 fallback 到 config.json。
    安装方法：pip install pywin32
    """
    try:
        import win32cred
        target = f"amber-hunter:{account}"
        cred = win32cred.CredRead(target, win32cred.CRED_TYPE_GENERIC)
        if cred and cred.get("CredentialBlob"):
            blob = cred["CredentialBlob"]
            # CredentialBlob 以 UTF-16-LE 编码字节串返回
            return blob.decode("utf-16-le") if isinstance(blob, bytes) else str(blob)
    except ImportError:
        pass  # pywin32 未安装，由 get_master_password() 处理 fallback
    except Exception:
        pass
    return None


def _windows_set(account: str, password: str) -> bool:
    """将密码写入 Windows 凭据管理器（需要 pywin32）。
    未安装 pywin32 时回落到 cmdkey（仅存储，无法读回）。
    安装方法：pip install pywin32
    """
    target = f"amber-hunter:{account}"
    # 优先使用 win32cred（可读回密码）
    try:
        import win32cred
        credential = {
            "Type": win32cred.CRED_TYPE_GENERIC,
            "TargetName": target,
            "UserName": "amber",
            "CredentialBlob": password,
            "Persist": win32cred.CRED_PERSIST_LOCAL_MACHINE,
        }
        win32cred.CredWrite(credential, 0)
        return True
    except ImportError:
        pass  # pywin32 未安装，fallback 到 cmdkey
    except Exception:
        return False
    # Fallback: cmdkey（密码无法被程序读回，但至少记录凭据存在）
    try:
        subprocess.run(["cmdkey", "/delete", target], capture_output=True)
        r = subprocess.run(
            ["cmdkey", "/generic:" + target, "/user:amber", "/pass:" + password],
            capture_output=True, timeout=5
        )
        return r.returncode == 0
    except Exception:
        return False


# ── Linux ────────────────────────────────────────────────
def _linux_is_headless() -> bool:
    """检测当前 Linux 是否为无桌面环境（VPS / headless server）。
    判断依据：无 DISPLAY/WAYLAND_DISPLAY 环境变量，或 secret-tool 不可用。
    """
    has_display = bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
    has_dbus = bool(os.environ.get("DBUS_SESSION_BUS_ADDRESS"))
    has_secret_tool = False
    try:
        r = subprocess.run(["which", "secret-tool"], capture_output=True, timeout=2)
        has_secret_tool = r.returncode == 0
    except Exception:
        pass
    return not (has_display and has_dbus and has_secret_tool)


def _linux_config_get(account: str) -> str | None:
    """从 config.json 读取凭据（headless 降级路径）"""
    if CONFIG_PATH.exists():
        try:
            cfg = json.loads(CONFIG_PATH.read_text())
            return cfg.get(account) or None
        except Exception:
            pass
    return None


def _linux_config_set(account: str, password: str) -> bool:
    """将凭据写入 config.json（headless 降级路径，明文存储，用户知情）"""
    try:
        cfg = {}
        if CONFIG_PATH.exists():
            cfg = json.loads(CONFIG_PATH.read_text())
        cfg[account] = password
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(json.dumps(cfg, indent=2))
        return True
    except Exception:
        return False


def _linux_get(account: str) -> str | None:
    # headless 环境（VPS）：直接从 config.json 读取
    if _linux_is_headless():
        return _linux_config_get(account)
    try:
        r = subprocess.run(
            ["secret-tool", "lookup", "amber-hunter", account],
            capture_output=True, text=True, timeout=3
        )
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def _linux_set(account: str, password: str) -> bool:
    # headless 环境（VPS）：写入 config.json（明文，用户知情）
    if _linux_is_headless():
        return _linux_config_set(account, password)
    try:
        r1 = subprocess.run(
            ["secret-tool", "store", f"--label=Amber Hunter {account}",
             "amber-hunter", account],
            input=password, capture_output=True, timeout=3, text=True
        )
        return r1.returncode == 0
    except Exception:
        return False


# ── Cross-platform dispatcher ────────────────────────────
def _credential_get(account: str):
    if OS == "macos":
        return _macos_get(account)
    elif OS == "windows":
        return _windows_get(account)
    elif OS == "linux":
        return _linux_get(account)
    return None


def _credential_set(account: str, password: str) -> bool:
    if OS == "macos":
        return _macos_set(account, password)
    elif OS == "windows":
        return _windows_set(account, password)
    elif OS == "linux":
        return _linux_set(account, password)
    return False


# ── Public API ──────────────────────────────────────────
def get_master_password() -> str | None:
    """
    获取 master_password。
    macOS:           从 Keychain（security CLI）读取。
    Linux（桌面）:   从 GNOME Keyring（secret-tool）读取。
    Linux（headless）: 从 config.json 读取（_linux_get 内部自动降级）。
    Windows:         cmdkey 无法读回密码，fallback 到 config.json（明文，用户知情）。
    """
    pw = _credential_get("master_password")
    if pw:
        return pw
    # Windows fallback: cmdkey 不支持通过命令行读回密码，从 config.json 读取
    if OS == "windows" and CONFIG_PATH.exists():
        try:
            cfg = json.loads(CONFIG_PATH.read_text())
            return cfg.get("master_password") or None
        except Exception:
            pass
    return None


def set_master_password(password: str) -> bool:
    """设置 master_password 到系统密钥链"""
    return _credential_set("master_password", password)


def get_api_token() -> str | None:
    """
    获取本地 API token。
    优先级：系统密钥链 > 环境变量 AMBER_TOKEN > config.json
    """
    # 1. 系统密钥链
    token = _credential_get("api_token")
    if token:
        return token

    # 2. 环境变量
    token = os.environ.get("AMBER_TOKEN")
    if token:
        return token

    # 3. config.json
    if CONFIG_PATH.exists():
        try:
            cfg = json.loads(CONFIG_PATH.read_text())
            return cfg.get("api_token") or cfg.get("api_key")
        except Exception:
            pass
    return None


def get_huper_url() -> str:
    if CONFIG_PATH.exists():
        try:
            cfg = json.loads(CONFIG_PATH.read_text())
            return cfg.get("huper_url", "https://huper.org/api")
        except Exception:
            pass
    return "https://huper.org/api"


def ensure_config_dir():
    (HOME / ".amber-hunter").mkdir(parents=True, exist_ok=True)


def get_os() -> str:
    """返回当前操作系统名称"""
    return OS


def is_headless() -> bool:
    """检测当前环境是否为无桌面 headless 环境。
    Linux headless（VPS）返回 True；macOS/Windows 始终返回 False。
    """
    if OS == "linux":
        return _linux_is_headless()
    return False
