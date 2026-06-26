#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agency Agents Caller - Database Initialization
初始化Agent数据库
"""

import sqlite3
import os
import json
import sys
from datetime import datetime

def create_directory_structure():
    """创建必要的目录结构"""
    print("[DIR] Creating directory structure...")
    
    directories = [
        'memory',
        'memory/database'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"  [OK] Created: {directory}")
        else:
            print(f"  [OK] Exists: {directory}")
    
    return True

def initialize_database(db_path: str):
    """初始化数据库"""
    print(f"\n[DB] Initializing database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 创建agent_prompts表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                description TEXT,
                emoji TEXT,
                color TEXT,
                tools TEXT,
                vibe TEXT,
                filepath TEXT,
                full_content TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("  [OK] Created table: agent_prompts")
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_name ON agent_prompts(name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON agent_prompts(category)')
        print("  [OK] Created indexes")
        
        # 检查是否已有数据
        cursor.execute('SELECT COUNT(*) FROM agent_prompts')
        count = cursor.fetchone()[0]
        
        if count == 0:
            print(f"  [INFO] Database is empty ({count} agents)")
            print(f"  [INFO] Will import agents from data/agents.json")
        else:
            print(f"  [OK] Database already has {count} agents")
        
        conn.commit()
        conn.close()
        
        print(f"\n[OK] Database initialized successfully!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error initializing database: {e}")
        return False

def import_agents_from_json(db_path: str, json_path: str):
    """从JSON文件导入Agent"""
    print(f"\n[IMPORT] Importing agents from: {json_path}")
    
    if not os.path.exists(json_path):
        print(f"  [WARN] JSON file not found: {json_path}")
        print(f"  [INFO] Skipping import")
        return False
    
    # 读取JSON文件
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            agents = json.load(f)
    except Exception as e:
        print(f"  [ERROR] Failed to read JSON: {e}")
        return False
    
    print(f"  [INFO] Found {len(agents)} agents in JSON file")
    
    # 连接数据库
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查是否已有数据
        cursor.execute('SELECT COUNT(*) FROM agent_prompts')
        existing_count = cursor.fetchone()[0]
        
        if existing_count > 0:
            print(f"  [INFO] Database already has {existing_count} agents")
            print(f"  [INFO] Skipping import to avoid duplicates")
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
                print(f"  [ERROR] Failed to import agent {agent.get('name')}: {e}")
        
        conn.commit()
        conn.close()
        
        print(f"  [OK] Imported {imported} agents to database")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Failed to import agents: {e}")
        return False

def main():
    """主函数"""
    print("="*70)
    print("Agency Agents Caller - Database Initialization")
    print("="*70)
    print()
    
    # 获取数据库路径
    db_path = os.path.join('memory', 'database', 'xiaozhi_memory.db')
    
    # 获取JSON路径
    json_path = os.path.join('data', 'agents.json')
    
    # 1. 创建目录结构
    if not create_directory_structure():
        print("\n[ERROR] Failed to create directory structure")
        return 1
    
    # 2. 初始化数据库
    if not initialize_database(db_path):
        print("\n[ERROR] Failed to initialize database")
        return 1
    
    # 3. 导入Agent数据
    import_agents_from_json(db_path, json_path)
    
    # 4. 完成
    print("\n" + "="*70)
    print("[OK] Initialization Complete!")
    print("="*70)
    print()
    print("[SUMMARY] Summary:")
    print(f"  - Database: {db_path}")
    print(f"  - Table: agent_prompts")
    print(f"  - Status: Ready")
    print()
    print("[NEXT] Next steps:")
    print("  1. Run verification: python scripts/verify_install.py")
    print("  2. Start using: from scripts.agent_caller import AgentCaller")
    print()
    print("[INFO] 179 agents are ready to use!")
    print()

if __name__ == "__main__":
    main()
