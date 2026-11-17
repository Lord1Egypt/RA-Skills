#!/usr/bin/env python3
"""rebuild_bench.py —— 从台账「方向起点基准」排名表重算 bench_pt，只读对账。

解决的问题：bench.json 里的 `bench_pt` 与台账正文的「相对中位」是两份数据，
一边复算、另一边没跟，就会出现「台账写 +18.89、bench 写 20.2」而无人发现。
本脚本让 bench_pt 变成**派生物**：从中位与涨幅算出，不再手填。

    用排名表的【起点/终点收盘】重算涨幅（无价格时退回表内「区间涨跌」列）
      → 算方向中位（口径：平均；偶数样本取中位两数均值）
      → 算每只的相对中位 → 与 bench.json 现值对照

🔴 只读：不写台账、不写 bench.json。
🔴 中位口径固定为「平均」，不要各方向自定：同一套数据用不同中位口径，
   相对值会整体偏移（实测两个方向分别用「上中位」和「平均」，差 1.05pt）。

用法：
    export STOCK_DATA_DIR=/path/to/your_stock_data
    python3 scripts/rebuild_bench.py            # 人读对账表
    python3 scripts/rebuild_bench.py --emit     # 输出可粘进 bench.json 的 bench_pt 块
退出码：0 = 全部一致；1 = 有差异 / 有结构问题。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

TOL = 0.15
MINUS = {ord("\u2212"): "-", ord("\uff0d"): "-", ord("\u2013"): "-", ord("\u2014"): "-"}


def data_dir() -> Path:
    d = os.environ.get("STOCK_DATA_DIR", "").rstrip("/")
    if not d:
        raise SystemExit(
            "🔴 未设置 STOCK_DATA_DIR（你的股票数据根目录）。\n"
            "   例：export STOCK_DATA_DIR=\"$HOME/stock_data\""
        )
    return Path(d)


def norm_num(s):
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return float(s)
    s = str(s).translate(MINUS).replace(",", "").replace("¥", "").replace("**", "")
    s = s.replace("+", "").replace("%", "").replace("pt", "").replace("PT", "")
    s = s.strip().strip("*").strip()
    try:
        return float(s)
    except ValueError:
        return None


ROW_RE = re.compile(
    r"^\|\s*\d+\s*\|"                 # 排名（可选，部分台账无排名列）
    r"[^|]*?(\d{6})[^|]*\|"           # 标的（含 6 位代码）
    r"([^|]*)\|"                      # 起点收盘 或 区间涨跌
    r"([^|]*)\|?"                     # 终点收盘（有价格时）
)
RANK_ROW_PRICE = re.compile(
    r"^\|\s*\d+\s*\|[^|]*?(\d{6})[^|]*\|\s*([^|]*?¥[^|]*)\|\s*([^|]*?¥[^|]*)\|"
    r"\s*([^|]*)\|"
)
RANK_ROW_PCT = re.compile(
    r"^\|\s*\d+\s*\|[^|]*?(\d{6})[^|]*\|\s*([+\-\u2212]?[\d.]+%)\s*\|?\s*$"
)


def parse_tables(text: str, name_map: dict | None = None):
    """→ rows [{code, pct, stated_rel}], base_line。

    两种表体都吃：
      · 价格表 `| 1 | 某某 600000 | ¥10.0 | ¥11.0 | +10% |` → 用收盘价重算涨幅
      · 涨跌表 `| 1 | 某某 | +5.00% |`                     → 直接用该列
    行内没有 6 位代码时，用台账文件名建的 name_map 反查（示例数据即如此）。
    """
    name_map = name_map or {}
    rows, seen = [], set()
    for line in text.splitlines():
        s = line.strip()
        if not (s.startswith("|") and re.match(r"^\|\s*\d+\s*\|", s)):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 3:
            continue
        body = " | ".join(cells[1:-1]) if len(cells) > 3 else cells[1]
        code = next((m.group(0) for m in re.finditer(r"\d{6}", cells[1])), None)
        if not code:
            for nm, cd in name_map.items():
                if nm and nm in cells[1]:
                    code = cd
                    break
        if not code or code in seen:
            continue
        prices = [norm_num(c) for c in cells if "¥" in c]
        prices = [p for p in prices if p]
        if len(prices) >= 2 and prices[0]:
            pct = round((prices[1] / prices[0] - 1) * 100, 2)
        else:
            pct = next((norm_num(c) for c in cells[2:] if "%" in c), None)
        if pct is None:
            continue
        rel = next((norm_num(c) for c in cells[2:] if "pt" in c.lower()), None)
        seen.add(code)
        rows.append({"code": code, "pct": pct, "stated_rel": rel})
    base = ""
    for line in text.splitlines():
        if ("基准起点" in line or "起点日" in line) and ("基准终点" in line or "终点日" in line):
            base = line.strip().lstrip("> ").strip()
            break
    return rows, base


def pick_median(pcts):
    s = sorted(pcts)
    n = len(s)
    if n % 2:
        return s[n // 2]
    return round((s[n // 2 - 1] + s[n // 2]) / 2, 2)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true", help="输出 bench_pt 候选块（不写盘）")
    args = ap.parse_args()

    d = data_dir()
    bench_file = d / "bench.json"
    if not bench_file.exists():
        raise SystemExit(f"🔴 找不到 {bench_file}")
    data = json.loads(bench_file.read_text(encoding="utf-8"))
    stock = data.get("stock") or {}
    if not stock:
        raise SystemExit("🔴 bench.json 的 stock 为空")

    ledgers = sorted(list((d / "股票台账" / "候选").glob("*.md"))
                     + list((d / "股票台账" / "持仓中").glob("*.md")))
    if not ledgers:
        raise SystemExit(f"🔴 {d}/股票台账 下没有台账")

    # 按 bench.json 里的 direction 归组
    label_of = {c: (v.get("direction") or "未标注") for c, v in stock.items()}
    name_map = {}
    for f in ledgers:
        m = re.match(r"(.+?)_(\d{6})_", f.name)
        if m:
            name_map[m.group(1)] = m.group(2)
    by_label = {}
    for f in ledgers:
        rows, base = parse_tables(f.read_text(encoding="utf-8"), name_map)
        if len(rows) < 2:
            continue
        votes = {}
        for r in rows:
            lb = label_of.get(r["code"])
            if lb:
                votes[lb] = votes.get(lb, 0) + 1
        if not votes:
            continue
        lb = max(votes.items(), key=lambda kv: (kv[1], kv[0]))[0]
        by_label.setdefault(lb, []).append({"file": f.name, "rows": rows, "base": base})

    struct, recomputed, medians = [], {}, {}
    for lb, ts in by_label.items():
        canon = sorted(ts, key=lambda t: -len(t["rows"]))[0]
        med = pick_median([r["pct"] for r in canon["rows"]])
        medians[lb] = {"n": len(canon["rows"]), "median": med, "file": canon["file"]}
        sizes = {}
        for t in ts:
            sizes.setdefault(len(t["rows"]), []).append(t["file"])
        if len(sizes) > 1:
            struct.append(f"[{lb}] 样本表不统一：{ {k: v for k, v in sorted(sizes.items())} }")
        for r in canon["rows"]:
            recomputed.setdefault(r["code"], {"rel": round(r["pct"] - med, 2),
                                              "pct": r["pct"], "label": lb})

    diff, missing = [], []
    for code, v in stock.items():
        want = v.get("bench_pt")
        rec = recomputed.get(code)
        if rec is None:
            if want is not None:
                missing.append(code)
            continue
        if want is None:
            diff.append((code, rec["label"], None, rec["rel"]))
        elif abs(rec["rel"] - float(want)) > TOL:
            diff.append((code, rec["label"], float(want), rec["rel"]))

    print("── 方向中位（口径：平均）")
    for lb, m in medians.items():
        print(f"  {lb:<12} n={m['n']:<3} 中位={m['median']:+.2f}   ← {m['file']}")
    print(f"\n一致 {len(stock) - len(diff) - len(missing)} 只 ｜ 不一致 {len(diff)} 只 "
          f"｜ 无排名表 {len(missing)} 只 ｜ 共 {len(stock)} 只")
    if diff:
        print("\n代码     方向            现值      重算     差")
        for code, lb, w, r in diff:
            ws = f"{w:+.2f}" if w is not None else "null"
            print(f"{code:<9}{lb:<14}{ws:>8}{r:>9.2f}{r - (w or 0):>8.2f}")
    if missing:
        print(f"\nℹ️ 这些标的在台账排名表里找不到（新股/单标的）：{', '.join(missing)}")
    if struct:
        print("\n🔴 结构问题（先处理，否则中位不可比）：")
        for s in struct:
            print(f"  - {s}")

    if args.emit:
        print("\n── bench_pt 候选（粘进 bench.json 的 stock.<code>.bench_pt；null = 方向内无对照）")
        for code, v in stock.items():
            rec = recomputed.get(code)
            if rec is None:
                continue
            print(f'    "{code}": {{ "bench_pt": {rec["rel"]} }},'
                  f'   # {rec["label"]}  原 {v.get("bench_pt")}')

    print("\n📌 只读脚本，未修改任何文件。改 bench.json 与台账请一并做，并跑校验器第7项。")
    return 0 if not diff and not struct and not missing else 1


if __name__ == "__main__":
    sys.exit(main())
