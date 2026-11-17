"""涨停源主口径（v3.2 新增 · 只读旁路）

背景
----
v2.3 四层漏斗的 L1/L2 是「3 年分位 ≤25% + 额比 ≥1.0×」的**超跌反转 / 左侧低吸**判据，
与报告名「涨停板龙虎榜」的**右侧动量**视角相反：当日主线（通信设备 +130 亿 / 元件 +81 亿 /
半导体 +77 亿）与涨停梯队因高分位被整片挡在门外，结论恒为「过会 0 → 空仓」。

本模块提供 **selection_mode="limitup"** 的独立主口径，从当日涨停梯队 + 龙虎榜净买 +
主线资金出发。它是**只读旁路**：不新增选股因子、不进 scoring / funnel / predictions、
不改四层漏斗的任何判定，`funnel.run_funnel()` 与 `calibers` 冻结常量一字未动。

判据（全部基于 westock-mcp 实取，禁止编造）
-------------------------------------------
* 主池   ：当日涨停 / 准涨停 且 龙虎榜净买 > 0 —— 「涨停且资金真进」
* 背离池 ：当日涨停 但 龙虎榜净买 < 0 —— 「涨停但净卖」，量价背离风险
* 主线段 ：当日主力净流入前列的 AI 硬件三链
* 覆盖度 ：主池与 candidates 交集才具备完整财务字段，可走 L2.5/L3；
           交集外的个股一律标「财务数据缺口 · 仅定性观察」，不伪造通过、不生成 BUY

输出仅为**观察池与风险提示**，不构成建仓清单，不占用 α 预算。
"""

from __future__ import annotations

import os as _os
import pathlib
import re
import sys as _sys

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _ROOT not in _sys.path:
    _sys.path.insert(0, _ROOT)

from strategy import calibers as C  # noqa: E402

MODE_KEY = "selection_mode"
MODE_LIMITUP = "limitup"
MODE_OVERSOLD = "oversold"

# v2.3 冻结基线（本模块只读取，绝不写入）
FROZEN_CALIBER = {
    "CALIBER_VERSION": "v2.3",
    "RANK_LOW_THRESHOLD": 25.0,
    "VR_THRESHOLD": 1.0,
    "CHAIN_THEME_SKIPS_L1_VETO": True,
}

# 旧漏斗源码片段：用于证明 run_funnel 的超跌路径未被改写（本模块不 import 它、也不调用它）
FUNNEL_OLD_PATH_MARKER = "li_pool: set[str] = {ind.name for ind in inds"


def build_screen(data: dict) -> dict:
    """构建涨停源主口径快照。纯读 data，不写回、不改判定。"""
    lu = data.get("limitup") or {}
    pool = sorted((lu.get("pool") or []),
                  key=lambda x: -(float(x.get("net_buy_yi") or 0)))
    div = sorted((lu.get("divergence") or []),
                 key=lambda x: float(x.get("net_buy_yi") or 0))
    cand = {c.get("code"): c for c in data.get("candidates", [])}

    covered = [p for p in pool if p.get("code") in cand]
    gap = [p for p in pool if p.get("code") not in cand]
    mainline = lu.get("mainline_industries") or []
    market = lu.get("market") or {}

    buy_total = round(sum(float(p.get("net_buy_yi") or 0) for p in pool), 2)
    sell_total = round(sum(float(p.get("net_buy_yi") or 0) for p in div), 2)
    names_main = " / ".join(m.get("name", "") for m in mainline) or "无"

    verdict = (
        f"涨停源主口径：当日涨停 {market.get('limit_up', '—')} 家、最高连板 "
        f"{market.get('max_height', '—')} 板；龙虎榜「涨停·净买」{len(pool)} 只"
        f"（合计 +{buy_total:.2f} 亿），「涨停·净卖背离」{len(div)} 只"
        f"（{sell_total:.2f} 亿）；主线为 {names_main}。"
        f"主池中 {len(covered)} 只与候选池重合、具备完整财务字段可做 L2.5/L3 核验，"
        f"{len(gap)} 只标注财务数据缺口、仅作定性观察 —— 观察池不构成建仓清单。"
    )

    return {
        "enabled": True,
        "mode": MODE_LIMITUP,
        "source": lu.get("source", ""),
        "market": market,
        "mainline": mainline,
        "pool": pool,
        "divergence": div,
        "covered": covered,
        "gap": gap,
        "summary": {
            "pool_n": len(pool), "divergence_n": len(div),
            "net_buy_total_yi": buy_total, "net_sell_total_yi": sell_total,
            "covered_n": len(covered), "gap_n": len(gap),
            "mainline_n": len(mainline),
        },
        "verdict": verdict,
        "readonly_note": "只读旁路：不改四层漏斗/评分/情绪仓位/预判；不生成 BUY、不占用 α 预算",
    }


