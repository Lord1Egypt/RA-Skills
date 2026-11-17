#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
abstract_translator.py — 英文摘要术语标注（英文→中文，术语级）

基于本地医学专业术语词典（内置 EN→ZH 词表 + references/term_map.json 的英文条目），
对命中术语做中文标注（替换为【中文】），未命中词保留原文。
纯本地、零联网——**无外部翻译 API**；非全文翻译。

Usage:
  python scripts/abstract_translator.py --text "This study evaluated..." --format json
  python scripts/abstract_translator.py --file abstract.txt --format ascii
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TERMIN_FILE = os.path.join(ROOT, "references", "term_map.json")

# 内置医学专业术语词典（高频）
MEDICAL_TERMS = {
    # 研究类型
    "randomized controlled trial": "随机对照试验",
    "rct": "随机对照试验",
    "meta-analysis": "荟萃分析",
    "systematic review": "系统综述",
    "cohort study": "队列研究",
    "case-control study": "病例对照研究",
    "cross-sectional study": "横断面研究",
    "clinical trial": "临床试验",
    "phase i": "I期",
    "phase ii": "II期",
    "phase iii": "III期",
    "phase iv": "IV期",
    "double-blind": "双盲",
    "placebo-controlled": "安慰剂对照",
    "multicenter": "多中心",
    "prospective": "前瞻性",
    "retrospective": "回顾性",
    
    # 统计术语
    "odds ratio": "比值比",
    "or": "比值比",
    "hazard ratio": "风险比",
    "hr": "风险比",
    "confidence interval": "置信区间",
    "ci": "置信区间",
    "p-value": "P值",
    "p value": "P值",
    "statistically significant": "统计学显著",
    "non-inferiority": "非劣效性",
    "superiority": "优效性",
    "intention-to-treat": "意向治疗",
    "per-protocol": "符合方案",
    "subgroup analysis": "亚组分析",
    "sensitivity analysis": "敏感性分析",
    
    # 终点指标
    "overall survival": "总生存期",
    "os": "总生存期",
    "progression-free survival": "无进展生存期",
    "pfs": "无进展生存期",
    "objective response rate": "客观缓解率",
    "orr": "客观缓解率",
    "disease control rate": "疾病控制率",
    "dcr": "疾病控制率",
    "complete response": "完全缓解",
    "cr": "完全缓解",
    "partial response": "部分缓解",
    "pr": "部分缓解",
    "stable disease": "疾病稳定",
    "sd": "疾病稳定",
    "progressive disease": "疾病进展",
    "pd": "疾病进展",
    "time to progression": "疾病进展时间",
    "ttp": "疾病进展时间",
    
    # 安全性
    "adverse event": "不良事件",
    "ae": "不良事件",
    "serious adverse event": "严重不良事件",
    "sae": "严重不良事件",
    "treatment-related": "治疗相关",
    "drug-related": "药物相关",
    "toxicity": "毒性",
    "tolerability": "耐受性",
    
    # 药物类型
    "monoclonal antibody": "单克隆抗体",
    "mab": "单克隆抗体",
    "tyrosine kinase inhibitor": "酪氨酸激酶抑制剂",
    "tki": "酪氨酸激酶抑制剂",
    "immune checkpoint inhibitor": "免疫检查点抑制剂",
    "pd-1 inhibitor": "PD-1抑制剂",
    "pd-l1 inhibitor": "PD-L1抑制剂",
    "vegf": "血管内皮生长因子",
    "egfr": "表皮生长因子受体",
    "alk": "间变性淋巴瘤激酶",
    
    # 疾病
    "non-small cell lung cancer": "非小细胞肺癌",
    "nsclc": "非小细胞肺癌",
    "small cell lung cancer": "小细胞肺癌",
    "sclc": "小细胞肺癌",
    "breast cancer": "乳腺癌",
    "colorectal cancer": "结直肠癌",
    "gastric cancer": "胃癌",
    "hepatocellular carcinoma": "肝细胞癌",
    "hcc": "肝细胞癌",
    "melanoma": "黑色素瘤",
    "lymphoma": "淋巴瘤",
    "leukemia": "白血病",
    
    # 常用动词/短语
    "evaluate": "评估",
    "assess": "评估",
    "compare": "比较",
    "analyze": "分析",
    "investigate": "调查",
    "determine": "确定",
    "demonstrate": "证明",
    "reveal": "揭示",
    "suggest": "提示",
    "indicate": "表明",
    "conclude": "结论",
    "aim": "目的",
    "objective": "目的",
    "method": "方法",
    "result": "结果",
    "conclusion": "结论",
    "background": "背景",
    "purpose": "目的",
    "significance": "意义",
    "efficacy": "疗效",
    "safety": "安全性",
    "patient": "患者",
    "patients": "患者",
    "treatment": "治疗",
    "therapy": "治疗",
    "regimen": "方案",
    "dosage": "剂量",
    "administration": "给药",
    "enrollment": "入组",
    "follow-up": "随访",
    "baseline": "基线",
    "characteristic": "特征",
    "demographic": "人口统计学",
    "endpoint": "终点",
    "outcome": "结局",
    "prognosis": "预后",
    "prognostic": "预后",
    "biomarker": "生物标志物",
    "mutation": "突变",
    "amplification": "扩增",
    "expression": "表达",
    "inhibition": "抑制",
    "combination": "联合",
    "monotherapy": "单药治疗",
    "first-line": "一线",
    "second-line": "二线",
    "relapse": "复发",
    "refractory": "难治性",
    "metastatic": "转移性",
    "advanced": "晚期",
    "early-stage": "早期",
    "locally advanced": "局部晚期",
    "resectable": "可切除",
    "unresectable": "不可切除",
}


