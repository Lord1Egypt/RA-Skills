"""
环境检测脚本

检测当前系统的视频生成能力，包括：
- GPU 类型和显存
- 已安装工具（ffmpeg、ComfyUI 等）
- API 密钥可用性
- 磁盘空间和网络连通性

输出 JSON 格式的检测报告和推荐后端列表。
"""

import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def detect_gpu() -> dict:
    """检测 GPU 信息。"""
    gpu_info = {
        "type": "none",
        "name": None,
        "vram_mb": 0,
        "cuda_available": False,
        "driver_version": None,
    }

    # 尝试通过 nvidia-smi 检测 NVIDIA GPU
    nvidia_smi = shutil.which("nvidia-smi")
    if nvidia_smi:
        try:
            result = subprocess.run(
                [nvidia_smi, "--query-gpu=name,memory.total,driver_version",
                 "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                parts = result.stdout.strip().split(", ")
                if len(parts) >= 3:
                    gpu_info["type"] = "nvidia"
                    gpu_info["name"] = parts[0].strip()
                    gpu_info["vram_mb"] = int(float(parts[1].strip()))
                    gpu_info["driver_version"] = parts[2].strip()
                    gpu_info["cuda_available"] = True
        except (subprocess.TimeoutExpired, Exception):
            pass

    # 如果没有 NVIDIA，尝试检测其他 GPU
    if gpu_info["type"] == "none":
        system = platform.system()
        if system == "Darwin":
            # macOS: 检测 Apple Silicon
            try:
                result = subprocess.run(
                    ["sysctl", "-n", "machdep.cpu.brand_string"],
                    capture_output=True, text=True, timeout=5
                )
                if "Apple" in result.stdout:
                    gpu_info["type"] = "apple_silicon"
                    gpu_info["name"] = result.stdout.strip()
            except (subprocess.TimeoutExpired, Exception):
                pass

    return gpu_info


def detect_tools() -> dict:
    """检测已安装的视频生成相关工具。"""
    tools = {}

    # ffmpeg
    ffmpeg_path = shutil.which("ffmpeg")
    tools["ffmpeg"] = {
        "installed": ffmpeg_path is not None,
        "path": ffmpeg_path,
        "version": None,
    }
    if ffmpeg_path:
        try:
            result = subprocess.run(
                [ffmpeg_path, "-version"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                first_line = result.stdout.split("\n")[0]
                tools["ffmpeg"]["version"] = first_line
        except (subprocess.TimeoutExpired, Exception):
            pass

    # Python
    tools["python"] = {
        "installed": True,
        "path": sys.executable,
        "version": platform.python_version(),
    }

    # git (ComfyUI 安装需要)
    git_path = shutil.which("git")
    tools["git"] = {
        "installed": git_path is not None,
        "path": git_path,
    }

    # ComfyUI
    comfyui_paths = [
        Path.home() / "ComfyUI",
        Path.home() / "comfyui",
        Path("C:/ComfyUI"),
        Path("D:/ComfyUI"),
    ]
    comfyui_found = None
    for p in comfyui_paths:
        if p.exists() and (p / "main.py").exists():
            comfyui_found = str(p)
            break
    tools["comfyui"] = {
        "installed": comfyui_found is not None,
        "path": comfyui_found,
    }

    # 检测关键 Python 包
    python_packages = {}
    for pkg in ["torch", "diffusers", "requests", "Pillow"]:
        try:
            __import__(pkg if pkg != "Pillow" else "PIL")
            python_packages[pkg] = True
        except ImportError:
            python_packages[pkg] = False
    tools["python_packages"] = python_packages

    return tools


def detect_api_keys() -> dict:
    """检测已配置的 API 密钥（仅检测存在性，不读取值）。"""
    keys = {
        "LUMAAI_API_KEY": bool(os.environ.get("LUMAAI_API_KEY")),
        "RUNWAY_API_KEY": bool(os.environ.get("RUNWAY_API_KEY")),
        "REPLICATE_API_TOKEN": bool(os.environ.get("REPLICATE_API_TOKEN")),
        "OPENAI_API_KEY": bool(os.environ.get("OPENAI_API_KEY")),
        "KLING_API_KEY": bool(os.environ.get("KLING_API_KEY")),
        "WEIBO_ACCESS_TOKEN": bool(os.environ.get("WEIBO_ACCESS_TOKEN")),
        "XHS_COOKIE": bool(os.environ.get("XHS_COOKIE")),
        "DOUYIN_ACCESS_TOKEN": bool(os.environ.get("DOUYIN_ACCESS_TOKEN")),
    }
    return keys


def detect_disk_space() -> dict:
    """检测可用磁盘空间。"""
    try:
        if platform.system() == "Windows":
            home = Path.home()
            usage = shutil.disk_usage(home.anchor)
        else:
            usage = shutil.disk_usage(Path.home())
        return {
            "total_gb": round(usage.total / (1024 ** 3), 1),
            "free_gb": round(usage.free / (1024 ** 3), 1),
            "sufficient_for_models": usage.free > 10 * (1024 ** 3),  # 10GB+
        }
    except Exception:
        return {"total_gb": 0, "free_gb": 0, "sufficient_for_models": False}


def detect_network() -> dict:
    """检测网络连通性。"""
    import urllib.request

    result = {"internet": False, "api_endpoints": {}}

    # 基础网络检测
    try:
        urllib.request.urlopen("https://httpbin.org/get", timeout=5)
        result["internet"] = True
    except Exception:
        try:
            urllib.request.urlopen("https://www.baidu.com", timeout=5)
            result["internet"] = True
        except Exception:
            pass

    return result


def recommend_backends(gpu: dict, tools: dict, api_keys: dict, disk: dict) -> list:
    """根据检测结果推荐最优后端（最小代价优先）。"""
    recommendations = []

    # 优先级 1: ComfyUI 本地（需要 NVIDIA GPU 8GB+）
    if (gpu["type"] == "nvidia" and gpu["vram_mb"] >= 8192
            and tools["comfyui"]["installed"]):
        recommendations.append({
            "priority": 1,
            "backend": "comfyui",
            "cost": "免费（仅电费）",
            "quality": "高",
            "status": "就绪",
            "note": f"本地 GPU: {gpu['name']}, {gpu['vram_mb']}MB VRAM",
        })
    elif (gpu["type"] == "nvidia" and gpu["vram_mb"] >= 8192
          and not tools["comfyui"]["installed"] and disk["sufficient_for_models"]):
        recommendations.append({
            "priority": 1,
            "backend": "comfyui",
            "cost": "免费（仅电费）",
            "quality": "高",
            "status": "需安装",
            "note": "检测到兼容 GPU，可安装 ComfyUI",
        })

    # 优先级 2-4: 云端 API（按免费额度优先）
    if api_keys.get("REPLICATE_API_TOKEN"):
        recommendations.append({
            "priority": 2,
            "backend": "replicate",
            "cost": "免费额度/按用量",
            "quality": "中",
            "status": "就绪",
        })

    if api_keys.get("LUMAAI_API_KEY"):
        recommendations.append({
            "priority": 3,
            "backend": "lumaai",
            "cost": "免费额度/~¥3.5每视频",
            "quality": "高",
            "status": "就绪",
        })

    if api_keys.get("RUNWAY_API_KEY"):
        recommendations.append({
            "priority": 4,
            "backend": "runway",
            "cost": "免费试用/~¥7每视频",
            "quality": "极高",
            "status": "就绪",
        })

    if api_keys.get("KLING_API_KEY"):
        recommendations.append({
            "priority": 5,
            "backend": "kling",
            "cost": "付费",
            "quality": "高",
            "status": "就绪",
            "note": "国内访问优化",
        })

    # 优先级 7: DALL-E + FFmpeg 兜底
    if api_keys.get("OPENAI_API_KEY") and tools["ffmpeg"]["installed"]:
        recommendations.append({
            "priority": 7,
            "backend": "dalle_ffmpeg",
            "cost": "~¥0.5/帧",
            "quality": "中",
            "status": "就绪",
            "note": "关键帧拼接方式",
        })

    # 如果没有任何可用方案
    if not recommendations:
        recommendations.append({
            "priority": 99,
            "backend": "none",
            "cost": "-",
            "quality": "-",
            "status": "需配置",
            "note": "请配置至少一个视频生成 API 密钥或安装 ComfyUI",
        })

    return sorted(recommendations, key=lambda x: x["priority"])


def run_full_detection() -> dict:
    """执行完整的环境检测。"""
    gpu = detect_gpu()
    tools = detect_tools()
    api_keys = detect_api_keys()
    disk = detect_disk_space()
    network = detect_network()

    recommendations = recommend_backends(gpu, tools, api_keys, disk)

    report = {
        "system": {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
        },
        "gpu": gpu,
        "tools": tools,
        "api_keys": api_keys,
        "disk": disk,
        "network": network,
        "recommendations": recommendations,
    }

    return report


if __name__ == "__main__":
    report = run_full_detection()
    print(json.dumps(report, indent=2, ensure_ascii=False))
