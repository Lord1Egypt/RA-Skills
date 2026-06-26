#!/usr/bin/env python3
"""
DeepTask Database Manager
管理 SQLite 数据库表结构和数据操作
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Any

# 数据库默认路径
DEFAULT_DB_PATH = os.path.expanduser("~/.openclaw/deeptask.db")


class DeepTaskDB:
    """DeepTask 数据库管理类"""
    
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        self.conn = None
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """确保数据库文件存在并初始化表结构"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """建立数据库连接"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
    
    def _create_tables(self):
        """创建所有数据表"""
        cursor = self.conn.cursor()
        
        # 1. 项目表 (projects)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                summary TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 2. 会话表 (sessions)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                summary TEXT,
                content TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT CHECK(status IN ('pending', 'in_progress', 'completed', 'review_pending')) DEFAULT 'pending',
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        """)
        
        # 3. 子任务表 (subtasks)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subtasks (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                summary TEXT,
                content TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT CHECK(status IN ('pending', 'in_progress', 'completed', 'review_pending')) DEFAULT 'pending',
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        """)
        
        # 4. MUF 表 (mufs)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mufs (
                id TEXT PRIMARY KEY,
                subtask_id TEXT NOT NULL,
                summary TEXT,
                content TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT CHECK(status IN ('pending', 'in_progress', 'completed', 'failed')) DEFAULT 'pending',
                FOREIGN KEY (subtask_id) REFERENCES subtasks(id)
            )
        """)
        
        # 5. 单元测试表 (unit_tests)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS unit_tests (
                id TEXT PRIMARY KEY,
                muf_id TEXT NOT NULL,
                test_code TEXT,
                status TEXT CHECK(status IN ('pending', 'passed', 'failed')) DEFAULT 'pending',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (muf_id) REFERENCES mufs(id)
            )
        """)
        
        # 6. 集成测试表 (integration_tests)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS integration_tests (
                id TEXT PRIMARY KEY,
                subtask_id TEXT NOT NULL,
                test_code TEXT,
                status TEXT CHECK(status IN ('pending', 'passed', 'failed')) DEFAULT 'pending',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (subtask_id) REFERENCES subtasks(id)
            )
        """)
        
        # 7. 人工审查记录表 (review_records)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS review_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_type TEXT NOT NULL,
                entity_id TEXT NOT NULL,
                reviewer TEXT,
                review_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT CHECK(status IN ('approved', 'rejected')),
                comments TEXT
            )
        """)
        
        # 创建索引以优化查询
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_project ON sessions(project_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_subtasks_session ON subtasks(session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_mufs_subtask ON mufs(subtask_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_unit_tests_muf ON unit_tests(muf_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_integration_tests_subtask ON integration_tests(subtask_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_review_records_entity ON review_records(entity_type, entity_id)")
        
        self.conn.commit()
    
    def _generate_id(self, prefix: str, table: str) -> str:
        """生成唯一 ID（格式：PREFIX-数字）"""
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        return f"{prefix}-{count + 1}"
    
    def create_project(self, name: str, description: str = "", summary: str = "") -> str:
        """创建新项目"""
        project_id = self._generate_id("DT", "projects")
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO projects (id, name, description, summary)
            VALUES (?, ?, ?, ?)
        """, (project_id, name, description, summary))
        self.conn.commit()
        return project_id
    
    def create_session(self, project_id: str, summary: str, content: str) -> str:
        """创建会话"""
        session_id = self._generate_id("SE", "sessions")
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO sessions (id, project_id, summary, content)
            VALUES (?, ?, ?, ?)
        """, (session_id, project_id, summary, content))
        self.conn.commit()
        return session_id
    
    def create_subtask(self, session_id: str, summary: str, content: str) -> str:
        """创建子任务"""
        subtask_id = self._generate_id("ST", "subtasks")
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO subtasks (id, session_id, summary, content)
            VALUES (?, ?, ?, ?)
        """, (subtask_id, session_id, summary, content))
        self.conn.commit()
        return subtask_id
    
    def create_muf(self, subtask_id: str, summary: str, content: str) -> str:
        """创建 MUF（最小功能单元）"""
        muf_id = self._generate_id("MUF", "mufs")
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO mufs (id, subtask_id, summary, content)
            VALUES (?, ?, ?, ?)
        """, (muf_id, subtask_id, summary, content))
        self.conn.commit()
        return muf_id
    
    def create_unit_test(self, muf_id: str, test_code: str) -> str:
        """创建单元测试"""
        ut_id = self._generate_id("UT", "unit_tests")
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO unit_tests (id, muf_id, test_code)
            VALUES (?, ?, ?)
        """, (ut_id, muf_id, test_code))
        self.conn.commit()
        return ut_id
    
    def create_integration_test(self, subtask_id: str, test_code: str) -> str:
        """创建集成测试"""
        it_id = self._generate_id("IT", "integration_tests")
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO integration_tests (id, subtask_id, test_code)
            VALUES (?, ?, ?)
        """, (it_id, subtask_id, test_code))
        self.conn.commit()
        return it_id
    
    def update_status(self, table: str, entity_id: str, status: str) -> bool:
        """更新实体状态"""
        cursor = self.conn.cursor()
        cursor.execute(f"""
            UPDATE {table}
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status, entity_id))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def add_review_record(self, entity_type: str, entity_id: str, reviewer: str, 
                          status: str, comments: str = "") -> int:
        """添加审查记录"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO review_records (entity_type, entity_id, reviewer, status, comments)
            VALUES (?, ?, ?, ?, ?)
        """, (entity_type, entity_id, reviewer, status, comments))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_project(self, project_id: str) -> Optional[Dict]:
        """获取项目信息"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_sessions_by_project(self, project_id: str) -> List[Dict]:
        """获取项目的所有会话"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE project_id = ? ORDER BY created_at", (project_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_subtasks_by_session(self, session_id: str) -> List[Dict]:
        """获取会话的所有子任务"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM subtasks WHERE session_id = ? ORDER BY created_at", (session_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_mufs_by_subtask(self, subtask_id: str) -> List[Dict]:
        """获取子任务的所有 MUF"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM mufs WHERE subtask_id = ? ORDER BY created_at", (subtask_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_unit_tests_by_muf(self, muf_id: str) -> List[Dict]:
        """获取 MUF 的所有单元测试"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM unit_tests WHERE muf_id = ? ORDER BY created_at", (muf_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_pending_sessions(self) -> List[Dict]:
        """获取所有待处理的会话"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE status = 'pending' ORDER BY created_at")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_pending_subtasks(self) -> List[Dict]:
        """获取所有待处理的子任务"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM subtasks WHERE status = 'pending' ORDER BY created_at")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_pending_mufs(self) -> List[Dict]:
        """获取所有待处理的 MUF"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM mufs WHERE status = 'pending' ORDER BY created_at")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_review_pending_sessions(self) -> List[Dict]:
        """获取待审核的会话"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE status = 'review_pending' ORDER BY created_at")
        return [dict(row) for row in cursor.fetchall()]
    
    def check_session_complete(self, session_id: str) -> bool:
        """检查会话是否所有子任务都已完成"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM subtasks 
            WHERE session_id = ? AND status != 'completed'
        """, (session_id,))
        return cursor.fetchone()[0] == 0
    
    def check_subtask_complete(self, subtask_id: str) -> bool:
        """检查子任务是否所有 MUF 都已完成"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM mufs 
            WHERE subtask_id = ? AND status != 'completed'
        """, (subtask_id,))
        return cursor.fetchone()[0] == 0
    
    def get_failed_mufs(self) -> List[Dict]:
        """获取所有失败的 MUF"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM mufs WHERE status = 'failed' ORDER BY updated_at DESC")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_all_projects(self) -> List[Dict]:
        """获取所有项目"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()


# 命令行工具函数
def init_db(db_path: str = DEFAULT_DB_PATH):
    """初始化数据库"""
    db = DeepTaskDB(db_path)
    print(f"数据库已初始化：{db_path}")
    db.close()


def show_status(db_path: str = DEFAULT_DB_PATH):
    """显示系统状态"""
    db = DeepTaskDB(db_path)
    
    print("\n=== DeepTask 系统状态 ===\n")
    
    # 项目统计
    projects = db.get_all_projects()
    print(f"项目总数：{len(projects)}")
    
    # 会话统计
    cursor = db.conn.cursor()
    cursor.execute("SELECT status, COUNT(*) FROM sessions GROUP BY status")
    print("\n会话状态:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")
    
    # 子任务统计
    cursor.execute("SELECT status, COUNT(*) FROM subtasks GROUP BY status")
    print("\n子任务状态:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")
    
    # MUF 统计
    cursor.execute("SELECT status, COUNT(*) FROM mufs GROUP BY status")
    print("\nMUF 状态:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")
    
    # 待审核项目
    review_pending = db.get_review_pending_sessions()
    if review_pending:
        print(f"\n⚠️  待审核会话：{len(review_pending)}")
        for s in review_pending[:5]:
            print(f"  - {s['id']}: {s['summary']}")
    
    # 失败项目
    failed = db.get_failed_mufs()
    if failed:
        print(f"\n🔴 失败的 MUF: {len(failed)}")
        for m in failed[:5]:
            print(f"  - {m['id']}: {m['summary']}")
    
    db.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "init":
            init_db()
        elif cmd == "status":
            show_status()
        else:
            print(f"未知命令：{cmd}")
            print("用法：python db_manager.py [init|status]")
    else:
        init_db()
