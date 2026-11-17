#!/usr/bin/env python3
"""explain_audit.py — 执行计划审计器（零依赖）

自动识别并解析三种执行计划格式，标记性能反模式：
  * MySQL  EXPLAIN FORMAT=JSON       (.json)
  * MySQL  EXPLAIN 表格输出           (纯文本)
  * PostgreSQL EXPLAIN (ANALYZE)     (纯文本 / JSON)

用法:
    mysql -e "EXPLAIN FORMAT=JSON SELECT ..." > plan.json
    python3 explain_audit.py plan.json

    psql -c "EXPLAIN (ANALYZE, BUFFERS) SELECT ..." > plan.txt
    python3 explain_audit.py plan.txt

    python3 explain_audit.py plan.txt --json
    cat plan.txt | python3 explain_audit.py -

退出码:
    0 = 无 error 级问题
    1 = 存在 error 级问题
    2 = 用法错误 / 无法解析
"""
from __future__ import annotations

import argparse
import json
import re
import sys

ROWS_MISESTIMATE_FACTOR = 10.0   # 估算/实际偏差超过此倍数即告警
BIG_TABLE_ROWS = 10_000          # 超过此行数的扫描才视为严重


# ---------------------------------------------------------------- 输出

LEVEL_ORDER = {"error": 0, "warning": 1, "info": 2}
ICON = {"error": "✗", "warning": "!", "info": "·"}


class Report:
    def __init__(self) -> None:
        self.issues: list[dict] = []

    def add(self, level: str, code: str, node: str, msg: str) -> None:
        self.issues.append({"level": level, "code": code,
                            "node": node, "message": msg})

    def counts(self) -> dict:
        return {lv: sum(1 for i in self.issues if i["level"] == lv)
                for lv in ("error", "warning", "info")}


# ---------------------------------------------------------------- MySQL JSON

def audit_mysql_json(plan: dict, rep: Report) -> None:
    def walk(node, path="query_block"):
        if isinstance(node, list):
            for x in node:
                walk(x, path)
            return
        if not isinstance(node, dict):
            return

        # filesort / temporary 也可能挂在 ordering_operation / grouping_operation 层，
        # 不只出现在 table 内部（实测踩坑：只查 table 会漏报）
        for op, label in (("ordering_operation", "ORDER BY"),
                          ("grouping_operation", "GROUP BY")):
            sub = node.get(op)
            if isinstance(sub, dict):
                if sub.get("using_filesort"):
                    rep.add("warning", "E004", label,
                            f"{label} 触发 Using filesort：额外排序，"
                            "让索引顺序匹配排序列（ESR 规则）")
                if sub.get("using_temporary_table"):
                    rep.add("warning", "E005", label,
                            f"{label} 触发 Using temporary：创建临时表")

        ti = node.get("table")
        if isinstance(ti, dict):
            name = ti.get("table_name", "?")
            atype = (ti.get("access_type") or "").lower()
            rows = ti.get("rows_examined_per_scan") or ti.get("rows") or 0
            key = ti.get("key")
            used = ti.get("using_filesort"), ti.get("using_temporary_table")

            if atype == "all":
                lvl = "error" if rows >= BIG_TABLE_ROWS else "warning"
                rep.add(lvl, "E001", name,
                        f"全表扫描 access_type=ALL，预计扫描 {rows} 行"
                        + ("（大表，必须建索引）" if lvl == "error" else "（小表，可接受）"))
            elif atype == "index":
                rep.add("warning", "E002", name,
                        f"全索引扫描 access_type=index，预计 {rows} 行：索引未能有效收窄范围")

            if key is None and atype not in ("system", "const"):
                rep.add("warning", "E003", name, "未使用任何索引 (key=NULL)")

            if ti.get("using_filesort"):
                rep.add("warning", "E004", name,
                        "Using filesort：额外排序。让索引顺序匹配 ORDER BY（ESR 规则）")
            if ti.get("using_temporary_table"):
                rep.add("warning", "E005", name,
                        "Using temporary：创建临时表，常由 GROUP BY / DISTINCT / UNION 引起")
            if ti.get("using_join_buffer"):
                rep.add("error", "E006", name,
                        f"Using join buffer ({ti.get('using_join_buffer')})："
                        "JOIN 无可用索引，给被驱动表关联列建索引")

            filt = ti.get("filtered")
            try:
                if filt is not None and float(filt) < 10 and rows >= BIG_TABLE_ROWS:
                    rep.add("warning", "E007", name,
                            f"filtered={filt}%：读取 {rows} 行仅少量满足条件，索引筛选力不足")
            except (TypeError, ValueError):
                pass
            _ = used

        for k, v in node.items():
            if isinstance(v, (dict, list)):
                walk(v, f"{path}.{k}")

    walk(plan.get("query_block", plan))


