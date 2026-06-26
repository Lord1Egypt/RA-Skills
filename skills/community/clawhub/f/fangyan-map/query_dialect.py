#!/usr/bin/env python3
"""
方言查询工具 v9（支持 SQLite 或 JSON + 拼音搜索）
支持：哈尔滨话 | 河南话 | 湖南话 | 天津话 | 北京话 | 上海话 | 广东话 | 东营方言 | 重庆方言 | 闽南话 | 大连话

用法：
  python3 query_dialect.py "干什么"
  python3 query_dialect.py "聊天" --dialect 上海话
  python3 query_dialect.py "贼" --fuzzy
  python3 query_dialect.py "ganma"          # 拼音查询（自动识别）
  python3 query_dialect.py --category 形容词
  python3 query_dialect.py --list-categories
  python3 query_dialect.py --list-all
"""

import sqlite3
import json
import gzip
import os
import random
import argparse

# 数据库路径优先级：SQLite > JSON > gzipped JSON
DB_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_PATH = os.path.join(DB_DIR, "data", "dialect.db")
JSON_PATH = os.path.join(DB_DIR, "data", "dialect_data.json")
GZ_PATH = os.path.join(DB_DIR, "data", "dialect_data.json.gz")

DIALECTS = ['哈尔滨话', '河南话', '湖南话', '天津话', '北京话', '上海话', '广东话', '东营方言', '重庆方言', '闽南话', '大连话']

# 拼音模块（可选，无外部依赖）
try:
    from pinyin_map import get_pinyin, is_pure_pinyin
except ImportError:
    get_pinyin = None
    is_pure_pinyin = lambda x: False


def load_data():
    """加载数据，支持 SQLite 或 JSON 格式"""
    if os.path.exists(SQLITE_PATH):
        # SQLite 模式
        conn = sqlite3.connect(SQLITE_PATH)
        cur = conn.cursor()
        cur.execute("SELECT dialect_name, category, standard_word, dialect_word, remark FROM dialect_map")
        rows = cur.fetchall()
        conn.close()
        return [(r[0], r[1], r[2], r[3], r[4]) for r in rows]
    elif os.path.exists(GZ_PATH):
        # gzipped JSON 模式
        with gzip.open(GZ_PATH, 'rt', encoding='utf-8') as f:
            data = json.load(f)
        return [(d['dialect_name'], d['category'], d['standard_word'], d['dialect_word'], d.get('remark', '')) for d in data]
    elif os.path.exists(JSON_PATH):
        # plain JSON 模式
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return [(d['dialect_name'], d['category'], d['standard_word'], d['dialect_word'], d.get('remark', '')) for d in data]
    else:
        raise FileNotFoundError("未找到数据库文件，请确保 data/ 目录下有 dialect.db 或 dialect_data.json 或 dialect_data.json.gz")


def query(keyword: str, target_dialect: str = None) -> list:
    """
    查询一个词在各方言中的说法
    返回：[(dialect_name, standard_word, dialect_word, remark), ...]
    """
    data = load_data()

    results = []
    dialects_to_check = [target_dialect] if target_dialect else DIALECTS

    for d in dialects_to_check:
        # 1. 普通话完全匹配
        for row in data:
            if row[0] == d and row[2] == keyword:
                results.append(row)
        if results and target_dialect:
            return results

        # 2. 普通话模糊匹配
        for row in data:
            if row[0] == d and keyword in row[2]:
                results.append(row)

        # 3. 方言词匹配
        for row in data:
            if row[0] == d and keyword in row[3]:
                results.append(row)

    # 去重
    seen = set()
    unique_results = []
    for r in results:
        key = r
        if key not in seen:
            seen.add(key)
            unique_results.append(r)

    return unique_results


