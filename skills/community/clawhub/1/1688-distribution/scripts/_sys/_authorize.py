#!/usr/bin/env python3
"""
AK 获取入口（通过浏览器授权）

双进程架构：
  触发模式（正常调用）：
    python3 scripts/_sys/_authorize.py [--timeout 300]
  服务进程模式（内部自调用）：
    python3 scripts/_sys/_authorize.py --server-only [--timeout 300]

流程：
    1. 触发模式启动后台服务子进程
    2. 服务子进程启动回调服务器，通过 stdout 报告端口
    3. 触发模式输出 browser_use 提示后立即退出
    4. 服务子进程独立存活，等待用户完成浏览器操作后接收回调
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import secrets
import signal
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlencode

# Windows 默认 GBK 编码，强制 stdout/stderr 使用 UTF-8 避免中文输出报错
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))

from scripts._sys._const import (
    AUTHORIZE_ENDPOINT,
    CALLBACK_HOST,
    AUTHORIZATION_TIMEOUT,
    AK_DATA_DIR,
    LOG_FILE,
)
from scripts._sys._callback_server import AKCallbackServer

logger = logging.getLogger(__name__)


def _setup_logging() -> None:
    """仅在作为独立脚本运行时初始化日志。"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8")],
        force=True,
    )


def _setup_server_signals() -> None:
    """注册退出信号处理。仅在非 Windows 上注册 SIGTERM。"""
    def _handle(signum, frame):
        raise SystemExit(0)

    if sys.platform != "win32":
        signal.signal(signal.SIGTERM, _handle)
        logger.debug("已注册 SIGTERM 处理器")


def _open_browser(url: str, timeout: int = AUTHORIZATION_TIMEOUT) -> None:
    """输出 browser_use 提示，告知 Agent 使用 browser_use 工具打开授权链接。"""
    print(json.dumps({
        "pending": True,
        "action": "browser_use",
        "url": url,
        "markdown": (
            f"授权链接已生成！请使用 browser_use 工具打开以下链接完成授权：\n\n{url}\n\n"
            f"回调服务器已在后台独立运行（最长等待 {timeout} 秒）。"
            f"browser_use 完成后请调用 `configure --status` 确认授权结果。"
        ),
    }, ensure_ascii=False), flush=True)


def output_json(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False), flush=True)


# ── PID 文件管理：跟踪后台服务进程 ──
_PID_FILE = AK_DATA_DIR / ".authorize.pid"


def _kill_stale_process() -> None:
    """检测并终止上一次遗留的后台回调服务进程"""
    if not _PID_FILE.exists():
        return
    try:
        old_pid = int(_PID_FILE.read_text().strip())
        if old_pid == os.getpid():
            return
        if sys.platform == "win32":
            logger.debug("Windows: 使用 taskkill 终止遗留进程 PID=%d", old_pid)
            subprocess.run(["taskkill", "/PID", str(old_pid), "/F"],
                           capture_output=True, check=False)
        else:
            logger.debug("Unix: 使用 SIGTERM 终止遗留进程 PID=%d", old_pid)
            os.kill(old_pid, signal.SIGTERM)
        logger.info("已终止上一次遗留的回调服务进程 (PID=%d)", old_pid)
    except (ValueError, ProcessLookupError, PermissionError):
        pass
    finally:
        _PID_FILE.unlink(missing_ok=True)


def _write_pid() -> None:
    """写入当前进程 PID（由服务进程调用）"""
    _PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    _PID_FILE.write_text(str(os.getpid()))


def _cleanup_pid() -> None:
    """只在 PID 文件记录的仍是当前进程时才删除。"""
    try:
        if _PID_FILE.exists() and _PID_FILE.read_text().strip() == str(os.getpid()):
            _PID_FILE.unlink(missing_ok=True)
    except OSError:
        pass


# ═══════════════════════════════════════════════════════
# 服务进程模式（--server-only）
# ═══════════════════════════════════════════════════════

