#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一键跑通演示：口径 → 公式 → 闸门 → 四层漏斗 → 评分管道 → 风控信号表。

用法：
    python3 strategy/run_demo.py
    python3 strategy/run_demo.py --data strategy/sample_data.json --equity 2000000

退出码 0 表示管道正常完成；1 表示输入校验失败。
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from strategy import calibers as C          # noqa: E402
from strategy import formulas as F          # noqa: E402
from strategy import funnel as FN           # noqa: E402
from strategy import pipeline as PL         # noqa: E402
from strategy import playbook as PB         # noqa: E402
from strategy import risk as RK             # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
BAR = "=" * 68


def h1(t: str) -> None:
    print(f"\n{BAR}\n {t}\n{BAR}")


def h2(t: str) -> None:
    print(f"\n--- {t} " + "-" * max(0, 60 - len(t)))


def load(path: pathlib.Path) -> dict:
    if not path.exists():
        print(f"[!] 数据文件不存在：{path}", file=sys.stderr)
        sys.exit(1)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[!] JSON 解析失败 {path}: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> int:
    ap = argparse.ArgumentParser(description="A股龙虎榜 + 财富密码策略演示")
    ap.add_argument("--data", default=str(HERE / "sample_data.json"), help="候选数据 JSON")
    ap.add_argument("--equity", type=float, default=None, help="账户权益（覆盖数据文件）")
    ap.add_argument("--stage", default=None, help="市场阶段 I/II/III/IV")
    ap.add_argument("--ice", action="store_true", help="强制按冰点处理")
    args = ap.parse_args()

    data = load(pathlib.Path(args.data))
    ctx = data.get("context", {}) or {}
    equity = args.equity if args.equity is not None else float(ctx.get("equity", 1_000_000))
    stage = (args.stage or ctx.get("stage", "II")).upper()
    ice = bool(args.ice or ctx.get("ice_point", False))

    # 若数据未显式给冰点，则用三条件判定
    if not ice and all(k in ctx for k in ("limit_up_count", "broken_rate", "index_pct")):
        ice = F.is_ice_point(int(ctx["limit_up_count"]), float(ctx["broken_rate"]), float(ctx["index_pct"]))

    h1("A股龙虎榜深度研判 + 财富密码策略 —— 策略包演示")
    h2("口径（唯一来源 strategy/calibers.py）")
    print(C.describe())

    h2("市场环境")
    print(f"  权益：{equity:,.0f} 元｜阶段：{stage}｜冰点：{'是' if ice else '否'}")
    print(f"  α_max = {F.alpha_max(stage, ice):.1%}"
          f"（上限 {equity * F.alpha_max(stage, ice):,.0f} 元）")
    print(f"  单笔风险 r = {F.RISK_R_ICE if ice else F.RISK_R_NORMAL:.2%}")

    # ---------------------------------------------------------- 四层漏斗
    h2("四层漏斗 L1 → L2 → L2.5 → L3")
    inds = [FN.Industry(i["code"], i["name"], float(i["rank"]), float(i["vr"]),
                        float(i.get("dispersion", 0.0)), i.get("note", ""))
            for i in data.get("industries", [])]
    stocks = []
    for c in data.get("candidates", []):
        raw = {k: v for k, v in c.items()
               if k not in ("code", "name", "sector", "rank", "vr", "note")}
        stocks.append(FN.Stock(c["code"], c["name"], c.get("sector", ""),
                               float(c["rank"]) if c.get("rank") is not None else None,
                               float(c["vr"]) if c.get("vr") is not None else None,
                               raw))

    print("\n  [L1] 行业扫描")
    for i in inds:
        tag = "入池" if i.rank <= C.RANK_LOW_THRESHOLD else "未入池"
        chain = "（链主题·跳过否决）" if C.is_chain_theme(i.name) else ""
        disp = FN.dispersion_alert(i.dispersion) if i.dispersion else "—"
        print(f"    {tag:4} {i.name:8} 分位 {i.rank:5.1f}%  额比 {i.vr:5.2f}×  {chain}  {disp}")

    fr = FN.run_funnel(inds, stocks)
    print(f"\n  [L2]   入池 {len(fr.l2_pass)} 只：" +
          ("、".join(s.name for s in fr.l2_pass) or "无"))
    print(f"  [L2.5] 剔除 {len(fr.l2_5_removed)} 只：")
    for g in fr.l2_5_removed:
        print(f"         ✕ {g.name} —— {g.reasons[0]}")
    print(f"  [L3]   否决 {len(fr.l3_vetoed)} 只：")
    for g in fr.l3_vetoed:
        print(f"         ✕ {g.name} —— {g.reasons[0]}")
    print(f"  最终通过 {len(fr.l3_pass)} 只：" +
          ("、".join(s.name for s in fr.l3_pass) or "无"))

    h2("敏感度（口径③收紧会改变过会数量，必须随报告披露）")
    print(f"  50% 相对线（默认）→ {fr.sensitivity['rule_50pct_relative']} 只过会")
    print(f"  任何减速即排除      → {fr.sensitivity['rule_any_deceleration']} 只过会")
    delta = fr.sensitivity['rule_50pct_relative'] - fr.sensitivity['rule_any_deceleration']
    print(f"  → ±{abs(delta)} 只敏感度，报告首页必须写明该口径依赖")

    # ---------------------------------------------------------- 评分管道
    # 把 funnel 的 l3_pass 喂给 pipeline：技术面已过 L2，可交易性已过 L2.5，
    # 财务面已过 L3 —— 只剩「综合分 → BUY/WATCH/AVOID」与 α 账本。
    # 若绕过 funnel 直接喂原始候选，pipeline 会让某些标的「高分但技术面不过 L2」
    # 通过 —— 这是已知缺陷，调用方必须保证 funnel 在前。
    funnel_pass = [s.merged for s in fr.l3_pass]
    if not funnel_pass:
        funnel_pass = data.get("candidates", [])
        print("  [!] funnel 无产出口降级为原始候选（仅用于 demo 演示）")
    h2("评分管道（S = 0.30·tech + 0.25·flow + 0.20·fund + 0.15·cycle + 0.10·fib）")
    result = PL.run_pipeline(funnel_pass, equity=equity, stage=stage, ice_point=ice)
    print(PL.render_signal_table(result))

    # ---------------------------------------------------------- 熔断阶梯
    h2("熔断阶梯")
    for row in RK.drawdown_table():
        print(f"  回撤 {row['threshold']:>6.0%} → {row['action']:6}  {row['note']}")

    # ---------------------------------------------------------- 盘前 6 项
    h2("盘前 6 项检查")
    for c in PB.PRE_OPEN_CHECKLIST:
        print(f"  {c['no']}. {c['item']:8} → {c['output']}")

    # ---------------------------------------------------------- 考核带
    lo, hi = F.target_band()
    h2("考核带与看板")
    print(f"  年化目标：{lo:.0%} – {hi:.0%}（按年复利）")
    print(f"  看板：{' + '.join(PB.PLAN_TARGET['dashboard'])}")
    print(f"\n  {PB.playbook()['disclaimer']}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