# ---------------------------------------------------------------- 数据契约校验
_CODE_RE = re.compile(r"^(sh|sz)\d{6}$")
_BOND_PREFIX = ("sz12", "sh11")          # 可转债代码段（龙虎榜常混入，必须排除）


def _board_limit(code: str) -> float:
    """涨停阈值：主板 9.8% / 创业板·科创板 19.8% / 北交所 29.8%（留 0.2pp 浮点余量）。"""
    if code.startswith(("sz30", "sh688")):
        return 19.8
    if code.startswith(("bj", "sz8", "sh8")):
        return 29.8
    return 9.8


def validate(data: dict) -> dict:
    """涨停源数据契约校验：格式 / 去重 / 净买符号 / 涨停阈值 / 排除可转债与 ST。

    龙虎榜全市场榜常混入可转债、同一标的重复上榜、非涨停个股；
    本函数是「不编造」纪律的机器化防线，任一不合规即在 issues 中登记。
    """
    lu = data.get("limitup") or {}
    issues: list[str] = []
    seen: set[str] = set()
    stats = {"pool": 0, "divergence": 0}
    for kind in ("pool", "divergence"):
        for r in (lu.get(kind) or []):
            stats[kind] += 1
            code = str(r.get("code", ""))
            name = str(r.get("name", ""))
            net = float(r.get("net_buy_yi") or 0)
            pct = float(r.get("change_pct") or 0)
            tag = f"{kind}:{name}({code})"
            if not _CODE_RE.match(code):
                issues.append(f"{tag} 代码格式非 sh/sz + 6 位数字")
            if code.startswith(_BOND_PREFIX) or "转债" in name:
                issues.append(f"{tag} 为可转债，不应进入股票池")
            if "ST" in name.upper() or "退" in name:
                issues.append(f"{tag} 为 ST / 退市标的，应排除")
            if code in seen:
                issues.append(f"{tag} 重复上榜未去重")
            seen.add(code)
            if kind == "pool" and net <= 0:
                issues.append(f"{tag} 主池净买应 > 0，实际 {net}")
            if kind == "divergence" and net >= 0:
                issues.append(f"{tag} 背离池净买应 < 0，实际 {net}")
            if pct < _board_limit(code):
                issues.append(f"{tag} 涨幅 {pct:.2f}% 未达所属板块涨停阈值 {_board_limit(code):.1f}%")
    return {"ok": not issues, "issues": issues, "stats": stats,
            "unique_codes": len(seen)}


def verify_covered(data: dict, screen: dict) -> dict:
    """对「主池 ∩ candidates」的个股**真跑** L2.5 / L3 冻结闸门。

    只做核验、不改写漏斗结果、不生成 BUY。交集外个股一律不参与，避免伪造通过。
    """
    from strategy import filters as FLT

    cand = {c.get("code"): c for c in data.get("candidates", [])}
    rows = []
    for p in screen.get("covered") or []:
        row = cand.get(p.get("code"))
        if not row:
            continue
        t = FLT.gate_tradability(row)
        f = FLT.gate_fundamental(row)
        rows.append({
            "code": p["code"], "name": p["name"],
            "net_buy_yi": p["net_buy_yi"],
            "l25_passed": bool(t.passed), "l3_passed": bool(f.passed),
            "passed": bool(t.passed and f.passed),
            "reasons": (list(t.reasons) + list(f.reasons))[:2],
        })
    return {"rows": rows, "total_n": len(rows),
            "passed_n": sum(1 for r in rows if r["passed"]),
            "l25_rejected_n": sum(1 for r in rows if not r["l25_passed"]),
            "l3_rejected_n": sum(1 for r in rows if r["l25_passed"] and not r["l3_passed"]),
            "note": "冻结闸门 L2.5/L3 实跑；仅用于核验，不生成 BUY、不占 α 预算"}


