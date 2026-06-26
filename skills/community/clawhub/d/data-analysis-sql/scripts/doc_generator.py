#!/usr/bin/env python3
"""
表结构文档自动生成器
功能：根据用户提供的信息自动生成 Markdown 格式的表结构说明文档
用法：python doc_generator.py [--input <输入文件>] [--output <输出文件>]
       或直接运行按提示输入
"""

import sys
import re
import json
from datetime import datetime


def parse_table_definition(text: str) -> dict:
    """
    解析用户输入的表定义文本，返回结构化字典
    支持格式：
      表名: xxx
      字段1: 说明
      字段2: 说明
    """
    lines = text.strip().split('\n')
    result = {
        'table_name': '',
        'table_desc': '',
        'business_note': '',
        'fields': []
    }

    current_section = 'header'  # header / business / fields
    field_pattern = re.compile(r'^([^\s:：]+)[:：]\s*(.*)$')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 表名行
        if line.startswith('```') or line.startswith('#'):
            continue

        # 检测表头
        if re.match(r'^[\u4e00-\u9fa5a-zA-Z_]+\([\u4e00-\u9fa5a-zA-Z_()]+\)', line):
            # 格式：TableName（中文名）
            m = re.match(r'^([^\(（]+)[\(（]([\u4e00-\u9fa5]+)[\)）]$', line)
            if m:
                result['table_name'] = m.group(1).strip()
                result['table_desc'] = m.group(2).strip()

        # 检测字段行
        m = field_pattern.match(line)
        if m:
            col_name = m.group(1).strip()
            col_desc = m.group(2).strip()
            # 检测类型
            col_type = ''
            type_match = re.search(r'\b(INT|VARCHAR|TEXT|DATE|DATETIME|TIMESTAMP|BIGINT|DECIMAL|FLOAT|DOUBLE|BOOLEAN|JSON|UUID)\b', col_desc, re.IGNORECASE)
            if type_match:
                col_type = type_match.group(0)
            result['fields'].append({
                'name': col_name,
                'type': col_type,
                'description': col_desc
            })

    return result


def fields_to_markdown(fields: list, col_width: int = 20) -> str:
    """将字段列表格式化为 Markdown 表格"""
    if not fields:
        return ''
    lines = []
    # 表头
    lines.append(f"| {'字段名':<18} | {'类型':<12} | {'描述':<40} |")
    lines.append(f"|{'-'*20}|{'-'*14}|{'-'*42}|")
    # 数据行
    for f in fields:
        name = f['name'][:18]
        col_type = f['type'][:12]
        desc = f['description'][:40]
        lines.append(f"| {name:<18} | {col_type:<12} | {desc:<40} |")
    return '\n'.join(lines)


def generate_table_markdown(table: dict) -> str:
    """生成单个表的 Markdown 内容"""
    lines = []
    lines.append(f"### {table['table_name']}")
    lines.append('')
    if table['table_desc']:
        lines.append(f"> {table['table_desc']}")
        lines.append('')
    if table['business_note']:
        lines.append(f"**业务说明：** {table['business_note']}")
        lines.append('')
    lines.append(fields_to_markdown(table['fields']))
    lines.append('')
    return '\n'.join(lines)


def generate_full_document(tables: list, title: str = '表结构说明', output_path: str = None) -> str:
    """
    生成完整的表结构说明文档
    """
    doc = []
    doc.append(f"# {title}")
    doc.append('')
    doc.append(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    doc.append('')
    doc.append('---')
    doc.append('')

    # 目录
    doc.append('## 目录')
    doc.append('')
    for i, t in enumerate(tables, 1):
        anchor = t['table_name'].lower().replace(' ', '-')
        doc.append(f"{i}. [{t['table_name']}](#{anchor}) - {t['table_desc']}")
    doc.append('')

    # 各表详情
    doc.append('---')
    doc.append('')
    for t in tables:
        doc.append(generate_table_markdown(t))
        doc.append('')
        doc.append('---')
        doc.append('')

    # 关联关系图
    doc.append('## 关联关系')
    doc.append('')
    doc.append('```')
    for t in tables:
        if t.get('relations'):
            for rel in t['relations']:
                doc.append(f"{t['table_name']} {rel['type']} {rel['target']} ({rel['condition']})")
    doc.append('```')
    doc.append('')

    result = '\n'.join(doc)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)

    return result