def _run_server_only(timeout: int) -> int:
    """AK 服务进程：写 PID，启动回调服务器，向父进程报告端口，阻塞等待回调。"""
    _setup_server_signals()
    _write_pid()

    state = secrets.token_urlsafe(32)
    server = AKCallbackServer(state=state)
    server.start()

    # 向父进程（通过 stdout pipe）报告端口和 state
    try:
        sys.stdout.write(json.dumps({"port": server.port, "state": state}, ensure_ascii=False) + "\n")
        sys.stdout.flush()
    except Exception:
        pass
    # 重定向到 /dev/null：安全隔断父进程管道
    try:
        sys.stdout = open(os.devnull, "w", encoding="utf-8")
    except Exception:
        pass

    # 独立阻塞等待，父进程已退出
    try:
        server.wait(timeout=timeout)
    finally:
        server.stop()
        _cleanup_pid()
    return 0


# ═══════════════════════════════════════════════════════
# 触发模式：启动服务子进程，输出 browser_use 提示后立即退出
# ═══════════════════════════════════════════════════════

def _spawn_server(timeout: int) -> dict:
    """
    以独立守护进程启动 --server-only 子进程。
    子进程通过 stdout 第一行 JSON 报告端口和 state，之后父进程关闭管道。
    """
    script = str(Path(__file__).resolve())
    cmd = [
        sys.executable, script,
        "--server-only",
        "--timeout", str(timeout),
    ]

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    stderr_sink = open(LOG_FILE, "a", encoding="utf-8")

    kwargs: dict = {
        "stdout": subprocess.PIPE,
        "stderr": stderr_sink,
        "text": True,
        "encoding": "utf-8",
    }
    if sys.platform == "win32":
        # CREATE_NO_WINDOW: 不弹控制台窗口
        # CREATE_NEW_PROCESS_GROUP: 父进程 Ctrl+C 不会传播到子进程
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP
        logger.debug("Windows 后台启动模式: CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP")
    else:
        kwargs["start_new_session"] = True
        logger.debug("Unix 后台启动模式: start_new_session=True")

    proc = subprocess.Popen(cmd, **kwargs)
    stderr_sink.close()
    line = proc.stdout.readline().strip()
    proc.stdout.close()  # 关闭管道，子进程独立运行

    try:
        return json.loads(line)
    except (json.JSONDecodeError, ValueError):
        proc.terminate()
        raise RuntimeError(f"回调服务器启动失败（输出: {line!r}）")


def get_ak(timeout: int = AUTHORIZATION_TIMEOUT) -> int:
    """
    启动浏览器授权流程获取 AK（双进程架构）。

    :param timeout: 等待超时秒数
    :return: 退出码 0=成功 1=失败
    """
    try:
        _kill_stale_process()
        server_info = _spawn_server(timeout)

        redirect_uri = f"http://{CALLBACK_HOST}:{server_info['port']}/callback"
        params = {"mode": "AK", "state": server_info["state"], "redirect_uri": redirect_uri}
        authorize_url = f"{AUTHORIZE_ENDPOINT}?{urlencode(params)}"

        _open_browser(authorize_url, timeout)
        return 0
    except Exception as e:
        logger.exception("AK 获取异常: %s", e)
        output_json({"success": False, "error_code": "AK_MODE_ERROR",
                     "markdown": f"获取 AK 失败：{e}"})
        return 1


def main() -> int:
    _setup_logging()
    parser = argparse.ArgumentParser(description="1688 AK 获取")
    parser.add_argument("--timeout", type=int, default=AUTHORIZATION_TIMEOUT)
    parser.add_argument("--server-only", action="store_true",
                        help="内部参数：以后台回调服务进程模式运行")
    args = parser.parse_args()

    if args.server_only:
        return _run_server_only(args.timeout)

    return get_ak(timeout=args.timeout)


if __name__ == "__main__":
    sys.exit(main())
