#!/usr/bin/env python3
# Author: SQ
"""
Garmin Connect 后台守护进程
定时检查并同步缺失的数据（每30分钟一次）
支持自动重启、限流保护、数据完整性检查

用法:
    python3 sync_daemon.py              # 前台运行（调试）
    python3 sync_daemon.py --daemon     # 后台守护运行
    python3 sync_daemon.py --stop       # 停止后台进程
    python3 sync_daemon.py --status     # 查看运行状态
"""
import os
import sys
import time
import json
import signal
import subprocess
import argparse
import socket
import fcntl
import struct
from pathlib import Path
from datetime import datetime, timedelta, timezone

LOCK_FILE = Path.home() / ".clawdbot" / "garmin" / "sync_daemon.lock"
PID_FILE = Path.home() / ".clawdbot" / "garmin" / "sync_daemon.pid"
STATE_FILE = Path.home() / ".clawdbot" / "garmin" / "sync_daemon_state.json"
SYNC_INTERVAL = 30 * 60  # 30分钟
MAX_RETRIES = 3
RETRY_DELAY = 5 * 60  # 5分钟
RATE_LIMIT_DELAY = 30 * 60  # 30分钟

# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def beijing_now():
    return datetime.now(timezone(timedelta(hours=8)))

def log(msg):
    print(f"[{beijing_now().strftime('%H:%M:%S')}] {msg}")

def get_pid():
    if PID_FILE.exists():
        try:
            return int(PID_FILE.read_text().strip())
        except:
            return None
    return None

def is_running():
    pid = get_pid()
    if pid and pid != os.getpid():
        try:
            os.kill(pid, 0)
            return pid
        except OSError:
            return None
    return None

def save_pid():
    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(os.getpid()))

def save_state(**kwargs):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state = {}
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text())
        except:
            pass
    state.update(kwargs)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except:
            pass
    return {}

def acquire_lock():
    """获取锁文件，防止重复启动"""
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(str(LOCK_FILE), os.O_RDWR | os.O_CREAT | os.O_TRUNC, 0o644)
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return fd
    except (OSError, IOError):
        return None

# ─────────────────────────────────────────────
# Garmin 同步核心
# ─────────────────────────────────────────────

def run_sync(source="daemon"):
    """运行一次同步"""
    sync_script = Path(__file__).parent / "sync_all.py"
    venv_python = Path.home() / ".venv" / "garmin" / "bin" / "python"

    cmd = [str(venv_python), str(sync_script), "--source", source]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "time": beijing_now().isoformat(),
        }
    except subprocess.TimeoutExpired:
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": "Sync timeout (>120s)",
            "time": beijing_now().isoformat(),
        }
    except Exception as e:
        return {
            "returncode": -2,
            "stdout": "",
            "stderr": str(e),
            "time": beijing_now().isoformat(),
        }

def check_rate_limit(result):
    """检查是否是限流错误"""
    stderr = result.get("stderr", "")
    return "429" in stderr or "Too Many Requests" in stderr or "rate limit" in stderr.lower()

# ─────────────────────────────────────────────
# 守护循环
# ─────────────────────────────────────────────

def daemon_loop():
    """主守护循环"""
    log("🚀 Garmin 守护进程启动")
    log(f"   同步间隔: {SYNC_INTERVAL // 60} 分钟")
    log(f"   重试次数: {MAX_RETRIES}")
    log(f"   锁文件: {LOCK_FILE}")

    consecutive_errors = 0
    last_rate_limit = None

    while True:
        loop_start = time.time()
        state = load_state()
        last_sync = state.get("last_success")
        consecutive_failures = state.get("consecutive_failures", 0)

        log(f"--- 同步检查 (上次成功: {last_sync or '从未'})")

        result = run_sync(source="daemon")

        if result["returncode"] == 0 and "✅" in result.get("stdout", ""):
            log(f"✅ 同步成功")
            consecutive_errors = 0
            consecutive_failures = 0
            save_state(last_success=result["time"], consecutive_failures=0)

            if last_rate_limit:
                log(f"   (限流已解除)")
                last_rate_limit = None

        elif check_rate_limit(result):
            # 限流，等更长时间
            wait = RATE_LIMIT_DELAY
            last_rate_limit = beijing_now().isoformat()
            log(f"⚠️ 触发限流，等待 {wait // 60} 分钟")
            save_state(last_rate_limit=last_rate_limit)
            time.sleep(wait)
            continue

        else:
            consecutive_errors += 1
            consecutive_failures += 1
            err_msg = result.get("stderr", "unknown error")
            log(f"❌ 同步失败: {err_msg[:80]}")
            log(f"   连续失败: {consecutive_failures}/{MAX_RETRIES}")

            if consecutive_failures >= MAX_RETRIES:
                log(f"⚠️ 连续 {MAX_RETRIES} 次失败，暂停 {RETRY_DELAY // 60} 分钟")
                save_state(
                    consecutive_failures=consecutive_failures,
                    last_failure=result["time"]
                )
                time.sleep(RETRY_DELAY)
                consecutive_failures = 0
            else:
                save_state(consecutive_failures=consecutive_failures, last_failure=result["time"])
                time.sleep(30)  # 等30秒再试

        elapsed = time.time() - loop_start
        sleep_time = max(SYNC_INTERVAL - elapsed, 60)
        log(f"   下次同步: {sleep_time / 60:.0f} 分钟后")
        time.sleep(sleep_time)

# ─────────────────────────────────────────────
# 命令行控制
# ─────────────────────────────────────────────

def daemon_start():
    pid = is_running()
    if pid:
        print(f"守护进程已在运行 (PID {pid})")
        return

    # 前台测试一次
    log("运行一次同步测试...")
    result = run_sync("daemon-test")
    if result["returncode"] == 0:
        log("同步测试成功！")
    else:
        log(f"同步测试失败: {result.get('stderr', 'unknown')[:100]}")

    print("启动后台守护进程...")
    pid = subprocess.Popen(
        [sys.executable, __file__],
        stdout=open(os.devnull, "w"),
        stderr=open(os.devnull, "w"),
        start_new_session=True
    ).pid
    print(f"守护进程已启动 (PID {pid})")

def daemon_stop():
    pid = is_running()
    if pid:
        print(f"正在停止守护进程 (PID {pid})...")
        os.kill(pid, signal.SIGTERM)
        time.sleep(2)
        print("已停止")
    else:
        print("守护进程未运行")

def daemon_status():
    pid = is_running()
    if pid:
        state = load_state()
        print(f"✅ 守护进程运行中 (PID {pid})")
        print(f"   上次成功: {state.get('last_success', '从未')}")
        print(f"   上次限流: {state.get('last_rate_limit', '无')}")
        print(f"   连续失败: {state.get('consecutive_failures', 0)}")
    else:
        print("❌ 守护进程未运行")

# ─────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Garmin Connect 后台守护进程")
    parser.add_argument("--daemon", action="store_true", help="后台守护运行")
    parser.add_argument("--stop", action="store_true", help="停止守护进程")
    parser.add_argument("--status", action="store_true", help="查看状态")
    args = parser.parse_args()

    if args.stop:
        daemon_stop()
    elif args.status:
        daemon_status()
    elif args.daemon:
        lock_fd = acquire_lock()
        if lock_fd is None:
            print("无法获取锁，守护进程可能已在运行")
            sys.exit(1)
        signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
        save_pid()
        daemon_loop()
    else:
        # 默认：前台运行一次测试，然后启动守护
        if acquire_lock() is None:
            print("守护进程已在运行（前台测试跳过）")
            sys.exit(0)
        daemon_loop()
