"""agentMemo v3.0.0 Python Client Library."""
from __future__ import annotations
import json
from typing import Any, Optional
import urllib.request
import urllib.parse
import urllib.error


class AgentMemoClient:
    """Lightweight client for agentMemo API. No external dependencies."""

    def __init__(self, base_url: str = "http://localhost:8790", api_key: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _request(self, method: str, path: str, data: Optional[dict] = None, params: Optional[dict] = None) -> Any:
        url = f"{self.base_url}{path}"
        if params:
            url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, method=method)
        req.add_header("Content-Type", "application/json")
        if self.api_key:
            req.add_header("X-API-Key", self.api_key)
        try:
            with urllib.request.urlopen(req) as resp:
                if resp.status == 204:
                    return None
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"agentMemo API error {e.code}: {e.read().decode()}") from e

    def store(self, text: str, namespace: str = "default", importance: float = 0.5,
              ttl_seconds: Optional[int] = None, metadata: Optional[dict] = None,
              half_life_hours: float = 168.0, tags: Optional[list[str]] = None) -> dict:
        """Store a memory. Returns {id, embedding_dim}."""
        return self._request("POST", "/v1/memories", data={
            "text": text, "namespace": namespace, "importance": importance,
            "ttl_seconds": ttl_seconds, "metadata": metadata or {},
            "half_life_hours": half_life_hours, "tags": tags or [],
        })

    def search(self, query: str, namespace: Optional[str] = None, limit: int = 10,
               budget_tokens: Optional[int] = None, min_score: float = 0.3,
               mode: str = "semantic", tags: Optional[list[str]] = None) -> dict:
        """Search memories. mode: semantic|keyword|hybrid. Returns {results, total_tokens, budget_tokens, mode}."""
        params = {"q": query, "namespace": namespace, "limit": limit,
                  "budget_tokens": budget_tokens, "min_score": min_score, "mode": mode}
        if tags:
            params["tags"] = ",".join(tags)
        return self._request("GET", "/v1/memories/search", params=params)

    def get(self, memory_id: str) -> dict:
        """Get a single memory by ID."""
        return self._request("GET", f"/v1/memories/{memory_id}")

    def update(self, memory_id: str, text: Optional[str] = None, importance: Optional[float] = None,
               ttl_seconds: Optional[int] = None, metadata: Optional[dict] = None,
               half_life_hours: Optional[float] = None, tags: Optional[list[str]] = None) -> dict:
        """Update a memory (creates a version). Returns updated memory."""
        data = {}
        if text is not None: data["text"] = text
        if importance is not None: data["importance"] = importance
        if ttl_seconds is not None: data["ttl_seconds"] = ttl_seconds
        if metadata is not None: data["metadata"] = metadata
        if half_life_hours is not None: data["half_life_hours"] = half_life_hours
        if tags is not None: data["tags"] = tags
        return self._request("PUT", f"/v1/memories/{memory_id}", data=data)

    def versions(self, memory_id: str) -> list[dict]:
        """Get version history of a memory."""
        return self._request("GET", f"/v1/memories/{memory_id}/versions")

    def rollback(self, memory_id: str, version: Optional[int] = None) -> dict:
        """Rollback a memory to a previous version."""
        params = {"version": version} if version else None
        return self._request("POST", f"/v1/memories/{memory_id}/rollback", params=params)

    def delete(self, memory_id: str) -> None:
        """Delete a memory."""
        self._request("DELETE", f"/v1/memories/{memory_id}")

    def batch(self, create: Optional[list[dict]] = None, delete: Optional[list[str]] = None,
              search: Optional[list[dict]] = None) -> dict:
        """Batch create/delete/search. Returns {created, deleted, searches}."""
        data = {
            "create": create or [],
            "delete": [{"id": d} for d in (delete or [])],
            "search": search or [],
        }
        return self._request("POST", "/v1/memories/batch", data=data)

    def publish_event(self, type: str, payload: Optional[dict] = None, namespace: str = "default") -> dict:
        """Publish an event."""
        return self._request("POST", "/v1/events", data={
            "type": type, "payload": payload or {}, "namespace": namespace,
        })

    def namespaces(self) -> list[dict]:
        """List all namespaces."""
        return self._request("GET", "/v1/namespaces")

    def stats(self) -> dict:
        """Get server stats."""
        return self._request("GET", "/v1/stats")

    def health(self) -> dict:
        """Health check."""
        return self._request("GET", "/health")

    def metrics(self) -> dict:
        """Get server metrics."""
        return self._request("GET", "/metrics")

    def import_memories(self, memories: list[dict]) -> dict:
        """Import memories. Returns {imported, ids}."""
        return self._request("POST", "/v1/import", data={"memories": memories})

    def export_memories(self, namespace: Optional[str] = None) -> dict:
        """Export memories. Returns {memories, exported, namespace}."""
        return self._request("GET", "/v1/export", params={"namespace": namespace})

    def create_api_key(self, name: str, namespaces: Optional[list[str]] = None) -> dict:
        """Create an API key (admin only)."""
        return self._request("POST", "/v1/api-keys", data={
            "name": name, "namespaces": namespaces or ["*"],
        })

    def list_api_keys(self) -> list[dict]:
        """List API keys (admin only)."""
        return self._request("GET", "/v1/api-keys")

    def delete_api_key(self, key: str) -> None:
        """Delete an API key (admin only)."""
        self._request("DELETE", f"/v1/api-keys/{key}")



# Backward-compatible alias (deprecated)
AgentVaultClient = AgentMemoClient  # noqa: F401 — kept for backward compat
