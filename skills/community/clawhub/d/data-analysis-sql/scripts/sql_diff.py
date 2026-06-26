#!/usr/bin/env python3
"""
SQL 差异分析工具 - 对比两段 SQL 的逻辑差异，输出结构化摘要
用法: python sql_diff.py old.sql new.sql
       python sql_diff.py "<old_sql>" "<new_sql>"
"""

import sys
import re
from difflib import unified_diff


def extract_sql_parts(sql: str) -> dict:
    """解析 SQL 各组成部分"""
    sql_upper = sql.upper()
    return {
        "raw": sql,
        "upper": sql_upper,
        "select_cols": _extract_select_cols(sql_upper),
        "from_tables": _extract_from_tables(sql_upper),
        "join_tables": _extract_joins(sql_upper),
        "where_conds": _extract_where(sql_upper),
        "group_by": _extract_group_by(sql_upper),
        "having_conds": _extract_having(sql_upper),
        "order_by": _extract_order_by(sql_upper),
        "window_fns": _extract_window_fns(sql),
        "with_clauses": _extract_ctes(sql_upper),
        "subqueries": _extract_subqueries(sql_upper),
    }


def _extract_select_cols(sql: str) -> list:
    """提取 SELECT 字段"""
    match = re.search(r'SELECT\s+(.*?)\s+FROM\b', sql, re.DOTALL)
    if not match:
        return []
    cols = match.group(1)
    return [c.strip() for c in cols.replace('\n', ' ').split(',') if c.strip() and c.strip() != '*']


def _extract_from_tables(sql: str) -> list:
    """提取主表"""
    match = re.search(r'FROM\s+([^\s(]+)', sql, re.IGNORECASE)
    return [match.group(1).strip()] if match else []


def _extract_joins(sql: str) -> list:
    """提取所有 JOIN"""
    pattern = re.compile(
        r'(LEFT|RIGHT|INNER|FULL|CROSS)?\s*JOIN\s+([^\s]+)\s+',
        re.IGNORECASE
    )
    return [f"{m.group(1) or 'INNER'} JOIN {m.group(2)}" for m in pattern.finditer(sql)]


def _extract_where(sql: str) -> list:
    """提取 WHERE 条件（简化）"""
    match = re.search(r'WHERE\s+(.*?)(?:GROUP BY|HAVING|ORDER BY|LIMIT|$)', sql, re.IGNORECASE | re.DOTALL)
    if not match:
        return []
    cond = match.group(1).replace('\n', ' ').strip()
    # 拆成独立条件
    parts = re.split(r'\s+AND\s+', cond, flags=re.IGNORECASE)
    return [p.strip() for p in parts if p.strip()]


def _extract_group_by(sql: str) -> list:
    match = re.search(r'GROUP BY\s+(.*?)(?:HAVING|ORDER BY|LIMIT|$)', sql, re.IGNORECASE | re.DOTALL)
    if not match:
        return []
    cols = match.group(1).replace('\n', ' ')
    return [c.strip() for c in cols.split(',') if c.strip()]


def _extract_having(sql: str) -> list:
    match = re.search(r'HAVING\s+(.*?)(?:ORDER BY|LIMIT|$)', sql, re.IGNORECASE | re.DOTALL)
    if not match:
        return []
    conds = match.group(1).replace('\n', ' ')
    parts = re.split(r'\s+AND\s+', conds, flags=re.IGNORECASE)
    return [p.strip() for p in parts if p.strip()]


def _extract_order_by(sql: str) -> list:
    match = re.search(r'ORDER BY\s+(.*?)(?:LIMIT|$)', sql, re.IGNORECASE | re.DOTALL)
    if not match:
        return []
    return [o.strip() for o in match.group(1).replace('\n', ' ').split(',') if o.strip()]


def _extract_window_fns(sql: str) -> list:
    """提取窗口函数"""
    pattern = re.compile(r'(\w+)\s*\(\s*[^)]+\)\s*OVER\s*\([^)]+\)', re.IGNORECASE)
    return list(set(m.group(1) for m in pattern.finditer(sql)))


def _extract_ctes(sql: str) -> list:
    """提取 WITH 子句"""
    pattern = re.compile(r'WITH\s+(\w+)\s+AS\s*\(', re.IGNORECASE)
    return [m.group(1) for m in pattern.finditer(sql)]


def _extract_subqueries(sql: str) -> int:
    """统计子查询数量"""
    return len(re.findall(r'\(\s*SELECT\s+', sql, re.IGNORECASE))


