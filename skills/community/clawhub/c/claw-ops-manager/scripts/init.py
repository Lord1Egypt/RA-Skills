#!/usr/bin/env python3
"""
Initialize the audit database and configuration
"""
import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime

DEFAULT_DB_PATH = Path.home() / ".openclaw" / "audit.db"
DEFAULT_CONFIG_PATH = Path.home() / ".openclaw" / "audit-config.json"

def create_database(db_path=DEFAULT_DB_PATH):
    """Create the audit database with all required tables"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Operations log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            session_id TEXT,
            tool_name TEXT,
            action TEXT,
            parameters TEXT,
            result TEXT,
            success BOOLEAN,
            duration_ms INTEGER,
            user TEXT,
            ip_address TEXT
        )
    """)

    # File changes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS file_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            operation_id INTEGER,
            file_path TEXT,
            operation_type TEXT,
            old_hash TEXT,
            new_hash TEXT,
            content_preview TEXT,
            FOREIGN KEY (operation_id) REFERENCES operations(id)
        )
    """)

    # Snapshots table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            name TEXT,
            description TEXT,
            snapshot_data TEXT,
            created_by TEXT
        )
    """)

    # Permission rules table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS permission_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_name TEXT UNIQUE,
            tool_pattern TEXT,
            action_pattern TEXT,
            path_pattern TEXT,
            allowed BOOLEAN,
            priority INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Audit alerts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            operation_id INTEGER,
            alert_type TEXT,
            severity TEXT,
            message TEXT,
            resolved BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (operation_id) REFERENCES operations(id)
        )
    """)

    # Create indexes for better query performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_operations_timestamp ON operations(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_operations_tool ON operations(tool_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_file_changes_path ON file_changes(file_path)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_severity ON audit_alerts(severity)")

    conn.commit()
    conn.close()
    print(f"✅ Database created at: {db_path}")

def create_default_config(config_path=DEFAULT_CONFIG_PATH):
    """Create default configuration"""
    config = {
        "database_path": str(DEFAULT_DB_PATH),
        "log_level": "INFO",
        "retention_days": 90,
        "snapshots_enabled": True,
        "auto_snapshot_interval_hours": 24,
        "protected_paths": [
            "/etc/ssh",
            "/etc/sudoers",
            "/usr/bin",
            "/usr/sbin",
            "~/.ssh"
        ],
        "notification": {
            "enabled": False,
            "webhook_url": ""
        },
        "web_ui": {
            "enabled": True,
            "port": 8080,
            "host": "localhost"
        },
        "permissions": {
            "default_policy": "allow",
            "require_confirmation_for": [
                "exec",
                "write",
                "edit"
            ]
        }
    }

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"✅ Configuration created at: {config_path}")

def insert_default_rules(db_path=DEFAULT_DB_PATH):
    """Insert default permission rules"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    default_rules = [
        ("protect-etc", "exec", "*", "/etc/*", False, 100),
        ("protect-usr-bin", "exec", "*", "/usr/bin/*", False, 100),
        ("protect-ssh", "write|edit", "*", "~/.ssh/*", False, 100),
        ("allow-read-ops", "read", "*", "*", True, 50),
        ("log-all-ops", "*", "*", "*", True, 0),
    ]

    for rule in default_rules:
        try:
            cursor.execute("""
                INSERT INTO permission_rules (rule_name, tool_pattern, action_pattern, path_pattern, allowed, priority)
                VALUES (?, ?, ?, ?, ?, ?)
            """, rule)
        except sqlite3.IntegrityError:
            pass  # Rule already exists

    conn.commit()
    conn.close()
    print("✅ Default permission rules inserted")

if __name__ == "__main__":
    print("🔧 Initializing Claw Audit Center...")
    create_database()
    create_default_config()
    insert_default_rules()
    print("\n✅ Initialization complete!")
    print("\nNext steps:")
    print("1. Review configuration at:", DEFAULT_CONFIG_PATH)
    print("2. Start the web UI: python scripts/server.py")
    print("3. Start the monitor: python scripts/monitor.py")
