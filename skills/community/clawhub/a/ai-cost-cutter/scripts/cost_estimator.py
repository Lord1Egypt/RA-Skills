# -*- coding: utf-8 -*-
"""AI 调用成本估算器（零依赖 stdlib）。

对比四档方案月成本：
  基线  = 全部用旗舰 API（逐条实时）
  A     = 路由分级（贱活→中档/本地）
  B     = A + 批处理折扣
  C     = B + 本地回退（部分任务零 API 费）

用法：
  python cost_estimator.py --calls 50000 --avg-in 800 --avg-out 400 \
      --price-flagship 0.01 --price-mid 0.003 --price-local 0.0 \
      --batch-disc 0.5 --local-frac 0.6 --cheap-frac 0.4

单价单位：每 1K token 美元（与主流 API 计价一致）。
"""
import argparse


def per_call_cost(avg_in, avg_out, pin, pout):
    return (avg_in / 1000.0) * pin + (avg_out / 1000.0) * pout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calls", type=int, required=True, help="月调用次数")
    ap.add_argument("--avg-in", type=int, default=800, help="平均输入 token")
    ap.add_argument("--avg-out", type=int, default=400, help="平均输出 token")
    ap.add_argument("--price-flagship", type=float, default=0.01, help="旗舰模型 $/1K tok (in=out 同价近似)")
    ap.add_argument("--price-mid", type=float, default=0.003, help="中档模型 $/1K tok")
    ap.add_argument("--price-local", type=float, default=0.0, help="本地模型 $/1K tok")
    ap.add_argument("--batch-disc", type=float, default=0.5, help="批处理折扣(0-1)")
    ap.add_argument("--cheap-frac", type=float, default=0.4, help="贱活占比(路由到中档/本地)")
    ap.add_argument("--local-frac", type=float, default=0.6, help="本地回退占比(在全部调用中)")
    args = ap.parse_args()

    c_full = per_call_cost(args.avg_in, args.avg_out, args.price_flagship, args.price_flagship)
    baseline = c_full * args.calls

    # A: 路由分级 —— 贱活(cheap_frac)走中档，其余旗舰
    c_cheap = per_call_cost(args.avg_in, args.avg_out, args.price_mid, args.price_mid)
    a_cost = (c_cheap * args.cheap_frac + c_full * (1 - args.cheap_frac)) * args.calls

    # B: A + 批处理折扣(整体)
    b_cost = a_cost * (1 - args.batch_disc)

    # C: B + 本地回退(local_frac 任务零费，其中贱活本就中档，贵活部分本地)
    # 本地回退从「非贱活的旗舰部分」里再切 local_frac 出去
    premium_frac = (1 - args.cheap_frac)
    local_from_premium = min(args.local_frac, premium_frac)
    remaining_premium = premium_frac - local_from_premium
    # 注意：本地部分总价 = price_local * (本地调用数)；本地调用数已含 ×calls，
    # 不能在外层再 ×calls（否则本地项被平方放大成百万级溢出）。
    c_cost = (c_cheap * args.cheap_frac + c_full * remaining_premium) * args.calls \
             + args.price_local * (local_from_premium * args.calls)
    c_cost *= (1 - args.batch_disc)

    def pct(v):
        # 钳制到 [0,100]：本地回退不可能比基线更贵，越界即异常输入
        return max(0.0, min(100.0, (1 - v / baseline) * 100)) if baseline else 0.0

    print(f"{'方案':<22}{'月成本(USD)':>14}{'节省':>10}")
    print("-" * 48)
    print(f"{'基线 全旗舰实时':<22}{baseline:>14.2f}{'—':>10}")
    print(f"{'A 路由分级':<22}{a_cost:>14.2f}{pct(a_cost):>9.1f}%")
    print(f"{'B +批处理折扣':<22}{b_cost:>14.2f}{pct(b_cost):>9.1f}%")
    print(f"{'C +本地回退':<22}{c_cost:>14.2f}{pct(c_cost):>9.1f}%")
    print()
    print(f"最高可省：{pct(c_cost):.1f}%  (≈ ${baseline - c_cost:.2f}/月)")


if __name__ == "__main__":
    main()
