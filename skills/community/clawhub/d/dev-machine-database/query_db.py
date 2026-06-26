#!/usr/bin/env python3
"""
开发机数据库查询工具
通过 SSH 连接到 datax 开发机，查询 MySQL 数据库中的 dw 库
"""

import subprocess
import json
import re
import sys

# 配置
DEV_MACHINE = "datax"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"  # MySQL 密码
DATABASE = "dw"  # 默认数据库名
MYSQL_CONTAINER = "mysql"  # Docker 容器名

def ssh_command(cmd, timeout=30):
    """执行 SSH 命令"""
    try:
        result = subprocess.run(
            ["ssh", DEV_MACHINE, cmd],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "SSH 命令超时"
    except Exception as e:
        return -1, "", str(e)

def query_mysql_docker(sql, database=DATABASE, limit=50):
    """通过 Docker exec 查询 MySQL"""
    # 添加 LIMIT 限制
    if "LIMIT" not in sql.upper() and sql.strip().upper().startswith("SELECT"):
        sql = f"{sql.rstrip(';')} LIMIT {limit}"
    
    # Docker exec 命令
    cmd = f'docker exec {MYSQL_CONTAINER} mysql -u{MYSQL_USER} -p{MYSQL_PASSWORD} {database} -e "{sql}"'
    
    # SSH 执行
    returncode, stdout, stderr = ssh_command(cmd)
    
    if returncode == 0:
        return True, stdout
    else:
        return False, stderr if stderr else stdout

def show_tables(database=DATABASE):
    """显示数据库中的所有表"""
    return query_mysql_docker(f"SHOW TABLES", database)

def desc_table(table_name, database=DATABASE):
    """查看表结构"""
    return query_mysql_docker(f"DESC {table_name}", database)

def select_data(table_name, columns="*", where="", database=DATABASE, limit=50):
    """查询表数据"""
    sql = f"SELECT {columns} FROM {table_name}"
    if where:
        sql += f" WHERE {where}"
    return query_mysql_docker(sql, database, limit)

def count_rows(table_name, database=DATABASE):
    """统计表行数"""
    return query_mysql_docker(f"SELECT COUNT(*) FROM {table_name}", database, 1)

def parse_mysql_output(output):
    """解析 MySQL 输出为表格"""
    lines = output.strip().split('\n')
    if len(lines) < 2:
        return []
    
    # 解析表头
    headers = lines[0].split('\t')
    
    # 解析数据行
    rows = []
    for line in lines[1:]:
        if line.startswith('-+') or not line.strip():
            continue
        rows.append(line.split('\t'))
    
    return headers, rows

def format_table(headers, rows):
    """格式化为 Markdown 表格"""
    if not headers or not rows:
        return "无数据"
    
    # 构建表格
    markdown = "| " + " | ".join(headers) + " |\n"
    markdown += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    
    for row in rows[:50]:  # 最多显示 50 行
        markdown += "| " + " | ".join([str(cell) for cell in row]) + " |\n"
    
    if len(rows) > 50:
        markdown += f"\n*... 还有 {len(rows) - 50} 行 ...*"
    
    return markdown

def main():
    """主函数 - 测试用"""
    print("=" * 80)
    print("开发机数据库查询工具")
    print("=" * 80)
    
    # 测试连接
    print("\n测试连接...")
    success, result = show_tables()
    
    if success:
        print("✅ 连接成功！")
        print("\n数据库中的表:")
        print(result)
    else:
        print("❌ 连接失败:")
        print(result)

if __name__ == "__main__":
    main()
