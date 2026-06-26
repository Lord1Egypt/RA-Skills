#!/usr/bin/env python3
"""
ETL 流程生成器 - 大数据专家版 (v2.0)
根据源表 DDL 生成标准化 ETL 加工 SQL

技能位置：~/.openclaw/workspace/skills/etl-generator/SKILL.md
"""

import re
import sys

def parse_table_ddl(ddl):
    """解析 CREATE TABLE 语句"""
    # 提取表名
    table_match = re.search(r'CREATE TABLE IF NOT EXISTS (\w+)', ddl)
    table_name = table_match.group(1) if table_match else "unknown"
    
    # 提取字段
    fields = []
    fields_section = re.search(r'\((.*?)\)\s*(?:PARTITIONED|TBLPROPERTIES|LIFECYCLE)', ddl, re.DOTALL)
    if fields_section:
        for line in fields_section.group(1).strip().split('\n'):
            line = line.strip().rstrip(',')
            if not line or line.startswith('--'):
                continue
            field_match = re.match(r'(\w+)\s+(\w+)(?:\(([^)]+)\))?(?:\s+COMMENT\s+[\'"]([^\'"]+)[\'"])?', line)
            if field_match:
                fields.append({
                    'name': field_match.group(1),
                    'type': field_match.group(2).upper(),
                    'size': field_match.group(3),
                    'comment': field_match.group(4) or ''
                })
    
    # 提取表注释
    comment_match = re.search(r"'comment'[ ]*=[ ]*'([^']+)'", ddl)
    table_comment = comment_match.group(1) if comment_match else ""
    
    return table_name, fields, table_comment

def is_time_field(field_name, field_type):
    """判断是否为时间字段（需要时区转换）"""
    # _at 或 _time 结尾，且类型为 TIMESTAMP
    if field_type == 'TIMESTAMP':
        return True
    if field_name.endswith('_at') or field_name.endswith('_time'):
        return True
    return False

def is_date_field(field_name):
    """判断是否为日期字段（不需要时区转换）"""
    # _date 结尾的字段不转换
    return field_name.endswith('_date')

def convert_type_for_dwd(field_name, field_type):
    """转换字段类型：TIMESTAMP → STRING"""
    if is_time_field(field_name, field_type) and not is_date_field(field_name):
        return 'STRING'
    return field_type

def generate_select_field(field, is_incremental=False, timezone='${timezone}'):
    """生成 SELECT 字段表达式"""
    field_name = field['name']
    field_type = field['type']
    
    # 日期字段不转换
    if is_date_field(field_name):
        if is_incremental:
            return f'get_json_object(values, "$.{field_name}") as {field_name}'
        return field_name
    
    # 时间字段需要时区转换
    if is_time_field(field_name, field_type):
        if is_incremental:
            return f'DATE_FORMAT(FROM_UTC_TIMESTAMP(get_json_object(values, "$.{field_name}"),"{timezone}"),"yyyy-MM-dd HH:mm:ss.SSS") AS {field_name}'
        return f'DATE_FORMAT(FROM_UTC_TIMESTAMP({field_name},"{timezone}"),"yyyy-MM-dd HH:mm:ss.SSS") AS {field_name}'
    
    # 普通字段直接映射
    if is_incremental:
        return f'get_json_object(values, "$.{field_name}") as {field_name}'
    return field_name

def generate_target_table_ddl(table_name, fields, table_comment):
    """生成目标表 DDL"""
    # 表名转换：ods_[表名]_di → dwd_[表名]_di
    dwd_table_name = table_name.replace('ods_', 'dwd_')
    
    ddl = f"""-- 目标表 DDL
CREATE TABLE IF NOT EXISTS {dwd_table_name}(
"""
    field_defs = []
    for field in fields:
        target_type = convert_type_for_dwd(field['name'], field['type'])
        field_def = f"  {field['name']} {target_type}"
        if field['comment']:
            field_def += f" COMMENT '{field['comment']}'"
        field_defs.append(field_def)
    
    ddl += ',\n'.join(field_defs)
    ddl += f"""
) 
PARTITIONED BY (ds STRING) 
STORED AS ALIORC  
TBLPROPERTIES ("columnar.nested.type"="true", "comment"="{table_comment}") 
LIFECYCLE 36500;
"""
    return ddl

