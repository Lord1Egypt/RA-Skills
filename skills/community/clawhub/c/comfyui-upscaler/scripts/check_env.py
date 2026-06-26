#!/usr/bin/env python3
"""
ComfyUI 环境检查脚本

检查以下内容：
1. ComfyUI 是否安装
2. 必要的放大节点是否可用
3. 放大模型是否存在
"""

import os
import sys
from pathlib import Path

# 常见 ComfyUI 安装路径
COMFYUI_PATHS = [
    Path.home() / "ComfyUI",
    Path.home() / "comfyui",
    Path.home() / "Documents" / "ComfyUI",
    Path("/Applications/ComfyUI.app"),  # macOS App
]

# 必要的节点
REQUIRED_NODES = [
    "CheckpointLoaderSimple",
    "CLIPTextEncode",
    "VAEDecode",
    "VAEEncode",
    "KSampler",
    "LatentScaleByFactor",  # 潜空间放大
    "SDUpscale",            # 分区放大
    "ImageUpscaleWithModel", # 模型放大
    "SaveImage",
]

# 推荐的基础模型
RECOMMENDED_BASE_MODELS = [
    "sd_xl_base_1.0.safetensors",
    "v1-5-pruned-emaonly.safetensors",
    "ponyDiffusionV6XL.safetensors",
]

# 推荐的放大模型
RECOMMENDED_UPSCALE_MODELS = [
    "4x-UltraSharp.pth",
    "4x_Nickelback.pth",
    "RealESRGAN_x4plus.pth",
    "R-ESRGAN_4x_De Bayer.pth",
]


def check_comfyui():
    """检查 ComfyUI 安装"""
    print("🔍 检查 ComfyUI 安装...")
    
    comfyui_path = None
    for path in COMFYUI_PATHS:
        if path.exists():
            comfyui_path = path
            break
    
    if comfyui_path:
        print(f"   ✅ 找到 ComfyUI: {comfyui_path}")
        
        # 检查主文件
        main_paths = [
            comfyui_path / "main.py",
            comfyui_path / "app.py",
            comfyui_path / "ComfyUI" / "main.py",
        ]
        
        found_main = False
        for mp in main_paths:
            if mp.exists():
                print(f"   ✅ 主文件: {mp}")
                found_main = True
                break
        
        if not found_main:
            print(f"   ⚠️ 未找到主文件")
        
        return comfyui_path
    else:
        print(f"   ❌ 未找到 ComfyUI")
        print(f"   请从 https://github.com/comfyanonymous/ComfyUI 下载安装")
        return None


def check_models(comfyui_path: Path):
    """检查放大模型"""
    print("\n🔍 检查放大模型...")
    
    if not comfyui_path:
        # 尝试常见路径
        model_dirs = [
            Path.home() / "ComfyUI" / "models",
            Path.home() / ".cache" / "huggingface" / "hub",
        ]
    else:
        model_dirs = [comfyui_path / "models"]
    
    found_models = []
    for model_dir in model_dirs:
        if model_dir.exists():
            print(f"   📁 模型目录: {model_dir}")
            
            # 检查放大模型
            upscale_dir = model_dir / "upscale_models"
            if upscale_dir.exists():
                models = list(upscale_dir.glob("*"))
                print(f"      放大模型: {len(models)} 个")
                for m in models[:5]:
                    print(f"        - {m.name}")
                found_models.extend(models)
            
            # 检查 Checkpoints
            checkpoints_dir = model_dir / "checkpoints"
            if checkpoints_dir.exists():
                checkpoints = list(checkpoints_dir.glob("*"))
                print(f"      Checkpoint: {len(checkpoints)} 个")
    
    if not found_models:
        print(f"   ⚠️ 未找到放大模型")
        print(f"   建议下载:")
        for m in RECOMMENDED_UPSCALE_MODELS:
            print(f"      - {m}")
    
    return found_models


def check_nodes(comfyui_path: Path):
    """检查必要的节点"""
    print("\n🔍 检查必要节点...")
    
    if not comfyui_path:
        print("   ⚠️ 无法检查节点（ComfyUI 未找到）")
        return False
    
    # 检查 custom_nodes 目录
    custom_nodes_dir = comfyui_path / "custom_nodes"
    if custom_nodes_dir.exists():
        nodes = list(custom_nodes_dir.iterdir())
        print(f"   📁 自定义节点: {len(nodes)} 个")
        
        # 检查特定节点
        for node in REQUIRED_NODES:
            found = False
            for n in nodes:
                if node.lower() in n.name.lower():
                    found = True
                    break
            status = "✅" if found else "❓"
            print(f"      {status} {node}")
    else:
        print(f"   📁 custom_nodes 目录不存在（正常，新安装）")
        print(f"   节点将使用内置实现")
    
    return True


def check_dependencies():
    """检查 Python 依赖"""
    print("\n🔍 检查 Python 依赖...")
    
    required = ["torch", "numpy", "PIL"]
    missing = []
    
    for mod in required:
        try:
            __import__(mod)
            print(f"   ✅ {mod}")
        except ImportError:
            print(f"   ❌ {mod} 未安装")
            missing.append(mod)
    
    if missing:
        print(f"\n   请运行: pip install {' '.join(missing)}")
        return False
    
    return True


def main():
    print("=" * 50)
    print("ComfyUI 三重放大环境检查")
    print("=" * 50)
    
    # 1. 检查 Python 依赖
    deps_ok = check_dependencies()
    
    # 2. 检查 ComfyUI
    comfyui_path = check_comfyui()
    
    # 3. 检查节点
    if comfyui_path:
        check_nodes(comfyui_path)
    
    # 4. 检查模型
    check_models(comfyui_path)
    
    # 总结
    print("\n" + "=" * 50)
    if comfyui_path and deps_ok:
        print("✅ 环境检查通过！可以生成工作流")
        print("\n下一步:")
        print("  python3 scripts/generate_workflow.py --output my_workflow.json")
    else:
        print("⚠️ 环境需要配置，请解决上述问题")
        sys.exit(1)


if __name__ == "__main__":
    main()