def load_term_map() -> Dict:
    """加载术语词典。"""
    terms = dict(MEDICAL_TERMS)
    if os.path.isfile(TERMIN_FILE):
        try:
            with open(TERMIN_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                terms.update(data)
        except Exception:
            pass
    return terms


def translate_abstract(text: str, term_map: Dict) -> Dict:
    """对英文文本做医学术语中文标注（术语级，非全文翻译）。

    修复（2026-08-15）：
    1. 只取**英文 key**——term_map.json 混入的中→英条目（中文 key）对英→中标注无效，
       且会干扰匹配（此前实测 "osimertinib" 被短词 "os" 子串误伤、循环替换导致嵌套）。
    2. **词边界匹配**（前后非字母数字）——"os" 不再命中 "osimertinib" 内部。
    3. **单轮交替替换**（最长匹配优先）——已替换区间不再被二次匹配，杜绝嵌套。
    """
    import re as _re
    _han = _re.compile(r"[\u4e00-\u9fff]")
    # 只保留英文 key（去掉中文 key / 纯符号 key）
    terms = {k: v for k, v in term_map.items()
             if isinstance(k, str) and isinstance(v, str) and not _han.search(k) and _re.search(r"[A-Za-z]", k)}
    if not terms:
        return {"original": text, "translated": text, "replacements": [],
                "n_replacements": 0}
    # 大小写归一索引（IGNORECASE 匹配后按原文大小写回查）
    lower2zh = {k.lower(): v for k, v in terms.items()}
    sorted_keys = sorted(terms, key=len, reverse=True)  # 最长匹配优先

    replacements = []
    counts = {}

    def _repl(m):
        en = m.group(0)
        zh = lower2zh.get(en.lower(), terms.get(en))
        counts[en] = counts.get(en, 0) + 1
        return "【%s】" % zh

    # 词边界 + 单轮交替（各分支按长度降序，re 从左到右尝试）
    pattern = _re.compile(
        r"(?<![A-Za-z0-9])(" + "|".join(_re.escape(k) for k in sorted_keys) + r")(?![A-Za-z0-9])",
        _re.IGNORECASE)
    translated = pattern.sub(_repl, text)
    for en, n in counts.items():
        replacements.append({"en": en, "zh": lower2zh.get(en.lower(), terms.get(en)),
                             "count": n})

    return {
        "original": text,
        "translated": translated,
        "replacements": replacements,
        "n_replacements": len(replacements),
    }


def format_ascii(result: Dict) -> str:
    """格式化为 ASCII。"""
    lines = []
    lines.append("=" * 70)
    lines.append("摘要翻译结果（英文→中文）")
    lines.append("=" * 70)
    lines.append("")
    lines.append("原文:")
    lines.append(result["original"][:500])
    lines.append("")
    lines.append("-" * 70)
    lines.append("翻译（术语替换版）:")
    lines.append(result["translated"][:500])
    lines.append("")
    lines.append("-" * 70)
    lines.append(f"替换术语数: {result['n_replacements']}")
    for r in result["replacements"][:10]:
        lines.append(f"  {r['en']:<30} → {r['zh']}")
    if len(result["replacements"]) > 10:
        lines.append(f"  ... 共 {len(result['replacements'])} 个术语")
    lines.append("=" * 70)
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Annotate English text with Chinese medical-term glosses (offline, term-level; not full-text translation)")
    p.add_argument("--text", type=str, default=None, help="input text")
    p.add_argument("--file", type=str, default=None,
                   help="input file path (reads only this local file you specify; no other file access)")
    p.add_argument("--format", choices=["json", "ascii"], default="ascii")
    p.add_argument("--output", type=str, default=None,
                   help="output file path (writes only to this local path you specify)")
    
    args = p.parse_args()
    
    if args.text:
        text = args.text
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        p.error("require --text or --file")
        return
    
    term_map = load_term_map()
    result = translate_abstract(text, term_map)
    
    if args.format == "json":
        out = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        out = format_ascii(result)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"Written: {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
