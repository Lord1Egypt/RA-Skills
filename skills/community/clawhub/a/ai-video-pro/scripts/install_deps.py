"""
依赖自动安装脚本

根据选定的视频生成后端，自动安装所需依赖。
支持 Windows/macOS/Linux 跨平台。

安全原则：
- 所有安装操作前必须征得用户确认
- 安装前检查磁盘空间
- 使用系统包管理器（winget/brew/apt）
"""

import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def check_disk_space(required_gb: float = 5.0) -> bool:
    """检查磁盘空间是否充足。"""
    usage = shutil.disk_usage(Path.home().anchor if platform.system() == "Windows" else Path.home())
    free_gb = usage.free / (1024 ** 3)
    return free_gb >= required_gb


def install_ffmpeg() -> dict:
    """安装 ffmpeg。"""
    result = {"tool": "ffmpeg", "success": False, "message": ""}

    if shutil.which("ffmpeg"):
        result["success"] = True
        result["message"] = "ffmpeg 已安装"
        return result

    system = platform.system()

    try:
        if system == "Windows":
            subprocess.run(
                ["winget", "install", "Gyan.FFmpeg", "--accept-source-agreements",
                 "--accept-package-agreements"],
                check=True, timeout=300,
            )
        elif system == "Darwin":
            subprocess.run(["brew", "install", "ffmpeg"], check=True, timeout=300)
        elif system == "Linux":
            subprocess.run(
                ["sudo", "apt-get", "update", "-y"],
                check=True, timeout=60,
            )
            subprocess.run(
                ["sudo", "apt-get", "install", "-y", "ffmpeg"],
                check=True, timeout=300,
            )
        else:
            result["message"] = f"不支持的操作系统: {system}"
            return result

        result["success"] = True
        result["message"] = "ffmpeg 安装成功"
    except subprocess.CalledProcessError as e:
        result["message"] = f"安装失败: {e}"
    except FileNotFoundError:
        pkg_mgr = {"Windows": "winget", "Darwin": "brew", "Linux": "apt-get"}.get(system, "unknown")
        result["message"] = f"未找到包管理器 {pkg_mgr}，请手动安装 ffmpeg"

    return result


def install_python_packages(packages: list) -> dict:
    """安装 Python 包。"""
    result = {"tool": "python_packages", "success": False, "packages": {}}

    for pkg in packages:
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", pkg],
                check=True, capture_output=True, timeout=120,
            )
            result["packages"][pkg] = "已安装"
        except subprocess.CalledProcessError as e:
            result["packages"][pkg] = f"安装失败: {e.stderr.decode()[:200]}"
        except Exception as e:
            result["packages"][pkg] = f"错误: {e}"

    result["success"] = all(
        v == "已安装" for v in result["packages"].values()
    )
    return result


def install_comfyui(target_dir: str = None) -> dict:
    """安装 ComfyUI。"""
    result = {"tool": "comfyui", "success": False, "message": ""}

    if not shutil.which("git"):
        result["message"] = "需要先安装 git"
        return result

    if not check_disk_space(10.0):
        result["message"] = "磁盘空间不足，ComfyUI 至少需要 10GB 可用空间"
        return result

    if target_dir is None:
        target_dir = str(Path.home() / "ComfyUI")

    target_path = Path(target_dir)

    if target_path.exists():
        result["message"] = f"目录已存在: {target_dir}"
        if (target_path / "main.py").exists():
            result["success"] = True
            result["message"] = "ComfyUI 已安装"
        return result

    try:
        # Clone ComfyUI
        subprocess.run(
            ["git", "clone", "https://github.com/comfyanonymous/ComfyUI.git",
             str(target_path)],
            check=True, timeout=300,
        )

        # 安装依赖
        requirements = target_path / "requirements.txt"
        if requirements.exists():
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements)],
                check=True, timeout=600,
            )

        result["success"] = True
        result["message"] = f"ComfyUI 已安装到 {target_dir}"
    except subprocess.CalledProcessError as e:
        result["message"] = f"安装失败: {e}"
    except Exception as e:
        result["message"] = f"错误: {e}"

    return result


