#!/usr/bin/env python3
"""
自动复盘引擎（复盘闭环第二步）

读 trading/journal/trades.json → 按「形态」统计胜率/期望，产出复盘报告。
可选：从券商 CSV 导入成交记录（FIFO 配对成笔）。

用法:
  python3 .../review.py                     # 按形态统计 + 写 trading/records/review-<date>.md
  python3 .../review.py --days 60           # 只看近 60 天入场的
  python3 .../review.py --import-csv <csv>  # 导入券商交割单(通用: date,code,name,side,price,qty[,fee])
  python3 .../review.py --lessons           # 顺带把结论追加进 references/lessons.md
"""
import argparse
import csv
import datetime as dt
import os
import statistics
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from radar_common import PATTERNS, load_journal, save_journal, ws_root  # noqa: E402


def group_stats(rows):
    out = {}
    for pat in PATTERNS:
        rs = [r for r in rows if r.get("pattern") == pat and r.get("pnl_pct") is not None]
        if not rs:
            continue
        pnls = [r["pnl_pct"] for r in rs]
        wins = [p for p in pnls if p > 0]
        losses = [p for p in pnls if p <= 0]
        out[pat] = {
            "n": len(rs),
            "win_rate": round(len(wins) / len(rs) * 100, 1),
            "avg": round(statistics.mean(pnls), 2),
            "avg_win": round(statistics.mean(wins), 2) if wins else 0.0,
            "avg_loss": round(statistics.mean(losses), 2) if losses else 0.0,
            "max_win": round(max(pnls), 2),
            "max_loss": round(min(pnls), 2),
            "expectancy": round(statistics.mean(pnls), 2),
        }
    return out


def _import_csv(path):
    """通用券商成交 CSV → FIFO 配对成笔 → 追加到 journal（仅新增 code 与新日期）。"""
    rows = load_journal()
    opens = {}   # code -> list of buy legs
    new = []
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for rec in reader:
            low = {k.lower().strip(): (v or "").strip() for k, v in rec.items()}
            def pick(*names):
                for n in names:
                    if n in low and low[n] != "":
                        return low[n]
                return ""
            date = pick("date", "成交日期", "交易日期", "trade_date")[:10]
            code = pick("code", "证券代码", "股票代码", "symbol")
            name = pick("name", "证券名称", "股票名称")
            side = pick("side", "买卖", "方向", "操作", "trade_type")
            price = pick("price", "成交价", "成交均价", "price")
            qty = pick("qty", "数量", "成交数量", "成交量", "shares")
            try:
                price = float(price); qty = float(qty)
            except Exception:
                continue
            is_buy = side.upper().startswith("B") or "买" in side or side.upper() in ("BUY",)
            if is_buy:
                opens.setdefault(code, []).append({"date": date, "price": price, "qty": qty, "name": name})
            else:
                legs = opens.get(code, [])
                remain = qty
                while remain > 0 and legs:
                    leg = legs[0]
                    use = min(remain, leg["qty"])
                    tid = max([r["id"] for r in rows + new], default=0) + 1
                    pnl = round((price - leg["price"]) / leg["price"] * 100, 2)
                    new.append({
                        "id": tid, "date_in": leg["date"], "code": code,
                        "name": name or leg["name"], "pattern": "其他",
                        "entry": leg["price"], "stop": None, "target": None, "size": None,
                        "date_out": date, "exit": price, "reason": "CSV导入",
                        "pnl_pct": pnl, "win": pnl > 0, "note": "导入自 " + os.path.basename(path),
                    })
                    leg["qty"] -= use
                    remain -= use
                    if leg["qty"] <= 0:
                        legs.pop(0)
    save_journal(rows + new)
    print("✅ CSV 导入完成：新增 {} 笔（形态待人工归类为 N字/平台突破/一阳穿三阴/竞价异动）".format(len(new)))
    return new


def main():
    ap = argparse.ArgumentParser(description="自动复盘")
    ap.add_argument("--days", type=int, default=0, help="只看近 N 天入场")
    ap.add_argument("--import-csv", default="", help="券商成交 CSV 路径")
    ap.add_argument("--lessons", action="store_true", help="把结论追加进 references/lessons.md")
    a = ap.parse_args()

    if a.import_csv:
        _import_csv(a.import_csv)

    rows = load_journal()
    if a.days:
        cut = (dt.date.today() - dt.timedelta(days=a.days)).isoformat()
        rows = [r for r in rows if (r.get("date_in") or "") >= cut]

    closed = [r for r in rows if r.get("pnl_pct") is not None]
    stats = group_stats(rows)

    lines = []
    lines.append("# 交易复盘（自动生成）")
    lines.append("")
    lines.append("生成时间：" + dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
    lines.append("样本：已平仓 {} 笔（{}）".format(
        len(closed), "近{}天".format(a.days) if a.days else "全部"))
    lines.append("")
    if not closed:
        lines.append("> 暂无已平仓记录。请先用 `trade_log.py add/close` 录入，或用 `--import-csv` 导入券商交割单。")
    else:
        allp = [r["pnl_pct"] for r in closed]
        wins = [p for p in allp if p > 0]
        lines.append("## 总览")
        lines.append("- 总胜率：{}/{} = **{:.1f}%**".format(len(wins), len(closed), len(wins) / len(closed) * 100))
        lines.append("- 平均单笔：{:+.2f}%　期望值：{:+.2f}%".format(
            statistics.mean(allp), statistics.mean(allp)))
        lines.append("- 最大盈利：{:+.2f}%　最大亏损：{:+.2f}%".format(max(allp), min(allp)))
        lines.append("")
        lines.append("## 分形态胜率")
        lines.append("")
        lines.append("| 形态 | 笔数 | 胜率 | 期望值 | 平均盈 | 平均亏 |")
        lines.append("|---|---|---|---|---|---|")
        for pat, s in sorted(stats.items(), key=lambda kv: -kv[1]["expectancy"]):
            lines.append("| {} | {} | {:.1f}% | {:+.2f}% | {:+.2f}% | {:+.2f}% |".format(
                pat, s["n"], s["win_rate"], s["expectancy"], s["avg_win"], s["avg_loss"]))
        lines.append("")
        best = max(stats.items(), key=lambda kv: kv[1]["expectancy"], default=None)
        worst = min(stats.items(), key=lambda kv: kv[1]["expectancy"], default=None)
        if best and worst:
            lines.append("**结论**：{} 期望最高（{:+.2f}%），{} 最差（{:+.2f}%）。".format(
                best[0], best[1]["expectancy"], worst[0], worst[1]["expectancy"]))

    report = "\n".join(lines) + "\n"
    out = os.path.join(ws_root(), "trading", "records", "review-{}.md".format(dt.date.today().isoformat()))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(report)
    print(report)
    print("→ 已写入 {}".format(os.path.relpath(out, ws_root())))

    if a.lessons and closed:
        lp = os.path.join(ws_root(), "skills", "trading-desk", "references", "lessons.md")
        os.makedirs(os.path.dirname(lp), exist_ok=True)
        with open(lp, "a", encoding="utf-8") as f:
            f.write("\n\n## 复盘自动汇总（{}）\n".format(dt.date.today().isoformat()))
            for pat, s in sorted(stats.items(), key=lambda kv: -kv[1]["expectancy"]):
                f.write("- {}：{}笔，胜率{:.1f}%，期望{:+.2f}%\n".format(
                    pat, s["n"], s["win_rate"], s["expectancy"]))
        print("→ 已追加进 references/lessons.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