def query_by_pinyin(pinyin_input: str, target_dialect: str = None) -> list:
    """
    拼音查询：用户输入拼音（如 ganma），返回对应普通话词条在各方言的说法
    """
    if not get_pinyin or not is_pure_pinyin(pinyin_input):
        return []

    data = load_data()
    results = []
    dialects_to_check = [target_dialect] if target_dialect else DIALECTS

    # 收集所有标准语并计算拼音
    candidates = {}
    for row in data:
        std = row[2]
        if std not in candidates:
            std_py = get_pinyin(std)
            candidates[std] = std_py

    # 匹配拼音一致的标准语
    py_clean = pinyin_input.lower().replace(' ', '')
    matched_stds = {std for std, py in candidates.items() if py == py_clean}

    if not matched_stds:
        # 部分包含匹配
        matched_stds = {std for std, py in candidates.items() if py_clean in py or py in py_clean}

    if not matched_stds:
        return []

    # 查询这些标准语在各方言的说法
    for d in dialects_to_check:
        for row in data:
            if row[0] == d and row[2] in matched_stds:
                results.append(row)

    return results


def list_categories(dialect_name: str = "哈尔滨话") -> list:
    data = load_data()
    cats = set()
    for row in data:
        if row[0] == dialect_name:
            cats.add(row[1])
    return sorted(list(cats))


def list_all(dialect_name: str = "哈尔滨话", limit: int = None) -> list:
    data = load_data()
    results = []
    for row in data:
        if row[0] == dialect_name:
            results.append(row[1:])  # category, standard_word, dialect_word, remark
    if limit:
        results = results[:limit]
    return results


def format_output(results: list, keyword: str) -> str:
    """格式化输出"""
    if not results:
        return f"未找到「{keyword}」的相关记录"

    by_std = {}
    for row in results:
        dialect, cat, std, dia, remark = row
        key = std
        if key not in by_std:
            by_std[key] = {}
        if dialect not in by_std[key]:
            by_std[key][dialect] = []
        by_std[key][dialect].append((dia, remark))

    lines = []
    active_dialects = DIALECTS
    dialect_header = " / ".join(active_dialects)

    lines.append(f"🔍 查询「{keyword}」：")
    lines.append(f"   普通话 → {dialect_header}")
    lines.append("-" * 80)

    for std, dialect_data in by_std.items():
        dia_strs = []
        for d in active_dialects:
            if d in dialect_data:
                dias = [dia.strip() for dia, _ in dialect_data[d] if dia]
                if dias:
                    dia_strs.append(", ".join(dias))
                else:
                    dia_strs.append("")
            else:
                dia_strs.append("")

        line = f"  {std} → " + " / ".join(dia_strs)
        lines.append(line)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="方言查询工具 v9（支持 SQLite/JSON + 拼音搜索）")
    parser.add_argument("keyword", nargs="?", help="查询词（普通话/方言/拼音均可）")
    parser.add_argument("--dialect", help="指定方言查询（如：上海话）")
    parser.add_argument("--category", help="按分类查询")
    parser.add_argument("--list-categories", action="store_true", help="列出所有分类")
    parser.add_argument("--list-all", action="store_true", help="列出所有词条")
    parser.add_argument("--fuzzy", action="store_true", help="模糊查询")
    parser.add_argument("--limit", type=int, default=20, help="限制条数")
    args = parser.parse_args()

    if args.list_categories:
        dialect = args.dialect or "哈尔滨话"
        cats = list_categories(dialect)
        print(f"📂 {dialect} 分类列表（共 {len(cats)} 个）：")
        for c in cats:
            print(f"  · {c}")
        return

    if args.list_all:
        dialect = args.dialect or "哈尔滨话"
        rows = list_all(dialect, limit=args.limit)
        print(f"📋 {dialect} 词条列表（前 {len(rows)} 条）：")
        for cat, std, dia, remark in rows:
            rem = f" [{remark}]" if remark else ""
            print(f"  {std} → {dia}{rem}")
        return

    if not args.keyword:
        print("用法：python3 query_dialect.py <关键词> [--dialect 方言名] [--fuzzy]")
        print("       python3 query_dialect.py <拼音>     # 拼音查询，如：ganma / zeihan")
        return

    # 拼音模式检测：纯英文字母输入 → 拼音查询
    if is_pure_pinyin(args.keyword):
        results = query_by_pinyin(args.keyword, args.dialect)
        if results:
            output = format_output(results, args.keyword)
            print(output)
        else:
            print(f"未找到拼音「{args.keyword}」对应的词条（可尝试输入汉字）")
        return

    results = query(args.keyword, args.dialect)
    output = format_output(results, args.keyword)
    print(output)


if __name__ == "__main__":
    main()