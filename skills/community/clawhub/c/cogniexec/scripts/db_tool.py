#!/usr/bin/env python3
"""
db_tool.py — SQLite 数据库工具（纯标准库）
覆盖：建表/查询/导入导出/Schema检查/CSV↔DB互转/批量执行SQL

用法：
  python db_tool.py create mydb.sqlite
  python db_tool.py query mydb.sqlite "SELECT * FROM users"
  python db_tool.py exec mydb.sqlite "CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)"
  python db_tool.py schema mydb.sqlite
  python db_tool.py tables mydb.sqlite
  python db_tool.py import-csv mydb.sqlite data.csv --table users
  python db_tool.py export mydb.sqlite users -o users.csv
  python db_tool.py batch-exec mydb.sqlite sql_file.sql
  python db_tool.py dump mydb.sqlite
  python db_tool.py info mydb.sqlite
"""

import sys
import os
import sqlite3
import csv
import json
import re
from typing import Optional


# ─── CLI ──────────────────────────────────────────────────────

def parse_args(argv=None):
    argv = argv or sys.argv[1:]
    if not argv or '-h' in argv or '--help' in argv:
        print(__doc__)
        sys.exit(0)
    cmd = argv[0]
    args = {'_cmd': cmd, '_pos': []}
    i = 1
    while i < len(argv):
        a = argv[i]
        if a.startswith('-'):
            key = a.lstrip('-').replace('-', '_')
            if i + 1 < len(argv) and not argv[i+1].startswith('-'):
                args[key] = argv[i + 1]
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            args['_pos'].append(a)
            i += 1
    return args