def diff_summary(old: dict, new: dict) -> list:
    """生成差异摘要"""
    diffs = []

    # 表变化
    old_tables = set(old["from_tables"])
    new_tables = set(new["from_tables"])
    if old_tables != new_tables:
        diffs.append(f"📋 主表变化: {old_tables} → {new_tables}")

    # JOIN 变化
    old_joins = set(old["join_tables"])
    new_joins = set(new["join_tables"])
    added = new_joins - old_joins
    removed = old_joins - new_joins
    if added:
        diffs.append(f"➕ 新增 JOIN: {', '.join(sorted(added))}")
    if removed:
        diffs.append(f"➖ 移除 JOIN: {', '.join(sorted(removed))}")

    # SELECT 字段变化
    old_cols = set(old["select_cols"])
    new_cols = set(new["select_cols"])
    added_cols = [c for c in (new_cols - old_cols) if len(c) < 60]
    removed_cols = [c for c in (old_cols - new_cols) if len(c) < 60]
    if added_cols:
        diffs.append(f"➕ 新增字段: {', '.join(sorted(added_cols, key=lambda x: -len(x))[:5])}")
    if removed_cols:
        diffs.append(f"➖ 移除字段: {', '.join(sorted(removed_cols, key=lambda x: -len(x))[:5])}")

    # WHERE 条件变化
    old_where = set(old["where_conds"])
    new_where = set(new["where_conds"])
    added_where = new_where - old_where
    removed_where = old_where - new_where
    if added_where:
        diffs.append(f"➕ 新增条件: {' AND '.join(sorted(added_where, key=lambda x: -len(x))[:3])}")
    if removed_where:
        diffs.append(f"➖ 移除条件: {' AND '.join(sorted(removed_where, key=lambda x: -len(x))[:3])}")

    # GROUP BY 变化
    if old["group_by"] != new["group_by"]:
        diffs.append(f"📊 GROUP BY 变化: {old['group_by']} → {new['group_by']}")

    # ORDER BY 变化
    if old["order_by"] != new["order_by"]:
        diffs.append(f"🔽 ORDER BY 变化: {old['order_by']} → {new['order_by']}")

    # 窗口函数变化
    old_win = set(old["window_fns"])
    new_win = set(new["window_fns"])
    if old_win != new_win:
        diffs.append(f"🪟 窗口函数: {old_win} → {new_win}")

    # CTE 变化
    old_cte = set(old["with_clauses"])
    new_cte = set(new["with_clauses"])
    if old_cte != new_cte:
        added_cte = new_cte - old_cte
        removed_cte = old_cte - new_cte
        if added_cte:
            diffs.append(f"🔗 新增 CTE: {', '.join(sorted(added_cte))}")
        if removed_cte:
            diffs.append(f"🔗 移除 CTE: {', '.join(sorted(removed_cte))}")

    # 子查询数量
    if old["subqueries"] != new["subqueries"]:
        diffs.append(f"📦 子查询数量: {old['subqueries']} → {new['subqueries']}")

    if not diffs:
        diffs.append("✅ 两段 SQL 结构和逻辑一致")

    return diffs


def main():
    if len(sys.argv) < 3:
        print("用法: python sql_diff.py <old_sql> <new_sql>")
        print("   或: python sql_diff.py old.sql new.sql")
        sys.exit(1)

    old_sql = sys.argv[1]
    new_sql = sys.argv[2]

    old_parts = extract_sql_parts(old_sql)
    new_parts = extract_sql_parts(new_sql)

    print("=" * 60)
    print("SQL 差异分析报告")
    print("=" * 60)

    print("\n【逻辑差异】")
    for item in diff_summary(old_parts, new_parts):
        print(f"  {item}")

    print("\n【OLD SQL 结构】")
    print(f"  主表: {old_parts['from_tables']}")
    print(f"  JOIN: {old_parts['join_tables']}")
    print(f"  CTE:  {old_parts['with_clauses']}")
    print(f"  SELECT 字段数: {len(old_parts['select_cols'])}")
    print(f"  GROUP BY: {old_parts['group_by']}")
    print(f"  窗口函数: {old_parts['window_fns']}")

    print("\n【NEW SQL 结构】")
    print(f"  主表: {new_parts['from_tables']}")
    print(f"  JOIN: {new_parts['join_tables']}")
    print(f"  CTE:  {new_parts['with_clauses']}")
    print(f"  SELECT 字段数: {len(new_parts['select_cols'])}")
    print(f"  GROUP BY: {new_parts['group_by']}")
    print(f"  窗口函数: {new_parts['window_fns']}")


if __name__ == '__main__':
    main()
