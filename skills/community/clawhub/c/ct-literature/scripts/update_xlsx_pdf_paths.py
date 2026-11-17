# -*- coding: utf-8 -*-
"""把磁盘上已下载的 PDF 本地路径写回 Excel 报告（**事后补救 / 重扫** 用途）。

⚠️ 现状（2026-09-08 加固）：`PdfDownloader.run()` 在构造时传入 `xlsx_out` 已会
**自动回写** Excel「PDF 本地路径」列。主流程 `--download-pdf` 与任何独立直驱脚本
（只要构造 PdfDownloader 时传了 `xlsx_out`）都不再需要手动调本工具。本脚本现仅用于
两类补救场景：
  ① 下载完成后手动把 PDF 拷入 pdf 目录、需按文件名（DOI 转义 / → _）补写路径；
  ② 某次运行因异常未回写成功时，用同一 .merged.json + pdf 目录重扫重渲。

用途：检索产出 .merged.json 后，用 PdfDownloader（或任何下载器）把 PDF 落到某目录；
     运行本脚本扫描该目录（文件名 = DOI 转义，/ → _，.pdf），按 DOI 匹配 works，
     重渲 lit_report.xlsx ——「PDF 本地路径」列呈现真实落盘路径。

用法:
  python scripts/update_xlsx_pdf_paths.py --merged .merged.json --pdf-dir pdfs [--xlsx lit_report.xlsx]
可选:
  --notes-json latest40_manifest.json   注入下载失败原因（该清单 items[].doi/.note，
                                         无 PDF 的项在 Excel「PDF 本地路径」列显示「失败」）
  --lang auto|zh|en        报告语言（默认 auto）
  --safety                 渲染 Safety-Related 表（默认按 merged meta.safety）
"""
import argparse
import json
import os
import sys


def _base_is_chinese_os():
    """无 deprecation 的系统语言检测：优先 Windows 用户语言，其次环境变量。"""
    for k in ("LC_ALL", "LC_CTYPE", "LANG"):
        v = (os.environ.get(k) or "").lower()
        if v.startswith("zh"):
            return True
    try:
        import ctypes
        lang_id = ctypes.windll.kernel32.GetUserDefaultLangID()
        # 简体中文 0x0804 / 繁体中文 0x0404；主语言位 = lang_id & 0x3FF == 0x04
        return (lang_id & 0x3FF) == 0x04
    except Exception:
        return False


def scan_pdf_dir(pdf_dir):
    """返回 {doi: abs_path}——按 PdfDownloader 落盘命名反解 DOI（stem 中 / → _）。"""
    out = {}
    if not pdf_dir or not os.path.isdir(pdf_dir):
        return out
    for fn in sorted(os.listdir(pdf_dir)):
        if not fn.lower().endswith(".pdf") or fn.lower().endswith(".part"):
            continue
        stem = fn[:-4]
        doi = stem.replace("_", "/")
        out[doi] = os.path.abspath(os.path.join(pdf_dir, fn))   # 绝对路径便于复制打开
    return out


def main():
    ap = argparse.ArgumentParser(description="write downloaded PDF paths back into the Excel report")
    ap.add_argument("--merged", required=True, help=".merged.json from a ct-literature run")
    ap.add_argument("--pdf-dir", default="", help="directory holding downloaded PDFs (DOI-named)")
    ap.add_argument("--xlsx", default="", help="target xlsx (default: <merged dir>/lit_report.xlsx)")
    ap.add_argument("--notes-json", default="",
                    help="download manifest JSON with items[].doi/.note for failed items")
    ap.add_argument("--lang", default="auto", choices=["auto", "zh", "en"])
    ap.add_argument("--safety", action="store_true", default=None, help=argparse.SUPPRESS)
    args = ap.parse_args()

    base = os.path.dirname(os.path.abspath(args.merged))
    merged = json.load(open(args.merged, encoding="utf-8"))
    works = list(merged.get("works") or [])
    meta = merged.get("meta") or {}
    if args.xlsx:
        xlsx_out = args.xlsx
    else:
        xlsx_out = os.path.join(base, "lit_report.xlsx")

    # 失败原因注入：导出器据此在无路径项上显示「失败」（而非空 —）
    fail_notes = {}
    if args.notes_json and os.path.isfile(args.notes_json):
        try:
            nm = json.load(open(args.notes_json, encoding="utf-8"))
            for it in (nm.get("items") or []):
                doi = ((it.get("doi") or "").strip().lower())
                if doi and not it.get("pdf_path") and it.get("note"):
                    fail_notes[doi] = it["note"]
        except Exception as _e:
            print(f"[WARN] notes-json parse failed (ignored): {_e}")

    pdf_map = scan_pdf_dir(args.pdf_dir or os.path.join(base, "pdfs"))
    hit = 0
    # 大小KB / 页数佐证列（2026-10-25）：重扫时按磁盘文件现算（页数需解析器，
    # 缺 pypdf/fitz 时留空——与 PdfDownloader 主路径同口径，不造假）。
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "adapters"))
        from pdf_download import _pdf_meta as _pdf_meta_fn
    except Exception:
        _pdf_meta_fn = None
    for w in works:
        doi = (w.get("doi") or "").strip().lower()
        p = pdf_map.get(doi)
        if p:
            w["local_pdf_path"] = p
            hit += 1
            if _pdf_meta_fn is not None:
                try:
                    _kb, _pg = _pdf_meta_fn(p)
                    w["pdf_size_kb"] = _kb
                    w["pdf_pages"] = _pg
                except Exception:
                    pass
        elif fail_notes.get(doi):
            w["pdf_download_note"] = fail_notes[doi]

    from export_xlsx import export_workbook   # scripts/ 同目录
    safety = args.safety if args.safety is not None else bool(meta.get("safety"))
    export_workbook({"count": len(works), "works": works, "meta": meta},
                    xlsx_out, lang=args.lang, safety=safety)

    zh = (args.lang == "zh") or (args.lang == "auto" and _base_is_chinese_os())
    if zh:
        print(f"[OK] Excel 已更新：{hit}/{len(works)} 篇的 PDF 本地路径已写入「PDF 本地路径」列 -> {xlsx_out}")
        if len(works) - hit:
            print(f"[TIP] {len(works) - hit} 篇未匹配到 PDF 文件（该列显示 —/失败）")
    else:
        print(f"[OK] xlsx updated: PDF path written for {hit}/{len(works)} works -> {xlsx_out}")
        if len(works) - hit:
            print(f"[TIP] {len(works) - hit} works without a matching PDF file (column shows —/failed)")


if __name__ == "__main__":
    sys.exit(main())
