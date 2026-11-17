#!/usr/bin/env python3
"""
CSV 工具集 (CSV Tools) v1.1.0

功能扩展: preview, filter, sort, merge, split, dedup, validate,
          stats, columns, detect, profile, sample — 12个子命令。

纯Python标准库(csv模块)，无外部依赖。

用法:
    python3 scripts/csv_tools.py preview data.csv
    python3 scripts/csv_tools.py stats data.csv
    python3 scripts/csv_tools.py profile data.csv
    python3 scripts/csv_tools.py columns data.csv --rename "old=new" --select col1,col2
"""

import argparse
import csv
import json
import math
import os
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


def read_csv(filepath, **kwargs):
    """读取 CSV 文件为字典列表。"""
    kwargs.setdefault("encoding", "utf-8-sig")
    with open(filepath, **kwargs) as f:
        rows = list(csv.DictReader(f))
    return rows


def write_csv(filepath, rows, fieldnames=None):
    """写入 CSV 文件。"""
    if not rows:
        return 0
    if not fieldnames:
        fieldnames = list(rows[0].keys())
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    return len(rows)


# ─── Preview ────────────────────────────────────────────────────
def cmd_preview(args):
    rows = read_csv(args.file)
    if not rows:
        print("(empty)")
        return
    fn = list(rows[0].keys())
    print(f"📋 {Path(args.file).name} — {len(rows)} rows × {len(fn)} columns")
    print(f"   Columns: {', '.join(fn[:20])}")
    if len(fn) > 20:
        print(f"   ... and {len(fn) - 20} more")
    print(f"   Preview (first {min(5, len(rows))} rows):")
    for row in rows[:5]:
        vals = [str(row.get(c, ""))[:30] for c in fn[:6]]
        print(f"   {' | '.join(vals)}")
    print(f"   ({'more rows below' if len(rows) > 5 else 'end'})")


# ─── Filter ─────────────────────────────────────────────────────
def cmd_filter(args):
    rows = read_csv(args.file)
    if "=" in args.where:
        col, val = args.where.split("=", 1)
        col, val = col.strip(), val.strip().strip("'\"")
    else:
        col, val = args.where.strip(), ""
    filtered = [r for r in rows if str(r.get(col, "")).strip() == val]
    print(f"🔍 Filtered: {len(filtered)}/{len(rows)} rows ({col}={val})")
    if args.output:
        write_csv(args.output, filtered)
        print(f"   Saved: {args.output}")


# ─── Sort ───────────────────────────────────────────────────────
def cmd_sort(args):
    rows = read_csv(args.file)
    cols = [c.strip() for c in args.by.split(",")]
    for k in reversed(cols):
        rows.sort(key=lambda r, k=k: str(r.get(k, "")), reverse=args.desc)
    print(f"🔤 Sorted by: {', '.join(cols)} {'desc' if args.desc else 'asc'}")
    if args.output:
        write_csv(args.output, rows)
        print(f"   Saved: {args.output}")


# ─── Merge ──────────────────────────────────────────────────────
def cmd_merge(args):
    all_rows = []
    for f in args.files:
        rows = read_csv(f)
        all_rows.extend(rows)
        print(f"  + {Path(f).name}: {len(rows)} rows")
    print(f"📎 Merged: {len(all_rows)} total rows")
    if args.output:
        write_csv(args.output, all_rows)
        print(f"   Saved: {args.output}")


# ─── Split ──────────────────────────────────────────────────────
def cmd_split(args):
    rows = read_csv(args.file)
    n = args.chunk_size
    base = Path(args.output or "chunk_")
    parts = []
    for i in range(0, len(rows), n):
        chunk = rows[i : i + n]
        stem = str(base)
        if stem.endswith(".csv"):
            stem = stem[:-4]
        out = f"{stem}_part{i // n + 1}.csv"
        write_csv(out, chunk)
        parts.append(out)
    print(f"✂️ Split: {len(parts)} parts ({n} rows each)")
    for p in parts:
        print(f"   {p}")


# ─── Dedup ──────────────────────────────────────────────────────
def cmd_dedup(args):
    rows = read_csv(args.file)
    cols = [c.strip() for c in args.on.split(",")] if args.on else list(rows[0].keys())
    seen = set()
    deduped = []
    dup_count = 0
    for r in rows:
        key = tuple(str(r.get(c, "")) for c in cols)
        if key in seen:
            dup_count += 1
        else:
            seen.add(key)
            deduped.append(r)
    print(f"🔁 Dedup: {dup_count} removed, {len(deduped)} kept (key: {', '.join(cols)})")
    if args.output:
        write_csv(args.output, deduped)
        print(f"   Saved: {args.output}")


