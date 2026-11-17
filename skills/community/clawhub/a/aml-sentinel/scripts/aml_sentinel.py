#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aml-sentinel — 反洗钱(AML)哨兵纵深工具（零依赖）。
对交易做可疑模式检测(拆分/快进快出/跨境无KYC/大额未报备)，输出风险等级。
理论真源：LGD 凡自治之物三律（SynomosAI）。"""
import argparse, json, sys
NAME = "aml-sentinel"
def scan(tx):
    hits = []
    amt = float(tx.get("amount", 0) or 0)
    kyc = bool(tx.get("counterparty_kyc"))
    cross = bool(tx.get("cross_border"))
    structured = bool(tx.get("structured"))
    freq = int(tx.get("freq", 0) or 0)
    fast = bool(tx.get("fast_in_out"))
    if amt >= 50000 and not tx.get("reported"): hits.append("大额未报备")
    if (amt >= 50000 or cross) and not kyc: hits.append("无对手KYC")
    if cross and not kyc: hits.append("跨境无KYC")
    if structured: hits.append("拆分/结构化交易")
    if fast and freq >= 3: hits.append("快进快出+高频")
    score = min(100, len(hits) * 25 + (30 if cross else 0))
    level = "高" if score >= 70 else ("中" if score >= 40 else "低")
    return {"hits": hits, "score": score, "level": level, "risk": score >= 70}
def main():
    ap = argparse.ArgumentParser(description=NAME + " · AML哨兵")
    ap.add_argument("--tx", help="单笔交易 JSON")
    ap.add_argument("--file", help="交易JSONL文件(逐行)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not a.tx and not a.file:
        print("用法: --tx <JSON> | --file <path>", file=sys.stderr); sys.exit(2)
    results = []
    if a.tx:
        try: results.append(scan(json.loads(a.tx)))
        except Exception as e: print("tx JSON 解析失败: " + str(e), file=sys.stderr); sys.exit(2)
    if a.file:
        for line in open(a.file, encoding="utf-8-sig"):
            line = line.strip()
            if line: results.append(scan(json.loads(line)))
    any_high = any(r["risk"] for r in results)
    if a.json: print(json.dumps({"results": results, "any_high_risk": any_high}, ensure_ascii=False, indent=2))
    else:
        print("=== " + NAME + " · AML 检测 ===")
        for r in results:
            print("  风险" + str(r["score"]) + " " + r["level"] + " 命中:" + (",".join(r["hits"]) or "无"))
        print("  结论: " + ("存在高风险 ⛔" if any_high else "未发现高风险 ✅"))
    sys.exit(1 if any_high else 0)
if __name__ == "__main__":
    main()
