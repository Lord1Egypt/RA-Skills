#!/usr/bin/env python3
"""
增量添加方言生词脚本

使用方法：
    python3 add_word.py <普通话> <方言词> [方言区] [词性] [备注]

示例：
    python3 add_word.py "冷门" "嘎咕" "哈尔滨话" "形容词" "形容很偏门"
    python3 add_word.py "找东西" "撒磨" "哈尔滨话" "动词"

流程：
    1. 追加到 memory/new_words.md 日志
    2. 追加到 data/incremental_words.sql（INSERT OR IGNORE）
"""

import sys
import os
import sqlite3

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_DIR = os.path.join(SCRIPT_DIR, "memory")
INCR_SQL = os.path.join(SCRIPT_DIR, "data", "incremental_words.sql")
DB_PATH = os.path.join(SCRIPT_DIR, "data", "dialect.db")


def get_today():
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d')


def add_to_log(std_word, dial_word, dial_name, category, remark):
    """追加到生词日志"""
    os.makedirs(MEMORY_DIR, exist_ok=True)
    log_file = os.path.join(MEMORY_DIR, "new_words.md")

    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    date_header = f"## {today}"

    # 检查今日是否已有记录
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if date_header not in content:
            # 插入日期分隔
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n\n{date_header}\n\n")
                f.write("| 序号 | 普通话 | 方言词 | 方言区 | 词性 | 备注 |\n")
                f.write("|------|--------|--------|--------|------|------|\n")

    # 读出行号（排除表头行 | 序号 |）
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    seq = sum(1 for line in lines if line.startswith('| ') and '|' in line and '序号' not in line)


    row = f"| {seq} | {std_word} | {dial_word} | {dial_name} | {category} | {remark} |\n"

    # 追加行（首次建表头时直接写入，不重复检查）
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(row)

    print(f"✅ 已记入日志: {std_word} → {dial_word}")


def add_to_sql(std_word, dial_word, dial_name, category, remark):
    """追加到增量SQL"""
    sql = f"INSERT OR IGNORE INTO dialect_map (dialect_name, category, standard_word, dialect_word, remark) VALUES ('{dial_name}', '{category}', '{std_word}', '{dial_word}', '{remark}');\n"
    with open(INCR_SQL, 'a', encoding='utf-8') as f:
        f.write(sql)
    print(f"✅ 已写入增量SQL: {INCR_SQL}")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    std_word = sys.argv[1]
    dial_word = sys.argv[2]
    dial_name = sys.argv[3] if len(sys.argv) > 3 else "哈尔滨话"
    category = sys.argv[4] if len(sys.argv) > 4 else "动词"
    remark = sys.argv[5] if len(sys.argv) > 5 else ""

    add_to_log(std_word, dial_word, dial_name, category, remark)
    add_to_sql(std_word, dial_word, dial_name, category, remark)

    print(f"\n🎉 生词添加完成！")
    print(f"   普通话：{std_word}")
    print(f"   方言词：{dial_word}（{dial_name}）")
    print(f"   词性：{category}")
    if remark:
        print(f"   备注：{remark}")
    print(f"\n运行 python3 init_db.py 合并到数据库")


if __name__ == "__main__":
    main()