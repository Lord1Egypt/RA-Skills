#!/usr/bin/env python3
"""Creative Studio dependency checker and installer.

Exit codes:
  0 - All required deps available
  1 - Missing required deps
  2 - Missing optional deps (usable in degraded mode)
"""

import argparse
import io
import subprocess
import sys
import importlib

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

REQUIRED = {
    "PIL": ("Pillow", "pip install Pillow"),
}

OPTIONAL = {
    "rembg": ("rembg", "pip install rembg"),
    "easyocr": ("easyocr", "pip install easyocr"),
    "edge_tts": ("edge-tts", "pip install edge-tts"),
}

SYSTEM_TOOLS = {
    "ffmpeg": ("FFmpeg", "https://ffmpeg.org/download.html"),
    "magick": ("ImageMagick", "https://imagemagick.org/script/download.php"),
}

LANG = {
    "zh": {
        "checking": "=== 萤火虫创意工坊 - 环境检测 ===",
        "python_ver": "Python 版本",
        "python_old": "版本过旧，建议 >= 3.9",
        "required_section": "--- 必需依赖 ---",
        "optional_section": "--- 可选依赖 ---",
        "system_section": "--- 系统工具 ---",
        "ok": "已安装",
        "missing": "未安装",
        "install_hint": "安装命令",
        "download_hint": "下载地址",
        "all_ok": "[✓] 所有必需依赖已就绪。",
        "optional_missing": "[!] 部分可选功能不可用，Skill 以降级模式运行。",
        "required_missing": "[✗] 缺少必需依赖",
        "installing": "正在安装",
        "install_success": "安装成功",
        "install_fail": "安装失败，请手动执行",
        "summary": "检测结果",
        "required_ok_count": "必需依赖通过",
        "optional_ok_count": "可选依赖通过",
        "system_ok_count": "系统工具通过",
        "features_available": "可用功能",
        "features_unavailable": "不可用功能",
        "feat_image_edit": "图片基础编辑",
        "feat_bg_remove": "AI 背景移除（抠图）",
        "feat_ocr": "OCR 文字识别",
        "feat_tts": "AI 语音配音",
        "feat_video": "视频剪辑处理",
        "feat_detail_pages": "详情页生成",
        "feat_3d": "3D 产品展示",
    },
    "en": {
        "checking": "=== Firefly Creative Studio - Environment Check ===",
        "python_ver": "Python version",
        "python_old": "Version too old, recommend >= 3.9",
        "required_section": "--- Required ---",
        "optional_section": "--- Optional ---",
        "system_section": "--- System Tools ---",
        "ok": "Installed",
        "missing": "Not installed",
        "install_hint": "Install",
        "download_hint": "Download",
        "all_ok": "[✓] All required dependencies ready.",
        "optional_missing": "[!] Some optional features unavailable.",
        "required_missing": "[✗] Missing required dependencies",
        "installing": "Installing",
        "install_success": "OK",
        "install_fail": "FAILED, run manually",
        "summary": "Summary",
        "required_ok_count": "Required passed",
        "optional_ok_count": "Optional passed",
        "system_ok_count": "System tools passed",
        "features_available": "Available",
        "features_unavailable": "Unavailable",
        "feat_image_edit": "Basic image editing",
        "feat_bg_remove": "AI background removal",
        "feat_ocr": "OCR text recognition",
        "feat_tts": "AI voiceover (TTS)",
        "feat_video": "Video editing",
        "feat_detail_pages": "Detail page generation",
        "feat_3d": "3D product display",
    },
}


def check_python(msg):
    v = sys.version_info
    print(f"  {msg['python_ver']}: {v.major}.{v.minor}.{v.micro}")
    if v < (3, 9):
        print(f"  ⚠ {msg['python_old']}")
        return False
    print(f"  ✓ {msg['ok']}")
    return True


def check_pip_pkg(import_name, pkg_info, msg):
    pkg_name, install_cmd = pkg_info
    try:
        importlib.import_module(import_name)
        print(f"  ✓ {pkg_name}")
        return True
    except ImportError:
        print(f"  ✗ {pkg_name} - {msg['missing']} ({msg['install_hint']}: {install_cmd})")
        return False


