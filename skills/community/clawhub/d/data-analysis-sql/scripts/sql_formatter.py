#!/usr/bin/env python3
"""
SQL 格式化工具 - 规范化 SQL 语句格式，提升可读性
用法: python sql_formatter.py "<sql>"
"""

import sys
import re


def format_sql(sql: str) -> str:
    """对 SQL 进行基本格式化"""
    # 预处理：合并多余空格
    sql = re.sub(r'\s+', ' ', sql).strip()

    # 关键字列表（大写形式，用于识别）
    keywords = [
        'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'JOIN', 'INNER JOIN', 'LEFT JOIN',
        'RIGHT JOIN', 'FULL OUTER JOIN', 'CROSS JOIN', 'LEFT OUTER JOIN',
        'ON', 'GROUP BY', 'HAVING', 'ORDER BY', 'LIMIT', 'OFFSET',
        'INSERT INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE FROM',
        'CREATE TABLE', 'ALTER TABLE', 'DROP TABLE', 'CREATE INDEX',
        'WITH', 'AS', 'UNION', 'UNION ALL', 'EXCEPT', 'INTERSECT',
        'CASE', 'WHEN', 'THEN', 'ELSE', 'END', 'IN', 'NOT IN',
        'BETWEEN', 'IS NULL', 'IS NOT NULL', 'LIKE', 'EXISTS',
        'DISTINCT', 'ASC', 'DESC', 'OVER', 'PARTITION BY', 'WINDOW'
    ]

    # 逐关键字大写并换行
    result = sql
    for kw in sorted(keywords, key=len, reverse=True):
        # 匹配完整单词（边界处理）
        pattern = re.compile(r'\b' + kw + r'\b', re.IGNORECASE)
        result = pattern.sub('\n' + kw, result)

    # 清理：去除多余空行，多个换行合并为一个
    lines = result.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            cleaned.append(stripped)

    return '\n'.join(cleaned)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python sql_formatter.py \"<sql>\"")
        sys.exit(1)

    sql_input = ' '.join(sys.argv[1:])
    print(format_sql(sql_input))