def generate_etl_sql(table_name, fields, table_comment):
    """生成 ETL 加工 SQL（大数据专家规范 v2.0）"""
    # 表名转换：ods_[表名]_di → dwd_[表名]_di
    dwd_table_name = table_name.replace('ods_', 'dwd_')
    
    # 提取基础表名（去掉 ods_前缀和_di后缀）
    base_table_name = table_name.replace('ods_', '').replace('_di', '')
    
    # 识别主键字段（通常是 id）
    primary_keys = ['id']
    
    # 识别时间字段
    time_fields = [f['name'] for f in fields if is_time_field(f['name'], f['type'])]
    
    # 生成 SELECT 字段列表（全量）
    select_fields_full = []
    for field in fields:
        select_fields_full.append(generate_select_field(field, is_incremental=False))
    
    # 生成 SELECT 字段列表（增量）
    select_fields_incr = []
    for field in fields:
        select_fields_incr.append(generate_select_field(field, is_incremental=True))
    
    # 添加分区字段 ds
    if 'created_at' in time_fields:
        select_fields_full.append('DATE_FORMAT(FROM_UTC_TIMESTAMP(created_at,"${timezone}"),"yyyy-MM-dd") AS ds')
        select_fields_incr.append('DATE_FORMAT(FROM_UTC_TIMESTAMP(get_json_object(values, "$.created_at"),"${timezone}"),"yyyy-MM-dd") AS ds')
    else:
        select_fields_full.append('DATE_FORMAT(FROM_UTC_TIMESTAMP(updated_at,"${timezone}"),"yyyy-MM-dd") AS ds')
        select_fields_incr.append('DATE_FORMAT(FROM_UTC_TIMESTAMP(get_json_object(values, "$.updated_at"),"${timezone}"),"yyyy-MM-dd") AS ds')
    
    # 生成 WITH 子句
    with_clause = """-- ============================================
-- ETL 加工 SQL
-- 源表：{source_table}
-- 目标表：{target_table}
-- 表注释：{comment}
-- ============================================

WITH ods_data AS (
  SELECT
    {select_fields_full}
  FROM {source_table}
  WHERE ds >= "${{y-m-d}}"
  UNION ALL
  -- 增量数据：处理历史数据更新
  SELECT
    {select_fields_incr}
  FROM ods_data_base_di 
  WHERE (
    (
      _after_image_ = "Y"
      AND _operation_ IN ("INSERT", "UPDATE")
    )
    OR (
      _operation_ = "DELETE"
      AND _before_image_ = "Y"
    )
    OR _id_ IS NULL
  )
  AND ds >= "${{y-m-d}}"
  AND table_name = "{base_table_name}"
  AND db_name = "source_db"
)
INSERT OVERWRITE TABLE {target_table} PARTITION(ds)
SELECT `(rn)?+.+` FROM (
  SELECT 
    *,
    ROW_NUMBER() OVER(PARTITION BY {primary_key} ORDER BY updated_at DESC) as rn 
  FROM (
    SELECT * FROM {target_table} WHERE ds IN (
      SELECT DISTINCT ds FROM ods_data
    )
    UNION ALL
    SELECT * FROM ods_data
  ) a
) t1
WHERE rn = 1
;""".format(
        source_table=table_name,
        target_table=dwd_table_name,
        comment=table_comment,
        select_fields_full=',\n    '.join(select_fields_full),
        select_fields_incr=',\n    '.join(select_fields_incr),
        base_table_name=base_table_name,
        primary_key=', '.join(primary_keys)
    )
    
    return with_clause

