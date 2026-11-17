#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tag_semantic_search.py

标签语义召回（确定性版·零依赖）：TF-IDF 字符 n-gram(1~3) + 余弦相似度。

确定性保证（同输入同输出，字符串级一致到小数点后6位）：
1. 特征选择：sorted(df.items(), key=lambda x: (-x[1], x[0])) 固定tie-break
2. 最终排序：key=(-similarity, tagId) tagId作为稳定tie-break
3. 文本归一化：统一_normalize()函数，固定正则规则
4. 浮点输出：所有similarity统一round(sim, 6)
5. tag_pool版本化：可选输出tag_pool_hash，同一hash下结果完全可复现

召回率提升：
1. 多路query合并（取max similarity）
2. 两段式召回：高精阶段(cosine) + 兜底阶段(关键词精确命中boost)
3. 核心词命中boost：Schema解析出的核心词命中时加固定小增益(+0.02~0.05，确定性)

输入：
- tags.json：标签池（query_tag_list.py输出，建议已过滤isDirectory=1）
- --query/--query-file：查询文本
- --boost-words：核心词列表(逗号分隔)，命中时加固定增益

输出：
- candidates.json：候选标签列表
  - tagId, tagName, parentId, tagType, isDirectory, similarity(round6)
"""

import argparse
import hashlib
import json
import math
import re
from collections import Counter
from typing import List, Dict, Tuple


# ============================================================
# 文本归一化（唯一入口，禁止在其他地方重复写清洗逻辑）
# ============================================================
_NORMALIZE_RE = re.compile(r'[^\u4e00-\u9fff\w\-]')

def _normalize(text: str) -> str:
    """统一文本归一化：去空白→转小写→只保留中文/字母/数字/下划线"""
    if not text:
        return ""
    text = text.strip().lower()
    text = _NORMALIZE_RE.sub('', text)
    return text


def _char_ngrams(text: str, ngram_range: Tuple[int, int] = (1, 3)) -> List[str]:
    """提取字符n-gram（中文友好，按字符切分）"""
    text = _normalize(text)
    if not text:
        return []
    grams = []
    for n in range(ngram_range[0], ngram_range[1] + 1):
        if len(text) < n:
            grams.append(text)
        else:
            grams.extend(text[i:i + n] for i in range(len(text) - n + 1))
    return grams


def _enhance_text(t: Dict) -> str:
    """增强文本：标签名 + 来源类型，提升来源区分度"""
    name = t.get("tagName") or ""
    tt = t.get("tagType")
    typ = "明略标签" if tt == 1 else "合作伙伴标签" if tt == 3 else ""
    return (_normalize(name) + " " + typ).strip()


# ============================================================
# TF-IDF 训练与查询（确定性版）
# ============================================================
def _fit_tfidf(texts: List[str], ngram_range=(1, 3), max_features=5000):
    """训练TF-IDF模型（特征选择确定性排序）"""
    df = Counter()
    tf_list = []
    for text in texts:
        grams = _char_ngrams(text, ngram_range)
        tf = Counter(grams)
        tf_list.append(tf)
        for g in set(grams):
            df[g] += 1

    N = len(texts)

    # 【C1-1修复】稳定特征选择：按df降序→gram字典序升序，消除Counter.most_common()并列不稳定
    if len(df) > max_features:
        sorted_grams = sorted(df.items(), key=lambda x: (-x[1], x[0]))
        top_grams = {g for g, _ in sorted_grams[:max_features]}
    else:
        sorted_grams = sorted(df.items(), key=lambda x: (-x[1], x[0]))
        top_grams = set(df.keys())

    # 计算tf-idf向量和L2范数
    vectors = []
    norms = []
    for tf in tf_list:
        vec = {}
        norm_sq = 0.0
        for g, tf_val in tf.items():
            if g not in top_grams:
                continue
            idf = math.log((N + 1) / (df[g] + 1)) + 1  # smoothed idf (sklearn风格)
            w = tf_val * idf
            vec[g] = w
            norm_sq += w * w
        vectors.append(vec)
        norms.append(math.sqrt(norm_sq))

    return df, top_grams, vectors, norms, N


def _transform_query(query: str, df: Counter, top_grams: set, N: int, ngram_range=(1, 3)):
    """将查询文本转为TF-IDF向量"""
    grams = _char_ngrams(query, ngram_range)
    tf = Counter(grams)
    vec = {}
    norm_sq = 0.0
    for g, tf_val in tf.items():
        if g not in top_grams:
            continue
        idf = math.log((N + 1) / (df.get(g, 0) + 1)) + 1
        w = tf_val * idf
        vec[g] = w
        norm_sq += w * w
    norm = math.sqrt(norm_sq)
    return vec, norm


def _cosine_similarity(v1: Dict[str, float], norm1: float, v2: Dict[str, float], norm2: float) -> float:
    """稀疏向量余弦相似度"""
    if norm1 == 0 or norm2 == 0:
        return 0.0
    if len(v1) > len(v2):
        v1, v2 = v2, v1
    dot = 0.0
    for g, w in v1.items():
        dot += w * v2.get(g, 0.0)
    return dot / (norm1 * norm2)


# ============================================================
# 标签池哈希（版本化）
# ============================================================
def _hash_tag_pool(tags: List[Dict]) -> str:
    """计算标签池内容hash，用于版本化：同一hash=同一标签池=结果可复现"""
    # 只取tagId和tagName（决定ngram的字段），按tagId排序
    simplified = sorted(
        [(str(t.get("tagId","")), _normalize(t.get("tagName",""))) for t in tags],
        key=lambda x: x[0]
    )
    raw = json.dumps(simplified, ensure_ascii=False, sort_keys=True)
    return hashlib.md5(raw.encode("utf-8")).hexdigest()[:12]


# ============================================================
# 主流程
# ============================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tags", required=True, help="tags.json路径")
    ap.add_argument("--query", default=None, help="查询文本（多query用|分隔）")
    ap.add_argument("--query-file", default=None, help="查询文件（每行一个query）")
    ap.add_argument("--boost-words", default="",
                    help="核心词(逗号分隔)，标签名包含核心词时加固定增益+BOOST_VALUE")
    ap.add_argument("--boost-words-json", default=None,
                    help="从build_queries.py输出的JSON文件中读取boost_words（优先级高于--boost-words）")
    ap.add_argument("--boost-value", type=float, default=0.03,
                    help="核心词增益值，默认0.03（建议0.02~0.05，不超过0.1）")
    ap.add_argument("--top-k", type=int, default=60)
    ap.add_argument("--threshold", type=float, default=0.05, help="相似度阈值，默认0.05")
    ap.add_argument("--ngram-range", default="1,3", help="n-gram范围，默认1,3 (char 1~3gram)")
    ap.add_argument("--max-features", type=int, default=5000, help="TF-IDF最大特征数，默认5000")
    ap.add_argument("--out", required=True, help="输出candidates.json")
    args = ap.parse_args()

    # 解析n-gram范围
    ngram_parts = args.ngram_range.split(",")
    ngram_range = (int(ngram_parts[0]), int(ngram_parts[1]))

    # 读取queries
    if not args.query and not args.query_file:
        raise SystemExit("必须提供 --query 或 --query-file")
    queries = []
    if args.query_file:
        with open(args.query_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
        # 支持两种格式：build_queries.py输出的JSON，或纯文本（每行一个query）
        if content.startswith("{"):
            qj = json.loads(content)
            queries = qj.get("queries", [])
        else:
            queries = [line.strip() for line in content.split("\n") if line.strip() and not line.startswith("#")]
    if args.query:
        queries.extend([q.strip() for q in args.query.split("|") if q.strip()])
    if not queries:
        raise SystemExit("查询文本为空")

    # 统一归一化query（避免query里的空白/标点导致差异）
    queries = [_normalize(q) for q in queries]

    # 读取boost words
    boost_words = []
    if args.boost_words_json:
        with open(args.boost_words_json, "r", encoding="utf-8") as f:
            bj = json.load(f)
        boost_words = [_normalize(w) for w in bj.get("boost_words", []) if w.strip()]
    elif args.boost_words:
        boost_words = [_normalize(w) for w in args.boost_words.split(",") if w.strip()]
    boost_val = max(0.0, min(args.boost_value, 0.1))  # 限幅0~0.1

    # 读取标签池
    with open(args.tags, "r", encoding="utf-8") as f:
        tags: List[Dict] = json.load(f)

    tag_pool_hash = _hash_tag_pool(tags)
    texts = [_enhance_text(t) for t in tags]

    # 训练TF-IDF
    df, top_grams, doc_vectors, doc_norms, N = _fit_tfidf(
        texts, ngram_range=ngram_range, max_features=args.max_features
    )

    # 多路query检索，合并取max score
    merged: Dict[int, float] = {}  # tag_idx -> best cosine score
    for q in queries:
        q_vec, q_norm = _transform_query(q, df, top_grams, N, ngram_range=ngram_range)
        if q_norm == 0:
            continue
        for i in range(len(tags)):
            sim = _cosine_similarity(q_vec, q_norm, doc_vectors[i], doc_norms[i])
            if sim > merged.get(i, 0):
                merged[i] = sim

    # 【D修复】关键词boost：标签名归一化后包含boost_words中任意词，加固定增益（确定性）
    if boost_words:
        for i in range(len(tags)):
            name_norm = _normalize(tags[i].get("tagName", ""))
            hit = any(bw in name_norm for bw in boost_words if bw)
            if hit:
                base = merged.get(i, 0.0)
                merged[i] = min(1.0, base + boost_val)

    # 【C1-2修复】稳定排序：按sim降序→tagId升序（tagId保证同分标签顺序永远一致）
    sorted_indices = sorted(merged.keys(), key=lambda i: (-merged[i], int(tags[i].get("tagId", 0))))

    # 构建输出
    out = []
    for i in sorted_indices:
        s = merged[i]
        if s < args.threshold:
            continue
        t = tags[i]
        out.append({
            "tagId": t.get("tagId"),
            "tagName": t.get("tagName"),
            "parentId": t.get("parentId"),
            "tagType": t.get("tagType"),
            "isDirectory": t.get("isDirectory"),
            "similarity": round(s, 6),  # 【C2修复】固定round6
        })
        if len(out) >= args.top_k:
            break

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    meta = {
        "ok": True,
        "queries": queries,
        "boost_words": boost_words,
        "boost_value": boost_val,
        "tag_pool_hash": tag_pool_hash,
        "ngram_range": list(ngram_range),
        "max_features": args.max_features,
        "total_tags": len(tags),
        "returned": len(out),
        "out": args.out,
    }
    print(json.dumps(meta, ensure_ascii=False))


if __name__ == "__main__":
    main()
