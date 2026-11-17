#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mesh_mapper.py — MeSH 术语自动映射与检索式构建

读取 references/mesh_terms_mapping.json 中的本地 MeSH 术语索引，
输入自由文本，自动匹配 MeSH 术语，构建专业检索式。

Usage:
  python scripts/mesh_mapper.py --text "lung cancer immunotherapy" --format json
  python scripts/mesh_mapper.py --text "NSCLC PD-1 inhibitor" --db pubmed --format ascii
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MESH_FILE = os.path.join(ROOT, "references", "mesh_terms_mapping.json")


def load_mesh_terms() -> Dict:
    """加载 MeSH 术语索引。"""
    if not os.path.isfile(MESH_FILE):
        return {"terms": {}, "error": f"MeSH 术语文件不存在: {MESH_FILE}"}
    with open(MESH_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def match_mesh_terms(text: str, mesh_data: Dict) -> List[Dict]:
    """从输入文本中匹配 MeSH 术语。
    
    返回匹配到的术语列表，按匹配得分排序。
    """
    text_lower = text.lower()
    matches = []
    
    for term_key, term_info in mesh_data.get("terms", {}).items():
        score = 0
        matched_terms = []
        
        # 检查主词
        if term_key.lower() in text_lower:
            score += 10
            matched_terms.append(term_key)
        
        # 检查入口词
        for entry in term_info.get("entry_terms", []):
            if entry.lower() in text_lower:
                score += 5
                matched_terms.append(entry)
        
        # 检查中文翻译
        zh = term_info.get("zh", "")
        if zh and zh in text:
            score += 8
            matched_terms.append(zh)
        
        if score > 0:
            matches.append({
                "term": term_key,
                "mesh_id": term_info.get("mesh_id", ""),
                "score": score,
                "matched_terms": matched_terms,
                "zh": zh,
            })
    
    # 按得分降序排序
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches


def build_query(matches: List[Dict], db: str = "pubmed") -> str:
    """根据匹配的 MeSH 术语构建检索式。
    
    支持 pubmed / embase / cochrane 格式。
    """
    if not matches:
        return ""
    
    # 取前 5 个最相关的术语
    top_matches = matches[:5]
    
    if db == "pubmed":
        # PubMed 格式：[MeSH Terms] OR [Title/Abstract]
        parts = []
        for m in top_matches:
            term = m["term"]
            mesh_id = m["mesh_id"]
            # 使用 MeSH 术语 + 自由词
            part = f'"{term}"[MeSH Terms] OR "{term}"[Title/Abstract]'
            parts.append(f"({part})")
        return " AND ".join(parts)
    
    elif db == "embase":
        # Embase 格式
        parts = []
        for m in top_matches:
            term = m["term"]
            part = f'"{term}"/exp OR "{term}"'
            parts.append(f"({part})")
        return " AND ".join(parts)
    
    elif db == "cochrane":
        # Cochrane 格式
        parts = []
        for m in top_matches:
            term = m["term"]
            part = f"MeSH DESCRIPTOR:{term} OR {term}"
            parts.append(f"({part})")
        return " AND ".join(parts)
    
    else:
        # 通用格式
        parts = [f'"{m["term"]}"' for m in top_matches]
        return " AND ".join(parts)


def format_ascii(text: str, matches: List[Dict], query: str, db: str) -> str:
    """格式化为 ASCII 表格。"""
    lines = []
    lines.append("=" * 70)
    lines.append(f"MeSH 术语映射结果")
    lines.append(f"输入: {text}")
    lines.append("=" * 70)
    lines.append("")
    
    if matches:
        lines.append(f"匹配到 {len(matches)} 个 MeSH 术语:")
        for i, m in enumerate(matches, 1):
            lines.append(f"  {i}. {m['term']}")
            lines.append(f"     MeSH ID: {m['mesh_id']}")
            lines.append(f"     中文: {m['zh']}")
            lines.append(f"     匹配词: {', '.join(m['matched_terms'])}")
            lines.append(f"     得分: {m['score']}")
            lines.append("")
        
        lines.append("-" * 70)
        lines.append(f"检索式 ({db}):")
        lines.append(query)
    else:
        lines.append("未匹配到 MeSH 术语")
    
    lines.append("=" * 70)
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="MeSH term mapping and query construction")
    p.add_argument("--text", required=True, help="input free text")
    p.add_argument("--db", choices=["pubmed", "embase", "cochrane", "generic"],
                   default="pubmed", help="target database")
    p.add_argument("--format", choices=["json", "ascii"], default="ascii",
                   help="output format")
    p.add_argument("--output", type=str, default=None, help="output file path")
    
    args = p.parse_args()
    
    mesh_data = load_mesh_terms()
    matches = match_mesh_terms(args.text, mesh_data)
    query = build_query(matches, args.db)
    
    if args.format == "json":
        result = {
            "input": args.text,
            "db": args.db,
            "matches": matches,
            "query": query,
            "n_matches": len(matches),
        }
        out = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        out = format_ascii(args.text, matches, query, args.db)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"Written: {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