# ─── Validate ──────────────────────────────────────────────────
def cmd_validate(args):
    rows = read_csv(args.file)
    issues = []
    for i, r in enumerate(rows, 2):
        for c in r:
            if r[c] is None or r[c].strip() == "":
                issues.append({"row": i, "column": c, "issue": "empty"})
            elif r[c].strip() in ("#N/A", "N/A", "NULL", "null", "NaN"):
                issues.append({"row": i, "column": c, "issue": "sentinel"})
    print(f"✅ Validate: {len(rows)} rows, {len(issues)} issues")
    if args.output:
        with open(args.output, "w") as f:
            json.dump({"file": args.file, "rows": len(rows), "issues": issues},
                      f, indent=2)
        print(f"   Saved: {args.output}")
    else:
        for iss in issues[:20]:
            print(f"   Row {iss['row']}, col {iss['column']}: {iss['issue']}")


# ─── Stats ──────────────────────────────────────────────────────
def _to_float(val):
    """尝试将字符串转为浮点数。"""
    try:
        return float(val.replace(",", "").replace(" ", ""))
    except (ValueError, AttributeError):
        return None



def _safe_math(expr):
    """安全计算数学表达式（仅数字和+-*/(），不使用 eval。"""
    tokens = re.findall(r"\d+\.?\d*|[+\-*\/\(\)]", expr)
    if not tokens:
        return None
    for t in tokens:
        if not re.match(r"^\d+\.?\d*$", t) and t not in "()+-*/":
            return None
    # Shunting-yard to RPN
    output = []
    ops = []
    prec = {"+": 1, "-": 1, "*": 2, "/": 2}
    for t in tokens:
        if re.match(r"^\d+\.?\d*$", t):
            output.append(float(t))
        elif t == "(":
            ops.append(t)
        elif t == ")":
            while ops and ops[-1] != "(":
                output.append(ops.pop())
            if ops and ops[-1] == "(":
                ops.pop()
        elif t in prec:
            while ops and ops[-1] != "(" and prec.get(ops[-1], 0) >= prec[t]:
                output.append(ops.pop())
            ops.append(t)
    while ops:
        output.append(ops.pop())
    # Evaluate RPN
    stack = []
    for t in output:
        if isinstance(t, float):
            stack.append(t)
        else:
            b = stack.pop()
            a = stack.pop() if t in "+-*/" else 0
            if t == "+": stack.append(a + b)
            elif t == "-": stack.append(a - b)
            elif t == "*": stack.append(a * b)
            elif t == "/": stack.append(a / b if b != 0 else 0)
    return stack[0] if stack else None


def cmd_stats(args):
    rows = read_csv(args.file)
    if not rows:
        print("(empty)")
        return
    fn = list(rows[0].keys())
    print(f"📊 Column Statistics — {Path(args.file).name}")
    print(f"   {'=' * 50}")

    for col in fn:
        nums = [_to_float(r[col]) for r in rows if r.get(col, "").strip()
                and _to_float(r[col]) is not None]
        blanks = sum(1 for r in rows if not r.get(col, "").strip())

        if not nums:
            # 非数值列：展示唯一值、最常见值
            vals = [str(r.get(col, "")) for r in rows if r.get(col, "").strip()]
            unique = len(set(vals))
            common = Counter(vals).most_common(1)[0] if vals else ("", 0)
            print(f"   [{col}] — 文本列")
            print(f"     非空: {len(vals)} | 空: {blanks} | 唯一值: {unique}")
            print(f"     最常见: \"{common[0][:40]}\" ({common[1]}次)")
            continue

        total = sum(nums)
        n = len(nums)
        avg = total / n
        mn = min(nums)
        mx = max(nums)
        if n > 1:
            variance = sum((x - avg) ** 2 for x in nums) / (n - 1)
            std = math.sqrt(variance)
        else:
            std = 0.0

        print(f"   [{col}] — 数值列")
        print(f"     计数: {n} | 空: {blanks} | 总和: {total:,.2f}")
        print(f"     平均: {avg:,.2f} | 中位: {sorted(nums)[n // 2]:,.2f}")
        print(f"     最小: {mn:,.2f} | 最大: {mx:,.2f} | 标准差: {std:,.2f}")


