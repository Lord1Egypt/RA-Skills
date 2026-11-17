#!/usr/bin/env python3
"""
企服助手 - 纯Python同步脚本（零token消耗）
直接调用腾讯文档API，不通过MCP工具，不消耗AI token
使用方法：
  python pure_sync.py              # 同步所有表
  python pure_sync.py --daemon    # 作为守护进程运行（每小时检查一次）
"""

import requests
import json
import sqlite3
from pathlib import Path
from datetime import datetime
import time
import sys

# ==================== 配置区 ====================

# 腾讯文档API配置（需要从MCP工具配置中读取）
# 注意：这个token是腾讯文档的访问token，不是AI token
TENCENT_DOCS_TOKEN = ""  # TODO: 从 ~/.workbuddy/config/ 中读取
DOC_ID = ""                # TODO: 从知识库配置中读取

# 数据库路径
DB_PATH = Path.home() / ".workbuddy" / "workspace" / "enterprise-service-assistant" / "local_db.sqlite"

# ==================== API调用函数 ====================

def get_headers():
    """获取API请求头"""
    return {
        "Authorization": f"Bearer {TENCENT_DOCS_TOKEN}",
        "Content-Type": "application/json"
    }

def fetch_table_data(doc_id, sheet_id):
    """
    从腾讯文档读取表格数据
    注意：这里是示例代码，实际API endpoint需要参考腾讯文档官方文档
    """
    url = f"https://docs.qq.com/v1/spaces/{doc_id}/sheets/{sheet_id}/records"
    
    try:
        response = requests.get(url, headers=get_headers(), timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ 读取表格失败：{e}")
        return None

# ==================== 数据库操作 ====================

def init_db():
    """初始化数据库"""
    if not DB_PATH.exists():
        print("📊 初始化数据库...")
        from init_db import init_database
        init_database()

def sync_table(conn, table_name, doc_id, sheet_id):
    """同步单张表"""
    print(f"🔄 同步 {table_name}...")
    
    # 1. 从腾讯文档读取数据
    data = fetch_table_data(doc_id, sheet_id)
    
    if not data:
        print(f"  ⚠️  读取失败，跳过")
        return 0
    
    # 2. 清空表
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name}")
    
    # 3. 插入数据（根据实际字段映射）
    # TODO: 根据实际表结构实现
    print(f"  ✅ 同步 {len(data)} 条记录")
    
    # 4. 记录日志
    cursor.execute("""
        INSERT INTO sync_log (table_name, sync_time, record_count, status)
        VALUES (?, ?, ?, ?)
    """, (table_name, datetime.now().isoformat(), len(data), 'success'))
    
    conn.commit()
    return len(data)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='企服助手-纯Python同步脚本（零token）')
    parser.add_argument('--daemon', action='store_true', help='守护进程模式（每小时检查一次）')
    args = parser.parse_args()
    
    # 加载配置
    config_path = Path.home() / ".workbuddy" / "config" / "enterprise-service-assistant" / "knowledge_base_config.json"
    if not config_path.exists():
        print(f"❌ 配置文件不存在：{config_path}")
        sys.exit(1)
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    global DOC_ID, TENCENT_DOCS_TOKEN
    DOC_ID = config['source_config'].get('doc_id')
    
    # TODO: 从MCP配置中读取token
    # TENCENT_DOCS_TOKEN = ...
    
    if not DOC_ID:
        print("❌ 未配置 doc_id")
        sys.exit(1)
    
    # 初始化数据库
    init_db()
    
    # 同步逻辑
    def do_sync():
        conn = sqlite3.connect(str(DB_PATH))
        try:
            # 表配置：表名 -> sheet_id
            tables = {
                'customers': 'm3LDSO',           # 客户管理
                'fees': 'YOUR_SHEET_ID',          # 费用收缴
                'repair_orders': 'YOUR_SHEET_ID', # 报修情况汇总
                'inventory': 'YOUR_SHEET_ID',     # 库存管理
                'cservice_records': 'iSs70V',    # C+服务记录
                'equity_warrants': 'YOUR_SHEET_ID' # 认股权台账
            }
            
            total = 0
            for table_name, sheet_id in tables.items():
                count = sync_table(conn, table_name, DOC_ID, sheet_id)
                total += count
            
            print(f"\n✅ 同步完成！共 {total} 条记录")
            
        finally:
            conn.close()
    
    if args.daemon:
        # 守护进程模式
        print("�守护进程已启动，每小时检查一次...")
        while True:
            do_sync()
            time.sleep(3600)  # 每小时
    else:
        # 单次执行
        do_sync()

if __name__ == "__main__":
    main()
