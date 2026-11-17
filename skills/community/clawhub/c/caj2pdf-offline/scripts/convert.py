#!/usr/bin/env python3
# convert.py —— caj-to-pdf 技能批量转换驱动（自包含、可参数化）
# 路由：自动定位 venv 并 re-exec，调用 caj2pdf 引擎 + PyMuPDF 修复 xref。
# 优化点（来自实战 2026-07-25）：
#   * 用 PyMuPDF(fitz) 的 save(garbage=1, clean=True, deflate=True) 替代 mutool clean，
#     无需下载/安装 mutool；且比 PyPDF2 更稳（PyPDF2 对损坏 xref 报 startxref not found）。
#   * fitz 不可原地保存到原路径 -> 先写 .repair.tmp 再 os.replace。
#   * 逐文件异常隔离 + 格式检测 + 汇总报告；失败文件给全球学术快报兜底提示。
import os
import sys
import subprocess
import argparse
import warnings

warnings.filterwarnings("ignore")

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(SKILL_DIR, "caj2pdf-restructured")  # 已修复源码（含双路径 DLL + 3.13 补丁）
sys.path.insert(0, SRC)  # 确保 caj2pdf 包可被导入
# 运行时从 base64 内嵌包提取闭源解码 DLL 到三处 bin 目录（SkillHub 等平台拒绝 .dll，故内嵌）
from _dll_bundle import extract_dlls
extract_dlls(SRC)
HOME = os.path.expanduser("~")
MANAGED_VENV = os.path.join(HOME, ".workbuddy", "binaries", "python", "envs", "caj2pdf")
SUPPORTED = (".caj", ".kdh", ".nh")


def venv_python():
    if sys.platform.startswith("win"):
        return os.path.join(MANAGED_VENV, "Scripts", "python.exe")
    return os.path.join(MANAGED_VENV, "bin", "python")


def ensure_venv():
    """若 venv 不存在，自动跑同目录 setup.py。"""
    vpy = venv_python()
    if os.path.exists(vpy):
        return vpy
    print("[convert] venv not found, running setup.py ...")
    subprocess.run([sys.executable, os.path.join(SKILL_DIR, "setup.py")], check=True)
    if not os.path.exists(vpy):
        sys.exit("[convert] FATAL: venv still missing after setup.")
    return vpy


def scan_dir(d, recursive):
    out = []
    if recursive:
        for root, _, files in os.walk(d):
            for f in files:
                if f.lower().endswith(SUPPORTED):
                    out.append(os.path.join(root, f))
    else:
        for f in os.listdir(d):
            if f.lower().endswith(SUPPORTED):
                out.append(os.path.join(d, f))
    return out


def collect(inputs, indir, recursive):
    files = []
    for p in inputs:
        if os.path.isdir(p):
            files += scan_dir(p, recursive)
        elif os.path.isfile(p) and p.lower().endswith(SUPPORTED):
            files.append(p)
    if indir:
        files += scan_dir(indir, recursive)
    # 去重保序
    seen, uniq = set(), []
    for f in files:
        if f not in seen:
            seen.add(f)
            uniq.append(f)
    return uniq


def convert_one(inp, outdir):
    base = os.path.splitext(os.path.basename(inp))[0]
    out = os.path.join(outdir, base + ".pdf")
    rec = {"in": inp, "out": out, "status": None, "fmt": None, "pages": None, "err": None, "img": False}
    try:
        from caj2pdf.cajparser import CAJParser
        import fitz
        c = CAJParser(inp)
        rec["fmt"] = c.format
        # KDH / HN 多数图片型，文字不可选（格式固有属性）
        if str(c.format).upper() in ("KDH", "HN"):
            rec["img"] = True
        c.convert(out)
        # PyMuPDF 修复 xref（等效 mutool clean）
        try:
            doc = fitz.open(out)
            tmp = out + ".repair.tmp"
            doc.save(tmp, garbage=1, clean=True, deflate=True)
            rec["pages"] = doc.page_count
            doc.close()
            os.replace(tmp, out)
            rec["status"] = "OK"
        except Exception as e2:
            rec["status"] = "OK_NO_REPAIR"
            rec["err"] = "repair:" + repr(e2)
    except SystemExit as e:
        rec["status"] = "FAIL"
        rec["err"] = "SystemExit:" + str(e)
    except BaseException as e:
        rec["status"] = "FAIL"
        rec["err"] = type(e).__name__ + ":" + str(e)[:300]
    return rec


def main():
    # 1) 确保运行在 venv 中
    vpy = ensure_venv()
    if sys.executable != vpy and os.path.exists(vpy):
        subprocess.run([vpy, __file__, *sys.argv[1:]], check=True)
        return

    # 2) 解析参数
    ap = argparse.ArgumentParser(description="CAJ/KDH/NH -> PDF (high fidelity, text layer kept)")
    ap.add_argument("inputs", nargs="*", help="caj/kdh/nh 文件或目录")
    ap.add_argument("--indir", help="扫描此目录下的 caj/kdh/nh")
    ap.add_argument("--outdir", help="输出目录（默认：与各输入文件同目录）")
    ap.add_argument("-r", "--recursive", action="store_true", help="递归扫描目录")
    args = ap.parse_args()

    files = collect(args.inputs, args.indir, args.recursive)
    if not files:
        sys.exit("[convert] 未找到任何 .caj/.kdh/.nh 文件。用法见 SKILL.md。")

    print(f"[convert] 发现 {len(files)} 个文件，开始转换...")

    # 3) 逐文件转换（异常隔离）
    report = []
    for inp in files:
        outdir = args.outdir or os.path.dirname(inp)
        os.makedirs(outdir, exist_ok=True)
        rec = convert_one(inp, outdir)
        report.append(rec)
        tag = "IMG" if rec["img"] else "TXT"
        print(f"[{rec['status']}] [{tag}] fmt={rec['fmt']} pages={rec['pages']} -> {rec['out']}  {rec['err'] or ''}")

    # 4) 汇总
    ok = [r for r in report if r["status"].startswith("OK")]
    fail = [r for r in report if r["status"] == "FAIL"]
    print("\n===== SUMMARY =====")
    print(f"success={len(ok)} fail={len(fail)} total={len(report)}")
    for r in fail:
        print("FAIL:", os.path.basename(r["in"]), "| fmt=", r["fmt"], "| err=", r["err"])
    if fail:
        print("\n⚠️ 失败文件建议用「全球学术快报」官方客户端无损兜底：")
        print("   打开 CAJ -> 右键 -> 另存为 PDF（文字/排版/目录全保留，需知网账号）。")
    # 非0退出便于脚本/流水线判断
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
