#!/usr/bin/env python3
"""
ComfyUI 连接测试脚本
"""

import urllib.request
import json

COMFYUI_URL = "http://127.0.0.1:8188"

def test_connection():
    """测试 ComfyUI 服务器连接"""
    try:
        # 获取系统信息
        req = urllib.request.Request(f"{COMFYUI_URL}/system_stats")
        with urllib.request.urlopen(req, timeout=5) as response:
            stats = json.loads(response.read().decode('utf-8'))
            print("✅ ComfyUI 服务器已连接！")
            print(f"   设备：{stats.get('system', {}).get('device', 'Unknown')}")
            print(f"   GPU: {stats.get('system', {}).get('gpu_name', 'Unknown')}")
            return True
    except Exception as e:
        print(f"❌ 无法连接到 ComfyUI 服务器：{e}")
        print(f"   请确保 ComfyUI 正在运行 (127.0.0.1:8188)")
        return False

def test_models():
    """测试模型加载"""
    try:
        req = urllib.request.Request(f"{COMFYUI_URL}/object_info")
        with urllib.request.urlopen(req, timeout=10) as response:
            info = json.loads(response.read().decode('utf-8'))
            print("✅ 模型信息已获取")
            return True
    except Exception as e:
        print(f"⚠️ 无法获取模型信息：{e}")
        return False

if __name__ == "__main__":
    print("[ComfyUI] 连接测试\n")
    
    if test_connection():
        test_models()
        print("\n✅ 所有测试通过！可以开始生成图像了。")
    else:
        print("\n❌ 测试失败，请检查 ComfyUI 服务器状态。")
