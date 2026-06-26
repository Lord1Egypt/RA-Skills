"""Chrome 进程管理（跨平台），用于 CDP 远程调试。

与 xiaohongshu-skills 的 chrome_launcher 结构一致；Profile 默认 ~/.kbs/chrome-profile。
"""

from __future__ import annotations

import contextlib
import json
import logging
import os
import platform
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_PORT = 9222

_chrome_process: subprocess.Popen | None = None

_CHROME_PATHS: dict[str, list[str]] = {
    "Darwin": [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ],
    "Linux": [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/snap/bin/chromium",
    ],
    "Windows": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ],
}

# 与小红书 skill 一致的反自动化特征启动参数
STEALTH_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--disable-infobars",
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-renderer-backgrounding",
    "--disable-component-update",
    "--disable-extensions",
    "--disable-sync",
]


def _get_default_data_dir() -> str:
    return str(Path.home() / ".kbs" / "chrome-profile")


def is_port_open(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        try:
            s.connect((host, port))
            return True
        except (ConnectionRefusedError, TimeoutError, OSError):
            return False


def find_chrome() -> str | None:
    env_path = os.getenv("CHROME_BIN")
    if env_path and os.path.isfile(env_path):
        return env_path

    chrome = (
        shutil.which("google-chrome")
        or shutil.which("chromium")
        or shutil.which("chrome")
        or shutil.which("chrome.exe")
    )
    if chrome:
        return chrome

    system = platform.system()
    if system == "Windows":
        for env_var in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA"):
            base = os.environ.get(env_var, "")
            if base:
                candidate = os.path.join(base, "Google", "Chrome", "Application", "chrome.exe")
                if os.path.isfile(candidate):
                    return candidate

    for path in _CHROME_PATHS.get(system, []):
        if os.path.isfile(path):
            return path

    return None


def is_chrome_running(port: int = DEFAULT_PORT) -> bool:
    return is_port_open(port)


def launch_chrome(
    port: int = DEFAULT_PORT,
    headless: bool = False,
    user_data_dir: str | None = None,
    chrome_bin: str | None = None,
) -> subprocess.Popen | None:
    global _chrome_process

    if is_port_open(port):
        logger.info("Chrome 已在运行 (port=%d)，跳过启动", port)
        return None

    if not chrome_bin:
        chrome_bin = find_chrome()
    if not chrome_bin:
        raise FileNotFoundError("未找到 Chrome，请设置 CHROME_BIN 环境变量或安装 Chrome")

    if not user_data_dir:
        user_data_dir = _get_default_data_dir()

    args = [
        chrome_bin,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data_dir}",
        *STEALTH_ARGS,
    ]

    if headless:
        args.append("--headless=new")

    proxy = os.getenv("KBS_PROXY") or os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY")
    if proxy:
        args.append(f"--proxy-server={proxy}")
        logger.info("使用代理: %s", proxy)

    logger.info("启动 Chrome: port=%d, headless=%s, profile=%s", port, headless, user_data_dir)
    process = subprocess.Popen(
        args,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    _chrome_process = process

    _wait_for_chrome(port)
    return process


def close_chrome(process: subprocess.Popen) -> None:
    if process.poll() is not None:
        return
    try:
        process.terminate()
        process.wait(timeout=5)
    except (subprocess.TimeoutExpired, OSError):
        process.kill()
        process.wait(timeout=3)
    logger.info("Chrome 进程已关闭")


def kill_chrome(port: int = DEFAULT_PORT) -> None:
    global _chrome_process

    try:
        import requests

        resp = requests.get(f"http://127.0.0.1:{port}/json/version", timeout=2)
        if resp.status_code == 200:
            ws_url = resp.json().get("webSocketDebuggerUrl")
            if ws_url:
                import websockets.sync.client

                ws = websockets.sync.client.connect(ws_url)
                ws.send(json.dumps({"id": 1, "method": "Browser.close"}))
                ws.close()
                logger.info("通过 CDP Browser.close 关闭 Chrome (port=%d)", port)
                time.sleep(1)
    except Exception:
        pass

    if _chrome_process and _chrome_process.poll() is None:
        try:
            _chrome_process.terminate()
            _chrome_process.wait(timeout=5)
            logger.info("通过 terminate 关闭追踪的 Chrome 进程")
        except Exception:
            with contextlib.suppress(Exception):
                _chrome_process.kill()
    _chrome_process = None

    if is_port_open(port):
        pids = _find_pids_by_port(port)
        if pids:
            for pid in pids:
                _kill_pid(pid)
            logger.info("通过进程终止关闭 Chrome (port=%d)", port)

    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        if not is_port_open(port):
            return
        time.sleep(0.5)

    if is_port_open(port):
        logger.warning("端口 %d 仍被占用，kill 可能未完全生效", port)


def ensure_chrome(
    port: int = DEFAULT_PORT,
    headless: bool = False,
    user_data_dir: str | None = None,
    chrome_bin: str | None = None,
) -> bool:
    if is_port_open(port):
        return True
    try:
        launch_chrome(
            port=port,
            headless=headless,
            user_data_dir=user_data_dir,
            chrome_bin=chrome_bin,
        )
        return is_port_open(port)
    except FileNotFoundError as e:
        logger.error("启动 Chrome 失败: %s", e)
        return False


def restart_chrome(
    port: int = DEFAULT_PORT,
    headless: bool = False,
    user_data_dir: str | None = None,
    chrome_bin: str | None = None,
) -> subprocess.Popen | None:
    logger.info("重启 Chrome: port=%d, headless=%s", port, headless)
    kill_chrome(port)
    time.sleep(1)
    return launch_chrome(
        port=port,
        headless=headless,
        user_data_dir=user_data_dir,
        chrome_bin=chrome_bin,
    )


def _wait_for_chrome(port: int, timeout: float = 15.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if is_port_open(port):
            logger.info("Chrome 已就绪 (port=%d)", port)
            return
        time.sleep(0.5)
    logger.warning("等待 Chrome 就绪超时 (port=%d)", port)


def _find_pids_by_port(port: int) -> list[int]:
    try:
        if sys.platform == "win32":
            result = subprocess.run(
                ["netstat", "-ano", "-p", "TCP"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode != 0:
                return []
            pids: list[int] = []
            for line in result.stdout.splitlines():
                if f":{port}" in line and "LISTENING" in line:
                    parts = line.split()
                    with contextlib.suppress(ValueError, IndexError):
                        pids.append(int(parts[-1]))
            return list(set(pids))
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0 or not result.stdout.strip():
            return []
        pids = []
        for p in result.stdout.strip().split("\n"):
            with contextlib.suppress(ValueError):
                pids.append(int(p))
        return pids
    except Exception:
        return []


def _kill_pid(pid: int) -> None:
    try:
        if sys.platform == "win32":
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/F"],
                capture_output=True,
                timeout=5,
            )
        else:
            import signal

            os.kill(pid, signal.SIGTERM)
    except Exception:
        logger.debug("终止进程 %d 失败", pid)


def has_display() -> bool:
    system = platform.system()
    if system in ("Windows", "Darwin"):
        return True
    return bool(os.getenv("DISPLAY") or os.getenv("WAYLAND_DISPLAY"))
