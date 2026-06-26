#!/usr/bin/env python3
"""
Agent MCP Bridge — Inter-agent message broker via MCP protocol.

Exposes 4 MCP tools:
  - send_message(to, subject, body, reply_to?) → message_id
  - poll_messages(agent_id, limit?) → list of pending messages
  - mark_read(message_id) → bool
  - list_agents() → list of known agent ids

Uses SQLite for persistence. Zero external dependencies beyond fastmcp.

Run: python server.py
Or:  uvicorn server:app --port 8765
"""
import asyncio
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import aiosqlite
from fastmcp import FastMCP

DB_PATH = Path(__file__).parent / "messages.db"
mcp = FastMCP("agent-bridge", instructions="Inter-agent message broker for Isaac and Hermes")

async def get_db(db_path: Optional[Path] = None):
    """Get database connection. Optionally use a custom path for testing."""
    path = db_path or DB_PATH
    db = await aiosqlite.connect(path)
    db.row_factory = aiosqlite.Row
    await db.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            from_agent TEXT NOT NULL,
            to_agent TEXT NOT NULL,
            subject TEXT DEFAULT '',
            body TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            thread_id TEXT,
            reply_to TEXT,
            status TEXT DEFAULT 'pending'
        )
    """)
    await db.commit()
    return db

@mcp.tool()
async def send_message(
    from_agent: str,
    to: str,
    subject: str,
    body: str,
    reply_to: Optional[str] = None,
) -> dict:
    """
    Send a message from one agent to another.
    Returns the message_id of the sent message.
    """
    message_id = str(uuid.uuid4())[:8]
    ts = datetime.now(timezone.utc).isoformat()
    thread_id = reply_to or message_id
    
    db = await get_db()
    try:
        await db.execute(
            "INSERT INTO messages VALUES (?,?,?,?,?,?,?,?,?)",
            (message_id, from_agent, to, subject, body, ts, thread_id, reply_to, "pending")
        )
        await db.commit()
    finally:
        await db.close()
    
    return {"message_id": message_id, "timestamp": ts, "status": "sent"}

@mcp.tool()
async def poll_messages(agent_id: str, limit: int = 10) -> list:
    """
    Poll for pending messages addressed to agent_id.
    Returns list of message dicts (oldest first).
    """
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT * FROM messages WHERE to_agent=? AND status='pending' ORDER BY timestamp ASC LIMIT ?",
            (agent_id, limit)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        await db.close()

@mcp.tool()
async def mark_read(message_id: str) -> dict:
    """
    Mark a message as read/processed.
    Returns success status.
    """
    db = await get_db()
    try:
        await db.execute(
            "UPDATE messages SET status='read' WHERE id=?",
            (message_id,)
        )
        await db.commit()
        return {"message_id": message_id, "status": "read"}
    finally:
        await db.close()

@mcp.tool()
async def list_agents() -> list:
    """
    List all agent ids that have sent or received messages.
    """
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT DISTINCT from_agent as agent FROM messages "
            "UNION SELECT DISTINCT to_agent FROM messages ORDER BY agent"
        )
        rows = await cursor.fetchall()
        return [row[0] for row in rows]
    finally:
        await db.close()

# Create ASGI app for uvicorn
app = mcp.http_app(transport="streamable-http")

if __name__ == "__main__":
    # Run with streamable-http transport
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8765)
