#!/usr/bin/env python3
"""
设计师情报站 - 信息源数据库迁移脚本 v1.4.1

迁移内容:
1. 添加 fetch_method 字段 (web/rss/api)
2. 添加 category 字段 (中文媒体/英文媒体/设计媒体/社区平台)
3. 根据 URL 和类型自动设置正确的抓取方式
4. 修正设计类信息源的抓取方式为 web
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "intelligence_sources.db"

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. 添加新字段
    print("添加新字段...")
    
    # 检查字段是否已存在
    cursor.execute("PRAGMA table_info(sources)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'fetch_method' not in columns:
        cursor.execute("ALTER TABLE sources ADD COLUMN fetch_method TEXT DEFAULT 'web'")
        print("  ✓ 添加 fetch_method 字段")
    
    if 'category' not in columns:
        cursor.execute("ALTER TABLE sources ADD COLUMN category TEXT DEFAULT '媒体'")
        print("  ✓ 添加 category 字段")
    
    # 2. 根据现有 type 字段设置正确的 fetch_method 和 category
    print("\n更新抓取方式和分类...")
    
    # RSS 源 → fetch_method=rss
    cursor.execute("""
        UPDATE sources 
        SET fetch_method = 'rss', category = 'RSS 源'
        WHERE type = 'RSS 源'
    """)
    print(f"  ✓ RSS 源：{cursor.rowcount} 条 → fetch_method=rss")
    
    # 社区平台 → fetch_method=api (GitHub/Product Hunt 等有 API)
    cursor.execute("""
        UPDATE sources 
        SET fetch_method = 'api', category = '社区平台'
        WHERE type = '社区平台'
    """)
    print(f"  ✓ 社区平台：{cursor.rowcount} 条 → fetch_method=api")
    
    # 设计媒体 → fetch_method=web (重要修正！)
    cursor.execute("""
        UPDATE sources 
        SET fetch_method = 'web', category = '设计媒体'
        WHERE type = '设计媒体'
    """)
    print(f"  ✓ 设计媒体：{cursor.rowcount} 条 → fetch_method=web")
    
    # 中文媒体 → fetch_method=web
    cursor.execute("""
        UPDATE sources 
        SET fetch_method = 'web', category = '中文媒体'
        WHERE type = '中文媒体'
    """)
    print(f"  ✓ 中文媒体：{cursor.rowcount} 条 → fetch_method=web")
    
    # 英文媒体 → fetch_method=web
    cursor.execute("""
        UPDATE sources 
        SET fetch_method = 'web', category = '英文媒体'
        WHERE type = '英文媒体'
    """)
    print(f"  ✓ 英文媒体：{cursor.rowcount} 条 → fetch_method=web")
    
    # 3. 特殊修正：晚点 LatePost 域名已变更
    print("\n修正失效域名...")
    cursor.execute("""
        UPDATE sources 
        SET url = 'https://www晚点 latepost.cn/', 
            notes = notes || ' | 域名已更新 (原 postlate.cn)'
        WHERE id = 'CN007'
    """)
    if cursor.rowcount > 0:
        print(f"  ✓ 修正晚点 LatePost 域名")
    
    # 4. 禁用已知持续失败的源（可选）
    # cursor.execute("""
    #     UPDATE sources 
    #     SET status = 'disabled', 
    #         notes = notes || ' | 自动禁用：持续 403 错误'
    #     WHERE id IN ('CN003', 'CN007')
    # """)
    # print(f"  ✓ 禁用持续失败源：{cursor.rowcount} 条")
    
    conn.commit()
    
    # 5. 验证结果
    print("\n验证迁移结果:")
    cursor.execute("""
        SELECT fetch_method, category, COUNT(*) as count
        FROM sources
        GROUP BY fetch_method, category
        ORDER BY fetch_method, category
    """)
    rows = cursor.fetchall()
    print(f"\n{'抓取方式':<10} | {'分类':<12} | {'数量'}")
    print('-'*35)
    for r in rows:
        print(f"{r[0]:<10} | {r[1]:<12} | {r[2]}")
    
    conn.close()
    print("\n✅ 迁移完成！")


if __name__ == '__main__':
    migrate()