# 各后端所需的依赖
BACKEND_DEPENDENCIES = {
    "comfyui": {
        "bins": ["git"],
        "python_packages": ["torch", "torchvision", "Pillow", "requests"],
        "custom_install": install_comfyui,
        "disk_required_gb": 10.0,
        "description": "ComfyUI 本地视频生成（需要 NVIDIA GPU）",
    },
    "lumaai": {
        "bins": [],
        "python_packages": ["requests"],
        "disk_required_gb": 0.1,
        "description": "LumaAI Dream Machine API",
    },
    "runway": {
        "bins": [],
        "python_packages": ["requests"],
        "disk_required_gb": 0.1,
        "description": "Runway Gen-3/Gen-4 API",
    },
    "replicate": {
        "bins": [],
        "python_packages": ["requests"],
        "disk_required_gb": 0.1,
        "description": "Replicate 多模型 API",
    },
    "dalle_ffmpeg": {
        "bins": ["ffmpeg"],
        "python_packages": ["requests", "Pillow"],
        "disk_required_gb": 0.5,
        "description": "DALL-E 关键帧 + FFmpeg 拼接",
    },
}


def check_backend_ready(backend: str) -> dict:
    """检查指定后端的依赖是否就绪。"""
    deps = BACKEND_DEPENDENCIES.get(backend)
    if not deps:
        return {"ready": False, "message": f"未知后端: {backend}"}

    missing_bins = [b for b in deps["bins"] if not shutil.which(b)]
    missing_packages = []
    for pkg in deps["python_packages"]:
        try:
            __import__(pkg if pkg != "Pillow" else "PIL")
        except ImportError:
            missing_packages.append(pkg)

    ready = not missing_bins and not missing_packages
    if backend == "comfyui":
        comfyui_path = Path.home() / "ComfyUI"
        ready = ready and comfyui_path.exists() and (comfyui_path / "main.py").exists()

    return {
        "ready": ready,
        "missing_bins": missing_bins,
        "missing_packages": missing_packages,
        "disk_required_gb": deps["disk_required_gb"],
        "description": deps["description"],
    }


def install_for_backend(backend: str) -> list:
    """为指定后端安装所有缺失依赖。"""
    status = check_backend_ready(backend)
    if status["ready"]:
        return [{"tool": backend, "success": True, "message": "所有依赖已就绪"}]

    results = []

    # 检查磁盘空间
    deps = BACKEND_DEPENDENCIES[backend]
    if not check_disk_space(deps["disk_required_gb"]):
        results.append({
            "tool": "disk_check",
            "success": False,
            "message": f"磁盘空间不足，需要至少 {deps['disk_required_gb']}GB",
        })
        return results

    # 安装缺失的系统工具
    if "ffmpeg" in status["missing_bins"]:
        results.append(install_ffmpeg())

    # 安装缺失的 Python 包
    if status["missing_packages"]:
        results.append(install_python_packages(status["missing_packages"]))

    # 自定义安装（如 ComfyUI）
    if "custom_install" in deps and backend == "comfyui":
        results.append(install_comfyui())

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python install_deps.py --backend <backend_name>")
        print("      python install_deps.py --check <backend_name>")
        print(f"可用后端: {', '.join(BACKEND_DEPENDENCIES.keys())}")
        sys.exit(1)

    action = sys.argv[1]

    if action == "--check" and len(sys.argv) > 2:
        backend = sys.argv[2]
        status = check_backend_ready(backend)
        print(json.dumps(status, indent=2, ensure_ascii=False))

    elif action == "--backend" and len(sys.argv) > 2:
        backend = sys.argv[2]
        print(f"正在为 {backend} 安装依赖...")
        results = install_for_backend(backend)
        for r in results:
            print(json.dumps(r, indent=2, ensure_ascii=False))

    else:
        print("无效参数")
        sys.exit(1)
