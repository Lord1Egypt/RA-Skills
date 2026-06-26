#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Import agents from JSON to database
"""

import sqlite3
import json
import os

def import_agents(db_path: str, json_path: str):
    """从JSON文件导入Agent到数据库"""
    if not os.path.exists(json_path):
        print(f"[ERROR] JSON file not found: {json_path}")
        return False

    # 读取JSON文件
    with open(json_path, 'r', encoding='utf-8') as f:
        agents = json.load(f)

    print(f"[INFO] Found {len(agents)} agents in JSON file")

    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 检查是否已有数据
    cursor.execute('SELECT COUNT(*) FROM agent_prompts')
    existing_count = cursor.fetchone()[0]

    if existing_count > 0:
        print(f"[INFO] Database already has {existing_count} agents")
        print(f"[INFO] Skipping import to avoid duplicates")
        conn.close()
        return True

    # 导入数据
    imported = 0
    for agent in agents:
        try:
            # 序列化metadata
            metadata = json.dumps(agent.get('metadata', {})) if agent.get('metadata') else None

            cursor.execute('''
                INSERT INTO agent_prompts (
                    name, category, description, emoji, color,
                    tools, vibe, filepath, full_content, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                agent.get('name'),
                agent.get('category'),
                agent.get('description'),
                agent.get('emoji'),
                agent.get('color'),
                agent.get('tools'),
                agent.get('vibe'),
                agent.get('filepath'),
                agent.get('full_content'),
                metadata
            ))
            imported += 1
        except Exception as e:
            print(f"[ERROR] Failed to import agent {agent.get('name')}: {e}")

    conn.commit()
    conn.close()

    print(f"[OK] Imported {imported} agents to database")
    return True

if __name__ == "__main__":
    db_path = 'memory/database/xiaozhi_memory.db'
    json_path = 'data/agents.json'

    # 导入
    success = import_agents(db_path, json_path)

    if success:
        print("\n[SUCCESS] Agent import completed!")
    else:
        print("\n[ERROR] Agent import failed!")
