#!/usr/bin/env python3
"""academic-figures 一键环境准备：依赖检测/安装、中文字体检测、字体缓存清理、自检报告。
v4.9：--fix 显式开启自动安装（默认源→清华→阿里镜像回退）；默认仍只检测不装（供应链安全）。"""
import os
import shutil
import subprocess
import sys

# v3.7：版本下限精确化（多库依赖的具体版本要求明确化）
REQUIRED = {
    "matplotlib": "matplotlib>=3.5",
    "numpy": "numpy>=1.21",
    "pymupdf": "pymupdf>=1.20",
    "scipy": "scipy>=1.7",
}
MIN_PYTHON = (3, 8)
FAIL_EMOJI = "\u2717"
OK_EMOJI = "\u2713"


def run(cmd, timeout=300):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).returncode == 0
    except Exception:
        return False


def check_python():
    v = sys.version_info
    ok = (v.major, v.minor) >= MIN_PYTHON
    print(f"[{'OK' if ok else FAIL_EMOJI}] Python {v.major}.{v.minor}.{v.micro}"
          + ("" if ok else f" (需要 >= {MIN_PYTHON[0]}.{MIN_PYTHON[1]})"))
    return ok


MIRRORS = [
    None,  # 默认源（官方 PyPI）
    "https://pypi.tuna.tsinghua.edu.cn/simple",   # v4.9：国内镜像 fallback
    "https://mirrors.aliyun.com/pypi/simple/",
]


def pip_install(spec):
    """v4.9 --fix 模式：按 默认源→清华→阿里 顺序安装，全败返回 False。"""
    for idx, mirror in enumerate(MIRRORS):
        cmd = [sys.executable, "-m", "pip", "install", spec]
        src = "默认源"
        if mirror:
            cmd += ["-i", mirror]
            src = mirror.split("//")[1].split("/")[0]
        print(f"        … 安装 {spec}（{src}）")
        if run(cmd, timeout=600):
            return True
        print(f"        {spec} 经 {src} 失败" + ("，切换镜像重试…" if idx < len(MIRRORS) - 1 else ""))
    return False


def check_import(pkg_name, import_name=None, fix=False):
    import_name = import_name or pkg_name
    try:
        __import__(import_name)
        print(f"[OK] {pkg_name} 已安装")
        return True
    except ImportError:
        print(f"[{FAIL_EMOJI}] {pkg_name} 未安装")
        if not fix:
            print(f"        请手动安装（默认不自动执行 pip，避免供应链风险）:")
            print(f"        {sys.executable} -m pip install {pkg_name}")
            print(f"        或使用自动安装+国内镜像回退: python3 scripts/setup_env.py --fix")
            return False
        spec = REQUIRED.get(pkg_name, pkg_name)
        if pip_install(spec):
            print(f"[OK] {pkg_name} 安装成功")
            return True
        print(f"[{FAIL_EMOJI}] {pkg_name} 自动安装失败——请检查网络/权限后手动安装:")
        print(f"        {sys.executable} -m pip install {spec} -i https://pypi.tuna.tsinghua.edu.cn/simple")
        return False


def check_cjk_font():
    detect = os.path.join(os.path.dirname(os.path.abspath(__file__)), "detect_cjk_font.py")
    try:
        result = subprocess.run([sys.executable, detect], capture_output=True, text=True, timeout=30)
        info = json_loads(result.stdout)
        if info.get("found"):
            print(f"[OK] 中文字体: {info.get('name', info.get('path'))}")
            return True
        print(f"[{FAIL_EMOJI}] 未检测到中文字体 → 需安装（Linux: fonts-noto-cjk; macOS: 系统自带）")
        return False
    except Exception:
        print(f"[{FAIL_EMOJI}] 字体检测失败")
        return False


def json_loads(s):
    import json
    try:
        return json.loads(s)
    except Exception:
        return {}


def clear_font_cache():
    if sys.platform == "linux":
        cache = os.path.expanduser("~/.cache/matplotlib")
    elif sys.platform == "darwin":
        cache = os.path.expanduser("~/Library/Caches/matplotlib")
    else:
        cache = os.path.expandvars(r"%LOCALAPPDATA%\matplotlib")
    if os.path.isdir(cache):
        shutil.rmtree(cache, ignore_errors=True)
        print(f"[OK] 已清理 matplotlib 字体缓存: {cache}")
    else:
        print("[OK] 无 matplotlib 缓存（位置: " + cache + "）")


def main():
    fix = "--fix" in sys.argv[1:]
    print("=== academic-figures 环境自检 ===" + ("（--fix：缺依赖自动安装，镜像回退）" if fix else ""))
    ok_all = []
    ok_all.append(check_python())
    for pkg, imp in REQUIRED.items():
        ok_all.append(check_import(pkg, fix=fix))
    clear_font_cache()
    ok_all.append(check_cjk_font())
    print()
    if all(ok_all):
        print("环境就绪 ✓ — 可直接使用: python3 scripts/gen_figure.py -t bar -d data.json -o fig.png")
        sys.exit(0)
    print("仍有未满足项，按上方提示安装后重跑本脚本。")
    sys.exit(1)


if __name__ == "__main__":
    main()