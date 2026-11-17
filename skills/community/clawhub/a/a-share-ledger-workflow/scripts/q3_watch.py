#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
q3_watch.py — 第5步 Q3 财报披露监控（第0步 Python 前置）

用途：cron 第0步先跑本脚本，只在「有标的已披露 Q3」时才调模型。
未披露 → SILENT（不发飞书、不发邮件），这是最常见分支。

标的清单＝扫台账目录自动得出（见 scan_ledger），建台账即纳入，不维护手工清单。
  下面的 RESERVED / DIRECTION_HINT 是**虚构示例**，换成你自己的标的：
  方向A   示例标的600000 示例标的600001
  方向B   示例标的600002
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

from data_guard import fetch_status, summary_line
# ── 数据根目录（环境变量；未设置即报错，不回落任何具体路径）──────────────
_D = os.environ.get("STOCK_DATA_DIR", "").rstrip("/")
if not _D:
    raise SystemExit(
        "🔴 未设置环境变量 STOCK_DATA_DIR（你的股票数据根目录）。\n"
        '   例：export STOCK_DATA_DIR="$HOME/stock_data"\n'
        "   目录结构见 README「数据目录约定」。"
    )



TZ = timezone(timedelta(hours=8))
# 🔴 窗口天数：持仓公告扫描只看最近这么多天。
#   在**运行时**计算，不要写成模块级常量 —— 写死会让窗口永远停在某个日期。
RISK_WINDOW_DAYS = 7

LEDGER = _D + "/股票台账/候选"
# 🔴 第7步持仓台账目录 —— 公告扫描要覆盖，不能只扫候选
HOLD = _D + "/股票台账/持仓中"

# 财报类公告标题关键词：判定「已披露」。漏一个关键字＝整批标的静默过期。
Q3_KEYS = ("第三季度报告", "三季度报告", "2026年第三季度", "Q3")

# 🔴 公告扫描要盯的关键字（与 Q3_KEYS 分开：这里盯的是「任何值得看的公告」）
# 漏一个 = 某类风险公告静默漏检
RISK_KEYS = (
    "业绩预告", "业绩快报", "业绩预亏", "业绩修正",
    "减持", "增持", "回购", "股份质押", "解除质押",
    "重大资产重组", "收购", "出售资产", "对外投资",
    "诉讼", "仲裁", "立案", "处罚", "问询函", "关注函", "监管函", "警示函",
    "停牌", "复牌", "风险提示", "退市", "ST",
    "合同", "中标", "订单", "合作", "协议",
    "定增", "配股", "可转债", "募集资金",
    "分红", "送转", "股权激励",
)

# 预约披露日：仅作提示，未知就是 None（不是故障）
RESERVED = {
    # 预约披露日示例（虚构代码+日期，换成你自己的；未知就写 None 或不填）
    "600000": "2026-10-27", "600001": "2026-10-28",
}

# 方向标签：给台账正文里的方向词（只用于输出可读性，取不到就是 "?"）
DIRECTION_HINT = {
    # 方向标签示例（虚构，换成你自己的；bench.json 有 direction 字段的可留空，输出取不到就显示 "?"）
    "600000": "方向A", "600001": "方向A", "600002": "方向B",
}


def scan_ledger(holdings_only=False):
    """⭐ 标的清单＝扫台账目录（建台账即纳入），与 candidate_gate.py 同源。

    🔴 为什么不写死 13 只：写死的清单每次新增台账都会静默漏掉，
    而 Q3 披露监控漏标的＝持仓/候选的财报基线悄悄过期，无人知晓。
    缺字典的标的照样纳入，只是方向标签显示 '?'。
    holdings_only=True 时只扫第7步持仓台账。
    """
    root = HOLD if holdings_only else LEDGER
    out = []
    try:
        for fn in sorted(os.listdir(root)):
            if not fn.endswith("_跟踪台账.md"):
                continue
            parts = fn.split("_")
            if len(parts) < 3 or len(parts[1]) != 6 or not parts[1].isdigit():
                continue
            out.append((parts[0], parts[1]))
    except Exception as exc:
        return None, f"台账目录不可读（{root}）：{type(exc).__name__}: {exc}"
    return out, ""