# ─── Columns ────────────────────────────────────────────────────
def cmd_columns(args):
    rows = read_csv(args.file)
    fn = list(rows[0].keys())

    # 重命名
    if args.rename:
        rename_map = {}
        for item in args.rename:
            if "=" not in item:
                continue
            old, new = item.split("=", 1)
            rename_map[old.strip()] = new.strip()
        for r in rows:
            for old, new in rename_map.items():
                if old in r:
                    r[new] = r.pop(old)
        fn = [rename_map.get(c, c) for c in fn]
        print(f"🔄 Renamed: {', '.join(f'{k}→{v}' for k, v in rename_map.items())}")

    # 选择列
    if args.select:
        keep = [c.strip() for c in args.select.split(",")]
        keep = [c for c in keep if c in fn]
        for r in rows:
            for k in list(r.keys()):
                if k not in keep:
                    del r[k]
        fn = keep
        print(f"🎯 Selected: {', '.join(fn)}")

    # 添加计算列
    if args.add:
        for spec in args.add:
            if "=" not in spec:
                continue
            col_name, expr = spec.split("=", 1)
            col_name = col_name.strip()
            expr = expr.strip()
            # 支持简单算术：col_a + col_b, col_a - col_b, col_a * col_b, col_a / col_b
            for r in rows:
                try:
                    # 替换列引用为数值
                    eval_expr = expr
                    for c in fn:
                        val = _to_float(r.get(c, ""))
                        if val is not None:
                            eval_expr = eval_expr.replace(c, str(val))
                        else:
                            eval_expr = eval_expr.replace(c, "0")
                    # 安全计算：使用 _safe_math 替代 eval
                    result = _safe_math(eval_expr)
                    if result is not None:
                        r[col_name] = f"{result:.2f}"
                    else:
                        r[col_name] = expr
                except Exception:
                    r[col_name] = ""
            fn = list(rows[0].keys())
            print(f"➕ Added column: {col_name} = {expr}")

    if args.output:
        write_csv(args.output, rows, fn)
        print(f"   Saved: {args.output}")
    else:
        # 打印预览
        print(f"📋 Result: {len(rows)} rows × {len(fn)} columns")
        for row in rows[:3]:
            vals = [str(row.get(c, ""))[:25] for c in fn[:6]]
            print(f"   {' | '.join(vals)}")


# ─── Detect ─────────────────────────────────────────────────────
def cmd_detect(args):
    rows = read_csv(args.file)
    if not rows:
        print("(empty)")
        return
    fn = list(rows[0].keys())
    print(f"🔎 Data Type Detection — {Path(args.file).name}")
    print(f"   {'=' * 50}")

    for col in fn:
        vals = [str(r.get(col, "")).strip() for r in rows if r.get(col, "").strip()]
        if not vals:
            print(f"   [{col}] ❓ 空列")
            continue

        # 类型判断
        int_count = sum(1 for v in vals if _is_int(v))
        float_count = sum(1 for v in vals if _is_float(v))
        date_count = sum(1 for v in vals if _is_date(v))
        bool_count = sum(1 for v in vals if v.lower() in ("true", "false", "yes", "no", "1", "0"))
        total = len(vals)

        pt_int = int_count / total * 100
        pt_float = float_count / total * 100
        pt_date = date_count / total * 100

        detected = "文本"
        if int_count == total:
            detected = "整数(Integer)"
        elif float_count == total:
            detected = "浮点数(Float)"
        elif date_count / total > 0.5:
            detected = "日期(Date)"
        elif bool_count / total > 0.5:
            detected = "布尔(Boolean)"
        elif int_count / total > 0.8:
            detected = f"多数为整数({pt_int:.0f}%)"
        elif float_count / total > 0.8:
            detected = f"多数为浮点数({pt_float:.0f}%)"

        print(f"   [{col}] → {detected}")
        if args.verbose:
            print(f"     int:{int_count}/{total} float:{float_count}/{total} "
                  f"date:{date_count}/{total} bool:{bool_count}/{total}")


def _is_int(v):
    try:
        int(v.replace(",", ""))
        return True
    except ValueError:
        return False


def _is_float(v):
    try:
        float(v.replace(",", ""))
        return True
    except ValueError:
        return False


def _is_date(v):
    # 常见日期格式
    date_patterns = [
        r"^\d{4}-\d{1,2}-\d{1,2}$",
        r"^\d{4}/\d{1,2}/\d{1,2}$",
        r"^\d{1,2}-\d{1,2}-\d{4}$",
        r"^\d{4}\.\d{1,2}\.\d{1,2}$",
        r"^\d{8}$",
    ]
    return any(re.match(p, v) for p in date_patterns)


# ─── Profile ────────────────────────────────────────────────────
def cmd_profile(args):
    rows = read_csv(args.file)
    if not rows:
        print("(empty)")
        return
    fn = list(rows[0].keys())
    total = len(rows)

    print(f"📋 Data Profile — {Path(args.file).name}")
    print(f"   Rows: {total} | Columns: {len(fn)}")
    print(f"   {'=' * 60}")

    for col in fn:
        vals = [str(r.get(col, "")).strip() for r in rows]
        non_blank = [v for v in vals if v]
        blanks = total - len(non_blank)
        missing_pct = blanks / total * 100
        unique = len(set(non_blank))
        unique_pct = unique / len(non_blank) * 100 if non_blank else 0

        # 分布摘要（最常见值）
        common = Counter(non_blank).most_common(3) if non_blank else []

        bar = _profile_bar(missing_pct)
        print(f"   [{col}]")
        print(f"     非空: {len(non_blank)} / {total} "
              f"({bar} {missing_pct:.0f}% 缺失)")
        print(f"     唯一值: {unique} ({unique_pct:.0f}%)")
        if common:
            top_str = ", ".join(f"\"{v[:20]}\"({c})" for v, c in common)
            print(f"     最常见: {top_str}")


