#!/usr/bin/env python3
"""
ComfyUI 图像生成 - WebSocket 版本
整合 openclaw-comfyui-imagegenerate 优点
"""

import websocket
import uuid
import json
import urllib.request
import urllib.parse
import os
import sys
import time
import random
from pathlib import Path

# 配置
COMFYUI_HOST = "127.0.0.1"
COMFYUI_PORT = 8000  # 桌面版端口
SERVER_ADDRESS = f"{COMFYUI_HOST}:{COMFYUI_PORT}"
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"
OUTPUT_DIR = Path("F:/comcyui 模型/output")
CLIENT_ID = str(uuid.uuid4())


def log(message: str, error: bool = False):
    """日志输出到 stderr"""
    prefix = "[ERR]" if error else "[INFO]"
    sys.stderr.write(f"{prefix} {message}\n")
    sys.stderr.flush()


def queue_prompt(prompt: dict) -> str:
    """提交任务"""
    payload = {
        "prompt": prompt,
        "client_id": CLIENT_ID
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result.get("prompt_id")


def get_image(filename: str, subfolder: str, folder_type: str) -> bytes:
    """下载图片"""
    params = {
        "filename": filename,
        "subfolder": subfolder,
        "type": folder_type
    }
    url = f"http://{SERVER_ADDRESS}/view?{urllib.parse.urlencode(params)}"
    
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read()


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


def update_workflow(workflow: dict, prompt: str, width: int, height: int, seed: int = -1):
    """更新工作流参数"""
    if seed == -1:
        seed = random.randint(0, 10**15)
    
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


def run_workflow(workflow: dict, timeout: int = 300) -> dict:
    """WebSocket 运行工作流"""
    # 创建输出目录
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 连接 WebSocket
    ws_url = f"ws://{SERVER_ADDRESS}/ws?clientId={CLIENT_ID}"
    log(f"连接 WebSocket: {ws_url}")
    
    ws = websocket.WebSocket()
    try:
        ws.connect(ws_url, timeout=10)
    except Exception as e:
        log(f"无法连接 ComfyUI: {e}", error=True)
        return {"success": False, "error": str(e)}
    
    # 提交任务
    prompt_id = queue_prompt(workflow)
    log(f"任务 ID: {prompt_id}")
    
    # 等待完成
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            msg = ws.recv()
            if isinstance(msg, str):
                message = json.loads(msg)
                msg_type = message.get('type')
                
                if msg_type == 'progress':
                    data = message.get('data', {})
                    node = data.get('node')
                    value = data.get('value')
                    max_val = data.get('max')
                    if value and max_val:
                        log(f"进度：{value}/{max_val}")
                
                elif msg_type == 'executing':
                    data = message.get('data', {})
                    node = data.get('node')
                    
                    # None 表示执行完成
                    if node is None:
                        log("生成完成！")
                        break
        
        except Exception as e:
            log(f"等待出错：{e}", error=True)
            break
    
    ws.close()
    
    # 获取历史
    history_url = f"http://{SERVER_ADDRESS}/history/{prompt_id}"
    with urllib.request.urlopen(history_url, timeout=30) as response:
        history = json.loads(response.read().decode('utf-8'))
    
    if prompt_id not in history:
        log("未找到历史记录", error=True)
        return {"success": False, "error": "No history"}
    
    # 提取图片
    result = {"success": True, "prompt_id": prompt_id, "images": []}
    history_item = history[prompt_id]
    
    for node_id, node_output in history_item.get('outputs', {}).items():
        if 'images' in node_output:
            for img in node_output['images']:
                if img.get('type') == 'output':
                    filename = img.get('filename')
                    subfolder = img.get('subfolder', '')
                    
                    # 下载图片
                    try:
                        img_data = get_image(filename, subfolder, img['type'])
                        
                        # 保存
                        save_dir = OUTPUT_DIR / subfolder if subfolder else OUTPUT_DIR
                        save_dir.mkdir(parents=True, exist_ok=True)
                        save_path = save_dir / filename
                        
                        with open(save_path, 'wb') as f:
                            f.write(img_data)
                        
                        result['images'].append(str(save_path))
                        log(f"已保存：{save_path}")
                    
                    except Exception as e:
                        log(f"下载失败：{e}", error=True)
    
    return result


def generate(prompt: str, workflow: str = "text-to-image",
             width: int = 1024, height: int = 1024, seed: int = -1):
    """主生成函数"""
    log(f"开始生成：{prompt[:50]}...")
    log(f"工作流：{workflow}, 尺寸：{width}x{height}")
    
    # 加载工作流
    wf = load_workflow(workflow)
    
    # 更新参数
    wf, actual_seed = update_workflow(wf, prompt, width, height, seed)
    log(f"种子：{actual_seed}")
    
    # 运行
    result = run_workflow(wf)
    
    if result['success'] and result.get('images'):
        log(f"\n成功生成 {len(result['images'])} 张图片！")
        # stdout 仅输出路径（OpenClaw 可捕获）
        for img_path in result['images']:
            sys.stdout.write(f"{img_path}\n")
        sys.stdout.flush()
        return result['images']
    else:
        log(f"生成失败：{result.get('error', 'Unknown')}", error=True)
        return []


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="ComfyUI WebSocket 生成")
    parser.add_argument("--prompt", "-p", type=str, required=True, help="提示词")
    parser.add_argument("--workflow", "-w", type=str, default="text-to-image")
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1024)
    parser.add_argument("--seed", type=int, default=-1)
    parser.add_argument("--timeout", type=int, default=300)
    
    args = parser.parse_args()
    
    prompt = args.prompt or args.prompt if hasattr(args, 'prompt') else None
    if not prompt:
        # 从 stdin 读取
        prompt = sys.stdin.read().strip()
    
    if not prompt:
        parser.print_help()
        sys.exit(1)
    
    images = generate(
        prompt=prompt,
        workflow=args.workflow,
        width=args.width,
        height=args.height,
        seed=args.seed
    )
    
    sys.exit(0 if images else 1)


if __name__ == "__main__":
    main()
