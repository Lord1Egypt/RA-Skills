#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
anchor_injector.py — 段落级 Block ID 锚点（升级项 G，2026-11-02）.

把已下载 PDF 的正文切成段落块，为每块注入确定性 Block ID：

    {doc_hash}:{page}-{block_index}      e.g.  3f9a1c2b7d:4-2

用途：把 evidence provenance 的溯源粒度从 **DOI 级** 下钻到 **段落级**。
CSR / 方案证据汇总时可直接定位原文段落，红点回查不必再翻整篇 PDF。

设计纪律：
  - **纯本地确定性**：不联网、不需要 key、不依赖 Coze；同一 PDF 同一参数下
    Block ID 恒定（doc_hash = 文件内容 sha1 前 10 位，与路径/时间无关）。
  - **honest degradation**：pypdf / PyMuPDF 都不可用时返回 status="unavailable"
    并说明原因，**绝不编造锚点**；扫描版 PDF（无文本层）返回 status="no_text"。
  - **只加字段不改 schema**：往 work 上挂可选的 `anchor` 块，旧消费者忽略即可。

参考来源：wenshu（文枢）anchor_injector.py 的段落锚点思路
（1559 页 PDF → 1402 锚点，5 问检索证据完整率 100%），
见 ct-update/reports/deep_read_wechat8skills_2026-11-02.md。

CLI:
    python adapters/anchor_injector.py --pdf paper.pdf                  # 单篇锚点清单
    python adapters/anchor_injector.py --in .merged.json --pdf-dir out/pdfs --out anchors.json
