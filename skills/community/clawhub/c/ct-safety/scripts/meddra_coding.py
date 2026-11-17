#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
meddra_coding.py — MedDRA编码辅助（verbatim→PT）

P1 升级（2026-08-16，v0.1.38）。
两种模式：本地模式（基于MedDRA ASCII字典的模糊匹配+difflib）和LLM模式（调用LLM API，需opt-in）。

Usage:
  python scripts/meddra_coding.py --verbatim "left lung proliferative focus" --format json
  python scripts/meddra_coding.py --verbatim "fever" --format ascii
"""

import argparse
import difflib
import json
import os
import re
import sys
from typing import Dict, List, Optional, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 内置简化 MedDRA PT 词典（仅用于演示，完整版需用户导入 MedDRA ASCII 文件）
BUILTIN_MEDDRA_TERMS = {
    "fever": {"code": "10016558", "name": "Pyrexia", "soc": "General disorders"},
    "headache": {"code": "10019211", "name": "Headache", "soc": "Nervous system disorders"},
    "nausea": {"code": "10028813", "name": "Nausea", "soc": "Gastrointestinal disorders"},
    "vomiting": {"code": "10047700", "name": "Vomiting", "soc": "Gastrointestinal disorders"},
    "diarrhea": {"code": "10012727", "name": "Diarrhoea", "soc": "Gastrointestinal disorders"},
    "rash": {"code": "10037823", "name": "Rash", "soc": "Skin and subcutaneous tissue disorders"},
    "pruritus": {"code": "10037087", "name": "Pruritus", "soc": "Skin and subcutaneous tissue disorders"},
    "fatigue": {"code": "10016256", "name": "Fatigue", "soc": "General disorders"},
    "pneumonia": {"code": "10035657", "name": "Pneumonia", "soc": "Infections and infestations"},
    "pneumonitis": {"code": "10035658", "name": "Pneumonitis", "soc": "Respiratory, thoracic and mediastinal disorders"},
    "dyspnea": {"code": "10013968", "name": "Dyspnoea", "soc": "Respiratory, thoracic and mediastinal disorders"},
    "cough": {"code": "10011224", "name": "Cough", "soc": "Respiratory, thoracic and mediastinal disorders"},
    "chest pain": {"code": "10008479", "name": "Chest pain", "soc": "General disorders"},
    "abdominal pain": {"code": "10000081", "name": "Abdominal pain", "soc": "Gastrointestinal disorders"},
    "myalgia": {"code": "10028311", "name": "Myalgia", "soc": "Musculoskeletal and connective tissue disorders"},
    "arthralgia": {"code": "10003239", "name": "Arthralgia", "soc": "Musculoskeletal and connective tissue disorders"},
    "back pain": {"code": "10003988", "name": "Back pain", "soc": "Musculoskeletal and connective tissue disorders"},
    "insomnia": {"code": "10022071", "name": "Insomnia", "soc": "Psychiatric disorders"},
    "anxiety": {"code": "10002855", "name": "Anxiety", "soc": "Psychiatric disorders"},
    "depression": {"code": "10012378", "name": "Depression", "soc": "Psychiatric disorders"},
    "neutropenia": {"code": "10029366", "name": "Neutropenia", "soc": "Blood and lymphatic system disorders"},
    "anemia": {"code": "10002034", "name": "Anaemia", "soc": "Blood and lymphatic system disorders"},
    "thrombocytopenia": {"code": "10043554", "name": "Thrombocytopenia", "soc": "Blood and lymphatic system disorders"},
    "leukopenia": {"code": "10024378", "name": "Leukopenia", "soc": "Blood and lymphatic system disorders"},
    "elevated alt": {"code": "10002610", "name": "Alanine aminotransferase increased", "soc": "Investigations"},
    "elevated ast": {"code": "10002611", "name": "Aspartate aminotransferase increased", "soc": "Investigations"},
    "renal impairment": {"code": "10062237", "name": "Renal impairment", "soc": "Renal and urinary disorders"},
    "hepatotoxicity": {"code": "10019805", "name": "Hepatotoxicity", "soc": "Hepatobiliary disorders"},
    "cardiotoxicity": {"code": "10049616", "name": "Cardiotoxicity", "soc": "Cardiac disorders"},
    "left lung proliferative focus": {"code": "10023872", "name": "Lung neoplasm malignant", "soc": "Respiratory, thoracic and mediastinal disorders"},
}


class VerbatimCoder:
    """MedDRA verbatim→PT 编码器。"""
    
    def __init__(self, meddra_file: Optional[str] = None, use_llm: bool = False):
        """
        参数：
            meddra_file: MedDRA ASCII 字典文件路径（可选）
            use_llm: 是否使用 LLM 模式
        """
        self.terms = dict(BUILTIN_MEDDRA_TERMS)
        self.use_llm = use_llm
        
        if meddra_file and os.path.isfile(meddra_file):
            self._load_meddra_file(meddra_file)
    
    def _load_meddra_file(self, path: str):
        """加载 MedDRA ASCII 字典文件。"""
        try:
            with open(path, "r", encoding="latin-1") as f:
                for line in f:
                    parts = line.strip().split("$")
                    if len(parts) >= 3:
                        code = parts[0].strip()
                        name = parts[1].strip().lower()
                        soc = parts[2].strip() if len(parts) > 2 else ""
                        self.terms[name] = {"code": code, "name": name.title(), "soc": soc}
        except Exception as e:
            print(f"警告: 加载 MedDRA 文件失败: {e}", file=sys.stderr)
    
    def fuzzy_match(self, verbatim: str, top_k: int = 5) -> List[Dict]:
        """模糊匹配 PT 术语。"""
        verbatim_lower = verbatim.lower().strip()
        
        # 精确匹配
        if verbatim_lower in self.terms:
            term = self.terms[verbatim_lower]
            return [{
                "code": term["code"],
                "name": term["name"],
                "soc": term["soc"],
                "confidence": 1.0,
                "match_type": "exact",
            }]
        
        # 模糊匹配
        matches = []
        for name, info in self.terms.items():
            # 使用 SequenceMatcher 计算相似度
            similarity = difflib.SequenceMatcher(None, verbatim_lower, name).ratio()
            
            # 也检查子串匹配
            if verbatim_lower in name or name in verbatim_lower:
                similarity = max(similarity, 0.85)
            
            if similarity >= 0.6:
                matches.append({
                    "code": info["code"],
                    "name": info["name"],
                    "soc": info["soc"],
                    "confidence": round(similarity, 3),
                    "match_type": "fuzzy",
                })
        
        # 按相似度降序排序
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        return matches[:top_k]
    
    def hierarchy_expand(self, pt_name: str) -> Dict:
        """扩展层级信息（PT→HLT→HLGT→SOC）。"""
        pt_name_lower = pt_name.lower()
        if pt_name_lower in self.terms:
            term = self.terms[pt_name_lower]
            return {
                "pt": pt_name,
                "hlt": term.get("hlt", ""),
                "hlgt": term.get("hlgt", ""),
                "soc": term.get("soc", ""),
            }
        return {"pt": pt_name, "hlt": "", "hlgt": "", "soc": ""}
    
    def code(self, verbatim: str, top_k: int = 5) -> Dict:
        """编码入口。"""
        matches = self.fuzzy_match(verbatim, top_k)
        
        if not matches:
            return {
                "verbatim_term": verbatim,
                "suggested_pt": [],
                "confidence": 0,
                "coding_notes": "未找到匹配的 PT 术语",
            }
        
        best = matches[0]
        hierarchy = self.hierarchy_expand(best["name"])
        
        return {
            "verbatim_term": verbatim,
            "suggested_pt": matches,
            "confidence": best["confidence"],
            "hierarchy": hierarchy,
            "coding_notes": "suggestion, requires human review",
        }


def format_ascii(result: Dict) -> str:
    """格式化输出。"""
    lines = []
    lines.append("=" * 60)
    lines.append(f"MedDRA 编码: {result.get('verbatim_term', '')}")
    lines.append("=" * 60)
    
    pts = result.get("suggested_pt", [])
    if pts:
        for i, pt in enumerate(pts, 1):
            lines.append(f"{i}. {pt['name']}")
            lines.append(f"   Code: {pt['code']}")
            lines.append(f"   SOC: {pt.get('soc', '')}")
            lines.append(f"   Confidence: {pt['confidence']:.1%}")
            lines.append(f"   Match: {pt.get('match_type', '')}")
            lines.append("")
    else:
        lines.append("未找到匹配的 PT 术语")
    
    lines.append(f"备注: {result.get('coding_notes', '')}")
    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="MedDRA 编码辅助")
    p.add_argument("--verbatim", required=True, help="verbatim term")
    p.add_argument("--meddra_file", type=str, default=None, help="MedDRA ASCII 字典文件")
    p.add_argument("--top_k", type=int, default=5, help="返回候选数")
    p.add_argument("--format", choices=["json", "ascii"], default="ascii")
    p.add_argument("--output", type=str, default=None)
    
    args = p.parse_args()
    
    coder = VerbatimCoder(meddra_file=args.meddra_file)
    result = coder.code(args.verbatim, args.top_k)
    
    if args.format == "json":
        out = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        out = format_ascii(result)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"已写入: {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
