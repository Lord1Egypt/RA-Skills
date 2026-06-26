#!/usr/bin/env python3
"""
OpenClaw Gateway Watchdog
Gateway 24/7 稳定运行 watchdog

用法:
  python gateway_watchdog.py start   - 启动 watchdog
  python gateway_watchdog.py stop    - 停止 watchdog
  python gateway_watchdog.py status  - 查看状态
  python gateway_watchdog.py restart - 重启 Gateway
"""

import subprocess
import time
import os
import sys
import platform
import json
import argparse
import signal
from pathlib import Path
from pathlib import PureWindowsPath

# 配置目录 - 放脚本同目录下
SCRIPT_DIR = Path(__file__).parent.resolve()
CONFIG_FILE = SCRIPT_DIR / "gateway_watchdog.json"
LOG_FILE = SCRIPT_DIR / "gateway_watchdog.log"
PID_FILE = SCRIPT_DIR / "gateway_watchdog.pid"

CHECK_INTERVAL = 10  # 秒
FAIL_THRESHOLD = 2   # 连续失败次数

def get_config_path() -> Path:
    """获取配置文件路径"""
    return CONFIG_FILE

def load_config() -> dict:
    """加载配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_config(config: dict):
    """保存配置"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def detect_openclaw() -> str:
    """检测 openclaw 命令路径"""
    system = platform.system()
    
    # 首先尝试直接调用 (可能已经在 PATH 中)
    try:
        result = subprocess.run(
            ["openclaw", "--version"],
            capture_output=True,
            timeout=10,
            shell=(system == "Windows")
        )
        if result.returncode == 0:
            return "openclaw"
    except:
        pass
    
    if system == "Windows":
        # Windows: 尝试常见位置
        paths_to_try = [
            "openclaw.ps1",  # npm 全局安装
            Path(os.environ.get("APPDATA", "")) / "npm" / "openclaw.ps1",
            Path("C:/Program Files/nodejs/openclaw.ps1"),
            Path(os.environ.get("LOCALAPPDATA", "")) / "npm" / "openclaw.ps1",
        ]
        
        for p in paths_to_try:
            try:
                result = subprocess.run(
                    [str(p), "--version"],
                    capture_output=True,
                    timeout=10,
                    shell=True
                )
                if result.returncode == 0:
                    return str(p)
            except:
                continue
        
        # 尝试 npx
        try:
            result = subprocess.run(
                ["npx", "openclaw", "--version"],
                capture_output=True,
                timeout=10,
                shell=True
            )
            if result.returncode == 0:
                return "npx openclaw"
        except:
            pass
            
    else:
        # Linux/Mac: 尝试常见位置
        paths_to_try = [
            "openclaw",
            "/usr/local/bin/openclaw",
            "/usr/bin/openclaw",
            Path.home() / ".nvm/versions/node/*/bin/openclaw",
        ]
        
        for p in paths_to_try:
            try:
                result = subprocess.run(
                    [str(p), "--version"],
                    capture_output=True,
                    timeout=10
                )
                if result.returncode == 0:
                    return str(p)
            except:
                continue
    
    return None

def get_openclaw_cmd() -> list:
    """获取 openclaw 命令列表"""
    config = load_config()
    cmd = config.get("openclaw_cmd", "openclaw")
    
    if platform.system() == "Windows" and " " in cmd:
        return cmd.split()
    return [cmd]