# ---------------------------------------------------------------- MySQL 表格

MYSQL_TABLE_HDR = re.compile(r"^\s*\|?\s*id\s*\|", re.I)


def audit_mysql_table(text: str, rep: Report) -> bool:
    lines = [l for l in text.splitlines() if l.strip()]
    hdr_i = next((i for i, l in enumerate(lines) if MYSQL_TABLE_HDR.match(l)), None)
    if hdr_i is None:
        return False
    cols = [c.strip().lower() for c in lines[hdr_i].strip().strip("|").split("|")]
    try:
        i_tab, i_type = cols.index("table"), cols.index("type")
    except ValueError:
        return False
    i_key = cols.index("key") if "key" in cols else None
    i_rows = cols.index("rows") if "rows" in cols else None
    i_extra = cols.index("extra") if "extra" in cols else None

    found = False
    for l in lines[hdr_i + 1:]:
        if set(l.strip()) <= set("+-| "):
            continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) < len(cols):
            continue
        found = True
        name = cells[i_tab] or "?"
        atype = cells[i_type].lower()
        rows = 0
        if i_rows is not None:
            try:
                rows = int(cells[i_rows])
            except ValueError:
                rows = 0
        extra = cells[i_extra] if i_extra is not None else ""

        if atype == "all":
            lvl = "error" if rows >= BIG_TABLE_ROWS else "warning"
            rep.add(lvl, "E001", name, f"全表扫描 type=ALL，预计 {rows} 行")
        elif atype == "index":
            rep.add("warning", "E002", name, f"全索引扫描 type=index，预计 {rows} 行")

        if i_key is not None and cells[i_key] in ("NULL", "", "None") \
                and atype not in ("system", "const"):
            rep.add("warning", "E003", name, "未使用任何索引 (key=NULL)")
        if "using filesort" in extra.lower():
            rep.add("warning", "E004", name, "Using filesort：额外排序")
        if "using temporary" in extra.lower():
            rep.add("warning", "E005", name, "Using temporary：创建临时表")
        if "join buffer" in extra.lower():
            rep.add("error", "E006", name, "Using join buffer：JOIN 无可用索引")
        if "using index" in extra.lower() and "using index condition" not in extra.lower():
            rep.add("info", "E010", name, "Using index：覆盖索引，无需回表 ✓")
    return found


# ---------------------------------------------------------------- PostgreSQL

# 拆成独立正则分别提取，避免"非贪婪 + 可选组"静默匹配空值（实测踩坑）
PG_NODE_NAME = re.compile(
    r"^\s*(?:->\s*)?"
    r"((?:Parallel\s+|Partial\s+|Finalize\s+)?"
    r"[A-Z][A-Za-z]*(?:\s+[A-Z][A-Za-z]*)*?"
    r"\s*(?:Scan|Join|Sort|Aggregate|Loop|Hash|Materialize|Gather|Append|Limit|Unique))"
    r"(?:\s+(?:using\s+(\S+)|on\s+(\S+)))?"
)
PG_COST = re.compile(r"\(cost=[\d.]+\.\.[\d.]+\s+rows=(\d+)")
PG_ACTUAL = re.compile(r"\(actual\s+time=[\d.]+\.\.[\d.]+\s+rows=(\d+)\s+loops=(\d+)\)")


