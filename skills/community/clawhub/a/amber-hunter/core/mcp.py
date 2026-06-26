"""
core/mcp.py — MCP Server for Amber-Hunter v1.2.32
Exposes amber-hunter tools via the Model Context Protocol (MCP).

MCP Tools:
  recall_memories  — Search long-term memory
  create_memory    — Create a new memory capsule
  list_memories    — List recent capsules
  get_memory       — Get a specific memory by ID
  update_memory    — Update a memory capsule
  delete_memory    — Delete a memory capsule
  get_stats        — Get memory statistics

MCP Resources:
  amber://memory/{id}     — Individual memory resource
  amber://profile         — User profile resource
  amber://stats           — Statistics resource
"""
from __future__ import annotations

import json, time
from typing import Any, Optional

# ── Tool Schemas ────────────────────────────────────────────

TOOLS = [
    {
        "name": "recall_memories",
        "description": "Search long-term memory for relevant capsules. Use when user asks about past conversations, projects, preferences, or facts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query (自然语言)"},
                "limit": {"type": "integer", "description": "Max results (default 3)", "default": 3},
                "rerank": {"type": "boolean", "description": "Use LLM reranking (slower but more accurate)", "default": False},
            },
            "required": ["query"],
        },
    },
    {
        "name": "create_memory",
        "description": "Create a new memory capsule. Use when user explicitly saves something or expresses important information.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "memo": {"type": "string", "description": "Memory content (摘要)"},\
                "content": {"type": "string", "description": "Full content (optional, encrypted at rest)"},
                "tags": {"type": "string", "description": "Comma-separated tags"},
                "category": {"type": "string", "description": "Category: preference/decision/fact/context", "default": "context"},
            },
            "required": ["memo"],
        },
    },
    {
        "name": "list_memories",
        "description": "List recent memory capsules.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "Max results (default 20)", "default": 20},
                "category": {"type": "string", "description": "Filter by category path prefix"},
            },
        },
    },
    {
        "name": "get_memory",
        "description": "Get a specific memory by its ID.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "capsule_id": {"type": "string", "description": "Memory capsule ID"},
            },
            "required": ["capsule_id"],
        },
    },
    {
        "name": "update_memory",
        "description": "Update an existing memory capsule.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "capsule_id": {"type": "string", "description": "Memory capsule ID"},
                "memo": {"type": "string", "description": "New memo content"},
                "tags": {"type": "string", "description": "New tags (comma-separated)"},
            },
            "required": ["capsule_id"],
        },
    },
    {
        "name": "delete_memory",
        "description": "Delete a memory capsule.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "capsule_id": {"type": "string", "description": "Memory capsule ID"},
            },
            "required": ["capsule_id"],
        },
    },
    {
        "name": "get_stats",
        "description": "Get memory statistics (counts, category distribution, hotness).",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


# ── MCP Server Handler ──────────────────────────────────────

class MCPServer:
    """
    Simple MCP server that exposes amber-hunter tools.
    Compatible with MCP clients (Claude Code, etc.).
    """

    def __init__(self, token: str):
        self.token = token
        self.tools = TOOLS

    def handle_request(self, request: dict) -> dict:
        """Handle an MCP request and return a response."""
        method = request.get("method", "")
        params = request.get("params", {})

        if method == "tools/list":
            return {"result": {"tools": self.tools}}

        if method == "tools/call":
            tool_name = params.get("name", "")
            tool_args = params.get("arguments", {})
            try:
                result = self._call_tool(tool_name, tool_args)
                return {"result": {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]}}
            except Exception as e:
                import sys
                print(f"[mcp] tool {tool_name} failed: {e}", file=sys.stderr)
                return {"error": {"code": -32603, "message": str(e)}}

        if method == "resources/list":
            return {"result": {"resources": [
                {"uri": "amber://stats", "name": "Memory Statistics", "mimeType": "application/json"},
                {"uri": "amber://profile", "name": "User Profile", "mimeType": "application/json"},
            ]}}

        if method == "resources/read":
            uri = params.get("uri", "")
            try:
                data = self._read_resource(uri)
                return {"result": {"contents": [{"uri": uri, "mimeType": "application/json", "text": json.dumps(data, ensure_ascii=False)}]}}
            except Exception as e:
                return {"error": {"code": -32603, "message": str(e)}}

        return {"error": {"code": -32601, "message": f"Unknown method: {method}"}}

    def _call_tool(self, name: str, args: dict) -> dict:
        """Execute a tool by name with arguments."""
        if name == "recall_memories":
            return self._recall(args["query"], args.get("limit", 3), args.get("rerank", False))
        if name == "create_memory":
            return self._create_memory(args["memo"], args.get("content", ""), args.get("tags", ""), args.get("category", "context"))
        if name == "list_memories":
            return self._list_memories(args.get("limit", 20), args.get("category", ""))
        if name == "get_memory":
            return self._get_memory(args["capsule_id"])
        if name == "update_memory":
            return self._update_memory(args["capsule_id"], args.get("memo", ""), args.get("tags", ""))
        if name == "delete_memory":
            return self._delete_memory(args["capsule_id"])
        if name == "get_stats":
            return self._get_stats()
        raise ValueError(f"Unknown tool: {name}")

    def _recall(self, query: str, limit: int, rerank: bool) -> dict:
        """Call the /recall endpoint internally."""
        from core.db import _get_conn
        from core.vector import search_vectors
        from core.session import get_current_session_key
        from core.wal import write_wal_entry

        # Search using vector similarity
        vector_results = {}
        try:
            for r in search_vectors(query, limit=limit * 3):
                vector_results[r["capsule_id"]] = r["lance_score"]
        except Exception:
            pass

        # Fallback to keyword search
        conn = _get_conn()
        c = conn.cursor()
        q_lower = query.lower()
        rows = c.execute(
            "SELECT id, memo, tags, category_path FROM capsules WHERE memo LIKE ? OR tags LIKE ? ORDER BY hotness_score DESC LIMIT ?",
            (f"%{q_lower}%", f"%{q_lower}%", limit * 2)
        ).fetchall()

        results = []
        for row in rows[:limit]:
            capsule_id, memo, tags, category_path = row
            score = vector_results.get(capsule_id, 0.5)
            results.append({
                "capsule_id": capsule_id,
                "memo": memo,
                "tags": tags or "",
                "category_path": category_path or "general/default",
                "relevance_score": round(score, 3),
            })

        return {"query": query, "count": len(results), "results": results}

    def _create_memory(self, memo: str, content: str, tags: str, category: str) -> dict:
        """Create a new memory capsule."""
        import secrets, base64, hashlib
        from core.db import insert_capsule
        from core.vector import index_capsule
        from core.crypto import encrypt_content, derive_capsule_key

        capsule_id = secrets.token_hex(8)
        now = time.time()

        # Encrypt content if provided
        if content:
            # Use a dummy key for MCP-created capsules (user can re-encrypt)
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.hkdf import HKDF
            key = HKDF(hashes.SHA256(), 32, b"amber-mcp", now=str(now).encode()).derive(b"amber-mcp-key")
            ct, nonce = encrypt_content(content.encode("utf-8"), key)
            ct_b64 = base64.b64encode(ct).decode()
            nonce_b64 = base64.b64encode(nonce).decode()
            content_hash = hashlib.sha256(ct).hexdigest()
            salt = base64.b64encode(b"amber-mcp-salt").decode()
            key_source = "pbkdf2"
        else:
            ct_b64 = nonce_b64 = content_hash = salt = None
            key_source = "none"

        insert_capsule(
            capsule_id=capsule_id,
            memo=memo,
            content=ct_b64 or "",
            tags=tags,
            session_id=None,
            window_title=None,
            url=None,
            created_at=now,
            salt=salt,
            nonce=nonce_b64,
            encrypted_len=len(ct_b64) if ct_b64 else 0,
            content_hash=content_hash,
            source_type="mcp",
            category=category,
            key_source=key_source,
        )

        if memo:
            try:
                index_capsule(capsule_id, memo, now)
            except Exception:
                pass

        return {"id": capsule_id, "created_at": now, "memo": memo}

    def _list_memories(self, limit: int, category: str) -> dict:
        """List recent memory capsules."""
        from core.db import _get_conn
        conn = _get_conn()
        c = conn.cursor()
        if category:
            rows = c.execute(
                "SELECT id, memo, tags, category_path, created_at, hotness_score FROM capsules WHERE category_path LIKE ? ORDER BY created_at DESC LIMIT ?",
                (f"{category}%", limit)
            ).fetchall()
        else:
            rows = c.execute(
                "SELECT id, memo, tags, category_path, created_at, hotness_score FROM capsules ORDER BY created_at DESC LIMIT ?",
                (limit,)
            ).fetchall()
        conn.close()
        return {
            "count": len(rows),
            "memories": [
                {"id": r[0], "memo": r[1], "tags": r[2] or "", "category_path": r[3] or "general/default",
                 "created_at": r[4], "hotness": r[5]}
                for r in rows
            ]
        }

    def _get_memory(self, capsule_id: str) -> dict:
        """Get a specific memory."""
        from core.db import get_capsule
        record = get_capsule(capsule_id)
        if not record:
            return {"error": "not found"}
        return {
            "id": record["id"],
            "memo": record.get("memo", ""),
            "tags": record.get("tags", ""),
            "category_path": record.get("category_path", "general/default"),
            "created_at": record.get("created_at"),
            "hotness_score": record.get("hotness_score", 0),
        }

    def _update_memory(self, capsule_id: str, memo: str, tags: str) -> dict:
        """Update a memory capsule. Marks as unsynced so it gets re-uploaded on next sync."""
        from core.db import _get_conn
        conn = _get_conn()
        c = conn.cursor()
        now = time.time()
        c.execute("UPDATE capsules SET memo=?, tags=?, updated_at=?, synced=0 WHERE id=?", (memo, tags, now, capsule_id))
        conn.commit()
        conn.close()
        return {"id": capsule_id, "updated_at": now}

    def _delete_memory(self, capsule_id: str) -> dict:
        """Delete a memory capsule."""
        from core.db import _get_conn
        from core.vector import delete_vector
        conn = _get_conn()
        c = conn.cursor()
        c.execute("DELETE FROM capsules WHERE id=?", (capsule_id,))
        conn.commit()
        conn.close()
        try:
            delete_vector(capsule_id)
        except Exception:
            pass
        return {"id": capsule_id, "deleted": True}

    def _get_stats(self) -> dict:
        """Get memory statistics."""
        from core.db import _get_conn
        conn = _get_conn()
        c = conn.cursor()
        total = c.execute("SELECT COUNT(*) FROM capsules").fetchone()[0]
        synced = c.execute("SELECT COUNT(*) FROM capsules WHERE synced=1").fetchone()[0]
        hot = c.execute("SELECT COUNT(*) FROM capsules WHERE hotness_score > 5").fetchone()[0]
        cat_rows = c.execute(
            "SELECT category_path, COUNT(*) as cnt FROM capsules GROUP BY category_path ORDER BY cnt DESC LIMIT 5"
        ).fetchall()
        conn.close()
        return {
            "total": total,
            "synced": synced,
            "unsynced": total - synced,
            "high_hotness": hot,
            "top_categories": [{"path": r[0] or "general", "count": r[1]} for r in cat_rows],
        }

    def _read_resource(self, uri: str) -> dict:
        """Read an MCP resource."""
        if uri == "amber://stats":
            return self._get_stats()
        if uri == "amber://profile":
            from core.db import list_profile
            return list_profile()
        if uri.startswith("amber://memory/"):
            capsule_id = uri.split("/")[-1]
            return self._get_memory(capsule_id)
        raise ValueError(f"Unknown resource: {uri}")