def generate_quality_checks(table_name, fields):
    """生成数据质量检查 SQL"""
    dwd_table_name = table_name.replace('ods_', 'dwd_')
    
    # 识别关键字段
    pno_field = None
    returned_field = None
    for f in fields:
        if 'pno' in f['name'].lower() or 'order' in f['name'].lower() or 'no' in f['name'].lower():
            pno_field = f['name']
        if 'return' in f['name'].lower() or 'returned' in f['name'].lower():
            returned_field = f['name']
    
    checks = []
    
    # 1. 主键空值检查
    if pno_field:
        checks.append(f"""-- 1. {pno_field}空值检查
SELECT 
  'null_{pno_field.lower()}_check' as check_item,
  COUNT(*) as error_count,
  0 as threshold
FROM {dwd_table_name} 
WHERE {pno_field} IS NULL 
  AND ds = '${{bizdate}}';
""")
    
    # 2. 退货件比例检查
    if returned_field:
        checks.append(f"""-- 2. 退货件比例检查
SELECT 
  'return_rate_check' as check_item,
  ROUND(SUM(CASE WHEN {returned_field} = 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) * 100, 2) as return_rate,
  30.00 as max_threshold
FROM {dwd_table_name} 
WHERE ds = '${{bizdate}}';
""")
    
    # 3. 数据量对比
    checks.append(f"""-- 3. 数据量对比
SELECT 
  'volume_check' as check_item,
  source_count,
  target_count,
  ROUND(ABS(source_count - target_count) * 1.0 / source_count * 100, 2) as diff_percent
FROM (
  SELECT 
    (SELECT COUNT(*) FROM {table_name} WHERE ds = '${{bizdate}}') as source_count,
    (SELECT COUNT(*) FROM {dwd_table_name} WHERE ds = '${{bizdate}}') as target_count
) t;
""")
    
    return '\n'.join(checks)

def generate_field_mapping_doc(fields):
    """生成字段映射说明文档"""
    doc = """-- ============================================
-- 字段映射说明
-- ============================================
-- 源表字段 ({}个): {}
-- 目标表字段 ({}个): {}
-- 分区字段：ds
-- 
-- 字段转换规则:
""".format(
        len(fields),
        ', '.join([f['name'] for f in fields]),
        len(fields),
        ', '.join([f['name'] for f in fields])
    )
    
    for field in fields:
        target_type = convert_type_for_dwd(field['name'], field['type'])
        if is_time_field(field['name'], field['type']) and not is_date_field(field['name']):
            doc += f"-- {field['name']}: {field['type']} → {target_type}, 时区转换\n"
        elif field['name'] == 'pno' or 'pno' in field['name'].lower():
            doc += f"-- {field['name']}: TRIM(UPPER()) - 去空格转大写\n"
        elif field['name'] == 'returned' or 'return' in field['name'].lower():
            doc += f"-- {field['name']}: CASE WHEN 标准化\n"
        else:
            doc += f"-- {field['name']}: 直接映射\n"
    
    doc += "-- ============================================\n"
    
    return doc

# 主函数
def main():
    # 从命令行参数或标准输入获取 DDL
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file, 'r') as f:
            odps_ddl = f.read()
    else:
        # 从标准输入读取
        odps_ddl = sys.stdin.read()
    
    # 执行转换
    print("=" * 80)
    print("ETL 流程生成器 - 大数据专家版 (v2.0)")
    print("=" * 80)
    print()
    
    table_name, fields, table_comment = parse_table_ddl(odps_ddl)
    print(f"源表名：{table_name}")
    print(f"字段数：{len(fields)}")
    print(f"表注释：{table_comment}")
    print()
    
    # 生成目标表 DDL
    target_ddl = generate_target_table_ddl(table_name, fields, table_comment)
    print(target_ddl)
    print()
    
    # 生成 ETL SQL
    etl_sql = generate_etl_sql(table_name, fields, table_comment)
    print(etl_sql)
    print()
    
    # 生成数据质量检查 SQL
    quality_checks = generate_quality_checks(table_name, fields)
    print(quality_checks)
    print()
    
    # 生成字段映射说明
    field_mapping = generate_field_mapping_doc(fields)
    print(field_mapping)
    
    print()
    print("=" * 80)
    print("ETL 流程生成完成！")
    print("=" * 80)

if __name__ == '__main__':
    main()
