#!/usr/bin/env python3
"""
DigitalSalesClaw - knowledge_qa.py
医药知识库RAG问答
基于合规规则库 + 法规知识域 + LLM推理

增强版: jieba 语义分词 + TF-IDF 检索

输入: {"question": "阿莫西林能和布洛芬一起吃吗？", "top_k": 5}
输出: {"answer, sources, related_questions, confidence}
"""

import sys
import json
import re
import math
from pathlib import Path
from datetime import datetime
from db import get_conn, close_conn

try:
    import jieba
    import jieba.analyse
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False

SKILL_DIR = Path(__file__).parent.parent
KNOWLEDGE_DIR = SKILL_DIR / "knowledge"


# ─────────────────────────────────────────
# 法规知识库（内嵌基础版）
# ─────────────────────────────────────────
PHARMA_KNOWLEDGE = {
    "药品管理法": {
        "key_points": [
            "药品上市许可持有人对药品质量负责",
            "禁止生产、销售假药、劣药",
            "处方药不得在大众传播媒介发布广告",
            "药品广告须经省级药监部门批准",
        ]
    },
    "广告法": {
        "medical_ad": [
            "医疗、药品、医疗器械广告不得含有：",
            "- 表示功效、安全性的断言或保证",
            "- 说明治愈率或有效率",
            "- 与其他药品、医疗器械比较",
            "- 利用代言人推荐",
            "药品广告内容须与说明书一致",
        ]
    },
    "处方药": {
        "promotion_rules": [
            "处方药只能在医学、药学专业刊物上发布广告",
            "禁止在大众媒体投放处方药广告",
            "禁止向公众进行处方药推广",
        ]
    },
    "合规红线": {
        "banned_expressions": [
            "最佳", "第一", "顶级", "极品", "国家级",
            "根治", "治愈", "药到病除", "无效退款",
            "保证治愈", "完全治愈", "彻底治愈",
            "神药", "万能", "包治百病",
        ]
    }
}


# ─────────────────────────────────────────
# jieba 分词 + TF-IDF 检索
# ─────────────────────────────────────────

def tokenize(text: str) -> list[str]:
    """使用 jieba 分词"""
    if JIEBA_AVAILABLE:
        return list(jieba.cut(text))
    # fallback: 简单字符分割
    return list(text)


def extract_keywords(text: str, topK: int = 10) -> list[str]:
    """提取关键词（jieba TF-IDF）"""
    if JIEBA_AVAILABLE:
        return jieba.analyse.extract_tags(text, topK=topK, withWeight=False)
    tokens = tokenize(text)
    # 简单词频统计
    freq = {}
    for t in tokens:
        if len(t) > 1:
            freq[t] = freq.get(t, 0) + 1
    return sorted(freq, key=freq.get, reverse=True)[:topK]


def compute_tf_idf_score(query_tokens: list[str], doc_tokens: list[str],
                         doc_freq: dict[str, int], total_docs: int) -> float:
    """计算 query 相对 doc 的 TF-IDF 相似度"""
    if not doc_tokens:
        return 0.0

    # TF
    doc_freq_map = {}
    for t in doc_tokens:
        doc_freq_map[t] = doc_freq_map.get(t, 0) + 1

    score = 0.0
    for qt in query_tokens:
        if qt in doc_freq_map:
            tf = doc_freq_map[qt] / len(doc_tokens)
            df = doc_freq.get(qt, 1)
            idf = math.log(total_docs / (df + 1))
            score += tf * idf
    return score


def retrieve_from_compliance_rules(query: str, top_k: int = 5) -> list[dict]:
    """从合规规则库检索，支持 jieba 语义匹配"""
    conn = get_conn()
    
    try:
        rules = conn.execute("""
            SELECT rule_code, rule_name, rule_type, category, pattern, action_level, description
            FROM compliance_rules
        """).fetchall()
        cols = [d[0] for d in conn.execute("SELECT * FROM compliance_rules LIMIT 0").description]
        rule_list = [dict(zip(cols, r)) for r in rules]
    finally:
        close_conn(conn)

    if not rule_list:
        return []

    total_docs = len(rule_list)
    doc_freq = {}  # term -> 多少文档包含该词

    # 构建每个规则的 token 集合
    rule_tokens = []
    for rule in rule_list:
        text = f"{rule.get('rule_name','')} {rule.get('category','')} {rule.get('description','')}"
        if JIEBA_AVAILABLE:
            tokens = list(jieba.cut(text))
        else:
            tokens = list(text)
        rule_tokens.append(tokens)
        for t in set(tokens):
            doc_freq[t] = doc_freq.get(t, 0) + 1

    # 提取 query 关键词
    query_tokens = tokenize(query)
    query_keywords = extract_keywords(query, topK=10)

    results = []
    for i, rule in enumerate(rule_list):
        tokens = rule_tokens[i]
        # 综合评分：关键词匹配 + TF-IDF
        kw_score = sum(1 for kw in query_keywords if kw in "".join(tokens))
        tfidf = compute_tf_idf_score(query_tokens, tokens, doc_freq, total_docs)
        score = kw_score * 2 + tfidf

        if score > 0:
            results.append({
                "source": "compliance_rules",
                "type": rule.get("rule_type", ""),
                "title": rule.get("rule_name", ""),
                "content": f"[{rule.get('action_level', '').upper()}] {rule.get('description', '')}",
                "pattern": rule.get("pattern", ""),
                "score": round(score, 4),
            })

    results.sort(key=lambda x: -x["score"])
    return results[:top_k]