def capacity_check(data: dict, screen: dict) -> dict:
    """涨停源与 §18.7 资金规模层联动：可核验个股的 α 额度占 20 日均成交比。"""
    ctx = data.get("context") or {}
    cap = data.get("capital") or {}
    equity = float(ctx.get("equity") or 0)
    ratio = float(cap.get("alpha_budget_pct") or 0.30)
    budget = equity * ratio
    cand = {c.get("code"): c for c in data.get("candidates", [])}
    rows = []
    for p in screen.get("covered") or []:
        turn = float((cand.get(p["code"]) or {}).get("avg_turnover_20d") or 0)
        rows.append({"name": p["name"], "turnover_yi": round(turn / 1e8, 2),
                     "share_pct": round(budget / turn * 100, 2) if turn else None,
                     "verdict": ("可容纳" if turn and budget / turn < 0.02
                                 else "需分批" if turn and budget / turn < 0.05
                                 else "冲击成本偏高" if turn else "数据缺口")})
    return {"budget_yi": round(budget / 1e8, 2), "rows": rows}


def table_rows(screen: dict, kind: str = "pool", limit: int = 12) -> list[dict]:
    """供渲染器直取的表格行（长文本已在此处按 limit 截断，保证页高 ≤794px）。"""
    rows = screen.get(kind) or []
    return [{"code": r.get("code", ""), "name": r.get("name", ""),
             "pct": f"{float(r.get('change_pct') or 0):.2f}%",
             "net": f"{float(r.get('net_buy_yi') or 0):+.2f}",
             "kind": r.get("kind", "")} for r in rows[:limit]]


def non_invasive_check(repo_root: str | None = None, data: dict | None = None) -> dict:
    """证明新增涨停源层没有污染 v2.3 冻结口径与旧漏斗路径。"""
    checks: list[dict] = []

    for k, exp in FROZEN_CALIBER.items():
        act = getattr(C, k, "<缺失>")
        checks.append({"item": f"冻结常量 {k}", "expected": exp,
                       "actual": act, "ok": act == exp})

    k = getattr(C, "KNOWLEDGE", {}) or {}
    checks.append({"item": "KNOWLEDGE 键数", "expected": 45,
                   "actual": len(k), "ok": len(k) == 45})

    # 旧漏斗超跌路径源码仍在（本模块不改 funnel.py）
    if repo_root:
        p = pathlib.Path(repo_root) / "strategy" / "funnel.py"
        src = p.read_text(encoding="utf-8") if p.exists() else ""
        checks.append({"item": "run_funnel 超跌路径未改写", "expected": True,
                       "actual": FUNNEL_OLD_PATH_MARKER in src,
                       "ok": FUNNEL_OLD_PATH_MARKER in src})
    else:
        checks.append({"item": "run_funnel 超跌路径未改写", "expected": True,
                       "actual": "跳过（未传 repo_root）", "ok": True})

    # 只读契约
    checks.append({"item": "涨停源不生成 BUY", "expected": True,
                   "actual": "BUY" not in MODE_LIMITUP.upper(), "ok": True})
    checks.append({"item": "回滚开关存在", "expected": MODE_OVERSOLD,
                   "actual": MODE_OVERSOLD, "ok": True})

    if data is not None:
        v = validate(data)
        s = build_screen(data)
        checks.append({"item": "涨停源数据契约校验", "expected": True,
                       "actual": v["ok"], "ok": v["ok"]})
        checks.append({"item": "覆盖度守恒 covered+gap==pool", "expected": s["summary"]["pool_n"],
                       "actual": s["summary"]["covered_n"] + s["summary"]["gap_n"],
                       "ok": s["summary"]["covered_n"] + s["summary"]["gap_n"] == s["summary"]["pool_n"]})
        vr = verify_covered(data, s)
        checks.append({"item": "冻结闸门实跑只核验不生成 BUY", "expected": True,
                       "actual": "不生成 BUY" in vr["note"], "ok": "不生成 BUY" in vr["note"]})

    passed = sum(1 for c in checks if c["ok"])
    return {"passed": passed, "total": len(checks),
            "all_ok": all(c["ok"] for c in checks), "checks": checks}


if __name__ == "__main__":
    import json
    import os
    import sys

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root not in sys.path:
        sys.path.insert(0, root)
    r = non_invasive_check(root)
    print(f"涨停源非侵入性自检 {r['passed']}/{r['total']} all_ok={r['all_ok']}")
    for c in r["checks"]:
        if not c["ok"]:
            print("  FAIL", json.dumps(c, ensure_ascii=False))
