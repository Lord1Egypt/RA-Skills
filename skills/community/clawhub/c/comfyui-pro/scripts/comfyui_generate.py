#!/usr/bin/env python3
"""
ComfyUI 自动化运行脚本
机械之神专用版本 - 2026-03-15

用法:
    python comfyui_generate.py --prompt "描述文字" --workflow text-to-image
    python comfyui_generate.py --prompt "描述" --width 1024 --height 1024 --seed 12345
"""

import json
import random
import time
import urllib.request
import urllib.parse
import argparse
import os
from pathlib import Path

# 配置
COMFYUI_HOST = "127.0.0.1"
COMFYUI_PORT = 8000  # ComfyUI 桌面版端口
COMFYUI_URL = f"http://{COMFYUI_HOST}:{COMFYUI_PORT}"

# 工作流路径
WORKFLOWS_DIR = Path(__file__).parent / "assets"
WORKFLOWS = {
    "text-to-image": "text-to-image.json",
    "image-to-image": "image-to-image.json",
    "controlnet": "controlnet.json"
}

# 输出目录
OUTPUT_DIR = Path("F:/comcyui 模型/output")


def load_workflow(workflow_name: str) -> dict:
    """加载工作流 JSON"""
    if workflow_name not in WORKFLOWS:
        raise ValueError(f"未知的工作流：{workflow_name}，可用：{list(WORKFLOWS.keys())}")
    
    workflow_path = WORKFLOWS_DIR / WORKFLOWS[workflow_name]
    with open(workflow_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def update_prompt(workflow: dict, prompt: str):
    """更新提示词"""
    for node_id, node in workflow.items():
        if node.get("_meta", {}).get("title") == "Positive Prompt":
            if "widgets_values" in node:
                node["widgets_values"][0] = prompt
            elif "inputs" in node and "value" in node["inputs"]:
                node["inputs"]["value"] = prompt
        if node.get("class_type") == "PrimitiveStringMultiline":
            if "widgets_values" in node:
                node["widgets_values"][0] = prompt


def update_seed(workflow: dict, seed: int = None):
    """更新随机种子"""
    if seed is None or seed == -1:
        seed = random.randint(1000000000, 9999999999)
    
    for node_id, node in workflow.items():
        if node.get("class_type") == "KSampler":
            if "widgets_values" in node:
                node["widgets_values"][0] = seed
            elif "inputs" in node and "seed" in node["inputs"]:
                node["inputs"]["seed"] = seed
    return seed


def update_size(workflow: dict, width: int, height: int):
    """更新图像尺寸"""
    for node_id, node in workflow.items():
        if node.get("class_type") == "EmptySD3LatentImage":
            if "widgets_values" in node:
                node["widgets_values"][0] = width
                node["widgets_values"][1] = height


def queue_prompt(workflow: dict) -> str:
    """发送工作流到 ComfyUI 队列"""
    data = json.dumps({"prompt": workflow}).encode('utf-8')
    req = urllib.request.Request(f"{COMFYUI_URL}/prompt", data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get("prompt_id")
    except Exception as e:
        raise RuntimeError(f"无法连接到 ComfyUI 服务器：{e}\n请确保 ComfyUI 正在运行 (127.0.0.1:{COMFYUI_PORT})")


def wait_for_completion(prompt_id: str, interval: float = 2.0, timeout: int = 300) -> dict:
    """等待生成完成"""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            req = urllib.request.Request(f"{COMFYUI_URL}/history/{prompt_id}")
            with urllib.request.urlopen(req, timeout=10) as response:
                history = json.loads(response.read().decode('utf-8'))
                
                if prompt_id in history:
                    result = history[prompt_id]
                    if result.get("outputs"):
                        return result
        except Exception as e:
            pass
        
        time.sleep(interval)
    
    raise TimeoutError(f"生成超时 ({timeout}秒)")


def get_images(result: dict) -> list:
    """从结果中提取图片信息"""
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


def ensure_server_running() -> bool:
    """确保服务器运行，如未运行则自动启动"""
    # 检查是否运行
    if check_server():
        print("   ✓ 服务器已在运行")
        return True
    
    # 自动启动
    print("   服务器未运行，正在启动...")
    import subprocess
    result = subprocess.run(
        ["python", str(Path(__file__).parent / "comfyui_service.py"), "start"],
        capture_output=True,
        text=True,
        timeout=90
    )
    
    # 等待服务器就绪
    for i in range(30):
        time.sleep(2)
        if check_server():
            print("   ✓ 服务器已启动")
            return True
    
    print("   ✗ 服务器启动失败")
    return False


def check_server(timeout: float = 3.0) -> bool:
    """检查服务器是否运行"""
    try:
        req = urllib.request.Request(f"{COMFYUI_URL}/system_stats")
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status == 200
    except Exception:
        return False


def generate(prompt: str, workflow: str = "text-to-image", 
             width: int = 1024, height: int = 1024, 
             seed: int = -1, steps: int = 4):
    """主生成函数"""
    print(f"[ComfyUI] 开始生成...")
    print(f"   提示词：{prompt}")
    print(f"   工作流：{workflow}")
    print(f"   尺寸：{width}x{height}")
    
    # 确保服务器运行
    if not ensure_server_running():
        print("   错误：无法启动 ComfyUI 服务器")
        return []
    
    # 加载工作流
    wf = load_workflow(workflow)
    
    # 更新参数
    update_prompt(wf, prompt)
    actual_seed = update_seed(wf, seed)
    print(f"   种子：{actual_seed}")
    update_size(wf, width, height)
    
    # 发送队列
    print(f"   连接到 ComfyUI 服务器...")
    prompt_id = queue_prompt(wf)
    print(f"   任务 ID: {prompt_id}")
    print(f"   正在生成...")
    
    # 等待完成
    result = wait_for_completion(prompt_id)
    
    # 获取图片
    images = get_images(result)
    
    if images:
        print(f"\n✅ 生成完成！")
        for img in images:
            path = OUTPUT_DIR / img["subfolder"] / img["filename"] if img["subfolder"] else OUTPUT_DIR / img["filename"]
            print(f"   📁 {path}")
        return images
    else:
        print(f"❌ 未找到输出图片")
        return []


def main():
    parser = argparse.ArgumentParser(description="ComfyUI 自动化生成")
    parser.add_argument("--prompt", type=str, required=True, help="图像描述提示词")
    parser.add_argument("--workflow", type=str, default="text-to-image", 
                       choices=list(WORKFLOWS.keys()), help="工作流类型")
    parser.add_argument("--width", type=int, default=1024, help="图像宽度")
    parser.add_argument("--height", type=int, default=1024, help="图像高度")
    parser.add_argument("--seed", type=int, default=-1, help="随机种子 (-1 为随机)")
    parser.add_argument("--steps", type=int, default=4, help="采样步数")
    
    args = parser.parse_args()
    
    try:
        images = generate(
            prompt=args.prompt,
            workflow=args.workflow,
            width=args.width,
            height=args.height,
            seed=args.seed,
            steps=args.steps
        )
        
        if images:
            print(f"\n🎉 成功生成 {len(images)} 张图片！")
            return 0
        else:
            return 1
            
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        return 1


if __name__ == "__main__":
    exit(main())
