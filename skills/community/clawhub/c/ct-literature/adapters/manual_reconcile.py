#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
manual_reconcile.py — needs_manual.csv 导出 + manual_incoming 回传归位（v1.5.3）。

参考 meta-analysis A3「内网/订阅全文下载共享后端」思想（a3_pending / a3_stash_pdf，
workbench/server.py:1832-1931）的 **CLI 化、无服务器版**：
  云端（coze）够不到用户内网，唯一带机构订阅/登录态的是**用户浏览器**。
  与 Sci-Hub 兜底（法律风险、用户自担）相比，本通道用的是**用户自己的订阅权**，
  完全合法合规——机构环境（GCP/申办方项目）的推荐兜底位，优先于 Sci-Hub。

工作流：
  1) --download-pdf 运行结束 → run() 末段导出 needs_manual.csv
     （仍无 PDF 且有 DOI 的条目，含 https://doi.org/<doi> 深链，供浏览器手动下载）；
  2) 用户用机构权限在浏览器下载这些 PDF，丢进 <out_dir>/pdfs/manual_incoming/；
  3) `python ct_literature.py --reconcile-manual <out_dir>` 扫描该目录：
     文件名/正文 DOI 提取 → 匹配 merged.json 的 works → %PDF 头 + 页数校验 →
     os.replace 归位为标准命名（pdfs/<safe_doi>.pdf）→ 回写 local_pdf_path /
     pdf_via="manual_incoming"（台账信任级 = 高·机构权限）→ 重写 .merged.json。