def _profile_bar(pct, width=20):
    """缺失率可视化。"""
    filled = int((100 - pct) / 100 * width)
    return "█" * filled + "░" * (width - filled)


# ─── Sample ─────────────────────────────────────────────────────
def cmd_sample(args):
    rows = read_csv(args.file)
    if not rows:
        print("(empty)")
        return
    n = min(args.n, len(rows))
    if args.method == "head":
        sampled = rows[:n]
    elif args.method == "tail":
        sampled = rows[-n:]
    elif args.method == "random":
        sampled = random.sample(rows, n)
    elif args.method == "systematic":
        step = max(1, len(rows) // n)
        sampled = [rows[i] for i in range(0, len(rows), step)][:n]
    else:
        sampled = rows[:n]

    fn = list(rows[0].keys())
    print(f"🎲 Sample ({args.method}, n={n}) — {Path(args.file).name}")
    for row in sampled:
        vals = [str(row.get(c, ""))[:30] for c in fn[:6]]
        print(f"   {' | '.join(vals)}")

    if args.output:
        write_csv(args.output, sampled)
        print(f"   Saved: {args.output}")


# ─── Main ───────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="CSV Tools v1.1.0")
    sp = p.add_subparsers(dest="command", required=True)

    # preview
    px = sp.add_parser("preview", help="预览结构与前5行")
    px.add_argument("file")

    # filter
    fl = sp.add_parser("filter", help="按条件筛选行")
    fl.add_argument("file")
    fl.add_argument("--where", required=True)
    fl.add_argument("--output", default="filtered.csv")

    # sort
    so = sp.add_parser("sort", help="排序")
    so.add_argument("file")
    so.add_argument("--by", required=True)
    so.add_argument("--desc", action="store_true")
    so.add_argument("--output", default="sorted.csv")

    # merge
    me = sp.add_parser("merge", help="纵向合并多个CSV")
    me.add_argument("files", nargs="+")
    me.add_argument("--output", default="merged.csv")

    # split
    sp2 = sp.add_parser("split", help="按行数分割")
    sp2.add_argument("file")
    sp2.add_argument("--chunk-size", type=int, default=1000)
    sp2.add_argument("--output", default="chunk.csv")

    # dedup
    dd = sp.add_parser("dedup", help="去重")
    dd.add_argument("file")
    dd.add_argument("--on", help="去重依据列（逗号分隔多列）")
    dd.add_argument("--output", default="deduped.csv")

    # validate
    vl = sp.add_parser("validate", help="检查空值/异常值")
    vl.add_argument("file")
    vl.add_argument("--output")

    # stats — NEW
    st = sp.add_parser("stats", help="列统计（sum/avg/min/max/std）")
    st.add_argument("file")

    # columns — NEW
    cl = sp.add_parser("columns", help="列操作（重命名/选择/加计算列）")
    cl.add_argument("file")
    cl.add_argument("--rename", action="append", default=[],
                    help="重命名列: old=new")
    cl.add_argument("--select", help="选择列（逗号分隔）")
    cl.add_argument("--add", action="append", default=[],
                    help="添加计算列: colname=expr")
    cl.add_argument("--output", default="")

    # detect — NEW
    dt = sp.add_parser("detect", help="数据类型自动检测")
    dt.add_argument("file")
    dt.add_argument("--verbose", action="store_true", help="显示详细匹配数")

    # profile — NEW
    pr = sp.add_parser("profile", help="数据画像（缺失率/唯一值/分布摘要）")
    pr.add_argument("file")

    # sample — NEW
    sm = sp.add_parser("sample", help="随机抽样")
    sm.add_argument("file")
    sm.add_argument("--n", type=int, default=10, help="抽样条数")
    sm.add_argument("--method", choices=["head", "tail", "random", "systematic"],
                    default="head", help="抽样方式")
    sm.add_argument("--output", default="")

    args = p.parse_args()

    dispatcher = {
        "preview": cmd_preview,
        "filter": cmd_filter,
        "sort": cmd_sort,
        "merge": cmd_merge,
        "split": cmd_split,
        "dedup": cmd_dedup,
        "validate": cmd_validate,
        "stats": cmd_stats,
        "columns": cmd_columns,
        "detect": cmd_detect,
        "profile": cmd_profile,
        "sample": cmd_sample,
    }
    dispatcher[args.command](args)


if __name__ == "__main__":
    main()
