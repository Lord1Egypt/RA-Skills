#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""条款对齐（阶段③核心）。

为什么需要它：招标文档常见「一章内多台设备各自 1/2/3 编号」的结构，
提取器产出的浅层 ID（如 七.5）会把「设备A的第5条」与「设备B的第5条」
混为同一 ID，导致 stage3 按 ID 对齐时大面积假阳性（同 ID 下内容完全不同）。

本脚本以「内容相似度」为**首选对齐方式**，ID 仅作辅助兜底：
  1) 先用归一化(去空白)文本做精确匹配（抓重复/仅空白差异）；
  2) 未匹配项用字符二元组 Jaccard 相似度做贪心最佳匹配；
  3) 低于阈值的 A 项 -> 删除，B 项 -> 新增；
  4) 高于阈值但非精确的 -> 修改。
输出 <changes.json>，供阶段④/⑤/报告消费。
"""
import argparse
import json
import re
import sys
from collections import Counter

# 用于相似度计算的标点集合（全角+半角），归一化时一并剔除，
# 以减少「仅标点/换气差异」造成的伪修改。
_PUNCT = set("，。、；：！？“”‘’（）()【】《》<>「」『』…·—–-./\\%,%￥$#@&*+=|:;\"' \t\n\r")


def norm_ws(t):
    """仅去空白，用于精确匹配。"""
    return re.sub(r"\s+", "", t or "")


def norm_punct(t):
    """去空白 + 去标点，用于相似度计算。"""
    s = re.sub(r"\s+", "", t or "")
    return "".join(ch for ch in s if ch not in _PUNCT)


def _bigrams(s):
    s = s.lower()
    if len(s) < 2:
        return {s}
    return {s[i:i + 2] for i in range(len(s) - 1)}


def similarity(a, b):
    """字符二元组 Jaccard 相似度，基于去标点归一化文本。"""
    a, b = norm_punct(a), norm_punct(b)
    if not a or not b:
        return 0.0
    ga, gb = _bigrams(a), _bigrams(b)
    union = ga | gb
    return len(ga & gb) / len(union) if union else 0.0


_NUM_RE = re.compile(r"\d+(?:\.\d+)?")

def _numbers(t):
    """提取文本中所有数值（含小数），用于数值变更检测。"""
    return re.findall(_NUM_RE, t or "")


def _strip_num_punct(t):
    """去除数字与标点，仅留文字，用于检测「关键词替换」类变更
    （如 彩超 → 自动发药机，数值不变但名词被替换）。"""
    s = re.sub(r"\s+", "", t or "")
    s = re.sub(r"\d+", "", s)
    return "".join(ch for ch in s if ch not in _PUNCT)


def _numeric_delta(a, b):
    """若 A/B 数值集合不同，返回可读的数值变更摘要；否则空串。

    用于在「高相似但非精确」的配对里找回被 0.95 阈值漏杀的
    小幅数值变更（如 23L/步 → 25L/步 仅改两字，整体相似度仍 ~0.97）。"""
    na, nb = _numbers(a), _numbers(b)
    if na == nb:
        return ""
    ca, cb = Counter(na), Counter(nb)
    parts = []
    for num in sorted(set(na) | set(nb)):
        if ca[num] != cb[num]:
            parts.append(f"{num}: {ca[num]}处→{cb[num]}处")
    return "数值变更 | " + "; ".join(parts)


MODIFY_LOW = 0.50      # 相似度低于此 -> 不视为同一条款（删除/新增）
UNCHANGED_HIGH = 0.95  # 相似度高于此 -> 默认视为未变更，但需二次核验


def align(a_clauses, b_clauses, modify_low=MODIFY_LOW, unchanged_high=UNCHANGED_HIGH):
    a_text = [c.get("text", "") for c in a_clauses]
    b_text = [c.get("text", "") for c in b_clauses]

    used_b = [False] * len(b_clauses)
    paired_ai = {}      # ai -> (bi, sim)
    matched_bi = set()

    # Pass 1: 精确匹配（去空白后完全一致 -> 未变更，跳过）
    b_by_key = {}
    for bi, t in enumerate(b_text):
        k = norm_ws(t)
        if k:
            b_by_key.setdefault(k, []).append(bi)
    for ai, t in enumerate(a_text):
        k = norm_ws(t)
        if not k:
            continue
        for bi in b_by_key.get(k, []):
            if not used_b[bi]:
                used_b[bi] = True
                matched_bi.add(bi)
                paired_ai[ai] = (bi, 1.0)
                break

    # Pass 2: 贪心相似度匹配剩余项
    for ai, t in enumerate(a_text):
        if ai in paired_ai:
            continue
        best_bi, best_sim = -1, -1.0
        for bi in range(len(b_text)):
            if used_b[bi]:
                continue
            s = similarity(t, b_text[bi])
            if s > best_sim:
                best_sim, best_bi = s, bi
        if best_bi >= 0 and best_sim >= modify_low:
            used_b[best_bi] = True
            matched_bi.add(best_bi)
            paired_ai[ai] = (best_bi, best_sim)

    modified, added, deleted = [], [], []
    for ai, (bi, sim) in paired_ai.items():
        a = a_clauses[ai]
        b = b_clauses[bi]
        at, bt = a.get("text", ""), b.get("text", "")
        # 完全精确匹配（Pass 1 已置 sim=1.0）-> 确属未变更，跳过
        if sim >= 1.0:
            continue
        # 高相似但非精确：长条款里极易藏有小幅但实质的变更
        # （数值微调、关键词替换），单纯 0.95 阈值会一刀切漏杀。
        # 故在此做二次核验：仅当「数值无变化」且「去数字标点后文字一致」
        # 时才视为未变更跳过；否则判为修改。
        if sim >= unchanged_high:
            nd = _numeric_delta(at, bt)
            word_changed = _strip_num_punct(at) != _strip_num_punct(bt)
            if not nd and not word_changed:
                continue  # 仅标点/空白/格式差异 -> 视为未变更
        modified.append({
            "clause_id": a.get("id", f"a{ai}"),
            "change_type": "修改",
            "old_text": at,
            "new_text": bt,
            "numeric_delta": _numeric_delta(at, bt),
            "context": a.get("context", ""),
            "sim": round(sim, 3),
        })
    for bi in range(len(b_clauses)):
        if bi not in matched_bi:
            b = b_clauses[bi]
            added.append({
                "clause_id": b.get("id", f"b{bi}"),
                "change_type": "新增",
                "old_text": "",
                "new_text": b.get("text", ""),
                "numeric_delta": "",
                "context": b.get("context", ""),
                "sim": 0.0,
            })
    for ai in range(len(a_clauses)):
        if ai not in paired_ai:
            a = a_clauses[ai]
            deleted.append({
                "clause_id": a.get("id", f"a{ai}"),
                "change_type": "删除",
                "old_text": a.get("text", ""),
                "new_text": "",
                "numeric_delta": "",
                "context": a.get("context", ""),
                "sim": 0.0,
            })

    return modified, added, deleted


def _load_doc(path):
    d = json.load(open(path, encoding="utf-8"))
    if isinstance(d, dict) and "documents" in d:
        return d["documents"]
    if isinstance(d, list):
        return d
    raise ValueError("无法识别的提取 JSON 结构")


def main():
    ap = argparse.ArgumentParser(description="条款内容相似度对齐")
    ap.add_argument("--extracted", required=True, help="extract_documents.py 输出 JSON")
    ap.add_argument("--out", required=True, help="对齐结果 JSON 输出路径")
    ap.add_argument("--modify-low", type=float, default=MODIFY_LOW)
    ap.add_argument("--unchanged-high", type=float, default=UNCHANGED_HIGH)
    args = ap.parse_args()

    docs = _load_doc(args.extracted)
    if len(docs) < 2:
        sys.stderr.write("错误：提取 JSON 需包含至少两份文档\n")
        sys.exit(2)

    a = docs[0]["clauses"]
    b = docs[1]["clauses"]
    modified, added, deleted = align(a, b, args.modify_low, args.unchanged_high)

    out = {
        "old_file": docs[0]["meta"].get("file", "A"),
        "new_file": docs[1]["meta"].get("file", "B"),
        "summary": {
            "A_clauses": len(a),
            "B_clauses": len(b),
            "modified": len(modified),
            "added": len(added),
            "deleted": len(deleted),
            "total_changes": len(modified) + len(added) + len(deleted),
            "alignment": "content-similarity (primary) + ID fallback",
        },
        "modified": modified,
        "added": added,
        "deleted": deleted,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"已对齐：修改 {len(modified)} / 新增 {len(added)} / 删除 {len(deleted)} "
          f"（合计 {out['summary']['total_changes']} 处变更）")


if __name__ == "__main__":
    main()