def fetch_announcements(code, pages=2):
    """东财公告接口。返回三态（OK / EMPTY / FETCH_FAIL）。"""
    def _do():
        got = []
        for pg in range(1, pages + 1):
            url = ("https://np-anotice-stock.eastmoney.com/api/security/ann"
                   f"?page_size=50&page_index={pg}&ann_type=A&client_source=web&stock_list={code}")
            r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", "Mozilla/5.0", url],
                               capture_output=True, text=True, timeout=30)
            d = json.loads(r.stdout)
            lst = (d.get("data") or {}).get("list") or []
            if not lst:
                break
            got += lst
        return got

    return fetch_status(_do, tries=2, delay=0.5)


def check_one(name, code, holdings=False, since=None):
    """since 只在 holdings 模式用；不要写成默认参数（绑定时机早于运行时计算）。"""
    rec = {"name": name, "code": code, "direction": "持仓" if holdings else DIRECTION_HINT.get(code, "?"),
           "reserved": RESERVED.get(code), "q3": None, "state": "UNKNOWN",
           "art_code": None, "ann_date": None, "pdf_url": None}

    r = fetch_announcements(code)
    if r.state == "FETCH_FAIL":
        # 🔴 取数失败 ≠ 未披露。必须显式上报，不能落到 PENDING 分支。
        rec["state"] = "FETCH_FAIL"
        rec["error"] = r.error
        return rec
    arts = r.value or []

    if holdings:
        # 持仓模式：盯风险类公告（近 RISK_WINDOW_DAYS 天），不是财报
        rec["since"] = since
        recent = [a for a in arts
                  if since and (a.get("notice_date") or "") >= since]
        hits = [a for a in recent
                if any(k in (a.get("title") or "") for k in RISK_KEYS)]
        hits.sort(key=lambda a: a.get("notice_date") or "", reverse=True)
        rec["risk_announcements"] = [
            {"title": a.get("title"), "date": (a.get("notice_date") or "")[:10],
             "pdf_url": f"https://pdf.dfcfw.com/pdf/H2_{a.get('art_code')}_1.pdf"}
            for a in hits[:8]
        ]
        rec["recent_total"] = len(recent)
        rec["state"] = "RISK_FOUND" if hits else "CLEAR"
        rec["latest_ann"] = (max((a.get("notice_date") or "") for a in arts)[:10]
                            if arts else None)
        return rec

    hits = [a for a in arts
            if any(k in (a.get("title") or "") for k in Q3_KEYS)
            and (a.get("notice_date") or "") >= "2026-10-01"]
    if hits:
        best = max(hits, key=lambda a: a.get("notice_date") or "")
        rec["state"] = "DISCLOSED"
        rec["ann_date"] = (best.get("notice_date") or "")[:10]
        rec["art_code"] = best.get("art_code")
        rec["pdf_url"] = f"https://pdf.dfcfw.com/pdf/H2_{best.get('art_code')}_1.pdf"
        rec["title"] = best.get("title")
    else:
        latest = max((a.get("notice_date") or "") for a in arts) if arts else None
        rec["state"] = "PENDING"
        rec["latest_ann"] = latest[:10] if latest else None
    return rec


def main():
    argv = sys.argv[1:]
    holdings = "--holdings" in argv
    path = argv[argv.index("--json-out") + 1] if "--json-out" in argv else None

    targets, err = scan_ledger(holdings_only=holdings)
    if targets is None:
        # 目录都读不到 = 全盘失效，不是「无标的」
        print(f"🔴 取数失败 · 台账目录扫描失败：{err}")
        print("action=FETCH_FAIL")
        return 1

    # 🔴 窗口在**运行时**算：写死会让窗口永远停在某个日期
    since = (datetime.now(TZ) - timedelta(days=RISK_WINDOW_DAYS)).strftime("%Y-%m-%d")
    results = [check_one(*w, holdings=holdings, since=since) for w in targets]
    failed = [r for r in results if r["state"] == "FETCH_FAIL"]

    out = {"mode": "holdings" if holdings else "candidates",
           "since": since, "window_days": RISK_WINDOW_DAYS,
           "failed": len(failed), "total": len(results), "results": results}
    if path:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

    return _render_holdings(results, failed, out, path) if holdings \
        else _render_candidates(results, failed, out, path)


