#!/usr/bin/env python3
"""
ComfyUI 服务管理器
机械之神专用 - 自动启停管理

功能：
- start: 启动 ComfyUI 服务器
- stop: 关闭 ComfyUI 服务器
- status: 检查服务器状态
- restart: 重启服务器
"""

import subprocess
import time
import urllib.request
import json
import os
import sys
from pathlib import Path

# 配置
COMFYUI_HOST = "127.0.0.1"
COMFYUI_PORT = 8000  # ComfyUI 桌面版默认端口
COMFYUI_URL = f"http://{COMFYUI_HOST}:{COMFYUI_PORT}"

# 路径配置
COMFYUI_DESKTOP_APP = "G:\\comfyui\\ComfyUI.exe"
COMFYUI_BASE = "F:\\comcyui 模型"
COMFYUI_PYTHON = "F:\\comcyui 模型\\.venv\\Scripts\\python.exe"
COMFYUI_MAIN = "G:\\comfyui\\resources\\ComfyUI\\main.py"

# 状态文件
STATE_FILE = Path(__file__).parent / "comfyui_server.state"


def check_server(timeout: float = 3.0) -> bool:
    """检查服务器是否运行"""
    try:
        req = urllib.request.Request(f"{COMFYUI_URL}/system_stats")
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status == 200
    except Exception:
        return False


def get_state() -> dict:
    """读取服务器状态"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {"running": False, "pid": None, "started_at": None}


def save_state(state: dict):
    """保存服务器状态"""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def start_server() -> dict:
    """启动 ComfyUI 服务器"""
    # 先检查是否已在运行
    if check_server():
        return {"success": True, "message": "服务器已在运行", "already_running": True}
    
    # 使用 ComfyUI 桌面版启动
    try:
        # 启动桌面版（后台运行）
        process = subprocess.Popen(
            [COMFYUI_DESKTOP_APP],
            cwd="G:\\comfyui",
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # 等待服务器启动（最多 60 秒）
        print("正在启动 ComfyUI 服务器...")
        for i in range(60):
            time.sleep(1)
            if check_server(timeout=2.0):
                state = {
                    "running": True,
                    "pid": process.pid,
                    "started_at": time.time(),
                    "method": "desktop"
                }
                save_state(state)
                return {
                    "success": True,
                    "message": f"服务器已启动（进程 ID: {process.pid}）",
                    "pid": process.pid,
                    "wait_time": i + 1
                }
        
        # 超时
        return {
            "success": False,
            "message": "服务器启动超时（60 秒）",
            "pid": process.pid
        }
        
    except Exception as e:
        return {"success": False, "message": f"启动失败：{e}"}


def stop_server() -> dict:
    """关闭 ComfyUI 服务器"""
    state = get_state()
    
    # 先尝试通过 API 关闭
    try:
        req = urllib.request.Request(f"{COMFYUI_URL}/shutdown", method='POST')
        with urllib.request.urlopen(req, timeout=5) as response:
            pass
    except Exception:
        pass
    
    # 强制结束进程
    if state.get("pid"):
        try:
            subprocess.run(["taskkill", "/F", "/PID", str(state["pid"])], 
                          capture_output=True, timeout=10)
        except Exception:
            pass
    
    # 清理所有 ComfyUI 相关进程
    try:
        subprocess.run(["taskkill", "/F", "/IM", "ComfyUI.exe"], 
                      capture_output=True, timeout=10)
    except Exception:
        pass
    
    try:
        subprocess.run(["taskkill", "/F", "/IM", "python.exe"], 
                      capture_output=True, timeout=10)
    except Exception:
        pass
    
    # 更新状态
    save_state({"running": False, "pid": None, "started_at": None})
    
    return {"success": True, "message": "服务器已关闭"}


def get_status() -> dict:
    """获取服务器状态"""
    is_running = check_server()
    state = get_state()
    
    status = {
        "running": is_running,
        "url": COMFYUI_URL,
        "port": COMFYUI_PORT
    }
    
    if is_running:
        try:
            req = urllib.request.Request(f"{COMFYUI_URL}/system_stats")
            with urllib.request.urlopen(req, timeout=5) as response:
                stats = json.loads(response.read().decode('utf-8'))
                status["version"] = stats.get("system", {}).get("comfyui_version", "Unknown")
                status["gpu"] = stats.get("devices", [{}])[0].get("name", "Unknown")
                status["vram_free"] = stats.get("devices", [{}])[0].get("vram_free", 0) / (1024**3)
        except Exception:
            pass
    
    if state.get("started_at"):
        uptime = time.time() - state["started_at"]
        status["uptime"] = f"{uptime/60:.1f} 分钟"
    
    return status


def auto_stop(idle_minutes: int = 30) -> dict:
    """自动关闭空闲服务器"""
    state = get_state()
    
    if not state.get("running") or not state.get("started_at"):
        return {"success": False, "message": "服务器未运行"}
    
    idle_time = (time.time() - state["started_at"]) / 60  # 分钟
    
    if idle_time >= idle_minutes:
        return stop_server()
    else:
        remaining = idle_minutes - idle_time
        return {
            "success": False,
            "message": f"服务器运行中，剩余 {remaining:.1f} 分钟后自动关闭",
            "idle_minutes": idle_time
        }


def main():
    if len(sys.argv) < 2:
        print("用法：python comfyui_service.py [start|stop|status|restart|auto-stop]")
        print("  start      - 启动服务器")
        print("  stop       - 关闭服务器")
        print("  status     - 检查状态")
        print("  restart    - 重启服务器")
        print("  auto-stop  - 自动关闭空闲服务器")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "start":
        result = start_server()
        print(f"{'✅' if result['success'] else '❌'} {result['message']}")
        sys.exit(0 if result['success'] else 1)
    
    elif command == "stop":
        result = stop_server()
        print(f"{'✅' if result['success'] else '❌'} {result['message']}")
        sys.exit(0 if result['success'] else 1)
    
    elif command == "status":
        status = get_status()
        print("🔷 ComfyUI 服务器状态")
        print(f"   运行状态：{'✅ 运行中' if status['running'] else '❌ 已停止'}")
        print(f"   地址：{status['url']}")
        if status['running']:
            print(f"   版本：{status.get('version', 'Unknown')}")
            print(f"   GPU: {status.get('gpu', 'Unknown')}")
            print(f"   可用显存：{status.get('vram_free', 0):.1f} GB")
            if status.get('uptime'):
                print(f"   运行时间：{status['uptime']}")
        sys.exit(0)
    
    elif command == "restart":
        print("正在关闭服务器...")
        stop_server()
        time.sleep(2)
        print("正在重启服务器...")
        result = start_server()
        print(f"{'✅' if result['success'] else '❌'} {result['message']}")
        sys.exit(0 if result['success'] else 1)
    
    elif command == "auto-stop":
        idle_minutes = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        result = auto_stop(idle_minutes)
        print(f"{'✅' if result['success'] else 'ℹ️'} {result['message']}")
        sys.exit(0)
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