def retrieve_from_pharma_knowledge(query: str, top_k: int = 5) -> list[dict]:
    """从内置知识库检索"""
    results = []
    query_tokens = set(tokenize(query))

    for category, data in PHARMA_KNOWLEDGE.items():
        cat_tokens = set(tokenize(category))
        overlap = len(query_tokens & cat_tokens)
        base_score = overlap * 2

        if isinstance(data, dict):
            for sub_key, items in data.items():
                if isinstance(items, list):
                    for item in items:
                        item_tokens = set(tokenize(item))
                        item_overlap = len(query_tokens & item_tokens)
                        score = base_score + item_overlap
                        if score > 0 or category in query:
                            results.append({
                                "source": "pharma_knowledge",
                                "type": category,
                                "title": sub_key,
                                "content": item,
                                "score": score,
                            })
        elif isinstance(data, list):
            for item in data:
                item_tokens = set(tokenize(item))
                item_overlap = len(query_tokens & item_tokens)
                score = base_score + item_overlap
                if score > 0:
                    results.append({
                        "source": "pharma_knowledge",
                        "type": category,
                        "title": category,
                        "content": item,
                        "score": score,
                    })

    results.sort(key=lambda x: -x.get("score", 0))

    # 去重
    seen = set()
    deduped = []
    for r in results:
        key = r.get("content", "")[:50]
        if key not in seen:
            seen.add(key)
            deduped.append(r)

    return deduped[:top_k]


def retrieve_relevant_knowledge(query: str, top_k: int = 5) -> list[dict]:
    """语义检索主函数：合并 compliance_rules + pharma_knowledge 结果"""
    rule_results = retrieve_from_compliance_rules(query, top_k)
    pharma_results = retrieve_from_pharma_knowledge(query, top_k)

    # 合并并按 score 排序
    merged = rule_results + pharma_results
    merged.sort(key=lambda x: -x.get("score", 0))

    # 去重
    seen = set()
    deduped = []
    for r in merged:
        key = r.get("content", "")[:50]
        if key not in seen:
            seen.add(key)
            deduped.append(r)

    return deduped[:top_k]


def qa(query: str, top_k: int = 5) -> dict:
    """知识库问答"""
    if not query or not query.strip():
        return {"error": "question is required"}

    context = retrieve_relevant_knowledge(query, top_k)

    if context:
        answer = "根据知识库检索结果：\n" + "\n".join([r.get("content", "") for r in context[:3]])
    else:
        answer = "抱歉，知识库中暂无相关信息。建议查阅《药品管理法》、《广告法》相关条款，或咨询专业法务人员。"

    related = []
    for kw in ["药品管理法", "广告法", "处方药", "合规", "违禁词"]:
        if kw not in query:
            related.append(f"关于{kw}的规定是什么？")

    return {
        "question": query,
        "answer": answer,
        "sources": [
            {
                "source": r.get("source", ""),
                "type": r.get("type", ""),
                "title": r.get("title", ""),
                "content_preview": r.get("content", "")[:100],
                "score": r.get("score", 0),
            }
            for r in context
        ],
        "related_questions": related[:3],
        "confidence": "high" if context else "low",
        "search_mode": "jieba_semantic" if JIEBA_AVAILABLE else "keyword_fallback",
    }


def search_regulations(keyword: str) -> dict:
    """搜索具体法规条款"""
    conn = get_conn()
    
    try:
        # 支持分词搜索
        kw_tokens = tokenize(keyword)
        kw_pattern = f"%{'%'.join(kw_tokens[:3])}%"

        rules = conn.execute("""
            SELECT rule_code, rule_name, rule_type, category, pattern, action_level, description
            FROM compliance_rules
            WHERE rule_name LIKE ? OR category LIKE ? OR pattern LIKE ? OR description LIKE ?
            LIMIT 20
        """, (kw_pattern, kw_pattern, kw_pattern, kw_pattern)).fetchall()

        cols = [d[0] for d in conn.execute("SELECT * FROM compliance_rules LIMIT 0").description]
        rule_list = [dict(zip(cols, r)) for r in rules]

        return {
            "keyword": keyword,
            "result_count": len(rule_list),
            "rules": [
                {
                    "code": r.get("rule_code"),
                    "name": r.get("rule_name"),
                    "type": r.get("rule_type"),
                    "level": r.get("action_level"),
                    "description": r.get("description"),
                }
                for r in rule_list
            ]
        }
    finally:
        close_conn(conn)


def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {"question": sys.argv[1]}
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {"question": data}
    return {}


if __name__ == "__main__":
    args = _parse_args()
    question = args.get("question")
    keyword = args.get("keyword")
    top_k = args.get("top_k", 5)

    if question:
        result = qa(question, top_k)
    elif keyword:
        result = search_regulations(keyword)
    else:
        result = {"error": "question or keyword required"}

    print(json.dumps(result, ensure_ascii=False, indent=2))