纯标准库；pypdf/fitz 可用时才做页数深度校验（缺失按放行，与主链路同口径）。
"""

import json
import os
import re

# 与 pdf_download._VIA_LABEL / _VIA_TRUST 对齐的台账口径（在此定义避免循环 import）
VIA = "manual_incoming"
VIA_LABEL = "手动回传(机构权限)"
VIA_TRUST = "高"


# ---------------------------------------------------------------------------
# ① needs_manual.csv 导出
# ---------------------------------------------------------------------------
def export_needs_manual(works, base_dir, log=None) -> str:
    """把「仍无本地 PDF 且有 DOI、非 skip/拒绝」的条目导出为 needs_manual.csv。

    base_dir：与 pdf_manifest.csv 同目录（xlsx_out 所在目录，运行根目录）。
    返回 CSV 绝对路径；无待下条目时不生成文件、返回 ""。
    """
    import csv
    log = log or (lambda m: None)
    rows = []
    for w in works or []:
        if w.get("local_pdf_path"):
            continue
        doi = (w.get("doi") or "").strip()
        if not doi:
            continue
        note = w.get("pdf_download_note") or ""
        if note.startswith("no DOI") or "non-OA" in note or "rejected" in note:
            continue
        rows.append([
            (w.get("title") or "")[:120],
            doi,
            f"https://doi.org/{doi}",
            note or "OA/预印本/云端解码均未命中",
        ])
    if not rows:
        return ""
    try:
        path = os.path.join(base_dir, "needs_manual.csv")
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            wcsv = csv.writer(f)
            wcsv.writerow(["题名", "DOI", "深链(机构权限浏览器打开)", "失败原因"])
            wcsv.writerows(rows)
        log(f"[OK] needs_manual.csv 已生成（{len(rows)} 篇待手动回传） -> {path}")
        return os.path.abspath(path)
    except Exception as e:
        log(f"[WARN] needs_manual.csv 生成失败（不影响主流程）: {type(e).__name__}: {e}")
        return ""


# ---------------------------------------------------------------------------
# ② DOI 提取（文件名 → 正文兜底）
# ---------------------------------------------------------------------------
_DOI_FILENAME_RE = re.compile(r"(10\.\d{4,9})[._\- ](.+?)(?:\.pdf)?$", re.I)
_DOI_TEXT_RE = re.compile(r"\b(10\.\d{4,9}/[^\s\"<>]+)", re.I)
_DOI_PREFIXES = ("https://doi.org/", "http://doi.org/", "doi:", "doi.org/")


def _norm_doi(doi: str) -> str:
    d = (doi or "").strip().lower()
    for p in _DOI_PREFIXES:
        if d.startswith(p):
            d = d[len(p):]
    return d.strip().rstrip(".,;")


def _doi_from_filename(stem: str) -> str:
    """从文件名提取 DOI。支持 `10.1038_s41586-021-03819-2` /
    `10.1038-s41586-021-03819-2` / `10.1038 s41586...` 等分隔符变体。"""
    m = _DOI_FILENAME_RE.search(stem)
    if not m:
        return ""
    return _norm_doi(f"{m.group(1)}/{m.group(2)}")


def _doi_from_pdf_text(path: str) -> str:
    """从 PDF 前 2 页正文提取 DOI（pypdf/fitz 任一可用时；都缺则返回 ""）。"""
    text = ""
    try:
        try:
            from pypdf import PdfReader
            with open(path, "rb") as f:
                r = PdfReader(f)
                text = "\n".join((p.extract_text() or "") for p in r.pages[:2])
        except ImportError:
            import fitz
            with fitz.open(path) as doc:
                text = "\n".join(doc[i].get_text() for i in range(min(2, doc.page_count)))
    except Exception:
        return ""
    m = _DOI_TEXT_RE.search(text or "")
    return _norm_doi(m.group(1)) if m else ""


# ---------------------------------------------------------------------------
# ③ reconcile：扫描 manual_incoming → 匹配 → 归位 → 回写
# ---------------------------------------------------------------------------
def reconcile_manual(out_dir: str, works: list, log=None) -> dict:
    """扫描 <out_dir>/pdfs/manual_incoming/*.pdf，按 DOI 匹配 works 并归位。

    归位 = os.replace 到 <out_dir>/pdfs/<safe_doi>.pdf（标准命名，与主链路一致），
    并设置 work 的 local_pdf_path / pdf_via / pdf_size_kb / pdf_pages，
    清除 pdf_download_note。匹配不上的文件**原地保留**（报告列出，不删不挪）。

    返回 stats：{incoming, matched, unmatched, invalid, no_doi}。
    """
    log = log or (lambda m: None)
    pdf_dir = os.path.join(out_dir, "pdfs")
    incoming = os.path.join(pdf_dir, "manual_incoming")
    stats = {"incoming": 0, "matched": 0, "unmatched": 0, "invalid": 0, "no_doi": 0}
    if not os.path.isdir(incoming):
        return stats
    # 延迟 import：深度校验/命名与主链路同口径
    from adapters.pdf_download import _pdf_is_valid, _pdf_meta, _safe_filename

    by_doi = {}
    for w in works or []:
        d = _norm_doi(w.get("doi") or "")
        if d and not w.get("local_pdf_path"):
            by_doi[d] = w

    for fn in sorted(os.listdir(incoming)):
        src = os.path.join(incoming, fn)
        if not fn.lower().endswith(".pdf") or not os.path.isfile(src):
            continue
        stats["incoming"] += 1
        # %PDF 头校验（拒绝登录页/验证页误存，与 meta-analysis a3_stash 同口径）
        try:
            with open(src, "rb") as f:
                if f.read(5) != b"%PDF-":
                    stats["invalid"] += 1
                    log(f"[reconcile] 非 PDF（疑似登录页/验证页），跳过: {fn}")
                    continue
        except OSError:
            stats["invalid"] += 1
            continue
        doi = _doi_from_filename(os.path.splitext(fn)[0]) or _doi_from_pdf_text(src)
        if not doi:
            stats["no_doi"] += 1
            log(f"[reconcile] 无法提取 DOI（文件名与正文均未命中），原地保留: {fn}")
            continue
        w = by_doi.get(doi)
        if w is None:
            stats["unmatched"] += 1
            log(f"[reconcile] DOI 不在本轮 works 或已有 PDF，原地保留: {fn} ({doi})")
            continue
        # 深度校验（残篇/加密判失败 → 不归位，原地保留待人工处理）
        if _pdf_is_valid(src) is False:
            stats["invalid"] += 1
            log(f"[reconcile] PDF 深度校验失败（残篇/截断），原地保留: {fn}")
            continue
        dest = os.path.join(pdf_dir, _safe_filename(doi))  # _safe_filename 自带 .pdf 后缀
        os.replace(src, dest)  # 覆盖写入而非删除，不触发 safe-delete 钩子
        kb, pg = _pdf_meta(dest)
        w["local_pdf_path"] = dest
        w["pdf_via"] = VIA
        w["pdf_source_url"] = f"https://doi.org/{doi} (manual incoming)"
        w["pdf_size_kb"] = kb
        w["pdf_pages"] = pg
        w.pop("pdf_download_note", None)
        stats["matched"] += 1
        log(f"[reconcile] 归位成功（{VIA_LABEL}，信任级 {VIA_TRUST}）: {fn} -> {os.path.basename(dest)}")
    return stats


def reconcile_from_merged(out_dir: str, log=None) -> dict:
    """独立入口：从 <out_dir>/.merged.json 读 works → reconcile → 原子回写。

    返回 (stats, merged_path)；.merged.json 不存在返回 ({}, "")。
    """
    log = log or (lambda m: None)
    merged_path = os.path.join(out_dir, ".merged.json")
    if not os.path.isfile(merged_path):
        return {}, ""
    with open(merged_path, encoding="utf-8") as f:
        data = json.load(f)
    works = data.get("works") if isinstance(data, dict) else data
    if not isinstance(works, list):
        return {}, merged_path
    stats = reconcile_manual(out_dir, works, log=log)
    if stats.get("matched"):
        tmp = merged_path + ".reconcile.tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, merged_path)  # 原子替换
        log(f"[OK] .merged.json 已回写（{stats['matched']} 篇归位）")
    return stats, merged_path


if __name__ == "__main__":
    # 自测（纯离线，合成 PDF）。脚本直跑时 sys.path[0]=adapters/，补技能根目录入 path
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import tempfile
    _td = tempfile.mkdtemp(prefix="reconcile_t_")
    _inc = os.path.join(_td, "pdfs", "manual_incoming")
    os.makedirs(_inc, exist_ok=True)

    def _build_minimal_pdf() -> bytes:
        # 规范完整 xref（与 tests/regression_pdf_enhance._build_minimal_pdf 同款，
        # pypdf-only 环境可解析，不依赖 fitz 修复扫描）
        objs = [b"<</Type/Catalog/Pages 2 0 R>>",
                b"<</Type/Pages/Kids[3 0 R]/Count 1>>",
                b"<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]>>"]
        out = bytearray(b"%PDF-1.4\n")
        offsets = []
        for i, body in enumerate(objs, 1):
            offsets.append(len(out))
            out += b"%d 0 obj" % i + body + b"endobj\n"
        xref_pos = len(out)
        out += b"xref\n0 4\n0000000000 65535 f \n"
        for off in offsets:
            out += b"%010d 00000 n \n" % off
        out += b"trailer<</Size 4/Root 1 0 R>>\nstartxref\n%d\n%%%%EOF\n" % xref_pos
        out += b"% padding\n" * 700
        return bytes(out)

    _MIN_PDF = _build_minimal_pdf()
    # 待归位：文件名含 DOI 变体
    with open(os.path.join(_inc, "10.1038_s41586-021-03819-2.pdf"), "wb") as f:
        f.write(_MIN_PDF)
    # 非 PDF 冒充（登录页）
    with open(os.path.join(_inc, "10.9999_login.pdf"), "wb") as f:
        f.write(b"<html>login required</html>")
    works = [{"doi": "10.1038/s41586-021-03819-2", "title": "T",
              "pdf_download_note": "failed"}, {"doi": "10.9999/login", "title": "L"}]
    # ① export
    p = export_needs_manual(works, _td, log=print)
    assert p and os.path.isfile(p), "needs_manual.csv 应生成"
    txt = open(p, encoding="utf-8-sig").read()
    assert "10.1038/s41586-021-03819-2" in txt and "10.9999/login" in txt
    # 无 DOI 条目不得出现
    assert export_needs_manual(works + [{"doi": "", "title": "N"}], _td) != ""
    no_doi_txt = export_needs_manual([{"doi": "", "title": "N"}], _td)
    assert no_doi_txt == ""
    # ② reconcile
    st = reconcile_manual(_td, works, log=print)
    assert st["matched"] == 1 and st["invalid"] == 1, st
    assert works[0]["pdf_via"] == VIA and os.path.isfile(
        os.path.join(_td, "pdfs", "10.1038_s41586-021-03819-2.pdf"))
    # ③ DOI 提取变体
    assert _doi_from_filename("10.1038_s41586-021-03819-2") == "10.1038/s41586-021-03819-2"
    assert _doi_from_filename("10.1002-hbm.12345") == "10.1002/hbm.12345"
    print("manual_reconcile selftest: ALL PASSED")
    sys.exit(0)
