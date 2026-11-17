import argparse, json, sys

def main():
    ap = argparse.ArgumentParser(description="fund-fee-calc · 资管产品费率与净收益试算（零依赖）")
    ap.add_argument("--amount", type=float, required=True, help="本金")
    ap.add_argument("--mgmt", type=float, default=0.0, help="年管理费率(如0.015)")
    ap.add_argument("--custody", type=float, default=0.0, help="年托管费率")
    ap.add_argument("--sales", type=float, default=0.0, help="年销售服务费率")
    ap.add_argument("--years", type=float, default=1, help="持有年数")
    ap.add_argument("--yield", dest="yld", type=float, default=0.0, help="预期年化收益(仅演示)")
    ap.add_argument("--claim", help="宣传口径文本，如 保本保收益")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.amount <= 0 or a.years <= 0:
        ap.error("--amount 与 --years 必须为正数")
    problems = []
    if a.claim:
        bad = [k for k in ("保本", "稳赚", "无风险", "保证收益") if k in a.claim]
        if bad:
            problems.append("宣传含" + "、".join(bad) + "——资管新规禁止保本保收益承诺")
    fee_rate = a.mgmt + a.custody + a.sales
    fees = a.amount * fee_rate * a.years
    gross = a.amount * a.yld * a.years
    net = gross - fees
    note = "预期收益仅为演示，不构成收益承诺；市场有风险，投资须谨慎"
    if a.json:
        print(json.dumps({"pass": not problems, "principal": a.amount,
                          "total_fee_rate_annual": round(fee_rate, 4), "total_fees": round(fees, 2),
                          "expected_gross": round(gross, 2), "expected_net": round(net, 2),
                          "note": note, "problems": problems}, ensure_ascii=False, indent=2))
    else:
        print("本金 %.2f · 年费率合计 %.2f%% · %g 年费用合计 %.2f" % (a.amount, fee_rate * 100, a.years, fees))
        print("演示口径预期毛收益 %.2f · 净收益 %.2f" % (gross, net))
        print("提示：" + note)
        for p in problems:
            print("  [FAIL] " + p)
        print("  判定：" + ("PASS" if not problems else "FAIL"))
    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    main()