"""
import argparse
import hashlib
import json
import os
import re
import sys

# 段落最小字符数：低于此长度的碎片（页眉、页脚、栏目标题）不单独成块，
# 避免生成大量无检索价值的锚点。0 表示不过滤。
MIN_BLOCK_CHARS = 40
# 单文档块数上限：防止超长综述 PDF 让 JSON 爆炸（超出部分按页截断并如实记录）
MAX_BLOCKS_PER_DOC = 4000

# 进程内锚点缓存：key = (abs_path, mtime, size, min_chars, max_blocks)
_ANCHOR_CACHE = {}


def doc_hash_of(path):
    """文件内容 sha1 前 10 位——锚点跨运行稳定，与路径、时间无关。"""
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:10]


def _norm_space(s):
    s = (s or "").replace("\r\n", "\n").replace("\r", "\n")
    s = re.sub(r"[ \t\u3000]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def split_blocks(text, page=None, min_chars=MIN_BLOCK_CHARS):
    """把一页正文切成段落块（纯 stdlib，无依赖）。

    切分规则：连续空行 → 段边界；单换行视为段内折行（PDF 排版常见）。
    过短碎片（< min_chars）并入上一块，而不是丢弃——丢弃会让锚点覆盖出现空洞。
    """
    text = _norm_space(text)
    if not text:
        return []
    raw = [p for p in re.split(r"\n\s*\n", text)]
    merged = []
    for p in raw:
        p = _norm_space(p)
        if not p:
            continue
        if merged and (len(p) < min_chars):
            merged[-1] = merged[-1] + " " + p
        else:
            merged.append(p)
    # 整页只有一行超长文本（无空行）时，按句子边界再切一次，避免"整页一块"
    if len(merged) == 1 and len(merged[0]) > 4 * max(min_chars, 1):
        merged = [s.strip() for s in re.split(r"(?<=[.。！？!?;；])\s+", merged[0]) if s.strip()]
    out = []
    for i, p in enumerate(merged):
        out.append({
            "block_id": "%s:%s-%d" % (page if page is not None else "?", page, i),
            "page": page,
            "block_index": i,
            "text": p,
        })
    return out


def extract_pages(pdf_path):
    """抽取 [(page_no, text)]。pypdf 优先，PyMuPDF 备选。

    Returns (pages, status) where status ∈ {"ok", "unavailable", "error", "no_text"}.
    """
    if not os.path.isfile(pdf_path):
        return [], "error"
    try:
        import pypdf  # noqa: F401
    except Exception:
        pypdf = None
    if pypdf is not None:
        try:
            pages = []
            with open(pdf_path, "rb") as f:
                reader = pypdf.PdfReader(f)
                for i, pg in enumerate(reader.pages, start=1):
                    try:
                        pages.append((i, pg.extract_text() or ""))
                    except Exception:
                        pages.append((i, ""))
            return pages, ("ok" if any(t.strip() for _, t in pages) else "no_text")
        except Exception:
            pass  # 落到 fitz
    try:
        import fitz
    except Exception:
        return [], "unavailable"
    try:
        pages = []
        with fitz.open(pdf_path) as doc:
            for i, pg in enumerate(doc, start=1):
                pages.append((i, pg.get_text() or ""))
        return pages, ("ok" if any(t.strip() for _, t in pages) else "no_text")
    except Exception as e:
        return [], "error:%s" % type(e).__name__


def build_anchors(pdf_path, min_chars=MIN_BLOCK_CHARS, max_blocks=MAX_BLOCKS_PER_DOC):
    """为单个 PDF 生成锚点结构（确定性、纯本地）。

    进程内缓存：同一文件（按 path+mtime+size 指纹）只解析一次。_finalize 可能被调用
    两次（preview + verified 刷新），没有缓存会让 PDF 抽取白白翻倍。
    """
    try:
        st = os.stat(pdf_path)
        _ck = (os.path.abspath(pdf_path), int(st.st_mtime), st.st_size, min_chars, max_blocks)
    except OSError:
        _ck = None
    if _ck is not None and _ck in _ANCHOR_CACHE:
        return _ANCHOR_CACHE[_ck]
    res = _build_anchors_uncached(pdf_path, min_chars, max_blocks)
    if _ck is not None:
        _ANCHOR_CACHE[_ck] = res
    return res


def _build_anchors_uncached(pdf_path, min_chars=MIN_BLOCK_CHARS, max_blocks=MAX_BLOCKS_PER_DOC):
    dh = doc_hash_of(pdf_path)
    pages, status = extract_pages(pdf_path)
    if status != "ok":
        return {
            "doc_hash": dh,
            "file": os.path.basename(pdf_path),
            "status": status,
            "page_count": len(pages),
            "block_count": 0,
            "blocks": [],
        }
    blocks = []
    for pno, text in pages:
        for b in split_blocks(text, page=pno, min_chars=min_chars):
            b["block_id"] = "%s:%s-%d" % (dh, pno, b["block_index"])
            blocks.append(b)
            if len(blocks) >= max_blocks:
                break
        if len(blocks) >= max_blocks:
            break
    return {
        "doc_hash": dh,
        "file": os.path.basename(pdf_path),
        "status": "ok",
        "page_count": len(pages),
        "block_count": len(blocks),
        "truncated": len(blocks) >= max_blocks,
        "blocks": blocks,
    }


def find_pdf_for_work(work, pdf_dir):
    """定位 work 对应的本地 PDF：优先 local_pdf_path，其次 DOI / 标题 slug 模糊匹配。"""
    p = work.get("local_pdf_path")
    if p and os.path.isfile(p):
        return p
    if not pdf_dir or not os.path.isdir(pdf_dir):
        return None
    doi = (work.get("doi") or "").strip().lower()
    if doi:
        slug = re.sub(r"[^a-z0-9]+", "_", doi)
        for fn in os.listdir(pdf_dir):
            if not fn.lower().endswith(".pdf"):
                continue
            norm = re.sub(r"[^a-z0-9]+", "_", fn.lower())
            if slug and slug in norm:
                return os.path.join(pdf_dir, fn)
    title = (work.get("title") or "").strip()
    if len(title) >= 20:
        head = re.sub(r"[^a-z0-9]+", "_", title.lower())[:40]
        for fn in os.listdir(pdf_dir):
            if fn.lower().endswith(".pdf") and head and head[:24] in re.sub(
                    r"[^a-z0-9]+", "_", fn.lower()):
                return os.path.join(pdf_dir, fn)
    return None


def attach(works, pdf_dir=None, min_chars=MIN_BLOCK_CHARS, progress=None):
    """给每个 work 挂 `anchor` 块 + `provenance` 段落级溯源字段。

    每个 work 的 anchor 只存**轻量指针 + 前若干块摘要**；完整块表落
    anchors.json（避免 .merged.json 膨胀成几十 MB）。
    """
    stats = {"total": len(works), "anchored": 0, "pdf_missing": 0,
             "unavailable": 0, "no_text": 0, "blocks": 0}
    for w in works:
        if not isinstance(w, dict):
            continue
        pdf = find_pdf_for_work(w, pdf_dir)
        if not pdf:
            stats["pdf_missing"] += 1
            w["anchor"] = {"status": "pdf_missing"}
            continue
        a = build_anchors(pdf, min_chars=min_chars)
        st = a.get("status")
        if st == "ok":
            stats["anchored"] += 1
            stats["blocks"] += a["block_count"]
            w["anchor"] = {
                "status": "ok",
                "doc_hash": a["doc_hash"],
                "file": a["file"],
                "page_count": a["page_count"],
                "block_count": a["block_count"],
                "blocks_preview": [
                    {"block_id": b["block_id"], "page": b["page"],
                     "quote_excerpt": b["text"][:160]}
                    for b in a["blocks"][:3]
                ],
            }
            # provenance：DOI 级 → 段落级（第一块作为默认锚点，供报告/CSR 引用回查）
            if a["blocks"]:
                b0 = a["blocks"][0]
                w["provenance"] = {
                    "doi": w.get("doi"),
                    "title": w.get("title"),
                    "block_id": b0["block_id"],
                    "page": b0["page"],
                    "quote_excerpt": b0["text"][:240],
                }
        elif st == "no_text":
            stats["no_text"] += 1
            w["anchor"] = {"status": "no_text", "doc_hash": a["doc_hash"],
                           "file": a["file"], "note": "扫描版/无文本层，需 OCR 才有锚点"}
        else:
            stats["unavailable"] += 1
            w["anchor"] = {"status": st, "file": a.get("file")}
        if progress:
            progress("anchored %s -> %s" % (w.get("doi") or w.get("title"), st))
    return stats


def provenance_of(work, block_id=None):
    """构造 ct-base §17.1 溯源记录：{doi, title, block_id, page, quote_excerpt}。"""
    a = work.get("anchor") or {}
    pv = dict(work.get("provenance") or {})
    pv.setdefault("doi", work.get("doi"))
    pv.setdefault("title", work.get("title"))
    if block_id:
        pv["block_id"] = block_id
    elif a.get("blocks_preview"):
        pv.setdefault("block_id", a["blocks_preview"][0]["block_id"])
    pv.setdefault("doc_hash", a.get("doc_hash"))
    return pv


def main():
    ap = argparse.ArgumentParser(
        description="Inject paragraph-level Block ID anchors into local PDFs (pure local).")
    ap.add_argument("--pdf", help="single PDF -> print anchor JSON")
    ap.add_argument("--in", dest="inp", help=".merged.json to annotate")
    ap.add_argument("--pdf-dir", dest="pdf_dir", default=None, help="PDF directory")
    ap.add_argument("--out", default=None, help="write annotated JSON / anchor index")
    ap.add_argument("--min-chars", dest="min_chars", type=int, default=MIN_BLOCK_CHARS)
    args = ap.parse_args()

    if args.pdf:
        res = build_anchors(args.pdf, min_chars=args.min_chars)
        head = {k: v for k, v in res.items() if k != "blocks"}
        head["blocks"] = res["blocks"][:20]
        txt = json.dumps(head, ensure_ascii=False, indent=2)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(txt)
            print("[OK] anchors -> %s (%d blocks)" % (args.out, res["block_count"]))
        else:
            print(txt)
        return 0

    if not args.inp:
        ap.error("--pdf 或 --in 至少给一个")
    with open(args.inp, "r", encoding="utf-8") as f:
        data = json.load(f)
    works = data.get("works") if isinstance(data, dict) else data
    if not isinstance(works, list):
        print("[ERROR] 输入 JSON 无 works 列表", file=sys.stderr)
        return 2
    pdf_dir = args.pdf_dir or os.path.join(os.path.dirname(os.path.abspath(args.inp)), "pdfs")
    stats = attach(works, pdf_dir=pdf_dir, min_chars=args.min_chars,
                   progress=lambda m: print("[anchor] " + m, file=sys.stderr))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    print("[OK] anchored=%d/%d blocks=%d pdf_missing=%d no_text=%d unavailable=%d" % (
        stats["anchored"], stats["total"], stats["blocks"],
        stats["pdf_missing"], stats["no_text"], stats["unavailable"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
