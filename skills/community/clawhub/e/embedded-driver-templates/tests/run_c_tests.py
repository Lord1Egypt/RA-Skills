# -*- coding: utf-8 -*-
"""
mcu-debug-mcp · C 驱动测试运行器（run_c_tests.py）

本文件由上游 mcu-debug-mcp/tests/ 随包复制，只改驱动路径前缀
（上游 drivers 目录 → 本包 assets/ 平铺 <驱动名>__<文件名>，判定逻辑一字未动）。

Makefile.logic 的等价物，但不需要 make，且**自动处理 Windows + msys2 的 cc1 PATH 坑**。

背景（实测踩过）：
    msys2 的 gcc.exe 单独能跑（--version 正常），但一旦真正编译就要 fork cc1.exe，
    而 cc1.exe 需要 mingw64/bin 下的运行时 DLL（libgmp/libmpfr/libisl/libmpc）。
    Windows 的 DLL 搜索路径不含 exe 所在目录（除非它就在 PATH 里），所以：
        gcc -E foo.c   →  rc=1，stdout/stderr 全空，看着像"被沙箱拦了"
    实际是 cc1.exe 崩在 STATUS_DLL_NOT_FOUND (0xC0000135)。
    修法：把 mingw64/bin 加到子进程 PATH 最前面。本脚本自动做这件事。

用法：
    python tests/run_c_tests.py              # 编译 9 款驱动（零警告检查）+ 链接 + 跑测试
    python tests/run_c_tests.py --warn-only  # 只做逐款零警告检查
    python tests/run_c_tests.py --gcc <path> # 指定 gcc
"""

import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS = os.path.join(ROOT, "tests")
# ★构建产物写系统临时目录，不落项目目录（与 test_fault_chain.py 同款说明）
BUILD = os.path.join(tempfile.gettempdir(), "mcu_debug_mcp_build")

DRIVERS = ["dht11", "hcsr04", "ds18b20", "mpu6050", "esp8266at",
           "ssd1306", "servo_sg90", "stepper_28byj48", "hc05"]

# Windows 常见的 gcc 安装位置（按优先级探测）
GCC_CANDIDATES = [
    r"D:\tools\msys64\mingw64\bin\gcc.exe",
    r"C:\msys64\mingw64\bin\gcc.exe",
    r"C:\msys64\ucrt64\bin\gcc.exe",
    r"D:\tools\w64devkit\bin\gcc.exe",
    r"C:\w64devkit\bin\gcc.exe",
]


def find_gcc(explicit=None):
    """定位 gcc，并把它的 bin 目录加进 PATH 以治好 cc1 的 DLL 搜索问题。"""
    gcc = explicit
    if gcc is None:
        gcc = shutil.which("gcc") or shutil.which("cc")
    if gcc is None:
        for c in GCC_CANDIDATES:
            if os.path.exists(c):
                gcc = c
                break
    if gcc is None:
        return None, None
    bindir = os.path.dirname(os.path.abspath(gcc))
    env = dict(os.environ)
    # 关键一步：cc1.exe 靠 PATH 找同目录 DLL
    env["PATH"] = bindir + os.pathsep + env.get("PATH", "")
    return gcc, env


def run(cmd, env, cwd=TESTS):
    return subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=cwd)


def check_warnings(gcc, env):
    """逐款编译，-Wall -Wextra 目标零警告。返回是否有问题。"""
    os.makedirs(BUILD, exist_ok=True)
    print("=== 逐款驱动编译（-Wall -Wextra -O1，目标零警告）===")
    objs, bad = [], []
    for d in DRIVERS:
        src = os.path.join(ROOT, "assets", "drivers", d, d + ".c")
        obj = os.path.join(BUILD, d + ".o")
        if not os.path.exists(src):
            print("  %-18s *** 源文件缺失 ***" % d)
            bad.append(d)
            continue
        r = run([gcc, "-c", "-Wall", "-Wextra", "-O1",
                 "-I", os.path.join(TESTS, "stub"),
                 "-I", os.path.join(ROOT, "assets", "drivers", d),
                 src, "-o", obj], env)
        w = r.stderr.strip()
        if r.returncode != 0:
            print("  %-18s FAIL rc=%d" % (d, r.returncode))
            print("     " + (w or "(无输出——检查 PATH 是否含 gcc 的 bin 目录)").replace("\n", "\n     "))
            bad.append(d)
        elif w:
            print("  %-18s 有警告" % d)
            print("     " + w.replace("\n", "\n     "))
            bad.append(d)
        else:
            print("  %-18s OK 零警告" % d)
            objs.append(obj)
    return objs, bad


def link_and_run(gcc, env, objs):
    print()
    print("=== 链接 + 运行 C 逻辑测试 ===")
    exe = os.path.join(BUILD, "test_driver_logic.exe" if os.name == "nt" else "test_driver_logic")
    cmd = [gcc, "-Wall", "-Wextra", "-O1", "-I", os.path.join(TESTS, "stub")]
    for d in DRIVERS:
        cmd += ["-I", os.path.join(ROOT, "assets", "drivers", d)]
    cmd += [os.path.join(TESTS, "test_driver_logic.c")] + objs + ["-o", exe]
    r = run(cmd, env)
    if r.returncode != 0:
        print("链接失败 rc=%d" % r.returncode)
        print(r.stderr[:2000])
        return 1
    if r.stderr.strip():
        print("链接警告：")
        print(r.stderr[:500])
    rr = subprocess.run([exe], capture_output=True, text=True, env=env, cwd=TESTS)
    out = rr.stdout + rr.stderr
    print(out[-3000:] if len(out) > 3000 else out)
    return rr.returncode


def main():
    ap = argparse.ArgumentParser(description="编译并运行 9 款驱动的 C 逻辑测试")
    ap.add_argument("--gcc", default=None, help="指定 gcc 路径")
    ap.add_argument("--warn-only", action="store_true", help="只做零警告检查，不链接运行")
    args = ap.parse_args()

    gcc, env = find_gcc(args.gcc)
    if gcc is None:
        print("没找到 gcc。安装任一：msys2（pacman -S mingw-w64-x86_64-gcc）/ w64devkit / linux gcc")
        return 2
    print("gcc: %s" % gcc)
    ver = run([gcc, "--version"], env)
    print("     %s" % (ver.stdout.splitlines() or ["?"])[0])
    print()

    objs, bad = check_warnings(gcc, env)
    if len(bad) == len(DRIVERS):
        print()
        print("全部编译失败。最可能原因：cc1.exe 找不到运行时 DLL。")
        print("本脚本已自动把 %s 加到 PATH；若仍失败，请确认该目录下有 libgmp-10.dll / libmpfr-6.dll。" %
              os.path.dirname(gcc))
        return 1
    if args.warn_only:
        print()
        print("零警告检查：%d/%d 款通过" % (len(DRIVERS) - len(bad), len(DRIVERS)))
        return 0 if not bad else 1

    rc = link_and_run(gcc, env, objs)
    print()
    if bad:
        print("注意：%d 款驱动有警告/失败：%s" % (len(bad), ", ".join(bad)))
    return rc


if __name__ == "__main__":
    sys.exit(main())