def check_system_tool(cmd, tool_info, msg):
    tool_name, url = tool_info
    shell = sys.platform == "win32"
    try:
        r = subprocess.run(
            [cmd, "--version"], capture_output=True, text=True,
            timeout=10, shell=shell
        )
        if r.returncode == 0:
            print(f"  ✓ {tool_name}")
            return True
    except Exception:
        pass
    try:
        r = subprocess.run(
            [cmd], capture_output=True, text=True,
            timeout=10, shell=shell
        )
        if r.returncode in (0, 1):
            print(f"  ✓ {tool_name}")
            return True
    except Exception:
        pass
    print(f"  ✗ {tool_name} - {msg['missing']} ({msg['download_hint']}: {url})")
    return False


def install_packages(packages, msg):
    print(f"\n  {msg['installing']}...")
    for pkg_name, install_cmd in packages:
        print(f"    {pkg_name}...", end=" ")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg_name],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                timeout=300,
            )
            print(msg["install_success"])
        except subprocess.CalledProcessError:
            print(f"{msg['install_fail']}: {install_cmd}")
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Creative Studio dependency checker")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--install-missing", action="store_true")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    args = parser.parse_args()

    msg = LANG[args.lang]

    print(msg["checking"])
    print()

    check_python(msg)
    print()

    # Required
    print(msg["required_section"])
    required_ok = []
    required_missing = []
    for name, info in REQUIRED.items():
        if check_pip_pkg(name, info, msg):
            required_ok.append(name)
        else:
            required_missing.append(info)
    print()

    # Optional
    print(msg["optional_section"])
    optional_ok = []
    optional_missing = []
    for name, info in OPTIONAL.items():
        if check_pip_pkg(name, info, msg):
            optional_ok.append(name)
        else:
            optional_missing.append(info)
    print()

    # System tools
    print(msg["system_section"])
    system_ok = []
    for cmd, info in SYSTEM_TOOLS.items():
        if check_system_tool(cmd, info, msg):
            system_ok.append(cmd)
    print()

    # Feature availability
    features_ok = [msg["feat_image_edit"], msg["feat_detail_pages"], msg["feat_3d"]]
    features_missing = []

    opt_missing_names = [info[0] for info in optional_missing]

    if "rembg" in opt_missing_names:
        features_missing.append(msg["feat_bg_remove"])
    else:
        features_ok.append(msg["feat_bg_remove"])

    if "easyocr" in opt_missing_names:
        features_missing.append(msg["feat_ocr"])
    else:
        features_ok.append(msg["feat_ocr"])

    if "edge-tts" in opt_missing_names:
        features_missing.append(msg["feat_tts"])
    else:
        features_ok.append(msg["feat_tts"])

    if "ffmpeg" not in system_ok:
        features_missing.append(msg["feat_video"])
    else:
        features_ok.append(msg["feat_video"])

    # Summary
    print(f"--- {msg['summary']} ---")
    print(f"  {msg['required_ok_count']}: {len(required_ok)}/{len(REQUIRED)}")
    print(f"  {msg['optional_ok_count']}: {len(optional_ok)}/{len(OPTIONAL)}")
    print(f"  {msg['system_ok_count']}: {len(system_ok)}/{len(SYSTEM_TOOLS)}")
    print()
    print(f"  ✓ {msg['features_available']}: {', '.join(features_ok)}")
    if features_missing:
        print(f"  ✗ {msg['features_unavailable']}: {', '.join(features_missing)}")
    print()

    # Install if requested
    if args.install_missing and (required_missing or optional_missing):
        if not install_packages(required_missing + optional_missing, msg):
            sys.exit(1)

    if required_missing:
        print(msg["required_missing"])
        sys.exit(1)
    elif optional_missing:
        print(msg["optional_missing"])
        sys.exit(2)
    else:
        print(msg["all_ok"])
        sys.exit(0)


if __name__ == "__main__":
    main()
