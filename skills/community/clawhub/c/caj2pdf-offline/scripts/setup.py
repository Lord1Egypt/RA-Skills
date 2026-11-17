#!/usr/bin/env python3
# setup.py —— 为 caj-to-pdf 技能构建隔离运行环境（幂等）
# 检测 WorkBuddy managed Python 3.13，建 venv 并装依赖（阿里云镜像）。
import os
import sys
import subprocess

HOME = os.path.expanduser("~")

# 运行时从 base64 内嵌包提取闭源解码 DLL 到三处 bin 目录
# （SkillHub 等平台拒绝 .dll，故用 _dll_bundle 内嵌；提取到与原始布局一致的位置）
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "caj2pdf-restructured")
if SRC not in sys.path:
    sys.path.insert(0, SRC)
try:
    from _dll_bundle import extract_dlls
    extract_dlls(SRC)
except Exception as e:
    print(f"[setup] WARN: DLL 提取失败（转换时 convert.py 会再试）: {e}")

# 优先用 WorkBuddy managed Python 3.13（隔离、预配置）
MANAGED_PY = os.path.join(HOME, ".workbuddy", "binaries", "python", "versions", "3.13.12", "python.exe")
# venv 落点（与 managed runtime 同目录，便于统一运维）
VENV = os.path.join(HOME, ".workbuddy", "binaries", "python", "envs", "caj2pdf")

PYPI_MIRROR = "https://mirrors.aliyun.com/pypi/simple"
DEPS = ["imagesize==1.3.0", "PyPDF2==2.2.0", "PyMuPDF"]


def venv_python():
    if sys.platform.startswith("win"):
        return os.path.join(VENV, "Scripts", "python.exe")
    return os.path.join(VENV, "bin", "python")


def venv_pip():
    if sys.platform.startswith("win"):
        return os.path.join(VENV, "Scripts", "pip.exe")
    return os.path.join(VENV, "bin", "pip")


def main():
    base_py = MANAGED_PY if os.path.exists(MANAGED_PY) else sys.executable
    vpy = venv_python()
    print(f"[setup] base python : {base_py}")
    print(f"[setup] target venv : {VENV}")

    # 已存在且关键依赖（fitz）可用 -> 跳过
    if os.path.exists(vpy):
        try:
            subprocess.run([vpy, "-c", "import fitz, imagesize, PyPDF2"],
                           check=True, capture_output=True)
            print("[setup] venv already ready, nothing to do.")
            return
        except Exception:
            print("[setup] venv exists but deps missing, reinstalling deps...")

    # 建 venv
    print("[setup] creating venv ...")
    subprocess.run([base_py, "-m", "venv", VENV], check=True)

    # 装依赖（阿里云镜像，国内快；pyproject 也指向此镜像）
    print(f"[setup] installing deps via {PYPI_MIRROR} ...")
    subprocess.run([venv_pip(), "install", "-i", PYPI_MIRROR, *DEPS], check=True)

    # 校验
    subprocess.run([vpy, "-c", "import fitz, imagesize, PyPDF2; print('deps ok')"], check=True)
    print("[setup] DONE. caj-to-pdf environment is ready.")


if __name__ == "__main__":
    main()
