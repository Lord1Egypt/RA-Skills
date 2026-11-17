#!/usr/bin/env python3
"""CTF 环境自检脚本：检测解题所需 Python 库与外部工具，输出缺失项与安装指引。

用法:
    python env-check.py            # 用当前 Python 检测
    python env-check.py --fix-hint # 额外输出安装命令

本脚本只用 Python 标准库，可在任何 Python 3.8+ 上运行。
"""
import os
import platform
import shutil
import struct
import subprocess
import sys

OK, WARN, MISS = "[OK]  ", "[WARN]", "[MISS]"


def section(title):
    print(f"\n=== {title} ===")


def check_python_lib(name, import_name=None, note=""):
    mod = import_name or name
    try:
        m = __import__(mod)
        ver = getattr(m, "__version__", None) or getattr(m, "version", None)
        if callable(ver):
            try:
                ver = ver()
            except Exception:
                ver = None
        suffix = f" ({ver})" if ver else ""
        print(f"{OK}{name}{suffix}{' - ' + note if note else ''}")
        return True
    except ImportError:
        print(f"{MISS}{name}{' - ' + note if note else ''}")
        return False


def find_command(names, extra_paths=None, glob_roots=None):
    """names: list[str]; 返回第一个能找到的 (显示名, 完整路径)。
    extra_paths: 精确候选路径; glob_roots: (目录, 相对通配) 列表，均支持通配符。"""
    import glob as _glob
    for n in names:
        p = shutil.which(n)
        if p:
            return n, p
    for p in extra_paths or []:
        p = os.path.expandvars(p)
        if os.path.exists(p):
            return os.path.basename(p), p
    for root_pat, rel in glob_roots or []:
        for cand in _glob.glob(os.path.expandvars(os.path.join(root_pat, rel)), recursive=True):
            if os.path.exists(cand):
                return os.path.basename(cand), cand
    return None, None


def check_external(names, purpose, install_hint, extra_paths=None, glob_roots=None):
    n, p = find_command(names if isinstance(names, list) else [names],
                        extra_paths=extra_paths, glob_roots=glob_roots)
    if p:
        print(f"{OK}{purpose}: {p}")
        return True
    print(f"{MISS}{purpose} -> 安装: {install_hint}")
    return False


def check_wsl_distro():
    if platform.system() != "Windows":
        return None
    wsl = shutil.which("wsl")
    if not wsl:
        return None
    try:
        out = subprocess.run(
            ["wsl", "--list", "--quiet"],
            capture_output=True, timeout=15,
        ).stdout.decode("utf-16-le", errors="ignore")
        distros = [l.strip().lstrip("*").strip() for l in out.splitlines() if l.strip()]
        return distros or None
    except Exception:
        return None


def main():
    print("CTF 环境自检")
    print(f"平台: {platform.system()} {platform.release()} | "
          f"Python {platform.python_version()} ({struct.calcsize('P') * 8}-bit) | "
          f"解释器: {sys.executable}")

    if struct.calcsize("P") * 8 != 64:
        print(f"{WARN}当前 Python 是 32 位，pwntools 不支持；请安装 64 位 Python 并重建虚拟环境。")

    section("解题 Python 库")
    libs = [
        ("pwntools", "pwn", "PWN 利用核心"),
        ("z3-solver", "z3", "约束求解"),
        ("sympy", None, "数论/符号计算"),
        ("pycryptodome", "Crypto", "对称/非对称加解密"),
        ("gmpy2", None, "大整数加速（RSA/格）"),
        ("requests", None, "Web 交互"),
        ("volatility3", "volatility3", "内存取证"),
        ("flask-unsign", "flask_unsign", "Flask 会话解码"),
        ("pillow", "PIL", "图像隐写"),
        ("numpy", None, "数值/位平面"),
        ("pyzbar", None, "QR 解码"),
        ("python-magic-bin", "magic", "文件类型识别"),
        ("dnspython", "dns", "DNS 解析"),
    ]
    missing = []
    for name, mod, note in libs:
        if not check_python_lib(name, mod, note):
            missing.append(name if name != "python-magic-bin" else "python-magic-bin")

    section("外部工具")
    checks = [
        (["tshark"], "流量分析 (tshark)", "winget install WiresharkFoundation.Wireshark",
         [r"%ProgramFiles%\Wireshark\tshark.exe", r"%ProgramFiles(x86)%\Wireshark\tshark.exe",
          r"%LOCALAPPDATA%\Programs\Wireshark\tshark.exe"], []),
        (["hashcat"], "哈希爆破", "winget install hashcat 或官网下载", [], []),
        (["semgrep"], "源码审计", "pip install semgrep（或独立 venv）", [], []),
        (["sqlmap"], "SQL 注入", "pip install sqlmap", [], []),
        (["ffuf"], "目录爆破", "winget install ffuf", [], []),
        (["ghidraRun", "analyzeHeadless"], "Ghidra 逆向", "官网下载绿色版解压，需 Java 17+",
         [], [(r"%USERPROFILE%\Tools\**", r"ghidra*\support\analyzeHeadless.bat"),
              (r"%USERPROFILE%", r"ghidra*\support\analyzeHeadless.bat"),
              ("C:\\", r"ghidra*\support\analyzeHeadless.bat"),
              ("D:\\", r"ghidra*\support\analyzeHeadless.bat"),
              (r"%LOCALAPPDATA%", r"ghidra*\support\analyzeHeadless.bat")]),
        (["java"], "Java 运行时（Ghidra 依赖）", "winget install Microsoft.OpenJDK.21", [], []),
    ]
    for names, purpose, hint, extra, globs in checks:
        check_external(names, purpose, hint, extra_paths=extra, glob_roots=globs)

    section("WSL / Linux 工具（可选但强烈推荐）")
    distros = check_wsl_distro()
    if distros:
        print(f"{OK}WSL 发行版: {', '.join(distros)}")
        print("    建议在 Kali 内补齐: gdb / binwalk / foremost / strings / john /")
        print("    checksec / ROPgadget / strace / ltrace / upx / nmap / 字典文件")
        print("    Kali: wsl --install kali-linux; 其他发行版: sudo apt install 对应包")
    elif platform.system() == "Windows":
        print(f"{MISS}未检测到 WSL 发行版 -> wsl --install kali-linux")
        print("    （gdb/ltrace/binwalk/foremost 等 Linux 工具需要 WSL）")
    else:
        print("    Linux/macOS: 直接用系统包管理器安装上述工具")

    if missing:
        print(f"\n>>> 缺失 Python 库可一键安装:\n    {sys.executable} -m pip install "
              + " ".join(missing))
    else:
        print("\n>>> Python 库齐全。")


if __name__ == "__main__":
    main()
