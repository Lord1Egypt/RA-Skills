#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""slowlog_digest.py —— MySQL 慢查询日志指纹聚合工具（零依赖，仅标准库）。

把成千上万条慢日志按 SQL 指纹归并，按总耗时排序，回答"先优化哪条"。
pt-query-digest 装不上、线上机器不给装包时用这个。

用法:
    python3 slowlog_digest.py /var/log/mysql/slow.log
    python3 slowlog_digest.py slow.log --top 10 --sort total
    python3 slowlog_digest.py slow.log --json
    python3 slowlog_digest.py slow.log --strict --max-avg 1.0 --max-ratio 100
    cat slow.log | python3 slowlog_digest.py -

排序键:
    total (默认)  按总耗时，决定优化优先级
    avg           按平均耗时，找单条最慢的
    count         按出现次数，找最频繁的
    examined      按总扫描行数，找最耗 IO 的

退出码:
    0 = 正常（或 strict 下未超阈值）
    1 = strict 模式下存在超阈值指纹
    2 = 用法/解析错误
"""

import argparse
import json
import re
import sys
from collections import OrderedDict

# ---------------------------------------------------------------- 日志行解析

RE_TIME = re.compile(r"^#\s*Time:\s*(.+)$")
RE_USER = re.compile(r"^#\s*User@Host:\s*(.+)$")
# 兼容 5.6/5.7/8.0 及带 Thread_id / Rows_affected 的扩展格式
RE_STAT = re.compile(
    r"Query_time:\s*(?P<qt>[\d.]+)"
    r"(?:\s+Lock_time:\s*(?P<lt>[\d.]+))?"
    r"(?:\s+Rows_sent:\s*(?P<rs>\d+))?"
    r"(?:\s+Rows_examined:\s*(?P<re>\d+))?"
)

# 需要跳过的非 SQL 正文行
RE_SKIP = re.compile(
    r"^\s*(?:SET\s+timestamp\s*=|use\s+\S+\s*;|/\*.*?\*/\s*;?\s*$)", re.IGNORECASE
)
# 日志头部噪音（mysqld 启动横幅）
RE_BANNER = re.compile(
    r"^(?:/\S*mysqld|Tcp port:|Time\s+Id\s+Command|.*started with:)", re.IGNORECASE
)


def _iter_events(lines):
    """把慢日志切成 (meta, sql) 事件流。"""
    cur_meta = None
    cur_sql = []

    def flush():
        if cur_meta is not None and cur_sql:
            sql = " ".join(s.strip() for s in cur_sql).strip()
            if sql:
                return (cur_meta, sql)
        return None

    for raw in lines:
        line = raw.rstrip("\n")
        if not line.strip():
            continue

        if line.startswith("#"):
            # 注释块：如果前一个事件已有 SQL，说明新事件开始了
            if RE_TIME.match(line) or RE_USER.match(line):
                ev = flush()
                if ev:
                    yield ev
                    cur_sql = []
                if cur_meta is None:
                    cur_meta = {}
                if RE_TIME.match(line):
                    # 新事件起点，重置统计
                    cur_meta = {"time": RE_TIME.match(line).group(1).strip()}
            m = RE_STAT.search(line)
            if m:
                if cur_meta is None:
                    cur_meta = {}
                cur_meta["query_time"] = float(m.group("qt"))
                cur_meta["lock_time"] = float(m.group("lt") or 0.0)
                cur_meta["rows_sent"] = int(m.group("rs") or 0)
                cur_meta["rows_examined"] = int(m.group("re") or 0)
            continue

        if RE_BANNER.match(line):
            continue
        if RE_SKIP.match(line):
            continue

        cur_sql.append(line)

    ev = flush()
    if ev:
        yield ev


# ---------------------------------------------------------------- SQL 指纹化

RE_COMMENT_BLOCK = re.compile(r"/\*.*?\*/", re.DOTALL)
RE_COMMENT_LINE = re.compile(r"(?:--|#)[^\n]*")
RE_STRING = re.compile(r"'(?:[^'\\]|\\.|'')*'|\"(?:[^\"\\]|\\.)*\"")
RE_NUMBER = re.compile(r"\b(?:0x[0-9a-fA-F]+|\d+\.\d+|\d+)\b")
RE_IN_LIST = re.compile(r"\bIN\s*\(\s*\?(?:\s*,\s*\?)+\s*\)", re.IGNORECASE)
RE_VALUES = re.compile(
    r"\bVALUES\s*\(\s*\?(?:\s*,\s*\?)*\s*\)(?:\s*,\s*\(\s*\?(?:\s*,\s*\?)*\s*\))+",
    re.IGNORECASE,
)
RE_WS = re.compile(r"\s+")


def fingerprint(sql):
    """把具体 SQL 归一成指纹：字面量 -> ?，IN 列表折叠，空白归一。"""
    s = RE_COMMENT_BLOCK.sub(" ", sql)
    s = RE_COMMENT_LINE.sub(" ", s)
    s = RE_STRING.sub("?", s)
    s = RE_NUMBER.sub("?", s)
    s = RE_IN_LIST.sub("IN (?+)", s)
    s = RE_VALUES.sub("VALUES (?+)", s)
    s = RE_WS.sub(" ", s).strip().rstrip(";")
    return s


def first_table(fp):
    """从指纹里粗提主表名，仅用于展示分组。"""
    m = re.search(
        r"\b(?:FROM|INTO|UPDATE|TABLE)\s+`?([A-Za-z_][\w$]*)`?", fp, re.IGNORECASE
    )
    return m.group(1) if m else "-"


def stmt_kind(fp):
    m = re.match(r"\s*(\w+)", fp)
    return m.group(1).upper() if m else "?"


# ---------------------------------------------------------------- 聚合

def digest(events):
    agg = OrderedDict()
    for meta, sql in events:
        fp = fingerprint(sql)
        if not fp:
            continue
        qt = meta.get("query_time", 0.0)
        lt = meta.get("lock_time", 0.0)
        rs = meta.get("rows_sent", 0)
        rex = meta.get("rows_examined", 0)

        it = agg.get(fp)
        if it is None:
            it = {
                "fingerprint": fp,
                "kind": stmt_kind(fp),
                "table": first_table(fp),
                "count": 0,
                "total_time": 0.0,
                "max_time": 0.0,
                "min_time": None,
                "total_lock": 0.0,
                "rows_sent": 0,
                "rows_examined": 0,
                "sample": sql.strip().rstrip(";"),
                "first_seen": meta.get("time"),
                "last_seen": meta.get("time"),
            }
            agg[fp] = it
        it["count"] += 1
        it["total_time"] += qt
        it["total_lock"] += lt
        it["rows_sent"] += rs
        it["rows_examined"] += rex
        if qt > it["max_time"]:
            it["max_time"] = qt
            it["sample"] = sql.strip().rstrip(";")
        if it["min_time"] is None or qt < it["min_time"]:
            it["min_time"] = qt
        if meta.get("time"):
            it["last_seen"] = meta["time"]

    for it in agg.values():
        it["avg_time"] = it["total_time"] / it["count"]
        it["min_time"] = it["min_time"] or 0.0
        it["avg_examined"] = it["rows_examined"] / it["count"]
        # 扫描/返回比只对 SELECT 有意义：UPDATE/DELETE/INSERT 的 Rows_sent 恒为 0，
        # 若一并计算会得到 ∞ 从而永远误报。
        if it["kind"] != "SELECT":
            it["ratio"] = None
        elif it["rows_sent"]:
            it["ratio"] = it["rows_examined"] / it["rows_sent"]
        else:
            it["ratio"] = float("inf")
    return list(agg.values())


SORT_KEYS = {
    "total": lambda i: i["total_time"],
    "avg": lambda i: i["avg_time"],
    "count": lambda i: i["count"],
    "examined": lambda i: i["rows_examined"],
}


def _fmt_ratio(r):
    if r is None:
        return "n/a"
    return "∞" if r == float("inf") else "%.0f" % r


def _short(s, n):
    s = s.replace("\n", " ")
    return s if len(s) <= n else s[: n - 1] + "…"


# ---------------------------------------------------------------- 输出

def render_text(items, total_events, total_time, top, max_avg, max_ratio):
    out = []
    out.append("MySQL 慢查询摘要")
    out.append("=" * 78)
    out.append(
        "事件总数: %d    指纹数: %d    总耗时: %.2fs"
        % (total_events, len(items), total_time)
    )
    out.append("")
    if not items:
        out.append("未解析到任何慢查询（检查日志格式或路径）。")
        return "\n".join(out)

    header = "%-4s %-7s %-16s %6s %9s %8s %8s %10s %7s" % (
        "#", "类型", "主表", "次数", "总耗时s", "均耗时s", "最大s", "扫描行", "扫/返",
    )
    out.append(header)
    out.append("-" * 78)
    for i, it in enumerate(items[:top], 1):
        out.append(
            "%-4d %-7s %-16s %6d %9.2f %8.3f %8.3f %10d %7s"
            % (
                i,
                it["kind"],
                _short(it["table"], 16),
                it["count"],
                it["total_time"],
                it["avg_time"],
                it["max_time"],
                it["rows_examined"],
                _fmt_ratio(it["ratio"]),
            )
        )
    out.append("")
    out.append("明细（按上表顺序）")
    out.append("-" * 78)
    for i, it in enumerate(items[:top], 1):
        share = it["total_time"] / total_time * 100 if total_time else 0
        flags = []
        if it["avg_time"] > max_avg:
            flags.append("均耗时超阈值(>%.2fs)" % max_avg)
        if it["ratio"] is not None and it["ratio"] > max_ratio:
            flags.append("扫描/返回比超阈值(>%d)" % max_ratio)
        out.append("[%d] 占总耗时 %.1f%%%s" % (i, share, "  ⚠ " + "；".join(flags) if flags else ""))
        out.append("    指纹: %s" % _short(it["fingerprint"], 300))
        out.append("    样本: %s" % _short(it["sample"], 300))
        out.append("")
    out.append("下一步：对占比最高的指纹取样本 SQL 跑 EXPLAIN，交给 explain_audit.py。")
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(
        description="MySQL 慢查询日志指纹聚合（零依赖）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
        "  python3 slowlog_digest.py slow.log --top 10\n"
        "  python3 slowlog_digest.py slow.log --sort avg --json\n"
        "  cat slow.log | python3 slowlog_digest.py - --strict\n",
    )
    p.add_argument("logfile", help="慢日志路径，- 表示从 stdin 读")
    p.add_argument("--top", type=int, default=10, help="展示前 N 个指纹（默认 10）")
    p.add_argument(
        "--sort",
        choices=sorted(SORT_KEYS),
        default="total",
        help="排序键（默认 total = 总耗时）",
    )
    p.add_argument("--json", action="store_true", help="输出 JSON，便于接管道")
    p.add_argument(
        "--strict",
        action="store_true",
        help="存在超阈值指纹时退出码为 1，可用于 CI 门禁",
    )
    p.add_argument("--max-avg", type=float, default=1.0, help="平均耗时阈值秒（默认 1.0）")
    p.add_argument(
        "--max-ratio", type=float, default=100.0, help="扫描/返回行比阈值（默认 100）"
    )
    args = p.parse_args(argv)

    try:
        if args.logfile == "-":
            lines = sys.stdin.read().splitlines()
        else:
            with open(args.logfile, "r", encoding="utf-8", errors="replace") as f:
                lines = f.read().splitlines()
    except OSError as e:
        sys.stderr.write("读取失败: %s\n" % e)
        return 2

    events = list(_iter_events(lines))
    items = digest(events)
    items.sort(key=SORT_KEYS[args.sort], reverse=True)
    total_time = sum(i["total_time"] for i in items)

    over = [
        i
        for i in items
        if i["avg_time"] > args.max_avg
        or (i["ratio"] is not None and i["ratio"] > args.max_ratio)
    ]

    if args.json:
        payload = {
            "events": len(events),
            "fingerprints": len(items),
            "total_time": round(total_time, 4),
            "sort": args.sort,
            "thresholds": {"max_avg": args.max_avg, "max_ratio": args.max_ratio},
            "over_threshold": len(over),
            "items": [
                {
                    k: (
                        None
                        if v == float("inf")
                        else (round(v, 4) if isinstance(v, float) else v)
                    )
                    for k, v in i.items()
                }
                for i in items[: args.top]
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(
            render_text(
                items, len(events), total_time, args.top, args.max_avg, args.max_ratio
            )
        )

    if args.strict and over:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
