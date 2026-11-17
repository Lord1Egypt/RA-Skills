# -*- coding: utf-8 -*-
"""依赖引导脚本（跨平台）。

策略：
  1. 若技能自带 assets/vendor/ 存在兼容轮子，则优先用其离线安装；
     pip 会自动忽略与本平台不兼容的轮子（如 Windows 轮子在非 Windows 上被跳过），
     因此按「每个包」逐个尝试，能装多少装多少。
  2. 自带轮子装不上的包（通常是非 Windows 平台缺少对应编译轮子，或本技能因
     SkillHub 10MB 体积限制未内置离线轮子），回退到 PyPI 网络安装。
  3. 仍缺失则给出友好提示，交由 WorkBuddy 等 AI 工具处理。

说明：为满足 SkillHub 上传体积上限（≤10MB），本技能发布包未内置离线轮子，
运行时依赖由 WorkBuddy 等 AI 工具环境预装或自动从 PyPI 安装（python-docx、
python-pptx 及其依赖 lxml、Pillow 等）。如需完全离线，可将对应平台的轮子放入
assets/vendor/ 后重新打包，引导脚本会自动优先使用。
"""
import importlib
import os
import subprocess
import sys

VENDOR_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "assets", "vendor"
)
# 顶层包名 -> pip 安装名
PACKAGES = (("docx", "python-docx"), ("pptx", "python-pptx"))


def is_installed(import_name):
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False


def pip(args):
    return subprocess.run([sys.executable, "-m", "pip", "install", "--quiet"] + args)


def install_from_vendor(pip_name):
    """尝试仅用自带轮子安装某个包（逐包，容忍平台不兼容导致的失败）。"""
    if not os.path.isdir(VENDOR_DIR):
        return False
    wheels = [f for f in os.listdir(VENDOR_DIR) if f.endswith(".whl")]
    if not wheels:
        return False
    r = pip(["--no-index", "--find-links", VENDOR_DIR, pip_name])
    return r.returncode == 0


def install_from_pypi(pip_name):
    r = pip([pip_name])
    return r.returncode == 0


def main():
    missing = [imp for imp, _ in PACKAGES if not is_installed(imp)]
    if not missing:
        print("依赖已就绪：python-docx、python-pptx 均可用。")
        return 0

    print("正在准备技能依赖，请稍候（可能需要一两分钟）……")
    # 第一步：逐个用自带轮子安装（跨平台自动跳过不兼容轮子）
    for imp, pip_name in PACKAGES:
        if is_installed(imp):
            continue
        if install_from_vendor(pip_name):
            print("  ✓ %s（使用技能自带安装包）" % pip_name)
    # 第二步：剩余缺失的走网络安装
    for imp, pip_name in PACKAGES:
        if is_installed(imp):
            continue
        print("  … %s 改用网络安装" % pip_name)
        if install_from_pypi(pip_name):
            print("  ✓ %s（网络安装）" % pip_name)
    # 结果核对
    still_missing = [imp for imp, _ in PACKAGES if not is_installed(imp)]
    if not still_missing:
        print("依赖安装成功，可正常生成产物。")
        return 0
    print("部分依赖仍不可用：%s。" % ", ".join(still_missing))
    print("请将以上提示反馈给 WorkBuddy 等 AI 工具，由其自动安装所需依赖后重试。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
