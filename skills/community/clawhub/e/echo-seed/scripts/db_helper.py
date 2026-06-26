#!/usr/bin/env python3
"""
Echo Seed Database Helper - 数据库连接管理

提供带超时、重试、连接池的数据库连接
"""

import sqlite3
import time
from pathlib import Path
from contextlib import contextmanager
import threading

# 数据库路径
DB_PATH = Path.home() / '.openclaw' / 'workspace' / 'memory' / 'capsules.db'

# 连接池锁
_db_lock = threading.Lock()
_db_conn = None

def get_db_connection(timeout=30, max_retries=3):
    """
    获取数据库连接（带重试机制）
    
    Args:
        timeout: 超时时间（秒）
        max_retries: 最大重试次数
    
    Returns:
        sqlite3.Connection: 数据库连接
    """
    global _db_conn
    
    for attempt in range(max_retries):
        try:
            # 确保目录存在
            DB_PATH.parent.mkdir(parents=True, exist_ok=True)
            
            # 创建连接
            conn = sqlite3.connect(str(DB_PATH), timeout=timeout, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            
            # 启用 WAL 模式（支持并发读取）
            conn.execute('PRAGMA journal_mode=WAL')
            conn.execute('PRAGMA busy_timeout=30000')  # 30 秒超时
            
            return conn
            
        except sqlite3.OperationalError as e:
            if 'locked' in str(e).lower() and attempt < max_retries - 1:
                # 数据库锁定，等待后重试
                wait_time = (attempt + 1) * 0.5  # 0.5s, 1.0s, 1.5s
                time.sleep(wait_time)
                continue
            else:
                raise
    
    raise sqlite3.OperationalError(f"Database locked after {max_retries} retries")


@contextmanager
def get_db_cursor():
    """
    数据库游标上下文管理器
    
    Usage:
        with get_db_cursor() as (conn, cursor):
            cursor.execute("SELECT * FROM capsules")
            results = cursor.fetchall()
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        yield conn, cursor
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass


def execute_query(query, params=(), fetch=False, commit=False):
    """
    执行 SQL 查询（带自动重试）
    
    Args:
        query: SQL 查询
        params: 查询参数
        fetch: 是否返回结果
        commit: 是否提交事务
    
    Returns:
        list or int: 查询结果或影响的行数
    """
    for attempt in range(3):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            if commit:
                conn.commit()
            
            if fetch:
                result = cursor.fetchall()
            else:
                result = cursor.rowcount
            
            cursor.close()
            conn.close()
            
            return result
            
        except sqlite3.OperationalError as e:
            if 'locked' in str(e).lower() and attempt < 2:
                time.sleep((attempt + 1) * 0.5)
                continue
            else:
                raise
    
    return None


def init_db():
    """初始化数据库（创建表）"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 创建种子表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS capsules (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL DEFAULT 'note',
            title TEXT,
            content TEXT,
            url TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reminder_at TIMESTAMP,
            status TEXT DEFAULT 'active',
            completed_at TIMESTAMP,
            archived_at TIMESTAMP,
            notion_id TEXT,
            calendar_event_id TEXT,
            voice_data TEXT,
            metadata TEXT
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON capsules(type)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON capsules(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_created ON capsules(created_at)')
    
    # AI 分析表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            capsule_id TEXT NOT NULL,
            analysis_type TEXT NOT NULL,
            input_content TEXT,
            output_content TEXT,
            tokens_used INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (capsule_id) REFERENCES capsules(id)
        )
    ''')
    
    # 种子关联表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS capsule_relations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_capsule_id TEXT NOT NULL,
            target_capsule_id TEXT NOT NULL,
            relation_type TEXT NOT NULL,
            similarity_score REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_capsule_id) REFERENCES capsules(id),
            FOREIGN KEY (target_capsule_id) REFERENCES capsules(id),
            UNIQUE(source_capsule_id, target_capsule_id)
        )
    ''')
    
    # 种子标签表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS capsule_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            capsule_id TEXT NOT NULL,
            tag_name TEXT NOT NULL,
            tag_source TEXT DEFAULT 'auto',
            confidence_score REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (capsule_id) REFERENCES capsules(id),
            UNIQUE(capsule_id, tag_name)
        )
    ''')
    
    conn.commit()
    conn.close()


if __name__ == '__main__':
    print("🗄️ 初始化数据库...")
    init_db()
    print("✅ 数据库初始化完成")
    
    # 测试连接
    result = execute_query("SELECT COUNT(*) FROM capsules", fetch=True)
    print(f"📊 种子数量：{result[0][0] if result else 0}")
