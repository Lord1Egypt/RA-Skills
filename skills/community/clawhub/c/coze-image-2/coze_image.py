#!/usr/bin/env python3
"""Coze Image Generation Tool - 通过 Seedream 4.5 生成图片"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import os
import requests
import urllib.parse

# ================== 需要配置的参数 ==================
# 请替换为你的 Coze API Token
API_TOKEN = "你的_Coze_API_Token"

# 请替换为你的图片生成工作流 ID
WORKFLOW_ID = "你的工作流_ID"

# 固定背景图（工作流内置的参考图）
BACKGROUND_IMAGE_URL = "https://p9-bot-workflow-sign.byteimg.com/tos-cn-i-mdko3gqilj/96fb6aada1a947419ffee9fe8eaee153.png~tplv-mdko3gqilj-image.image"

# API 地址（通常不需要修改）
API_URL = "https://api.coze.cn/v1/workflow/run"
# ==================================================

CONFIG = {
    "api_token": API_TOKEN,
    "workflow_id": WORKFLOW_ID,
    "api_url": API_URL
}


def generate_image(prompt: str, save_path: str = None) -> dict:
    """Generate image using Coze Seedream workflow"""
    headers = {
        "Authorization": f"Bearer {CONFIG['api_token']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "workflow_id": CONFIG["workflow_id"],
        "parameters": {"input": prompt}
    }
    
    print("Generating image...")
    print(f"Prompt: {prompt[:50]}...")
    
    try:
        response = requests.post(
            CONFIG["api_url"],
            headers=headers,
            json=payload,
            timeout=180
        )
        
        result = response.json()
        
        if result.get("code") != 0:
            return {"success": False, "error": result.get("msg", "Unknown error")}
        
        # Extract image URL from response
        data = result.get("data", "")
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                pass
        
        image_url = data.get("output") if isinstance(data, dict) else None
        
        if not image_url:
            return {"success": False, "error": "No image URL in response"}
        
        print(f"Image URL: {image_url}")
        
        # Download if save_path provided
        if save_path:
            print(f"Downloading to: {save_path}")
            # Handle redirect URLs
            try:
                img_response = requests.get(image_url, timeout=60, allow_redirects=True)
                if img_response.status_code == 200:
                    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
                    with open(save_path, "wb") as f:
                        f.write(img_response.content)
                    print(f"Saved to: {save_path}")
                    return {"success": True, "image_url": image_url, "local_path": save_path}
            except Exception as e:
                print(f"Download warning: {e}")
        
        return {"success": True, "image_url": image_url}
        
    except requests.Timeout:
        return {"success": False, "error": "Timeout"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    if len(sys.argv) < 2:
        print("Coze Image Generation Tool")
        print("Usage:")
        print("  python coze_image.py generate <prompt>")
        print("  python coze_image.py generate <prompt> -o <save_path>")
        print("  python coze_image.py xhs <skill_name> <feature1> [feature2] [feature3]")
        print("")
        print("Examples:")
        print("  python coze_image.py generate 'a cute white kitten'")
        print("  python coze_image.py xhs self-improving-agent AI自学习 能力进化 记忆系统")
        sys.exit(1)
    
    command = sys.argv[1]
    
    # 小红书配图生成命令
    if command == "xhs":
        if len(sys.argv) < 4:
            print("Error: Please provide skill name and at least one feature")
            print("Usage: python coze_image.py xhs <skill_name> <feature1> [feature2] [feature3]")
            sys.exit(1)
        
        skill_name = sys.argv[2]
        features = sys.argv[3:]
        feature_text = "、".join(features[:3])  # 最多3个功能
        
        prompt = f"添加文字，顶部居中用紫色字体显示标题：{skill_name}，中间添加功能点：{feature_text}"
        
        save_path = None
        if "-o" in sys.argv:
            idx = sys.argv.index("-o")
            if idx + 1 < len(sys.argv):
                save_path = sys.argv[idx + 1]
        
        result = generate_image(prompt, save_path)
        print("\n" + "="*50)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    if command == "generate":
        if len(sys.argv) < 3:
            print("Error: Please provide prompt")
            sys.exit(1)
        
        prompt = sys.argv[2]
        save_path = None
        
        if "-o" in sys.argv:
            idx = sys.argv.index("-o")
            if idx + 1 < len(sys.argv):
                save_path = sys.argv[idx + 1]
        
        result = generate_image(prompt, save_path)
        print("\n" + "="*50)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()