def audit_pg_text(text: str, rep: Report) -> bool:
    found = False
    for line in text.splitlines():
        if "(cost=" not in line and "actual time" not in line:
            # 仍需捕获 Sort Method / Buffers 这类附属行
            low = line.strip().lower()
            if low.startswith("sort method:") and "disk" in low:
                rep.add("error", "P004", "Sort",
                        f"排序落盘（{line.strip()}）：work_mem 不足，"
                        "会话级 SET work_mem 后重测")
            elif low.startswith("heap fetches:"):
                try:
                    n = int(low.split(":")[1].strip())
                    if n > 1000:
                        rep.add("warning", "P005", "Index Only Scan",
                                f"Heap Fetches={n}：visibility map 过期，"
                                "Index Only Scan 退化，需加强 autovacuum")
                except (ValueError, IndexError):
                    pass
            continue

        m = PG_NODE_NAME.match(line)
        if not m:
            continue
        found = True
        node = re.sub(r"\s+", " ", m.group(1).strip())
        idx_name, tbl_name = m.group(2), m.group(3)

        mc = PG_COST.search(line)
        ma = PG_ACTUAL.search(line)
        est = int(mc.group(1)) if mc else None
        act = int(ma.group(1)) if ma else None
        loops = int(ma.group(2)) if ma else 1
        if idx_name:
            label = f"{node} using {idx_name}"
        elif tbl_name:
            label = f"{node} on {tbl_name}"
        else:
            label = node

        if node.endswith("Seq Scan") or node == "Seq Scan":
            n = act if act is not None else (est or 0)
            lvl = "error" if n >= BIG_TABLE_ROWS else "warning"
            rep.add(lvl, "P001", label,
                    f"顺序扫描 {n} 行" + ("（大表，考虑建索引）" if lvl == "error"
                                          else "（小表，优化器选择合理）"))

        # loops 很大说明该节点被反复执行，真实耗时 = actual time × loops
        if loops > 1000:
            rep.add("error", "P002", label,
                    f"节点被执行 {loops} 次（loops={loops}）：真实耗时需乘以该值。"
                    "通常是 Nested Loop 外层行数过多，内层应有索引或改走 Hash Join")

        # PG 的 estimated rows 与 actual rows 都是「每次循环」的值，直接比即可。
        # 乘以 loops 再比会对 Nested Loop 内层节点产生假阳性（实测踩坑）。
        if est is not None and act is not None and act > 0 and est > 0:
            ratio = max(est / act, act / est)
            if ratio >= ROWS_MISESTIMATE_FACTOR:
                rep.add("warning", "P003", label,
                        f"行数估算偏差 {ratio:.0f}x（估 {est} / 实际 {act}，每次循环）："
                        "先 ANALYZE 更新统计信息，再谈索引")

        if node.startswith("Index Only Scan"):
            rep.add("info", "P010", label, "Index Only Scan：覆盖索引 ✓")
    return found


# ---------------------------------------------------------------- 主流程

def detect_and_audit(raw: str, rep: Report) -> str:
    stripped = raw.strip()
    if stripped.startswith("{") or stripped.startswith("["):
        try:
            data = json.loads(stripped)
        except json.JSONDecodeError:
            data = None
        if data is not None:
            # PG 的 EXPLAIN (FORMAT JSON) 是 [{"Plan": {...}}]
            if isinstance(data, list) and data and "Plan" in data[0]:
                audit_pg_text(json.dumps(data, indent=1), rep)
                return "postgres-json"
            if isinstance(data, dict) and "query_block" in data:
                audit_mysql_json(data, rep)
                return "mysql-json"
            if isinstance(data, dict):
                audit_mysql_json(data, rep)
                return "mysql-json"

    if audit_mysql_table(raw, rep):
        return "mysql-table"
    if audit_pg_text(raw, rep):
        return "postgres-text"
    return ""


def main() -> int:
    ap = argparse.ArgumentParser(
        description="执行计划审计器：标记全表扫描、filesort、估算偏差等反模式（零依赖）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  mysql -e 'EXPLAIN FORMAT=JSON SELECT ...' > p.json && "
               "python3 explain_audit.py p.json\n"
               "  psql -c 'EXPLAIN (ANALYZE,BUFFERS) SELECT ...' > p.txt && "
               "python3 explain_audit.py p.txt",
    )
    ap.add_argument("file", help="执行计划文件，用 - 表示 stdin")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--strict", action="store_true", help="warning 也视为失败")
    args = ap.parse_args()

    try:
        raw = sys.stdin.read() if args.file == "-" else open(
            args.file, encoding="utf-8").read()
    except OSError as e:
        print(f"无法读取文件: {e}", file=sys.stderr)
        return 2

    rep = Report()
    fmt = detect_and_audit(raw, rep)
    if not fmt:
        print("无法识别执行计划格式（支持 MySQL EXPLAIN 表格/JSON、"
              "PostgreSQL EXPLAIN 文本/JSON）", file=sys.stderr)
        return 2

    rep.issues.sort(key=lambda i: (LEVEL_ORDER[i["level"]], i["code"]))
    counts = rep.counts()

    if args.json:
        print(json.dumps({"format": fmt, "counts": counts, "issues": rep.issues},
                         ensure_ascii=False, indent=2))
    else:
        print(f"\nexplain_audit  格式={fmt}\n")
        for i in rep.issues:
            print(f"  {ICON[i['level']]} {i['code']} [{i['node']}] {i['message']}")
        if not rep.issues:
            print("  未发现明显反模式")
        print(f"\n汇总: error={counts['error']}  warning={counts['warning']}  "
              f"info={counts['info']}\n")

    if counts["error"] or (args.strict and counts["warning"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
