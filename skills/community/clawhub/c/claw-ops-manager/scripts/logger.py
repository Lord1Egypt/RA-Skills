#!/usr/bin/env python3
"""
Operation logger - intercepts and logs all OpenClaw operations
"""
import sqlite3
import json
import os
import sys
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

class OperationLogger:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path.home() / ".openclaw" / "audit.db"
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """Connect to the database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()

    def log_operation(
        self,
        tool_name: str,
        action: str,
        parameters: Dict[str, Any],
        result: Any = None,
        success: bool = True,
        duration_ms: int = 0,
        session_id: str = None,
        user: str = None
    ) -> int:
        """Log an operation to the database"""
        self.connect()
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO operations (
                tool_name, action, parameters, result, success,
                duration_ms, session_id, user, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tool_name,
            action,
            json.dumps(parameters, default=str),
            json.dumps(result, default=str)[:1000],  # Limit result size
            success,
            duration_ms,
            session_id,
            user,
            datetime.now().isoformat()
        ))

        operation_id = cursor.lastrowid
        self.conn.commit()
        self.close()

        return operation_id

    def log_file_change(
        self,
        operation_id: int,
        file_path: str,
        operation_type: str,
        old_hash: str = None,
        new_hash: str = None,
        content_preview: str = None
    ):
        """Log a file change"""
        self.connect()
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO file_changes (
                operation_id, file_path, operation_type,
                old_hash, new_hash, content_preview
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            operation_id,
            file_path,
            operation_type,
            old_hash,
            new_hash,
            (content_preview or "")[:500]  # Limit preview size
        ))

        self.conn.commit()
        self.close()

    def calculate_file_hash(self, file_path: str) -> Optional[str]:
        """Calculate SHA256 hash of a file"""
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            return None

    def check_permission(
        self,
        tool_name: str,
        action: str,
        path: str = None
    ) -> tuple[bool, Optional[str]]:
        """Check if an operation is allowed based on permission rules"""
        self.connect()
        cursor = self.conn.cursor()

        # Get rules ordered by priority (descending)
        cursor.execute("""
            SELECT rule_name, tool_pattern, action_pattern, path_pattern, allowed
            FROM permission_rules
            ORDER BY priority DESC
        """)

        import fnmatch
        import re

        for rule in cursor.fetchall():
            tool_match = fnmatch.fnmatch(tool_name, rule["tool_pattern"])
            action_match = fnmatch.fnmatch(action, rule["action_pattern"])
            path_match = True

            if path and rule["path_pattern"]:
                path_match = fnmatch.fnmatch(path, rule["path_pattern"])

            if tool_match and action_match and path_match:
                self.close()
                return rule["allowed"], rule["rule_name"]

        # Default: allow if no rules matched
        self.close()
        return True, None

    def create_alert(
        self,
        operation_id: int,
        alert_type: str,
        severity: str,
        message: str
    ):
        """Create an audit alert"""
        self.connect()
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO audit_alerts (
                operation_id, alert_type, severity, message
            ) VALUES (?, ?, ?, ?)
        """, (operation_id, alert_type, severity, message))

        self.conn.commit()
        self.close()

    def get_recent_operations(self, limit=100, tool_name=None):
        """Get recent operations"""
        self.connect()
        cursor = self.conn.cursor()

        if tool_name:
            cursor.execute("""
                SELECT * FROM operations
                WHERE tool_name = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (tool_name, limit))
        else:
            cursor.execute("""
                SELECT * FROM operations
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))

        results = cursor.fetchall()
        self.close()
        return [dict(row) for row in results]

    def get_statistics(self):
        """Get operation statistics"""
        self.connect()
        cursor = self.conn.cursor()

        stats = {}

        # Total operations
        cursor.execute("SELECT COUNT(*) as count FROM operations")
        stats["total_operations"] = cursor.fetchone()["count"]

        # Operations by tool
        cursor.execute("""
            SELECT tool_name, COUNT(*) as count
            FROM operations
            GROUP BY tool_name
            ORDER BY count DESC
        """)
        stats["by_tool"] = [dict(row) for row in cursor.fetchall()]

        # Success rate
        cursor.execute("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful
            FROM operations
        """)
        row = cursor.fetchone()
        stats["success_rate"] = row["successful"] / row["total"] if row["total"] > 0 else 0

        # Recent alerts
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM audit_alerts
            WHERE resolved = 0
        """)
        stats["unresolved_alerts"] = cursor.fetchone()["count"]

        self.close()
        return stats

if __name__ == "__main__":
    # Test the logger
    logger = OperationLogger()

    # Test logging
    op_id = logger.log_operation(
        tool_name="exec",
        action="run_command",
        parameters={"command": "ls -la"},
        result={"stdout": "file1.txt\nfile2.txt", "stderr": ""},
        success=True,
        duration_ms=150,
        session_id="test-session",
        user="test-user"
    )

    print(f"✅ Logged operation with ID: {op_id}")

    # Test file change logging
    logger.log_file_change(
        operation_id=op_id,
        file_path="/tmp/test.txt",
        operation_type="write",
        new_hash=logger.calculate_file_hash("/tmp/test.txt")
    )

    print("✅ Logged file change")

    # Test statistics
    stats = logger.get_statistics()
    print(f"\n📊 Statistics:")
    print(f"  Total operations: {stats['total_operations']}")
    print(f"  Success rate: {stats['success_rate']:.2%}")
    print(f"  Unresolved alerts: {stats['unresolved_alerts']}")
