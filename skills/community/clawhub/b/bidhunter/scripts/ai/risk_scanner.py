#!/usr/bin/env python3
"""
risk_scanner.py - Detect exclusionary / pre-determined risk clauses (BidHunter v2.0, B2).

Two-layer scan:
  1. Rule-based: matches a curated list of risk keywords/patterns (no API needed).
  2. LLM-assisted: when MiniMax key is configured, asks the model to find
     subtle倾向性条款 (specified brand, sole supplier, specific track-record门槛).

Outputs a list of findings with severity and a snippet.

Usage:
  python3 risk_scanner.py <doc_text_file.txt>
  python3 risk_scanner.py <doc_text_file.txt> --llm      # also run LLM scan
"""
import os
import sys
import json
import re

# Rule-based risk patterns (substring / regex). severity: high/medium/low
RISK_PATTERNS = [
    ("high", r"指定(品牌|型号|厂家|供应商)", "指定品牌/厂家——疑似排他性条款"),
    ("high", r"唯一(的)?(供应|代理|授权)", "唯一供应商/代理——内定风险"),
    ("high", r"限定(特定|某)[一]?(品牌|厂家|型号)", "限定特定品牌——排他风险"),
    ("medium", r"(须|需|必须).{0,12}(原厂|制造商).{0,8}授权", "要求原厂授权——抬高门槛"),
    ("medium", r"(特定|指定).{0,8}(业绩|案例|项目)", "指定特定业绩/案例——倾向性"),
    ("medium", r"本地(注册|纳税|分支机构)", "要求本地注册/纳税——地域限制"),
    ("low", r"无正当理由.{0,6}不得", "不合理限制条款，需人工复核"),
    ("low", r"甲方(自行|单方面).{0,6}(解释|变更|终止)", "甲方单方解释权——商务风险"),
]

MAX_CHARS = 9000


def rule_scan(text):
    findings = []
    for sev, pat, desc in RISK_PATTERNS:
        for m in re.finditer(pat, text):
            s, e = max(0, m.start() - 20), min(len(text), m.end() + 20)
            snippet = text[s:e].replace("\n", " ")
            findings.append({"severity": sev, "type": desc,
                             "snippet": snippet, "layer": "rule"})
            break  # one per pattern to avoid noise
    return findings


def llm_scan(text):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        from minimax_client import MiniMaxClient, ConfigError
        client = MiniMaxClient.from_config()
    except ConfigError as e:
        return [{"severity": "info", "type": "LLM 未配置，跳过智能扫描",
                 "snippet": str(e), "layer": "llm"}]
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n...（已截断）"
    system = ("你是招投标合规审查专家。请从文本中找出可能构成排他性、内定倾向或"
              "不合理限制的条款。只输出 JSON 数组，每项含 severity(high/medium/low)、"
              "type(风险类型)、snippet(原文片段,≤40字)。无则输出空数组 []。")
    prompt = f"招标文件文本：\n'''{text}'''"
    try:
        raw = client.chat(prompt, system=system, json_mode=True)
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw[raw.find("["): raw.rfind("]") + 1]
        items = json.loads(raw)
        for it in items:
            it["layer"] = "llm"
        return items
    except Exception as e:
        return [{"severity": "info", "type": f"LLM 扫描失败: {e}", "snippet": "", "layer": "llm"}]


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 risk_scanner.py <file.txt> [--llm]", file=sys.stderr)
        sys.exit(1)
    src = sys.argv[1]
    use_llm = "--llm" in sys.argv[2:]
    with open(src, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    findings = rule_scan(text)
    if use_llm:
        findings += llm_scan(text)
    sev_order = {"high": 0, "medium": 1, "low": 2, "info": 3}
    findings.sort(key=lambda x: sev_order.get(x["severity"], 9))
    print(json.dumps({"total": len(findings), "findings": findings}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