def color(text: str, fg: str = '') -> str:
    codes = {'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'cyan': 36}
    code = codes.get(fg, '')
    if not code:
        return text
    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        return f'\033[{code}m{text}\033[0m'
    return text


def echo(text: str, fg: str = '', bold=False):
    print(color(text, fg))


# ══════════════════════════════════════════════════════════════
#  命令实现
# ══════════════════════════════════════════════════════════════

def _get_db(args) -> sqlite3.Connection:
    """从参数获取数据库路径并返回连接"""
    pos = args.get('_pos', [])
    if not pos:
        echo('❌ 缺少数据库文件路径', 'red')
        sys.exit(1)
    db_path = pos[0]
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn, db_path


def _validate_identifier(name: str) -> str:
    """校验 SQL 标识符（表名/列名），只允许字母数字下划线，防止 SQL 注入"""
    if not re.match(r'^[a-zA-Z_\u4e00-\u9fff][a-zA-Z0-9_\u4e00-\u9fff]*$', name):
        raise ValueError(f"无效的标识符: {name!r}（只允许字母、数字、下划线）")
    return name


def _format_row(row, columns):
    """格式化单行输出"""
    if isinstance(row, sqlite3.Row):
        return {col: row[col] for col in columns}
    return dict(zip(columns, row)) if hasattr(row, '__len__') else row


# ─── 创建数据库 ─────────────────────────────────────────────

def cmd_create(args):
    """创建新的 SQLite 数据库"""
    pos = args.get('_pos', [])
    if not pos:
        echo('❌ 请指定数据库名称', 'red')
        sys.exit(1)
    db_path = pos[0]
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        echo(f'⚠️  数据库已存在: {db_path} ({size} bytes)', 'yellow')
        return
    conn = sqlite3.connect(db_path)
    # 启用外键约束
    conn.execute('PRAGMA foreign_keys=ON')
    # 启用 WAL 模式提升并发性能
    conn.execute('PRAGMA journal_mode=WAL')
    conn.commit()
    conn.close()
    echo(f'✅ 数据库已创建: {db_path}', 'green')


# ─── 执行 SQL 查询 ──────────────────────────────────────────

def cmd_query(args):
    """执行 SELECT 查询并以表格形式输出结果"""
    conn, db_path = _get_db(args)
    pos = args.get('_pos', [])

    if len(pos) < 2:
        echo('❌ 缺少 SQL 查询语句', 'red')
        conn.close()
        sys.exit(1)

    sql = pos[1]
    fmt = args.get('format', '')          # json / csv / table (default)
    limit_val = args.get('limit')         # 行数限制
    header_only = args.get('header')

    try:
        cursor = conn.cursor()
        if limit_val:
            # 校验 limit 值为正整数，防止注入
            try:
                limit_int = int(limit_val)
                if limit_int < 1:
                    raise ValueError
            except (ValueError, TypeError):
                echo('❌ --limit 必须是正整数', 'red')
                conn.close()
                sys.exit(1)
            sql = f"{sql} LIMIT {limit_int}"
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        if header_only:
            echo(', '.join(columns), 'cyan')
            conn.close()
            return

        if fmt == 'json':
            result = [_format_row(r, columns) for r in rows]
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif fmt == 'csv':
            writer = csv.writer(sys.stdout)
            writer.writerow(columns)
            for r in rows:
                writer.writerow(list(r))
        else:
            # 表格输出
            if not rows:
                echo('(空结果集)', 'yellow')
            else:
                _print_table(columns, rows)

        echo(f'\n📊 共 {len(rows)} 行', 'cyan')
    except Exception as e:
        echo(f'❌ 查询失败: {e}', 'red')
        sys.exit(1)
    finally:
        conn.close()


# ─── 执行 SQL（非查询） ─────────────────────────────────────

def cmd_exec(args):
    """执行 INSERT/UPDATE/DELETE/DDL 等非查询语句"""
    conn, db_path = _get_db(args)
    pos = args.get('_pos', [])

    if len(pos) < 2:
        echo('❌ 缺少 SQL 语句', 'red')
        conn.close()
        sys.exit(1)

    sql = pos[1]
    dry_run = args.get('dry_run')

    if dry_run:
        echo(f'[DRY RUN] 将执行: {sql}', 'yellow')
        conn.close()
        return

    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        affected = cursor.rowcount
        lastid = cursor.lastrowid
        msg = f'✅ 执行成功'
        if affected >= 0:
            msg += f' | 影响行数: {affected}'
        if lastid is not None:
            msg += f' | 最后插入ID: {lastid}'
        echo(msg, 'green')
    except Exception as e:
        echo(f'❌ 执行失败: {e}', 'red')
        sys.exit(1)
    finally:
        conn.close()


# ─── Schema 信息 ────────────────────────────────────────────

def cmd_schema(args):
    """显示表结构（字段、类型、约束）"""
    conn, db_path = _get_db(args)
    pos = args.get('_pos', [])
    table_name = pos[1] if len(pos) > 1 else None
    detail = args.get('detail')   # 显示完整信息含索引

    try:
        cursor = conn.cursor()

        if table_name:
            # 单表结构
            _validate_identifier(table_name)
            cursor.execute(f"PRAGMA table_info('{table_name}')")
            cols = cursor.fetchall()
            if not cols:
                echo(f'❌ 表不存在: {table_name}', 'red')
                conn.close()
                sys.exit(1)

            echo(f'\n📋 表: {table_name}', 'bold')
            print(f"{'字段':<20} {'类型':<12} {'NOT NULL':<8} {'默认值':<15} {'主键'}")
            print('-' * 70)
            for c in cols:
                cid, name, ctype, notnull, default, pk = c
                pk_str = 'PK' if pk else ''
                nn_str = 'YES' if notnull else ''
                def_str = str(default) if default is not None else ''
                print(f"{name:<20} {str(ctype):<12} {nn_str:<8} {def_str:<15} {pk_str}")

            if detail:
                # 索引信息
                cursor.execute(f"PRAGMA index_list('{table_name}')")
                indexes = cursor.fetchall()
                if indexes:
                    echo(f'\n  索引:', 'cyan')
                    for idx in indexes:
                        echo(f'    - {idx[1]} (unique={bool(idx[2])})', 'cyan')

                # 外键信息
                cursor.execute(f"PRAGMA foreign_key_list('{table_name}')")
                indexes = cursor.fetchall()
                if indexes:
                    echo(f'\n  索引:', 'cyan')
                    for idx in indexes:
                        echo(f'    - {idx[1]} (unique={bool(idx[2])})', 'cyan')

                # 外键信息
                cursor.execute(f"PRAGMA foreign_key_list('{table_name}')")
                fks = cursor.fetchall()
                if fks:
                    echo(f'\n  外键:', 'cyan')
                    for fk in fks:
                        echo(f'    - {fk[3]} -> {fk[2]}({fk[4]})', 'cyan')
        else:
            # 所有表的结构概览
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = [r[0] for r in cursor.fetchall()]
            if not tables:
                echo('⚠️  数据库中没有表', 'yellow')
                conn.close()
                return

            for t in tables:
                _validate_identifier(t)
                cursor.execute(f"PRAGMA table_info('{t}')")
                cols = cursor.fetchall()
                col_names = [c[1] for c in cols]
                echo(f'\n📋 {t}: ({", ".join(col_names)})', 'cyan')

    except Exception as e:
        echo(f'❌ 获取 Schema 失败: {e}', 'red')
        sys.exit(1)
    finally:
        conn.close()


# ─── 列出所有表 ────────────────────────────────────────────

def cmd_tables(args):
    """列出所有表及其行数"""
    conn, db_path = _get_db(args)

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        rows = cursor.fetchall()

        if not rows:
            echo('⚠️  数据库中没有表', 'yellow')
            conn.close()
            return

        echo(f'\n📁 数据库: {os.path.basename(db_path)}', 'bold')
        print(f"{'表名':<30} {'行数':>10}")
        print('-' * 45)
        total_rows = 0
        for r in rows:
            tname = r[0]
            try:
                c2 = conn.cursor()
                c2.execute(f'SELECT COUNT(*) FROM "{tname}"')
                cnt = c2.fetchone()[0]
                total_rows += cnt
                print(f"{tname:<30} {cnt:>10}")
            except Exception:
                print(f"{tname:<30} {'ERROR':>10}")
        print('-' * 45)
        echo(f'共 {len(rows)} 张表, 总计 {total_rows} 行', 'cyan')

    except Exception as e:
        # 如果上面的子查询失败（某些表可能有问题），用简单方式
        try:
            cursor2 = conn.cursor()
            cursor2.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
            tables = [r[0] for r in cursor2.fetchall()]
            for t in tables:
                echo(f'  - {t}', 'cyan')
            echo(f'共 {len(tables)} 张表', 'cyan')
        except Exception as e2:
            echo(f'❌ 查询失败: {e2}', 'red')
    finally:
        conn.close()


# ─── CSV 导入到表 ──────────────────────────────────────────

def cmd_import_csv(args):
    """将 CSV 文件导入为数据库表"""
    conn, db_path = _get_db(args)
    pos = args.get('_pos', [])

    if len(pos) < 2:
        echo('❌ 缺少 CSV 文件路径', 'red')
        conn.close()
        sys.exit(1)

    csv_path = pos[1]
    table = args.get('table') or os.path.splitext(os.path.basename(csv_path))[0]
    skip_existing = args.get('skip')
    detect_type = args.get('detect')     # 自动检测列类型

    if not os.path.exists(csv_path):
        echo(f'❌ CSV 文件不存在: {csv_path}', 'red')
        conn.close()
        sys.exit(1)

    try:
        with open(csv_path, 'r', encoding='utf-8-sig', newline='') as f:
            reader = csv.reader(f)
            headers = next(reader)
            # 清洗列名
            headers = [re.sub(r'[^a-zA-Z0-9_]', '_', h.strip()) for h in headers]

            rows_data = list(reader)

        if skip_existing:
            # 检查表是否存在
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?", (table,))
            if cursor.fetchone()[0]:
                echo(f'⚠️  表 {table} 已存在，跳过创建', 'yellow')
            else:
                _create_table_from_csv(conn, table, headers, rows_data, detect_type)
        else:
            _create_table_from_csv(conn, table, headers, rows_data, detect_type)

        # 插入数据
        if rows_data:
            placeholders = ', '.join(['?' for _ in headers])
            insert_sql = f'INSERT INTO "{table}" VALUES ({placeholders})'
            cursor = conn.cursor()
            cursor.executemany(insert_sql, rows_data)
            conn.commit()
            echo(f'✅ 导入完成: {len(rows_data)} 行 → 表 {table}', 'green')
        else:
            echo(f'⚠️  CSV 无数据行（仅创建了表 {table}）', 'yellow')

    except Exception as e:
        echo(f'❌ 导入失败: {e}', 'red')
        sys.exit(1)
    finally:
        conn.close()


def _create_table_from_csv(conn, table, headers, rows_data, detect_type=False):
    """根据 CSV 头和数据推断建表语句"""
    col_defs = []
    for i, h in enumerate(headers):
        if detect_type and rows_data:
            sample = [row[i] for row in rows_data[:100] if i < len(row)]
            col_type = _infer_column_type(sample)
        else:
            col_type = 'TEXT'
        col_defs.append(f'"{h}" {col_type}')

    sql = f'CREATE TABLE IF NOT EXISTS "{table}" ({", ".join(col_defs)})'
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


def _infer_column_type(samples):
    """推断列的数据类型"""
    int_count, float_count, other_count = 0, 0, 0
    for v in samples:
        v = v.strip()
        if not v:
            continue
        try:
            int(v)
            int_count += 1
        except ValueError:
            try:
                float(v)
                float_count += 1
            except ValueError:
                other_count += 1

    if other_count == 0:
        if float_count == 0:
            return 'INTEGER'
        elif int_count == 0:
            return 'REAL'
        return 'REAL'
    return 'TEXT'


# ─── 导出表为 CSV ──────────────────────────────────────────

def cmd_export(args):
    """将表或查询结果导出为 CSV/JSON"""
    conn, db_path = _get_db(args)
    pos = args.get('_pos', [])

    if len(pos) < 2:
        echo('❌ 缺少表名或查询语句', 'red')
        conn.close()
        sys.exit(1)

    target = pos[1]
    output = args.get('o') or f'{target}.csv'
    fmt = args.get('format', '')
    if output.endswith('.json'):
        fmt = 'json'

    try:
        cursor = conn.cursor()
        # 判断是表名还是 SQL
        if target.upper().startswith('SELECT'):
            sql = target
        else:
            sql = f'SELECT * FROM "{target}"'

        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        out_dir = os.path.dirname(output)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        if fmt == 'json':
            result = [_format_row(r, columns) for r in rows]
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        else:
            with open(output, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                for r in rows:
                    writer.writerow(list(r))

        echo(f'✅ 导出完成: {len(rows)} 行 → {output}', 'green')

    except Exception as e:
        echo(f'❌ 导出失败: {e}', 'red')
        sys.exit(1)
    finally:
        conn.close()


# ─── 批量执行 SQL 文件 ─────────────────────────────────────

def cmd_batch_exec(args):
    """从 SQL 文件批量执行语句（分号分隔）"""
    conn, db_path = _get_db(args)
    pos = args.get('_pos', [])

    if len(pos) < 2:
        echo('❌ 缺少 SQL 文件路径', 'red')
        conn.close()
        sys.exit(1)

    sql_file = pos[1]
    dry_run = args.get('dry_run')

    if not os.path.exists(sql_file):
        echo(f'❌ SQL 文件不存在: {sql_file}', 'red')
        conn.close()
        sys.exit(1)

    with open(sql_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 分割 SQL 语句（简单按分号分割，忽略字符串内的）
    statements = []
    current = []
    in_string = False
    string_char = None
    for ch in content:
        if ch in ('"', "'") and not in_string:
            in_string = True
            string_char = ch
            current.append(ch)
        elif ch == string_char and in_string:
            in_string = False
            current.append(ch)
            string_char = None
        elif ch == ';' and not in_string:
            stmt = ''.join(current).strip()
            if stmt:
                statements.append(stmt)
            current = []
        else:
            current.append(ch)

    tail = ''.join(current).strip()
    if tail:
        statements.append(tail)

    if not statements:
        echo('⚠️  SQL 文件没有可执行的语句', 'yellow')
        conn.close()
        return

    echo(f'📄 解析到 {len(statements)} 条语句\n', 'cyan')

    success, failed = 0, 0
    cursor = conn.cursor()
    for idx, stmt in enumerate(statements, 1):
        # 跳过纯注释和空白
        stripped = stmt.strip()
        if not stripped or stripped.startswith('--'):
            continue
        if dry_run:
            echo(f'  [{idx}] {stripped[:80]}{"..." if len(stripped) > 80 else ""}', 'yellow')
            success += 1
            continue
        try:
            cursor.execute(stmt)
            conn.commit()
            echo(f'  [{idx}] ✅ OK  | {stripped[:60]}{"..." if len(stripped) > 60 else ""}', 'green')
            success += 1
        except Exception as e:
            echo(f'  [{idx}] ❌ ERR| {str(e)[:60]}', 'red')
            failed += 1

    echo(f'\n▶ 完成: {success} 成功, {failed} 失败', 'green' if failed == 0 else 'red')
    conn.close()


# ─── 数据库 Dump（SQL 格式） ──────────────────────────────

def cmd_dump(args):
    """将整个数据库导出为 SQL 文件（类似 sqlite3 .dump）"""
    conn, db_path = _get_db(args)
    output = args.get('o') or (db_path + '.sql')
    data_mode = args.get('data')       # 是否包含数据（默认包含）
    no_data = str(data_mode).lower() in ('false', 'no', '0')

    try:
        cursor = conn.cursor()
        lines = []

        # 表定义
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
        tables = cursor.fetchall()

        if not tables:
            echo('⚠️  数据库中没有可导出的表', 'yellow')
            conn.close()
            return

        lines.append('-- Generated by db_tool.py')
        lines.append(f"-- Database: {os.path.basename(db_path)}")
        lines.append('--\n')

        for tbl_name, tbl_sql in tables:
            if tbl_sql:
                lines.append(f'DROP TABLE IF EXISTS "{tbl_name}";')
                lines.append(tbl_sql + ';')
                lines.append('')

                if not no_data:
                    cursor.execute(f'SELECT * FROM "{tbl_name}"')
                    rows = cursor.fetchall()
                    for row in rows:
                        vals = []
                        for v in row:
                            if v is None:
                                vals.append('NULL')
                            elif isinstance(v, (int, float)):
                                vals.append(str(v))
                            else:
                                escaped = str(v).replace("'", "''")
                                vals.append(f"'{escaped}'")
                        lines.append(f'INSERT INTO "{tbl_name}" VALUES ({",".join(vals)});')
                    lines.append('')

        # 索引
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%' AND sql IS NOT NULL")
        indexes = cursor.fetchall()
        for idx_name, idx_sql in indexes:
            lines.append(idx_sql + ';')
            lines.append('')

        content = '\n'.join(lines)
        out_dir = os.path.dirname(output)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        with open(output, 'w', encoding='utf-8') as f:
            f.write(content)

        table_count = len(tables)
        echo(f'✅ Dump 完成: {table_count} 张表 → {output}', 'green')

    except Exception as e:
        echo(f'❌ Dump 失败: {e}', 'red')
        sys.exit(1)
    finally:
        conn.close()


# ─── 数据库信息 ────────────────────────────────────────────

def cmd_info(args):
    """显示数据库概览信息（大小、页数、编码、版本等）"""
    conn, db_path = _get_db(args)

    try:
        cursor = conn.cursor()

        # 数据库文件信息
        file_size = os.path.getsize(db_path)

        # PRAGMA 信息
        pragmas = [
            ('page_size', 'PRAGMA page_size'),
            ('page_count', 'PRAGMA page_count'),
            ('encoding', 'PRAGMA encoding'),
            ('journal_mode', 'PRAGMA journal_mode'),
            ('foreign_keys', 'PRAGMA foreign_keys'),
            ('integrity_check', 'PRAGMA integrity_check'),
        ]

        echo(f'\n📦 数据库: {os.path.basename(db_path)}', 'bold')
        echo(f'   路径: {os.path.abspath(db_path)}', 'cyan')
        echo(f'   大小: {_format_size(file_size)}', 'cyan')
        echo('', '')

        # 表统计
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
        tables = [r[0] for r in cursor.fetchall()]
        echo(f'   表数量: {len(tables)}', 'cyan')

        total_rows = 0
        for t in tables:
            try:
                c2 = conn.cursor()
                c2.execute(f'SELECT COUNT(*) FROM "{t}"')
                cnt = c2.fetchone()[0]
                total_rows += cnt
            except:
                cnt = '?'

        echo(f'   总行数: {total_rows}', 'cyan')

        echo('\n--- PRAGMA ---', 'yellow')
        for label, pragma_sql in pragmas:
            try:
                cursor.execute(pragma_sql)
                val = cursor.fetchone()[0]
                print(f'  {label:<18}: {val}')
            except:
                pass

        # 版本
        echo(f'\n   SQLite 版本: {sqlite3.sqlite_version}', 'cyan')
        echo(f'   驱动版本:    {sqlite3.version}', 'cyan')

    except Exception as e:
        echo(f'❌ 获取信息失败: {e}', 'red')
    finally:
        conn.close()


# ─── 辅助函数 ──────────────────────────────────────────────

def _print_table(columns, rows):
    """打印简易表格"""
    widths = [max(
        len(str(col)),
        max((len(str(r[i])) if i < len(r) else 0 for r in rows), default=0)
    ) for i, col in enumerate(columns)]

    header = '| ' + ' | '.join(str(c).ljust(widths[i]) for i, c in enumerate(columns)) + ' |'
    sep = '+' + '+'.join('-' * (w + 2) for w in widths) + '+'

    print(sep)
    print(header)
    print(sep)
    for r in rows:
        line = '| ' + ' | '.join(str(r[i]).ljust(widths[i]) if i < len(r) else ''.ljust(widths[i]) for i in range(len(columns))) + ' |'
        print(line)
    print(sep)


def _format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(size_bytes) < 1024.0:
            return f'{size_bytes:.1f} {unit}'
        size_bytes /= 1024.0
    return f'{size_bytes:.1f} TB'


# ══════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════

COMMANDS = {
    'create': cmd_create,
    'query': cmd_query,
    'exec': cmd_exec,
    'schema': cmd_schema,
    'tables': cmd_tables,
    'import-csv': cmd_import_csv,
    'export': cmd_export,
    'batch-exec': cmd_batch_exec,
    'dump': cmd_dump,
    'info': cmd_info,
}

ALIASES = {
    'new': 'create', 'init': 'create',
    'select': 'query', 'q': 'query',
    'run': 'exec', 'execute': 'exec',
    'describe': 'schema', 'desc': 'schema', 'struct': 'schema',
    'ls': 'tables', 'list-tables': 'tables',
    'import': 'import-csv', 'csv-import': 'import-csv',
    'export-csv': 'export',
    'batch': 'batch-exec', 'source': 'batch-exec',
    'backup': 'dump', 'dump-sql': 'dump',
    'status': 'info', 'overview': 'info', 'about': 'info',
}


def main():
    args = parse_args()
    cmd = args['_cmd']
    cmd = ALIASES.get(cmd, cmd)

    if cmd not in COMMANDS:
        available = ', '.join(sorted(set(list(COMMANDS.keys()) + list(ALIASES.keys()))))
        echo(f'❌ 未知命令: {cmd}', 'red')
        echo(f'可用命令: {available}', 'cyan')
        sys.exit(1)

    COMMANDS[cmd](args)


if __name__ == '__main__':
    main()
