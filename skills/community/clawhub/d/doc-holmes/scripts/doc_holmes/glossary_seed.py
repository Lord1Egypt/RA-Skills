#!/usr/bin/env python3
"""加密 PDF 解密 + 术语自适应种子（v2.10.0）。

qpdf --decrypt 解密密码保护 PDF 后走现有管线。
术语自适应种子：从源 PDF 抽取高频术语 → 用户自配端点 LLM 翻译 → 写 CSV
注入引擎 --glossaries。协议铁律：**先翻译后写表，空/缺失翻译的术语绝不入表**
（v2.8.0 事故：空 target 行 "term,,zh" 令引擎 glossary 加载崩溃，功能整体下线）。
"""

from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import urllib.request
from collections import Counter


def needs_decrypt(pdf_path: str) -> bool:
    import pymupdf
    try:
        doc = pymupdf.open(pdf_path)
        encrypted = doc.needs_pass
        doc.close()
        return encrypted
    except Exception:
        return False


def decrypt_pdf(pdf_path: str, password: str, outdir: str) -> str:
    """qpdf --decrypt 解密 PDF。返回解密后路径。"""
    qpdf = shutil_which("qpdf")
    if not qpdf:
        raise RuntimeError(
            "qpdf 未安装。解密密码保护 PDF 需要 qpdf：\n"
            "  · Debian/Ubuntu：apt install qpdf\n"
            "  · 或提供已解密的 PDF 文件。")
    os.makedirs(outdir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(pdf_path))[0]
    out_path = os.path.join(outdir, stem + "_decrypted.pdf")
    cmd = [qpdf, "--password", password, "--decrypt", pdf_path, out_path]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if proc.returncode != 0:
        raise RuntimeError("qpdf 解密失败（rc=%d）：%s"
                           % (proc.returncode, (proc.stderr or "")[-200:]))
    return out_path


def shutil_which(name):
    from shutil import which
    return which(name)


# ===== 术语自适应种子（v2.10.0）=====

# 通用英文停用词（简化版，仅覆盖高频功能词）
_STOP = {"the", "and", "for", "are", "but", "not", "you", "all", "any", "can",
         "her", "was", "one", "our", "out", "day", "get", "has", "him", "his",
         "how", "its", "new", "now", "old", "see", "two", "way", "who", "did",
         "each", "that", "this", "with", "from", "they", "have", "been", "were",
         "their", "which", "will", "would", "about", "there", "these", "other",
         "could", "than", "then", "them", "more", "when", "what", "into", "time",
         "only", "over", "such", "most", "also", "may", "should", "after",
         "between", "through", "our", "these", "some", "than", "then", "well",
         # URL/网页碎片（实测种子产物混入 https 等，对翻译无意义）
         "https", "http", "www", "com", "org", "net", "cn", "html", "web"}

_SEED_PROMPT_HEAD = (
    "You are a medical/technical translator. Translate English terms to "
    "Chinese. Output one term per line in exactly this format: term=translation. "
    "No extra text, no numbering. Keep established abbreviations (e.g. MRI, "
    "PD-L1) as-is in the translation when standard.")


def extract_domain_terms(text: str, min_len: int = 5, top_n: int = 20) -> list:
    """从源 PDF 文本提取高频领域术语（≥min_len 字母、非停用词、按频次排序）。"""
    words = re.findall(r"[a-zA-Z]{%d,}" % min_len, text)
    stop = {w.lower() for w in _STOP}
    terms = Counter(
        w for w in words
        if w.lower() not in stop and not w.isupper() and len(w) >= min_len)
    return [term for term, _ in terms.most_common(top_n)]


