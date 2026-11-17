#!/usr/bin/env python3
"""
企服助手 - 腾讯文档→SQLite同步脚本
从腾讯文档智能表格读取数据，写入本地SQLite数据库
用法：
  python sync_to_sqlite.py --all              # 同步所有表
  python sync_to_sqlite.py --table customers  # 同步指定表
  python sync_to_sqlite.py --force           # 强制全量同步（忽略缓存）
"""

import sqlite3
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 数据库路径
DB_PATH = Path.home() / ".workbuddy" / "workspace" / "enterprise-service-assistant" / "local_db.sqlite"

# 腾讯文档配置（从知识库配置读取）
CONFIG_PATH = Path.home() / ".workbuddy" / "config" / "enterprise-service-assistant" / "knowledge_base_config.json"

def load_config():
    """加载腾讯文档配置"""
    if not CONFIG_PATH.exists():
        print(f"❌ 配置文件不存在：{CONFIG_PATH}")
        print(f"请先创建配置文件：cp knowledge_base_config.example.json {CONFIG_PATH}")
        sys.exit(1)
    
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    if config.get('source_type') != 'tencent_docs':
        print(f"❌ 当前数据源类型为 {config.get('source_type')}，本脚本仅支持 tencent_docs")
        sys.exit(1)
    
    return config['source_config']

def init_db():
    """初始化数据库（如果不存在）"""
    if not DB_PATH.exists():
        print("📊 数据库不存在，正在初始化...")
        from init_db import init_database
        init_database()

def sync_customers(conn, doc_id):
    """同步客户管理表"""
    print("🔄 同步客户管理表...")
    
    # TODO: 实际使用时，AI会调用 MCP 工具读取数据
    # 这里提供脚本框架，实际数据读取由AI执行
    
    cursor = conn.cursor()
    
    # 清空表（全量同步）
    cursor.execute("DELETE FROM customers")
    
    # 示例数据插入（实际应从MCP读取）
    # data = mcp__tencent-docs__smartsheet.list_records(doc_id, table_id='👨客户管理👨')
    
    print("  ⚠️  本脚本为框架，实际同步需由AI调用MCP工具执行")
    print("  💡 触发方式：@企服助手 同步数据库")
    
    conn.commit()
    return 0

def sync_fees(conn, doc_id):
    """同步费用收缴表"""
    print("🔄 同步费用收缴表...")
    # TODO: 实现同步逻辑
    return 0

def sync_repair_orders(conn, doc_id):
    """同步报修情况汇总表"""
    print("🔄 同步报修情况汇总表...")
    # TODO: 实现同步逻辑
    return 0

def sync_inventory(conn, doc_id):
    """同步库存管理表"""
    print("🔄 同步库存管理表...")
    # TODO: 实现同步逻辑
    return 0

def sync_cservice_records(conn, doc_id):
    """同步C+服务记录表"""
    print("🔄 同步C+服务记录表...")
    # TODO: 实现同步逻辑
    return 0

def sync_equity_warrants(conn, doc_id):
    """同步认股权台账表"""
    print("🔄 同步认股权台账表...")
    # TODO: 实现同步逻辑
    return 0

def log_sync(conn, table_name, record_count, status, error_msg=None):
    """记录同步日志"""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sync_log (table_name, sync_time, record_count, status, error_msg)
        VALUES (?, ?, ?, ?, ?)
    """, (table_name, datetime.now().isoformat(), record_count, status, error_msg))
    conn.commit()

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='企服助手-腾讯文档同步脚本')
    parser.add_argument('--all', action='store_true', help='同步所有表')
    parser.add_argument('--table', type=str, help='同步指定表（customers/fees/repair/inventory/cservice/equity）')
    parser.add_argument('--force', action='store_true', help='强制全量同步')
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config()
    doc_id = config.get('doc_id')
    
    if not doc_id:
        print("❌ 配置文件中未找到 doc_id")
        sys.exit(1)
    
    # 初始化数据库
    init_db()
    
    # 连接数据库
    conn = sqlite3.connect(str(DB_PATH))
    
    try:
        if args.all:
            # 同步所有表
            sync_customers(conn, doc_id)
            sync_fees(conn, doc_id)
            sync_repair_orders(conn, doc_id)
            sync_inventory(conn, doc_id)
            sync_cservice_records(conn, doc_id)
            sync_equity_warrants(conn, doc_id)
        elif args.table:
            # 同步指定表
            table_map = {
                'customers': sync_customers,
                'fees': sync_fees,
                'repair': sync_repair_orders,
                'inventory': sync_inventory,
                'cservice': sync_cservice_records,
                'equity': sync_equity_warrants
            }
            
            if args.table in table_map:
                table_map[args.table](conn, doc_id)
            else:
                print(f"❌ 未知表名：{args.table}")
                sys.exit(1)
        else:
            print("❌ 请指定 --all 或 --table")
            parser.print_help()
            sys.exit(1)
        
        print(f"\n✅ 同步完成！数据库：{DB_PATH}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()
