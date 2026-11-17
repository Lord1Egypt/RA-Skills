#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fin-reg-calc — 金融AI合规计算纵深工具（零依赖）。
把 LGD 三律"有证/有门禁"落地为可执行的合规计算：投资者适当性 + 大额上报阈值。
理论真源：LGD 凡自治之物三律（SynomosAI）。"""
import argparse, json, sys
NAME = "fin-reg-calc"
# 大额上报阈值(量级参考, 以监管最新为准)
LARGE_TX_THRESHOLD = 50000
def suitability(client_risk, product_risk):
    diff = product_risk - client_risk
    if diff <= 0:
        return "允许", True
    if diff == 1:
        return "限制(加签/告知)", True
    return "禁止(适当性不匹配)", False
def threshold(amount):
    over = amount > LARGE_TX_THRESHOLD
    return ("超大额须报备" if over else "未超阈"), (not over)
def main():
    ap = argparse.ArgumentParser(description=NAME + " · 金融AI合规计算")
    ap.add_argument("--suitability", nargs=2, type=int, metavar=("CLIENT_RISK", "PRODUCT_RISK"), help="适当性: 客户风险等级 产品风险等级(1-5)")
    ap.add_argument("--threshold", type=float, help="大额上报阈值校验: 交易金额(元)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not a.suitability and a.threshold is None:
        print("用法: --suitability 客户风险 产品风险 | --threshold 金额", file=sys.stderr); sys.exit(2)
    out = {}
    ok = True
    if a.suitability:
        r, c = suitability(a.suitability[0], a.suitability[1])
        out["suitability"] = {"client": a.suitability[0], "product": a.suitability[1], "result": r, "compliant": c}
        ok = ok and c
    if a.threshold is not None:
        r, c = threshold(a.threshold)
        out["threshold"] = {"amount": a.threshold, "result": r, "compliant": c}
        ok = ok and c
    out["compliant"] = ok
    if a.json: print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("=== " + NAME + " · 金融AI合规计算 ===")
        for k, v in out.items():
            if k != "compliant": print("  " + k + ": " + json.dumps(v, ensure_ascii=False))
        print("  结论: " + ("合规 ✅" if ok else "存在违规项 ⛔"))
    sys.exit(0 if ok else 1)
if __name__ == "__main__":
    main()