def generate_sql_summary(sql: str, db_type: str = 'PostgreSQL') -> dict:
    """
    分析 SQL 并生成摘要信息（用于迁移参考）
    """
    # 提取表名
    from_pattern = re.compile(r'(?:FROM|JOIN)\s+(?:data_busi\.)?[""]?(\w+)[""]?', re.IGNORECASE)
    tables = list(dict.fromkeys(from_pattern.findall(sql)))

    # 提取字段
    select_pattern = re.compile(r'SELECT\s+(.*?)\s+FROM', re.IGNORECASE | re.DOTALL)
    select_match = select_pattern.search(sql)
    output_fields = []
    if select_match:
        fields_raw = select_match.group(1)
        field_items = [f.strip() for f in re.split(r',\s*', fields_raw)]
        for f in field_items:
            # 提取别名
            alias_m = re.search(r'(?:AS\s+)?[""]?(\w+)[""]?\s*(?:AS|$|,)', f)
            if alias_m:
                output_fields.append(alias_m.group(1))

    # 提取 CTE
    cte_pattern = re.compile(r'WITH\s+(\w+)\s+AS', re.IGNORECASE)
    ctes = cte_pattern.findall(sql)

    # 提取 WHERE 条件
    where_pattern = re.compile(r'WHERE\s+(.*?)(?:GROUP|ORDER|LIMIT|$)', re.IGNORECASE | re.DOTALL)
    where_match = where_pattern.search(sql)
    filters = []
    if where_match:
        filter_text = where_match.group(1).strip()
        conditions = re.findall(r'[""\'"]?(\w+)[""\'"]?\s*(?:=|>|<|IN|LIKE)\s*[""\'"]?([^"\'"\)]+)', filter_text)
        for c in conditions:
            filters.append({'field': c[0].strip(), 'op': '=', 'value': c[1].strip()[:50]})

    return {
        'db_type': db_type,
        'source_tables': tables,
        'ctes': ctes,
        'output_fields': output_fields[:20],  # 限制数量
        'filters': filters[:10],
        'line_count': len(sql.split('\n'))
    }


def generate_migration_doc(tables: list, sqls: list, target_db: str = 'MySQL') -> str:
    """
    生成可用于迁移的文档（表结构 + SQL 对照）
    """
    doc = []
    doc.append(f"# 数据迁移文档")
    doc.append('')
    doc.append(f"> 目标数据库：{target_db}")
    doc.append(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    doc.append('')
    doc.append('---')
    doc.append('')

    # 表清单
    doc.append('## 一、数据表清单')
    doc.append('')
    doc.append(f"| 序号 | 表名 | 描述 | 字段数 |")
    doc.append(f"|------|------|------|--------|")
    for i, t in enumerate(tables, 1):
        doc.append(f"| {i} | `{t['table_name']}` | {t['table_desc']} | {len(t['fields'])} |")
    doc.append('')

    # 各表结构
    doc.append('## 二、表结构详情')
    doc.append('')
    for t in tables:
        doc.append(generate_table_markdown(t))
    doc.append('')

    # SQL 清单
    doc.append('## 三、业务 SQL 清单')
    doc.append('')
    for i, sql_info in enumerate(sqls, 1):
        doc.append(f'#### SQL {i}（{sql_info["db_type"]}）')
        doc.append('')
        doc.append(f'**数据源表：** {", ".join(sql_info["source_tables"])}')
        doc.append(f'**CTE：** {", ".join(sql_info["ctes"]) if sql_info["ctes"] else "无"}')
        doc.append(f'**输出字段数：** {len(sql_info["output_fields"])}')
        doc.append('')
        doc.append('**过滤条件：**')
        for f in sql_info['filters']:
            doc.append(f"  - `{f['field']} {f['op']} {f['value']}`")
        doc.append('')

    return '\n'.join(doc)


def interactive_mode():
    """交互式生成文档"""
    print("=" * 50)
    print("表结构文档生成器")
    print("=" * 50)
    print()

    # 输入表数量
    n = int(input("请输入要录入的表数量: ").strip())
    tables = []

    for i in range(1, n + 1):
        print(f"\n--- 第 {i}/{n} 张表 ---")
        table_name = input("表名（如 meas_item）: ").strip()
        table_desc = input("中文描述（如 事项表）: ").strip()
        business_note = input("业务说明（直接回车跳过）: ").strip()

        print("请输入字段（输入空行结束）:")
        fields = []
        while True:
            line = input("  字段名: ").strip()
            if not line:
                break
            parts = line.split(':', 1)
            if len(parts) == 2:
                fields.append({'name': parts[0].strip(), 'type': '', 'description': parts[1].strip()})
            else:
                fields.append({'name': parts[0].strip(), 'type': '', 'description': ''})

        tables.append({
            'table_name': table_name,
            'table_desc': table_desc,
            'business_note': business_note,
            'fields': fields
        })

    output_file = input("\n输出文件路径（直接回车输出到屏幕）: ").strip()

    if output_file:
        content = generate_full_document(tables, f'表结构说明_{datetime.now().strftime("%Y%m%d")}', output_file)
        print(f"\n✅ 文档已保存至: {output_file}")
    else:
        content = generate_full_document(tables)
        print(content)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        interactive_mode()
    elif '--help' in sys.argv or '-h' in sys.argv:
        print("用法:")
        print("  python doc_generator.py                # 交互式输入")
        print("  python doc_generator.py --help        # 显示帮助")
    else:
        print("详细用法请参考 doc-guide.md")
