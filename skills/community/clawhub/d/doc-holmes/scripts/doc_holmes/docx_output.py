#!/usr/bin/env python3
"""DOCX 回转：翻译产物 PDF → 可编辑 Word 文档（v2.5.0 双向管道闭环）。

LibreOffice headless PDF→DOCX 转换。产物是可编辑格式（文本框保留、
图表嵌入），但排版保真度低于原 PDF——用户文档里如实声明。
"""

from __future__ import annotations

import os
import shutil
import subprocess


def pdf_to_docx(pdf_path: str, outdir: str, timeout: int = 300) -> str:
    """翻译产物 PDF → DOCX。返回 DOCX 路径。

    使用 HOME 暂存目录（snap 沙箱限制：读不到 /tmp 和点目录），
    转换完成后搬运到 outdir 并清理暂存源。
    """
    lo_bin = _find_libreoffice()
    if not lo_bin:
        raise RuntimeError(_guidance(pdf_path))
    staging = os.path.join(os.path.expanduser("~"), "doc-holmes-office")
    os.makedirs(staging, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)
    staged_src = os.path.join(staging, os.path.basename(pdf_path))
    shutil.copyfile(pdf_path, staged_src)
    try:
        proc = subprocess.run(
            [lo_bin, "--headless", "--convert-to", "docx",
             "--outdir", staging, staged_src],
            capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise RuntimeError("LibreOffice DOCX 转换超时（%ds）：%s"
                           % (timeout, os.path.basename(pdf_path)))
    docx_stem = os.path.splitext(os.path.basename(pdf_path))[0] + ".docx"
    docx_staged = os.path.join(staging, docx_stem)
    if proc.returncode != 0 or not os.path.isfile(docx_staged):
        raise RuntimeError("LibreOffice DOCX 转换失败（rc=%s）：%s"
                           % (proc.returncode, (proc.stderr or "")[-200:]))
    final = os.path.join(outdir, docx_stem)
    shutil.move(docx_staged, final)
    return final


def _find_libreoffice() -> str | None:
    for name in ("libreoffice", "soffice"):
        found = shutil.which(name)
        if found:
            return found
    import glob
    for cand in ("/snap/bin/libreoffice", "/usr/bin/libreoffice",
                 "/usr/local/bin/libreoffice", "/snap/bin/soffice",
                 "/usr/bin/soffice", "/opt/libreoffice*/program/soffice"):
        hits = glob.glob(cand)
        if hits and os.path.isfile(hits[0]) and os.access(hits[0], os.X_OK):
            return hits[0]
    return None


def _guidance(pdf_path: str) -> str:
    return ("本机未安装 LibreOffice，无法把翻译 PDF 转成 DOCX。\n"
            "  · Debian/Ubuntu：apt install libreoffice\n"
            "  · macOS：brew install --cask libreoffice\n"
            "  · 或使用 --output-format pdf 保持 PDF 输出。")