def log(msg: str):
    """写日志"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def check_gateway() -> bool:
    """检查 Gateway 是否正常运行"""
    try:
        cmd = get_openclaw_cmd() + ["gateway", "status"]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=15,
            shell=(platform.system() == "Windows")
        )
        return result.returncode == 0
    except Exception as e:
        log(f"检查失败: {e}")
        return False

def restart_gateway():
    """重启 Gateway"""
    try:
        log("Gateway 连续失败，准备重启...")
        cmd = get_openclaw_cmd() + ["gateway", "restart"]
        subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            shell=(platform.system() == "Windows")
        )
        log("Gateway 重启命令已发送")
        return True
    except Exception as e:
        log(f"重启失败: {e}")
        return False

def watchdog_loop():
    """Watchdog 主循环"""
    log("=" * 50)
    log(f"Gateway Watchdog 启动 ({platform.system()})")
    log(f"检查间隔: {CHECK_INTERVAL}s, 失败阈值: {FAIL_THRESHOLD}")
    log("=" * 50)

    consecutive_failures = 0

    while True:
        try:
            if check_gateway():
                if consecutive_failures > 0:
                    log(f"Gateway 恢复正常 (之前连续失败 {consecutive_failures} 次)")
                    consecutive_failures = 0
            else:
                consecutive_failures += 1
                log(f"Gateway 检查失败 ({consecutive_failures}/{FAIL_THRESHOLD})")

                if consecutive_failures >= FAIL_THRESHOLD:
                    restart_gateway()
                    consecutive_failures = 0

        except Exception as e:
            log(f"循环异常: {e}")

        time.sleep(CHECK_INTERVAL)

def start_watchdog():
    """启动 watchdog"""
    # 检查是否已运行
    if PID_FILE.exists():
        with open(PID_FILE, "r") as f:
            old_pid = f.read().strip()
        try:
            # 检查进程是否存在
            if platform.system() == "Windows":
                result = subprocess.run(
                    f"tasklist /FI \"PID eq {old_pid}\"",
                    capture_output=True,
                    text=True,
                    shell=True
                )
                if old_pid in result.stdout:
                    print(f"Watchdog 已在运行 (PID: {old_pid})")
                    return
            else:
                os.kill(int(old_pid), 0)
                print(f"Watchdog 已在运行 (PID: {old_pid})")
                return
        except:
            pass
        PID_FILE.unlink()
    
    # 检测 openclaw
    openclaw_path = detect_openclaw()
    if not openclaw_path:
        print("错误: 无法找到 openclaw 命令")
        print("请确保 OpenClaw 已正确安装")
        sys.exit(1)
    
    # 保存配置
    config = load_config()
    config["openclaw_cmd"] = openclaw_path
    save_config(config)
    print(f"OpenClaw 路径: {openclaw_path}")
    
    # 启动 watchdog
    log("启动 Gateway Watchdog...")
    
    if platform.system() == "Windows":
        # Windows: 用 start /b 后台运行
        proc = subprocess.Popen(
            [sys.executable, __file__, "run"],
            stdout=open(LOG_FILE, "a"),
            stderr=subprocess.STDOUT,
            cwd=os.getcwd(),
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        # Linux: nohup
        proc = subprocess.Popen(
            ["nohup", sys.executable, __file__, "run"],
            stdout=open(LOG_FILE, "a"),
            stderr=subprocess.STDOUT,
            cwd=os.getcwd()
        )
    
    # 等待一下让进程启动
    time.sleep(2)
    
    # 写入子进程 PID
    with open(PID_FILE, "w") as f:
        f.write(str(proc.pid))
    
    print(f"✅ Gateway Watchdog 已启动")
    print(f"日志: {LOG_FILE}")

def stop_watchdog():
    """停止 watchdog"""
    if not PID_FILE.exists():
        print("Watchdog 未运行")
        return
    
    with open(PID_FILE, "r") as f:
        pid = f.read().strip()
    
    try:
        if platform.system() == "Windows":
            subprocess.run(f"taskkill /PID {pid} /F", shell=True)
        else:
            os.kill(int(pid), signal.SIGTERM)
        PID_FILE.unlink()
        print("✅ Watchdog 已停止")
    except Exception as e:
        print(f"停止失败: {e}")

def status_watchdog():
    """查看状态"""
    print("=" * 50)
    print("1. Gateway Watchdog 进程")
    print("=" * 50)
    
    # 检查 watchdog
    if PID_FILE.exists():
        with open(PID_FILE, "r") as f:
            pid = f.read().strip()
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    f"tasklist /FI \"PID eq {pid}\"",
                    capture_output=True,
                    text=True,
                    shell=True
                )
                running = pid in result.stdout
            else:
                os.kill(int(pid), 0)
                running = True
        except:
            running = False
        
        if running:
            print(f"✅ 运行中 (PID: {pid})")
        else:
            print("❌ 已停止 (PID 文件过期)")
    else:
        print("❌ 未运行")
    
    # 检查 Gateway
    print("\n" + "=" * 50)
    print("2. OpenClaw Gateway")
    print("=" * 50)
    try:
        cmd = get_openclaw_cmd() + ["gateway", "status"]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=15,
            shell=(platform.system() == "Windows")
        )
        if result.returncode == 0:
            print("✅ Gateway 运行中")
            # 显示详细输出
            if result.stdout.strip():
                print(result.stdout)
        else:
            print("❌ Gateway 已停止")
            if result.stderr.strip():
                print(result.stderr[:500])
            elif result.stdout.strip():
                print(result.stdout[:500])
    except Exception as e:
        print(f"❌ 检查失败: {e}")

def restart_gateway_cmd():
    """重启 Gateway 命令"""
    log("手动重启 Gateway...")
    try:
        cmd = get_openclaw_cmd() + ["gateway", "restart"]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            shell=(platform.system() == "Windows")
        )
        if result.returncode == 0:
            print("✅ Gateway 已重启")
        else:
            print(f"❌ 重启失败: {result.stderr}")
    except Exception as e:
        print(f"❌ 重启失败: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw Gateway Watchdog",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python gateway_watchdog.py start    启动 watchdog
  python gateway_watchdog.py stop     停止 watchdog
  python gateway_watchdog.py status    查看状态
  python gateway_watchdog.py restart   重启 Gateway
        """
    )
    
    parser.add_argument("action", choices=["start", "stop", "status", "restart", "run"],
                       help="操作: start=启动, stop=停止, status=状态, restart=重启Gateway, run=运行循环")
    parser.add_argument("--interval", type=int, default=10, help="检查间隔(秒)")
    parser.add_argument("--threshold", type=int, default=2, help="失败阈值")
    
    args = parser.parse_args()
    
    global CHECK_INTERVAL, FAIL_THRESHOLD
    CHECK_INTERVAL = args.interval
    FAIL_THRESHOLD = args.threshold
    
    if args.action == "start":
        start_watchdog()
    elif args.action == "stop":
        stop_watchdog()
    elif args.action == "status":
        status_watchdog()
    elif args.action == "restart":
        restart_gateway_cmd()
    elif args.action == "run":
        watchdog_loop()

if __name__ == "__main__":
    main()