def _render_holdings(results, failed, out, path):
    """持仓模式：只有「有风险公告」或「取数失败」才输出。
    🔴 CLEAR = 无风险公告 = 静默，不调模型。"""
    hit = [r for r in results if r["state"] == "RISK_FOUND"]
    if failed and len(failed) == len(results):
        action, why = "FAULT_ONCE", f"全部 {len(failed)} 只公告接口失败"
    elif failed:
        action, why = "REVIEW", f"{len(failed)} 只取数失败（{'、'.join(r['name'] for r in failed)}）"
    elif hit:
        action = "REVIEW"
        why = f"{len(hit)} 只有风险类公告：{'、'.join(r['name'] for r in hit)}"
    else:
        action, why = "SILENT", f"{len(results)} 只持仓近 {out['window_days']} 天无风险类公告"

    out["action"], out["why"] = action, why
    if path:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

    if action == "SILENT":
        print(f"[q3_watch] ✅ 持仓公告扫描：{why}（静默）")
        return 0

    print("=" * 96)
    print(f"持仓风险公告扫描｜{out['since']} 起 {out['window_days']} 天｜规则：{action}")
    print("=" * 96)
    for r in results:
        if r["state"] == "FETCH_FAIL":
            print(f"  ❌取数失败  {r['name']}({r['code']})  {r.get('error','')}")
            continue
        anns = r.get("risk_announcements") or []
        if not anns:
            print(f"  ✅无风险公告 {r['name']}({r['code']})  "
                  f"近{out['window_days']}天共{r.get('recent_total',0)}条｜最新{r.get('latest_ann')}")
            continue
        print(f"  🔔{len(anns)}条风险公告 {r['name']}({r['code']})")
        for a in anns:
            print(f"     · {a['date']}｜{a['title'][:52]}")
            print(f"       PDF: {a['pdf_url']}")
    print(f"action={action}")
    tail = summary_line([r["code"] for r in results], [r["code"] for r in failed])
    if tail:
        print(tail)
    if path:
        print(f"[JSON] {path}")
    return 0


def _render_candidates(results, failed, out, path):
    """候选模式：盯 Q3 财报披露（原行为）。"""
    disclosed = [r for r in results if r["state"] == "DISCLOSED"]

    if failed and len(failed) == len(results):
        action, why = "FAULT_ONCE", f"全部 {len(failed)} 只公告接口失败"
    elif disclosed:
        action, why = "REVIEW", f"{len(disclosed)} 只已披露 Q3：{'、'.join(r['name'] for r in disclosed)}"
    elif failed:
        action, why = "REVIEW", (f"{len(failed)} 只取数失败（{'、'.join(r['name'] for r in failed)}）；"
                                f"其余未披露")
    else:
        action, why = "SILENT", f"{len(results)} 只均未披露 Q3，且无新公告"

    out["action"], out["why"] = action, why
    out["disclosed"] = len(disclosed)
    if path:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

    print("=" * 96)
    print(f"Q3 披露监控｜规则：{action}｜{why}")
    print("=" * 96)
    for r in results:
        mark = {"DISCLOSED": "🔔已披露", "PENDING": "⏳未披露",
                "FETCH_FAIL": "❌取数失败", "UNKNOWN": "?"}[r["state"]]
        extra = (f" {r['ann_date']}｜PDF={r['pdf_url']}" if r["state"] == "DISCLOSED"
                 else (f" 最新公告{r.get('latest_ann')}" if r["state"] == "PENDING"
                       else f" {r.get('error','')}"))
        print(f"  {mark:<8} {r['name']:<8}{r['code']:<9}{r['direction']:<9}{extra}")
    print("-" * 96)
    print(f"总计 {len(results)}｜🔔已披露 {len(disclosed)}｜⏳待披露 "
          f"{len(results)-len(disclosed)-len(failed)}｜❌失败 {len(failed)}")
    print(f"action={action}")
    # 🔴 汇总行非空即触发投递：no_agent 判定是「stdout 非空」
    tail = summary_line([r["code"] for r in results], [r["code"] for r in failed])
    if tail:
        print(tail)
    if path:
        print(f"[JSON] {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)