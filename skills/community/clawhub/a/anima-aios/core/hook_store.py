"""
Hook Store - SQLite based storage for Hook metadata and execution records
"""
import sqlite3
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class HookTrigger(Enum):
    """Hook trigger timing"""
    PRE_EXECUTE = "pre_execute"
    POST_EXECUTE = "post_execute"
    ON_ERROR = "on_error"
    ON_SUCCESS = "on_success"
    ON_TIMEOUT = "on_timeout"


class Priority(Enum):
    """Hook priority"""
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3


@dataclass
class HookMetadata:
    """Hook metadata"""
    name: str
    description: str
    trigger: HookTrigger
    priority: Priority = Priority.MEDIUM
    enabled: bool = True
    timeout_ms: int = 5000
    retry_count: int = 0


@dataclass
class HookExecution:
    """Hook execution record"""
    hook_id: str
    task_id: str
    status: str  # "success", "failed", "skipped"
    duration_ms: float
    error: Optional[str] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class HookStore:
    """Hook data storage using SQLite"""
    
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # hooks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hooks (
                hook_id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                trigger TEXT NOT NULL,
                priority INTEGER DEFAULT 2,
                enabled INTEGER DEFAULT 1,
                timeout_ms INTEGER DEFAULT 5000,
                retry_count INTEGER DEFAULT 0,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        # hook_executions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hook_executions (
                execution_id INTEGER PRIMARY KEY AUTOINCREMENT,
                hook_id TEXT NOT NULL,
                task_id TEXT,
                status TEXT NOT NULL,
                duration_ms REAL,
                error TEXT,
                created_at TEXT,
                FOREIGN KEY (hook_id) REFERENCES hooks(hook_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_hook(self, name: str, metadata: HookMetadata) -> None:
        """Save hook metadata"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT OR REPLACE INTO hooks
            (hook_id, name, description, trigger, priority, enabled, timeout_ms, retry_count, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            metadata.name,
            metadata.description,
            metadata.trigger.value,
            metadata.priority.value,
            int(metadata.enabled),
            metadata.timeout_ms,
            metadata.retry_count,
            now,
            now
        ))
        
        conn.commit()
        conn.close()
    
    def get_hook(self, name: str) -> Optional[Dict]:
        """Get hook metadata by name"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT hook_id, name, description, trigger, priority, enabled, timeout_ms, retry_count, created_at, updated_at
            FROM hooks WHERE name = ?
        """, (name,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            "hook_id": row[0],
            "name": row[1],
            "description": row[2],
            "trigger": row[3],
            "priority": row[4],
            "enabled": bool(row[5]),
            "timeout_ms": row[6],
            "retry_count": row[7],
            "created_at": row[8],
            "updated_at": row[9]
        }
    
    def get_all_hooks(self) -> List[Dict]:
        """Get all hooks"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT hook_id, name, description, trigger, priority, enabled, timeout_ms, retry_count, created_at, updated_at
            FROM hooks ORDER BY priority ASC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "hook_id": row[0],
                "name": row[1],
                "description": row[2],
                "trigger": row[3],
                "priority": row[4],
                "enabled": bool(row[5]),
                "timeout_ms": row[6],
                "retry_count": row[7],
                "created_at": row[8],
                "updated_at": row[9]
            }
            for row in rows
        ]
    
    def save_execution(self, execution: HookExecution) -> None:
        """Save hook execution record"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO hook_executions
            (hook_id, task_id, status, duration_ms, error, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            execution.hook_id,
            execution.task_id,
            execution.status,
            execution.duration_ms,
            execution.error,
            execution.created_at.isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def get_hook_stats(self, hook_id: str) -> Dict:
        """Get hook execution statistics"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                AVG(duration_ms) as avg_duration
            FROM hook_executions
            WHERE hook_id = ?
        """, (hook_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return {
            "total": row[0] or 0,
            "success": row[1] or 0,
            "failed": row[2] or 0,
            "avg_duration_ms": row[3] or 0.0
        }
    
    def get_recent_executions(self, hook_id: str, limit: int = 10) -> List[Dict]:
        """Get recent hook executions"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT execution_id, hook_id, task_id, status, duration_ms, error, created_at
            FROM hook_executions
            WHERE hook_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (hook_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "execution_id": row[0],
                "hook_id": row[1],
                "task_id": row[2],
                "status": row[3],
                "duration_ms": row[4],
                "error": row[5],
                "created_at": row[6]
            }
            for row in rows
        ]
    
    def delete_hook(self, name: str) -> None:
        """Delete a hook"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM hooks WHERE name = ?", (name,))
        conn.commit()
        conn.close()
    
    def update_hook_status(self, name: str, enabled: bool) -> None:
        """Update hook enabled status"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        
        cursor.execute(
            "UPDATE hooks SET enabled = ?, updated_at = ? WHERE name = ?",
            (int(enabled), now, name)
        )
        
        conn.commit()
        conn.close()
    
    def hook_exists(self, name: str) -> bool:
        """Check if hook exists"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM hooks WHERE name = ?", (name,))
        count = cursor.fetchone()[0]
        
        conn.close()
        return count > 0
