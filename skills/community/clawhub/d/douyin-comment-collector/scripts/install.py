# -*- coding: utf-8 -*-
"""抖音评论采集 · 依赖安装器（一键装齐，装到「运行脚本的解释器」）。

为什么需要它：最常见的「装完跑不起来」是 pip 把包装进了另一个 python，
导致运行脚本时仍报 ModuleNotFoundError。本安装器始终用 ``sys.executable -m pip``，
保证装和运行是同一个解释器。

用法：
  cd <skill>/scripts
  python install.py                 # 装必装（httpx），跑完自检
  python install.py --all           # 必装 + 词频(jieba) + 浏览器(playwright+chromium)
  python install.py --with-analyze  # 额外装 jieba
  python install.py --with-browser  # 额外装 playwright 并下载 chromium
  python install.py --no-check      # 装完不跑自检

退出码：0 = 必装装好且自检通过；1 = 必装安装/自检失败。
"""

import argparse
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
REQUIRED = ["httpx>=0.27"]
OPTIONAL = {
    "analyze": ["jieba>=0.42"],
    "browser": ["playwright>=1.40"],
}


def _pip(args):
    """用当前解释器的 pip 执行；返回 (returncode, combined_output)。"""
    cmd = [sys.executable, "-m", "pip", "install", "--quiet"] + args
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def _is_externally_managed(out: str) -> bool:
    return "externally-managed-environment" in out or "This environment is externally managed" in out


def install_packages(packages, label):
    if not packages:
        return True
    print(f"[安装] {label}：{' '.join(packages)}  ->  {sys.executable}")
    rc, out = _pip(packages)
    if rc == 0:
        print(f"[安装] {label} 完成 ✅")
        return True
    if _is_externally_managed(out):
        # PEP 668：系统 python 禁止直接 pip install。引导建 venv。
        venv = os.path.join(_HERE, ".venv")
        print("[安装] 当前解释器为 externally-managed（系统 python），不可直接装。")
        print(f"        建议在该技能目录建虚拟环境后重试：")
        print(f"          python -m venv {venv}")
        if os.name == "nt":
            print(f"          {venv}\\Scripts\\activate")
        else:
            print(f"          source {venv}/bin/activate")
        print(f"          python install.py")
        return False
    print(f"[安装] {label} 失败 ❌：{out[-800:]}")
    return False


def install_browser():
    """playwright 装完后还需下载 chromium 二进制（较大的独立下载）。"""
    print("[安装] 浏览器底座：playwright + chromium")
    rc, out = _pip(OPTIONAL["browser"])
    if rc != 0:
        print(f"[安装] playwright 安装失败 ❌：{out[-800:]}")
        return False
    # 下载 chromium（仅二进制，非 pip 包）
    dl = subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        capture_output=True,
        text=True,
    )
    if dl.returncode != 0:
        print(f"[安装] chromium 下载失败 ❌：{(dl.stdout + dl.stderr)[-800:]}")
        return False
    print("[安装] chromium 就绪 ✅")
    return True


def run_self_check() -> int:
    print("[自检] 运行环境自检 ...")
    proc = subprocess.run([sys.executable, os.path.join(_HERE, "self_check.py")])
    return proc.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description="抖音评论采集 · 依赖安装器")
    ap.add_argument("--with-analyze", action="store_true", help="额外安装 jieba（词频分析）")
    ap.add_argument("--with-browser", action="store_true", help="额外安装 playwright + chromium（浏览器免登录）")
    ap.add_argument("--all", action="store_true", help="等价于 --with-analyze --with-browser")
    ap.add_argument("--no-check", action="store_true", help="装完不跑自检")
    args = ap.parse_args()

    print("=" * 60)
    print("抖音评论采集 · 依赖安装")
    print(f"目标解释器：{sys.executable}")
    print("=" * 60)

    # 1) 必装层（核心 HTTP 抓取必须）
    ok = install_packages(REQUIRED, "必装（httpx）")
    if not ok:
        print("[结果] ❌ 必装依赖未就绪，核心抓取不可用。")
        return 1

    # 2) 可选层
    if args.with_analyze or args.all:
        install_packages(OPTIONAL["analyze"], "可选（jieba 词频）")
    if args.with_browser or args.all:
        install_browser()

    # 3) 自检收尾
    if args.no_check:
        print("[结果] ✅ 必装依赖已安装（已跳过自检）。")
        return 0
    rc = run_self_check()
    if rc == 0:
        print("[结果] ✅ 必装层通过，环境就绪。")
    else:
        print("[结果] ❌ 自检发现必装层问题，请按上方自检报告修复。")
    return rc


if __name__ == "__main__":
    sys.exit(main())
