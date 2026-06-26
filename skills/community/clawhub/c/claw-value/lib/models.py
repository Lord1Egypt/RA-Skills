#!/usr/bin/env python3
"""
ClawValue 数据模型
定义 SQLite 数据库表结构
"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path


class ClawValueDB:
    """ClawValue SQLite 数据库管理类"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            data_dir = os.environ.get('CLAWVALUE_DATA_DIR', 
                                       str(Path.home() / '.openclaw' / 'workspace' / 'data'))
            os.makedirs(data_dir, exist_ok=True)
            db_path = os.path.join(data_dir, 'clawvalue.db')
        
        self.db_path = db_path
        self.conn = None
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        
        # 采集记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collection_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                collected_at TEXT NOT NULL,
                total_sessions INTEGER DEFAULT 0,
                total_skills INTEGER DEFAULT 0,
                total_agents INTEGER DEFAULT 1,
                total_tokens INTEGER DEFAULT 0,
                usage_days INTEGER DEFAULT 0,
                skill_categories TEXT,
                error_count INTEGER DEFAULT 0
            )
        ''')
        
        # 技能表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                version TEXT,
                author TEXT,
                category TEXT,
                is_custom INTEGER DEFAULT 0,
                is_high_risk INTEGER DEFAULT 0,
                dependencies TEXT,
                first_seen TEXT,
                last_updated TEXT
            )
        ''')
        
        # 会话表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_key TEXT NOT NULL UNIQUE,
                channel TEXT,
                model TEXT,
                created_at TEXT,
                last_active TEXT,
                message_count INTEGER DEFAULT 0,
                token_count INTEGER DEFAULT 0
            )
        ''')
        
        # 评估结果表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                evaluated_at TEXT NOT NULL,
                usage_level TEXT,
                value_estimate TEXT,
                lobster_skill TEXT,
                skill_score INTEGER DEFAULT 0,
                automation_score INTEGER DEFAULT 0,
                integration_score INTEGER DEFAULT 0,
                total_score INTEGER DEFAULT 0,
                raw_data TEXT
            )
        ''')
        
        # 配置快照表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS config_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                captured_at TEXT NOT NULL,
                primary_model TEXT,
                heartbeat_interval INTEGER,
                sandbox_enabled INTEGER DEFAULT 0,
                tools_profile TEXT,
                channels TEXT,
                agent_count INTEGER DEFAULT 1
            )
        ''')
        
        self.conn.commit()
    
    def insert_collection_record(self, data: dict) -> int:
        """插入采集记录"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO collection_records 
            (collected_at, total_sessions, total_skills, total_agents, total_tokens, 
             usage_days, skill_categories, error_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('collected_at', datetime.now().isoformat()),
            data.get('total_sessions', 0),
            data.get('total_skills', 0),
            data.get('total_agents', 1),
            data.get('total_tokens', 0),
            data.get('usage_days', 0),
            data.get('skill_categories', ''),
            data.get('error_count', 0)
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def insert_skill(self, skill: dict) -> int:
        """插入或更新技能"""
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO skills (name, description, version, author, category, is_custom, 
                                is_high_risk, dependencies, first_seen, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                description = excluded.description,
                version = excluded.version,
                last_updated = excluded.last_updated
        ''', (
            skill.get('name', ''),
            skill.get('description', ''),
            skill.get('version', ''),
            skill.get('author', ''),
            skill.get('category', ''),
            1 if skill.get('is_custom') else 0,
            1 if skill.get('is_high_risk') else 0,
            skill.get('dependencies', ''),
            skill.get('first_seen', now),
            now
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def insert_session(self, session: dict) -> int:
        """插入或更新会话"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO sessions (session_key, channel, model, created_at, last_active,
                                   message_count, token_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(session_key) DO UPDATE SET
                last_active = excluded.last_active,
                message_count = excluded.message_count,
                token_count = excluded.token_count
        ''', (
            session.get('session_key', ''),
            session.get('channel', ''),
            session.get('model', ''),
            session.get('created_at', ''),
            session.get('last_active', ''),
            session.get('message_count', 0),
            session.get('token_count', 0)
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def insert_evaluation(self, evaluation: dict) -> int:
        """插入评估结果"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO evaluations 
            (evaluated_at, usage_level, value_estimate, lobster_skill, skill_score,
             automation_score, integration_score, total_score, raw_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            evaluation.get('evaluated_at', datetime.now().isoformat()),
            evaluation.get('usage_level', ''),
            evaluation.get('value_estimate', ''),
            evaluation.get('lobster_skill', ''),
            evaluation.get('skill_score', 0),
            evaluation.get('automation_score', 0),
            evaluation.get('integration_score', 0),
            evaluation.get('total_score', 0),
            evaluation.get('raw_data', '')
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_latest_stats(self) -> dict:
        """获取最新统计数据"""
        cursor = self.conn.cursor()
        
        # 最新采集记录
        cursor.execute('SELECT * FROM collection_records ORDER BY collected_at DESC LIMIT 1')
        latest = cursor.fetchone()
        
        # 技能总数
        cursor.execute('SELECT COUNT(*) FROM skills')
        skill_count = cursor.fetchone()[0]
        
        # 自定义技能数
        cursor.execute('SELECT COUNT(*) FROM skills WHERE is_custom = 1')
        custom_skill_count = cursor.fetchone()[0]
        
        # 会话总数
        cursor.execute('SELECT COUNT(*) FROM sessions')
        session_count = cursor.fetchone()[0]
        
        # 总 Token 消耗
        cursor.execute('SELECT SUM(token_count) FROM sessions')
        total_tokens = cursor.fetchone()[0] or 0
        
        # 使用天数（基于最早记录）
        cursor.execute('SELECT MIN(collected_at) FROM collection_records')
        first_record = cursor.fetchone()[0]
        usage_days = 0
        if first_record:
            first_date = datetime.fromisoformat(first_record)
            usage_days = (datetime.now() - first_date).days + 1
        
        return {
            'latest_collection': dict(latest) if latest else None,
            'skill_count': skill_count,
            'custom_skill_count': custom_skill_count,
            'session_count': session_count,
            'total_tokens': total_tokens,
            'usage_days': usage_days
        }
    
    def get_skill_list(self) -> list:
        """获取技能列表"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM skills ORDER BY last_updated DESC')
        return [dict(row) for row in cursor.fetchall()]
    
    def get_evaluation_history(self, limit: int = 10) -> list:
        """获取评估历史"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM evaluations ORDER BY evaluated_at DESC LIMIT ?', (limit,))
        return [dict(row) for row in cursor.fetchall()]
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()


if __name__ == '__main__':
    # 测试数据库初始化
    db = ClawValueDB()
    print(f"✅ 数据库已初始化: {db.db_path}")
    
    # 插入测试数据
    test_record = {
        'total_sessions': 100,
        'total_skills': 15,
        'total_tokens': 50000,
        'usage_days': 30
    }
    db.insert_collection_record(test_record)
    print("✅ 测试数据已插入")
    
    # 读取统计
    stats = db.get_latest_stats()
    print(f"📊 统计数据: {stats}")
    
    db.close()