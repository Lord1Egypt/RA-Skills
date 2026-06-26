#!/usr/bin/env python3
"""
AI Mother Database - SQLite storage for AI agent state and history
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path.home() / ".openclaw/skills/ai-mother/ai-mother.db"

def init_db():
    """Initialize database schema"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Agents table (current state)
    c.execute('''
        CREATE TABLE IF NOT EXISTS agents (
            pid INTEGER PRIMARY KEY,
            ai_type TEXT NOT NULL,
            workdir TEXT NOT NULL,
            task TEXT,
            status TEXT NOT NULL,
            notes TEXT,
            first_seen INTEGER NOT NULL,
            last_seen INTEGER NOT NULL,
            runtime_seconds INTEGER
        )
    ''')
    
    # History table (all checks)
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid INTEGER NOT NULL,
            ai_type TEXT NOT NULL,
            workdir TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT,
            checked_at INTEGER NOT NULL,
            cpu_percent REAL,
            memory_mb INTEGER
        )
    ''')
    
    # Create indexes
    c.execute('CREATE INDEX IF NOT EXISTS idx_history_pid ON history(pid)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_history_checked_at ON history(checked_at)')
    
    conn.commit()
    conn.close()

def update_agent(pid, ai_type, workdir, task, status, notes, cpu_percent=None, memory_mb=None):
    """Update or insert agent state"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = int(datetime.now().timestamp())
    
    # Check if exists
    c.execute('SELECT first_seen FROM agents WHERE pid = ?', (pid,))
    row = c.fetchone()
    
    if row:
        # Update existing
        first_seen = row[0]
        runtime = now - first_seen
        c.execute('''
            UPDATE agents 
            SET ai_type=?, workdir=?, task=?, status=?, notes=?, last_seen=?, runtime_seconds=?
            WHERE pid=?
        ''', (ai_type, workdir, task, status, notes, now, runtime, pid))
    else:
        # Insert new
        c.execute('''
            INSERT INTO agents (pid, ai_type, workdir, task, status, notes, first_seen, last_seen, runtime_seconds)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
        ''', (pid, ai_type, workdir, task, status, notes, now, now))
    
    # Add to history
    c.execute('''
        INSERT INTO history (pid, ai_type, workdir, status, notes, checked_at, cpu_percent, memory_mb)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (pid, ai_type, workdir, status, notes, now, cpu_percent, memory_mb))
    
    conn.commit()
    conn.close()

def get_all_agents():
    """Get all current agents"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM agents ORDER BY last_seen DESC')
    rows = c.fetchall()
    conn.close()
    
    agents = []
    for row in rows:
        agents.append({
            'pid': row[0],
            'ai_type': row[1],
            'workdir': row[2],
            'task': row[3],
            'status': row[4],
            'notes': row[5],
            'first_seen': row[6],
            'last_seen': row[7],
            'runtime_seconds': row[8]
        })
    return agents

def get_agent_history(pid, limit=50):
    """Get history for specific agent"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT checked_at, status, notes, cpu_percent, memory_mb
        FROM history WHERE pid = ?
        ORDER BY checked_at DESC LIMIT ?
    ''', (pid, limit))
    rows = c.fetchall()
    conn.close()
    return rows

def cleanup_dead_agents():
    """Remove agents not seen in 24h"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    cutoff = int(datetime.now().timestamp()) - 86400
    c.execute('DELETE FROM agents WHERE last_seen < ?', (cutoff,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Initialize on first run
    init_db()
    print(f"✅ Database initialized: {DB_PATH}")
