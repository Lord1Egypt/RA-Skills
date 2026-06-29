#!/usr/bin/env python3
"""
Chrome浏览器启动器 - 跨平台统一入口
直接启动 Chrome 带调试端口，不依赖批处理脚本

使用方法:
    python launcher.py [--mode {independent|reuse}]

参数:
    --mode independent  - 独立profile模式（无痕）
    --mode reuse        - 复用主profile模式（默认）
"""

import argparse
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


def get_system():
    """检测操作系统类型"""
    system = platform.system().lower()
    if system == "windows" or system == "win32":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"


def find_chrome_windows():
    """在 Windows 上查找 Chrome 路径"""
    possible_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # 尝试使用 where 命令
    try:
        result = subprocess.run(
            ["where", "chrome.exe"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout.strip().split('\n')[0]
    except:
        pass
    
    return None


def find_chrome_unix():
    """在 macOS/Linux 上查找 Chrome/Chromium 路径"""
    system = get_system()
    
    if system == "macos":
        possible_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ]
    else:  # linux
        possible_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
            "/snap/bin/chromium",
        ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # 尝试使用 which 命令
    for cmd in ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser"]:
        try:
            result = subprocess.run(
                ["which", cmd],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout:
                return result.stdout.strip()
        except:
            pass
    
    return None


def kill_process_on_port(port=9222):
    """关闭占用指定端口的进程"""
    system = get_system()
    
    if system == "windows":
        try:
            # 查找占用端口的进程
            result = subprocess.run(
                ["netstat", "-ano"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            for line in result.stdout.split('\n'):
                if f":{port}" in line and "LISTENING" in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[-1]
                        try:
                            subprocess.run(
                                ["taskkill", "/F", "/PID", pid],
                                capture_output=True,
                                timeout=5
                            )
                        except:
                            pass
        except:
            pass
    else:
        # macOS/Linux
        try:
            subprocess.run(
                ["lsof", "-ti", f":{port}"],
                capture_output=True,
                timeout=5
            )
        except:
            pass


def start_chrome_independent():
    """使用独立 profile 启动 Chrome"""
    system = get_system()
    
    # 查找 Chrome
    if system == "windows":
        chrome_path = find_chrome_windows()
    else:
        chrome_path = find_chrome_unix()
    
    if not chrome_path:
        print("[ERROR] Chrome browser not found.")
        print("Please make sure Google Chrome is installed.")
        return False
    
    print(f"[INFO] Chrome path: {chrome_path}")
    
    # 关闭占用 9222 端口的进程
    print("[INFO] Checking port 9222...")
    kill_process_on_port(9222)
    time.sleep(0.5)
    
    # 准备启动参数
    if system == "windows":
        debug_profile = os.path.expandvars(r"%USERPROFILE%\chrome-debug-profile")
        cmd = [
            chrome_path,
            "--remote-debugging-port=9222",
            f"--user-data-dir={debug_profile}",
            "--no-first-run",
            "--no-default-browser-check"
        ]
        # Windows 使用 CREATE_NEW_PROCESS_GROUP 来避免阻塞
        creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        debug_profile = os.path.expanduser("~/.chrome-debug-profile")
        cmd = [
            chrome_path,
            "--remote-debugging-port=9222",
            f"--user-data-dir={debug_profile}",
            "--no-first-run",
            "--no-default-browser-check"
        ]
        creation_flags = 0
    
    print(f"[INFO] Debug profile: {debug_profile}")
    print("[INFO] Starting Chrome in background...")
    
    # 启动 Chrome（非阻塞）
    try:
        if system == "windows":
            subprocess.Popen(
                cmd,
                creationflags=creation_flags,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        else:
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        return True
    except Exception as e:
        print(f"[ERROR] Failed to start Chrome: {e}")
        return False


def start_chrome_reuse():
    """复用主 profile 启动 Chrome（会关闭现有窗口）"""
    system = get_system()
    
    # 查找 Chrome
    if system == "windows":
        chrome_path = find_chrome_windows()
    else:
        chrome_path = find_chrome_unix()
    
    if not chrome_path:
        print("[ERROR] Chrome browser not found.")
        print("Please make sure Google Chrome is installed.")
        return False
    
    print(f"[INFO] Chrome path: {chrome_path}")
    
    # 关闭所有 Chrome 进程
    print("[WARNING] Closing all Chrome processes...")
    if system == "windows":
        try:
            subprocess.run(
                ["taskkill", "/F", "/IM", "chrome.exe"],
                capture_output=True,
                timeout=10
            )
        except:
            pass
    else:
        try:
            subprocess.run(
                ["pkill", "-9", "-f", "Google Chrome"],
                capture_output=True,
                timeout=10
            )
        except:
            pass
    
    time.sleep(2)
    
    # 关闭占用 9222 端口的进程
    print("[INFO] Checking port 9222...")
    kill_process_on_port(9222)
    time.sleep(0.5)
    
    # 准备启动参数
    # macOS/Linux 不能直接在默认 profile 开启远程调试，
    # 必须复制默认 profile 到一个临时目录再用 --user-data-dir 启动。
    if system == "windows":
        cmd = [
            chrome_path,
            "--remote-debugging-port=9222"
        ]
    else:
        default_profile = None
        if system == "macos":
            default_profile = os.path.expanduser(
                "~/Library/Application Support/Google/Chrome"
            )
        else:  # linux
            default_profile = os.path.expanduser("~/.config/google-chrome")

        reuse_profile = os.path.expanduser("~/.chrome-reuse-profile")

        if default_profile and os.path.isdir(default_profile):
            print(f"[INFO] Copying default profile to {reuse_profile}...")
            try:
                import shutil

                def _ignore_runtime_files(src, names):
                    return {
                        name for name in names
                        if name in {
                            "SingletonLock",
                            "SingletonCookie",
                            "SingletonSocket",
                            "RunningChromeVersion",
                        }
                    }

                if os.path.exists(reuse_profile):
                    shutil.rmtree(reuse_profile)
                shutil.copytree(
                    default_profile,
                    reuse_profile,
                    ignore=_ignore_runtime_files,
                )
                print("[INFO] Profile copied successfully")
            except Exception as e:
                print(f"[WARNING] Failed to copy default profile: {e}")
                print("[WARNING] Falling back to independent profile")
                reuse_profile = os.path.expanduser("~/.chrome-debug-profile")
        else:
            print("[WARNING] Default profile not found, using independent profile")
            reuse_profile = os.path.expanduser("~/.chrome-debug-profile")

        cmd = [
            chrome_path,
            "--remote-debugging-port=9222",
            f"--user-data-dir={reuse_profile}",
            "--no-first-run",
            "--no-default-browser-check"
        ]
    
    print("[INFO] Starting Chrome in background...")
    
    # 启动 Chrome（非阻塞）
    try:
        if system == "windows":
            subprocess.Popen(
                cmd,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        else:
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        return True
    except Exception as e:
        print(f"[ERROR] Failed to start Chrome: {e}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Chrome浏览器启动器 - 启动带调试端口的Chrome",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python launcher.py                    # 默认复用主profile
    python launcher.py --mode reuse       # 复用主profile（会关闭现有窗口）
    python launcher.py --mode independent # 独立profile（无痕模式）
        """
    )
    parser.add_argument(
        "--mode",
        choices=["independent", "reuse"],
        default="reuse",
        help="启动模式：independent(独立profile) 或 reuse(复用主profile，默认)"
    )
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("Chrome Browser Launcher")
    print("=" * 50)
    print()
    
    system = get_system()
    
    if system == "unknown":
        print("[ERROR] Unsupported operating system")
        sys.exit(1)
    
    print(f"[INFO] Detected {system}")
    print(f"[INFO] Mode: {'Independent profile' if args.mode == 'independent' else 'Reuse main profile'}")
    print()
    
    # 启动 Chrome
    if args.mode == "independent":
        success = start_chrome_independent()
    else:
        success = start_chrome_reuse()
    
    if success:
        print()
        print("=" * 50)
        print("[SUCCESS] Chrome launch command executed!")
        print("[SUCCESS] Debug endpoint: http://127.0.0.1:9222")
        print("=" * 50)
        print()
        print("Note: Chrome is starting in background.")
        print("      Wait 2-3 seconds before connecting.")
        sys.exit(0)
    else:
        print()
        print("=" * 50)
        print("[ERROR] Failed to start Chrome")
        print("=" * 50)
        sys.exit(1)


if __name__ == "__main__":
    main()
