#!/usr/bin/env python3
"""office_input v2.7.0：DOCX/PPTX/PPT/XLSX/ODS 输入转换。

libreoffice headless → PDF → 现有管线。
HOME 暂存破解 snap 沙箱；源文件也拷入暂存（snap 读不到 /tmp）。
转换完成后清理暂存（finally）。
"""

from __future__ import annotations

import os
import shutil
import subprocess

SUPPORTED = {".docx": "writer", ".doc": "writer", ".pptx": "impress",
             ".ppt": "impress", ".xlsx": "calc", ".ods": "calc"}

_CANDIDATES = (
    "/snap/bin/libreoffice", "/usr/bin/libreoffice", "/usr/local/bin/libreoffice",
    "/snap/bin/soffice", "/usr/bin/soffice",
    "/opt/libreoffice*/program/soffice",
)


def libreoffice_bin() -> str | None:
    for name in ("libreoffice", "soffice"):
        found = shutil.which(name)
        if found:
            return found
    import glob
    for cand in _CANDIDATES:
        hits = glob.glob(cand)
        if hits and os.path.isfile(hits[0]) and os.access(hits[0], os.X_OK):
            return hits[0]
    return None


def conversion_guidance(input_path: str) -> str:
    return (
        "[转换] 本机未安装 libreoffice，无法把 %s 转成 PDF。\n"
        "  · Debian/Ubuntu：apt install libreoffice\n"
        "  · macOS：brew install --cask libreoffice\n"
        "  · 或先手动另存为 PDF 后重试。" % os.path.basename(input_path))


def convert_to_pdf(input_path: str, outdir: str, timeout: int = 300) -> str:
    """libreoffice headless 转 PDF。转换完自动清理暂存（finally）。"""
    binpath = libreoffice_bin()
    if not binpath:
        raise RuntimeError(conversion_guidance(input_path))
    ext = os.path.splitext(input_path)[1].lower()
    if ext not in SUPPORTED:
        raise RuntimeError("不支持的输入格式：%s（支持 %s）"
                           % (ext, "/".join(sorted(SUPPORTED.keys()))))
    staging = os.path.join(os.path.expanduser("~"), "doc-holmes-office")
    os.makedirs(staging, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)
    staged_src = os.path.join(staging, os.path.basename(input_path))
    shutil.copyfile(input_path, staged_src)
    try:
        proc = subprocess.run(
            [binpath, "--headless", "--convert-to", "pdf",
             "--outdir", staging, staged_src],
            capture_output=True, text=True, timeout=timeout,
            start_new_session=True)
        produced = os.path.join(
            staging, os.path.splitext(os.path.basename(input_path))[0] + ".pdf")
        if proc.returncode != 0 or not os.path.isfile(produced):
            raise RuntimeError("libreoffice 转换失败（rc=%s）：%s"
                               % (proc.returncode, (proc.stderr or "")[-200:]))
        final = os.path.join(outdir, os.path.basename(produced))
        shutil.move(produced, final)
        return final
    finally:
        # 清理暂存（含源文件拷贝，防医疗文书滞留）
        for f in (staged_src,):
            try:
                os.remove(f)
            except OSError:
                pass
