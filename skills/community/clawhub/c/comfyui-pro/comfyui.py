#!/usr/bin/env python3
"""
ComfyUI 图像生成 - 技能入口
机械之神专用 v1.0

用法:
    python comfyui.py "生成一张图片：美丽的山水风景"
    python comfyui.py --prompt "赛博朋克城市" --width 1920 --height 1080
    python comfyui.py --service start
    python comfyui.py --service status
    python comfyui.py --service stop
"""

import sys
import os
import time
import json
import random
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# 配置
COMFYUI_HOST = "127.0.0.1"
COMFYUI_PORT = 8000
COMFYUI_URL = f"http://{COMFYUI_HOST}:{COMFYUI_PORT}"
OUTPUT_DIR = Path("F:/comcyui 模型/output")
SCRIPTS_DIR = Path(__file__).parent / "scripts"
ASSETS_DIR = Path(__file__).parent / "assets"
STATE_FILE = SCRIPTS_DIR / "comfyui_server.state"

# 自动关闭配置
AUTO_STOP_MINUTES = 30


def log(message: str):
    """日志输出"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    # 替换 emoji 为 ASCII
    message = message.replace("✓", "[OK]").replace("✗", "[ERR]")
    print(f"[{timestamp}] {message}")


def check_server(timeout: float = 3.0) -> bool:
    """检查服务器状态"""
    try:
        req = urllib.request.Request(f"{COMFYUI_URL}/system_stats")
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status == 200
    except Exception:
        return False


def start_server() -> bool:
    """启动服务器"""
    if check_server():
        log("✓ 服务器已在运行")
        return True
    
    log("正在启动 ComfyUI 服务器...")
    import subprocess
    
    try:
        # 启动桌面版
        process = subprocess.Popen(
            ["G:\\comfyui\\ComfyUI.exe"],
            cwd="G:\\comfyui",
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # 等待启动
        for i in range(60):
            time.sleep(1)
            if check_server(timeout=2.0):
                # 保存状态
                with open(STATE_FILE, 'w', encoding='utf-8') as f:
                    json.dump({
                        "running": True,
                        "pid": process.pid,
                        "started_at": time.time(),
                        "last_used": time.time()
                    }, f, ensure_ascii=False, indent=2)
                
                log(f"✓ 服务器已启动 (等待 {i+1} 秒)")
                return True
        
        log("✗ 服务器启动超时")
        return False
        
    except Exception as e:
        log(f"✗ 启动失败：{e}")
        return False


def stop_server():
    """关闭服务器"""
    import subprocess
    
    # API 关闭
    try:
        req = urllib.request.Request(f"{COMFYUI_URL}/shutdown", method='POST')
        with urllib.request.urlopen(req, timeout=5) as response:
            pass
    except Exception:
        pass
    
    # 强制结束进程
    try:
        subprocess.run(["taskkill", "/F", "/IM", "ComfyUI.exe"], 
                      capture_output=True, timeout=10)
    except Exception:
        pass
    
    # 清理状态
    if STATE_FILE.exists():
        STATE_FILE.unlink()
    
    log("✓ 服务器已关闭")


def get_server_status() -> dict:
    """获取服务器状态"""
    is_running = check_server()
    status = {"running": is_running, "url": COMFYUI_URL}
    
    if is_running:
        try:
            req = urllib.request.Request(f"{COMFYUI_URL}/system_stats")
            with urllib.request.urlopen(req, timeout=5) as response:
                stats = json.loads(response.read().decode('utf-8'))
                status["version"] = stats.get("system", {}).get("comfyui_version")
                status["gpu"] = stats.get("devices", [{}])[0].get("name")
                status["vram_free_gb"] = stats.get("devices", [{}])[0].get("vram_free", 0) / (1024**3)
        except Exception:
            pass
    
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                state = json.load(f)
                if state.get("started_at"):
                    uptime = (time.time() - state["started_at"]) / 60
                    status["uptime_minutes"] = uptime
        except Exception:
            pass
    
    return status


def load_workflow(workflow_name: str) -> dict:
    """加载工作流"""
    workflow_map = {
        "text-to-image": "text-to-image.json",
        "image-to-image": "image-to-image.json",
        "controlnet": "controlnet.json"
    }
    
    if workflow_name not in workflow_map:
        raise ValueError(f"未知工作流：{workflow_name}")
    
    workflow_path = ASSETS_DIR / workflow_map[workflow_name]
    with open(workflow_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def update_workflow(workflow: dict, prompt: str, width: int, height: int, seed: int):
    """更新工作流参数"""
    if seed == -1:
        seed = random.randint(1000000000, 9999999999)
    
    for node_id, node in workflow.items():
        # 跳过非节点数据
        if not isinstance(node, dict):
            continue
        
        # 更新提示词
        if node.get("_meta", {}).get("title") == "Positive Prompt":
            if "widgets_values" in node:
                node["widgets_values"][0] = prompt
        
        # 更新种子
        if node.get("class_type") == "KSampler":
            if "widgets_values" in node:
                node["widgets_values"][0] = seed
        
        # 更新尺寸
        if node.get("class_type") == "EmptySD3LatentImage":
            if "widgets_values" in node:
                node["widgets_values"][0] = width
                node["widgets_values"][1] = height
    
    return workflow, seed


def queue_prompt(workflow: dict) -> str:
    """发送队列"""
    data = json.dumps({"prompt": workflow}).encode('utf-8')
    req = urllib.request.Request(f"{COMFYUI_URL}/prompt", data=data, 
                                  headers={'Content-Type': 'application/json'})
    
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result.get("prompt_id")


def wait_for_completion(prompt_id: str, timeout: int = 300) -> dict:
    """等待完成"""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            req = urllib.request.Request(f"{COMFYUI_URL}/history/{prompt_id}")
            with urllib.request.urlopen(req, timeout=10) as response:
                history = json.loads(response.read().decode('utf-8'))
                
                if prompt_id in history:
                    result = history[prompt_id]
                    if result.get("outputs"):
                        # 更新最后使用时间
                        if STATE_FILE.exists():
                            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                                state = json.load(f)
                            state["last_used"] = time.time()
                            with open(STATE_FILE, 'w', encoding='utf-8') as f:
                                json.dump(state, f, ensure_ascii=False, indent=2)
                        return result
        except Exception:
            pass
        
        time.sleep(2)
    
    raise TimeoutError(f"生成超时 ({timeout}秒)")


def get_images(result: dict) -> list:
    """提取图片"""
    images = []
    outputs = result.get("outputs", {})
    
    for node_id, output in outputs.items():
        if "images" in output:
            for img in output["images"]:
                if img.get("type") == "output":
                    images.append({
                        "filename": img.get("filename"),
                        "subfolder": img.get("subfolder", ""),
                        "type": img.get("type", "output")
                    })
    
    return images


def copy_to_workspace(image_path: Path) -> Path:
    """复制图片到工作空间目录（OpenClaw 允许访问的目录）"""
    import shutil
    
    # 工作空间目录（OpenClaw 允许访问）
    workspace_dir = Path.home() / ".openclaw" / "workspace" / "comfyui_images"
    workspace_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成新文件名（使用时间戳避免冲突）
    import time
    timestamp = int(time.time())
    dest_path = workspace_dir / f"comfyui_{timestamp}.png"
    
    # 复制文件
    shutil.copy2(image_path, dest_path)
    log(f"已复制到工作空间：{dest_path}")
    return dest_path


def generate_image(prompt: str, workflow: str = "text-to-image",
                   width: int = 1024, height: int = 1024, seed: int = -1):
    """生成图片主函数"""
    log(f"开始生成：{prompt[:50]}...")
    
    # 确保服务器运行
    if not check_server():
        if not start_server():
            log("错误：无法启动服务器")
            return []
    
    # 加载工作流
    wf = load_workflow(workflow)
    
    # 更新参数
    wf, actual_seed = update_workflow(wf, prompt, width, height, seed)
    log(f"参数：{width}x{height}, 种子={actual_seed}")
    
    # 发送队列
    log("正在生成...")
    prompt_id = queue_prompt(wf)
    
    # 等待完成
    result = wait_for_completion(prompt_id)
    
    # 获取图片
    images = get_images(result)
    
    if images:
        saved_paths = []
        for img in images:
            path = OUTPUT_DIR / img["subfolder"] / img["filename"] if img["subfolder"] else OUTPUT_DIR / img["filename"]
            log(f"✓ 已保存：{path}")
            
            # 复制到工作空间目录
            workspace_path = copy_to_workspace(path)
            saved_paths.append(str(workspace_path))
        return saved_paths
    else:
        log("✗ 未找到输出图片")
        return []


def check_auto_stop():
    """检查是否应该自动关闭"""
    if not STATE_FILE.exists():
        return
    
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        if not state.get("running") or not state.get("last_used"):
            return
        
        idle_minutes = (time.time() - state["last_used"]) / 60
        
        if idle_minutes >= AUTO_STOP_MINUTES:
            log(f"检测到空闲 {idle_minutes:.1f} 分钟，自动关闭服务器...")
            stop_server()
    except Exception:
        pass


def show_status():
    """显示状态"""
    status = get_server_status()
    
    print("\n[ComfyUI] 图像生成服务")
    print("=" * 40)
    running_text = "运行中" if status['running'] else "已停止"
    print(f"运行状态：{running_text}")
    print(f"服务地址：{status['url']}")
    
    if status['running']:
        print(f"版本：{status.get('version', 'Unknown')}")
        print(f"GPU: {status.get('gpu', 'Unknown')}")
        vram = status.get('vram_free_gb', 0)
        print(f"可用显存：{vram:.1f} GB")
        if status.get('uptime_minutes'):
            print(f"运行时间：{status['uptime_minutes']:.1f} 分钟")
    
    print("=" * 40)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="ComfyUI 图像生成技能")
    parser.add_argument("prompt", nargs="?", help="图像描述提示词")
    # parser.add_argument("--prompt", "-p", type=str, help="图像描述提示词")  # 移除重复
    parser.add_argument("--workflow", "-w", type=str, default="text-to-image",
                       choices=["text-to-image", "image-to-image", "controlnet"])
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1024)
    parser.add_argument("--seed", type=int, default=-1)
    parser.add_argument("--service", type=str, choices=["start", "stop", "status", "restart"])
    parser.add_argument("--auto-stop", action="store_true", help="检查并关闭空闲服务器")
    
    args = parser.parse_args()
    
    # 服务管理
    if args.service:
        if args.service == "start":
            start_server()
        elif args.service == "stop":
            stop_server()
        elif args.service == "status":
            show_status()
        elif args.service == "restart":
            stop_server()
            time.sleep(2)
            start_server()
        return
    
    # 自动关闭检查
    if args.auto_stop:
        check_auto_stop()
        return
    
    # 生成图片
    prompt = args.prompt or (args.prompt if hasattr(args, 'prompt') else None)
    if not prompt:
        parser.print_help()
        return
    
    images = generate_image(
        prompt=prompt,
        workflow=args.workflow,
        width=args.width,
        height=args.height,
        seed=args.seed
    )
    
    if images:
        log(f"\n[OK] 成功生成 {len(images)} 张图片！")
    else:
        log("\n[ERR] 生成失败")


if __name__ == "__main__":
    main()