def _load_builtin_sources(built_in_path: str) -> dict:
    """读内置表 → {lower(source): (source, target)}；坏行跳过，空 target 跳过。"""
    table = {}
    if built_in_path and os.path.isfile(built_in_path):
        try:
            with open(built_in_path, encoding="utf-8-sig") as f:
                for row in csv.DictReader(f):
                    src = (row.get("source") or "").strip()
                    tgt = (row.get("target") or "").strip()
                    if src and tgt:
                        table[src.lower()] = (src, tgt)
        except Exception:
            return {}
    return table


def seed_glossary(pdf_path: str, built_in_path: str, out_dir: str, *,
                  translate_fn, top_n: int = 12, min_len: int = 5,
                  sample_pages: int = 5) -> dict:
    """文档术语自适应种子：抽取 → translate_fn 翻译 → 写 CSV（永不空 target）。

    translate_fn(terms: list[str]) -> dict {term: translation}；
    返回字典缺失的术语/空翻译一律不写表（v2.8.0 空 target 崩溃的机制层根治）。
    异常向上抛（接线层决定降级），本函数不吞。
    返回 {"path": csv|None, "seeded": [...], "candidates": n, "builtin_covered": n}
    """
    import pymupdf
    doc = pymupdf.open(pdf_path)
    text = " ".join(doc[i].get_text() for i in range(min(doc.page_count,
                                                         sample_pages)))
    doc.close()
    extracted = extract_domain_terms(text, min_len=min_len, top_n=top_n)
    builtin = _load_builtin_sources(built_in_path)
    todo, covered = [], 0
    for term in extracted:
        if term.lower() in builtin:
            covered += 1
        else:
            todo.append(term)
    info = {"path": None, "seeded": [], "candidates": len(extracted),
            "builtin_covered": covered}
    if not todo:
        return info
    translated = translate_fn(todo) or {}
    rows = []
    for term in todo:
        tgt = (translated.get(term) or "").strip()
        if not tgt:
            continue
        if tgt.lower() == term.lower():
            continue          # 恒等映射（如 https）不注入——对术语一致性无意义
        rows.append((term, tgt, "zh"))
    if not rows:
        return info
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.abspath(os.path.join(out_dir, "seeded_glossary.csv"))
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")   # \n 行尾对齐内置表（引擎解析器实测 \r\n 有挂死风险）
        w.writerow(["source", "target", "tgt_lng"])
        w.writerows(rows)
    info["path"] = out_path
    info["seeded"] = [r[0] for r in rows]
    return info


def translate_terms_llm(terms: list, base_url: str, api_key: str, model: str,
                        timeout: int = 60) -> dict:
    """批量翻译术语（一次小请求）。返回 {原样术语: 译文}。

    协议：每行 term=translation；无法对回请求集的行、空译文、截断（
    finish_reason=length）均不产出该术语。术语表很小（默认 ≤12 条），
    prompt 固定长度，不构成大文档巨型提示超时风险。
    """
    user_text = "Terms:\n" + "\n".join(terms)
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": _SEED_PROMPT_HEAD},
            {"role": "user", "content": user_text},
        ],
        "temperature": 0,
        "max_tokens": max(512, 160 * len(terms)),
    }, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions", data=body, method="POST",
        headers={"Authorization": "Bearer " + api_key,
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        d = json.loads(resp.read().decode("utf-8", "ignore"))
    choice = d["choices"][0]
    if choice.get("finish_reason") == "length":
        raise ValueError("LLM 输出被截断（finish_reason=length），种子放弃")
    wanted = {t.lower(): t for t in terms}
    out = {}
    for line in (choice["message"]["content"] or "").splitlines():
        line = line.strip().lstrip("-•* ").strip()
        if "=" not in line:
            continue
        src, _, tgt = line.partition("=")
        # LLM 常见格式清洗：编号前缀（"1. term"）、译文包裹（**译文**、`译文`）
        src = re.sub(r"^\d+[.、)]\s*", "", src.strip()).strip()
        tgt = tgt.strip().strip("*`_").strip()
        key = wanted.get(src.lower())
        if key and tgt:
            out.setdefault(key, tgt)
    return out
