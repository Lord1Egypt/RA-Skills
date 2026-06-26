#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Caller Core Script
用于按需调用179个专业Agent
"""

import sqlite3
import json
from typing import List, Dict, Optional

class AgentCaller:
    """Agent调用器 - 从数据库按需调用179个Agent"""
    
    def __init__(self, db_path: str = None):
        """
        初始化Agent调用器
        
        Args:
            db_path: 数据库路径（默认使用内置路径）
        """
        if db_path is None:
            # 默认数据库路径
            db_path = "memory/database/xiaozhi_memory.db"
        
        self.db_path = db_path
        self.conn = None
    
    def _get_connection(self):
        """获取数据库连接"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def list_all_agents(self, limit: int = 20) -> List[Dict]:
        """
        列出所有Agent（分页）
        
        Args:
            limit: 返回数量限制
            
        Returns:
            Agent列表
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, category, description, emoji, color, tools, vibe
            FROM agent_prompts
            ORDER BY id
            LIMIT ?
        ''', (limit,))
        
        agents = []
        for row in cursor.fetchall():
            agents.append({
                'id': row['id'],
                'name': row['name'],
                'category': row['category'],
                'description': row['description'],
                'emoji': row['emoji'],
                'color': row['color'],
                'tools': row['tools'],
                'vibe': row['vibe']
            })
        
        return agents
    
    def search_agents(self, keyword: str) -> List[Dict]:
        """
        搜索Agent
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的Agent列表
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, category, description, emoji, tools
            FROM agent_prompts
            WHERE name LIKE ? OR description LIKE ? OR category LIKE ?
            ORDER BY name
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        
        agents = []
        for row in cursor.fetchall():
            agents.append({
                'id': row['id'],
                'name': row['name'],
                'category': row['category'],
                'description': row['description'],
                'emoji': row['emoji'],
                'tools': row['tools']
            })
        
        return agents
    
    def get_agent_by_name(self, name: str) -> Optional[Dict]:
        """
        根据名称获取Agent
        
        Args:
            name: Agent名称
            
        Returns:
            Agent信息（包含完整prompt）
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM agent_prompts
            WHERE name LIKE ?
            LIMIT 1
        ''', (f'%{name}%',))
        
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    
    def get_agents_by_category(self, category: str) -> List[Dict]:
        """
        根据分类获取Agent
        
        Args:
            category: 分类名称
            
        Returns:
            该分类下的Agent列表
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, category, description, emoji
            FROM agent_prompts
            WHERE category = ?
            ORDER BY name
        ''', (category,))
        
        agents = []
        for row in cursor.fetchall():
            agents.append({
                'id': row['id'],
                'name': row['name'],
                'category': row['category'],
                'description': row['description'],
                'emoji': row['emoji']
            })
        
        return agents
    
    def get_random_agent(self) -> Optional[Dict]:
        """
        随机获取一个Agent
        
        Returns:
            随机Agent信息
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM agent_prompts
            ORDER BY RANDOM()
            LIMIT 1
        ''')
        
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    
    def count_agents(self) -> int:
        """
        统计Agent总数
        
        Returns:
            Agent总数
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM agent_prompts")
        return cursor.fetchone()[0]
    
    def get_categories(self) -> List[str]:
        """
        获取所有Agent分类
        
        Returns:
            分类列表
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT category
            FROM agent_prompts
            WHERE category IS NOT NULL
            ORDER BY category
        ''')
        
        return [row[0] for row in cursor.fetchall()]
    
    def get_agent_full_prompt(self, agent_id: int) -> Optional[str]:
        """
        获取Agent的完整prompt
        
        Args:
            agent_id: Agent ID
            
        Returns:
            完整prompt内容
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT full_content FROM agent_prompts
            WHERE id = ?
        ''', (agent_id,))
        
        row = cursor.fetchone()
        if row:
            return row[0]
        return None
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            self.conn = None

# CLI接口
if __name__ == "__main__":
    import sys
    
    caller = AgentCaller()
    
    print("="*70)
    print("Agent Caller System - 179 Agents Available")
    print("="*70)
    
    # 统计信息
    total = caller.count_agents()
    print(f"\nTotal Agents: {total}")
    
    # 获取分类
    categories = caller.get_categories()
    print(f"\nCategories ({len(categories)}): {', '.join(categories[:10])}")
    
    # 根据参数执行不同操作
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
        
        if keyword == '--random':
            agent = caller.get_random_agent()
            if agent:
                print(f"\nRandom Agent:")
                print(f"  Name: {agent['name']}")
                print(f"  Category: {agent['category']}")
                print(f"  Description: {agent['description']}")
        
        elif keyword == '--categories':
            print("\nAgents by Category:")
            for category in categories:
                agents = caller.get_agents_by_category(category)
                print(f"  {category}: {len(agents)} agents")
        
        else:
            print(f"\nSearching for: {keyword}")
            agents = caller.search_agents(keyword)
            print(f"Found: {len(agents)} agents")
            
            for agent in agents[:10]:
                print(f"\n- {agent['name']} ({agent['category']})")
                print(f"  {agent['description']}")
    
    else:
        print("\nFirst 20 Agents:")
        agents = caller.list_all_agents(20)
        
        for i, agent in enumerate(agents, 1):
            print(f"\n{i}. {agent['name']} ({agent['category']})")
            desc = agent['description'][:80] + '...' if len(agent['description']) > 80 else agent['description']
            print(f"   {desc}")
    
    caller.close()
