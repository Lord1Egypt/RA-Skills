#!/usr/bin/env python3
"""
自动仓位计算（把「2% 风险 + 单票 10–20% 仓」规则自动化）

用法:
  python3 position_size.py --capital 20000 --entry 39.20 --stop 37.40
  python3 position_size.py --capital 20000 --entry 39.20 --stop 37.40 --max-risk-pct 2 --max-pos-pct 20

规则: 手数 = floor(单笔可亏金额 ÷ (每股风险 × 100))；单笔风险 ≤ 总资金×max_risk_pct；
      单票占用 ≤ 总资金×max_pos_pct。取两者较小值，向下取整到「手」。
"""
import argparse
import math
import sys


def size(capital, entry, stop, risk_pct, pos_pct, lot=100):
    per_share = entry - stop
    if per_share <= 0:
        return {"ok": False, "msg": "止损必须低于入场价（做多）"}
    loss_budget = capital * risk_pct / 100.0          # 可亏金额
    shares_risk = math.floor(loss_budget / per_share / lot) * lot
    shares_pos = math.floor(capital * pos_pct / 100.0 / entry / lot) * lot
    shares = min(shares_risk, shares_pos)
    if shares < lot:
        return {"ok": False, "msg": "按纪律不够 1 手（可亏预算{:.0f}元 ÷ 每股风险{:.2f} → 0手）".format(
            loss_budget, per_share), "loss_budget": loss_budget}
    cost = shares * entry
    max_loss = shares * per_share
    tgt_gain = lambda t: shares * (t - entry)
    return {"ok": True, "shares": shares, "lots": shares // lot, "cost": cost,
            "max_loss": max_loss, "max_loss_pct": max_loss / capital * 100,
            "cost_pct": cost / capital * 100,
            "bind": "风险约束" if shares_risk <= shares_pos else "仓位约束",
            "loss_budget": loss_budget,
            "tgt_gain": tgt_gain}


def main():
    ap = argparse.ArgumentParser(description="自动仓位计算")
    ap.add_argument("--capital", type=float, required=True, help="总资金（元）")
    ap.add_argument("--entry", type=float, required=True)
    ap.add_argument("--stop", type=float, required=True)
    ap.add_argument("--max-risk-pct", type=float, default=2.0, help="单笔风险上限%%，默认2")
    ap.add_argument("--max-pos-pct", type=float, default=20.0, help="单票仓位上限%%，默认20")
    ap.add_argument("--targets", default="", help="目标价，逗号分隔，如 41.5,43.0")
    a = ap.parse_args()

    r = size(a.capital, a.entry, a.stop, a.max_risk_pct, a.max_pos_pct)
    print("==== 仓位计算 ====")
    print("总资金 {:.0f} 元 ｜ 入场 {:.2f} ｜ 止损 {:.2f}（每股风险 {:.2f}，{:.2f}%）".format(
        a.capital, a.entry, a.stop, a.entry - a.stop, (a.entry - a.stop) / a.entry * 100))
    if not r["ok"]:
        print("❌ " + r["msg"]); return 0
    print("→ 建议买入：{} 股（{} 手）".format(r["shares"], r["lots"]))
    print("   占用资金 {:.0f} 元（{:.1f}% 仓）｜ 最大亏损 {:.0f} 元（{:.2f}%）｜ 由{}决定".format(
        r["cost"], r["cost_pct"], r["max_loss"], r["max_loss_pct"], r["bind"]))
    if a.targets:
        print("   止盈测算：")
        for t in [x for x in a.targets.split(",") if x.strip()]:
            tv = float(t)
            print("     目标 {:.2f} → 盈利 {:+.0f} 元（{:+.1f}%）".format(
                tv, r["tgt_gain"](tv), (tv / a.entry - 1) * 100))
    print("\n纪律：单笔风险≤{:.1f}%、单票≤{:.1f}% 仓；浮亏绝不加仓摊平。".format(
        a.max_risk_pct, a.max_pos_pct))
    return 0


if __name__ == "__main__":
    sys.exit(main())
