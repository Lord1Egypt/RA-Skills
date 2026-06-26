"""
KVStore API — In-memory key-value store with TTL.

Endpoints:
  POST   /v1/set              — set a key-value pair (optional TTL)
  GET    /v1/get/{key}         — get a value by key
  DELETE /v1/delete/{key}      — delete a key
  GET    /v1/keys              — list all keys (optional prefix filter)
  POST   /v1/flush             — delete all keys
  GET    /v1/stats             — get store statistics
"""

from fastapi import FastAPI, HTTPException, Query

from .models import (
    DeleteResponse,
    FlushResponse,
    GetResponse,
    KeyListResponse,
    SetRequest,
    SetResponse,
    StatsResponse,
)
from .state import delete_key, flush_all, get_key, list_keys, set_key, stats

app = FastAPI(
    title="KVStore API",
    description="In-memory key-value store with TTL for AI agents.",
    version="0.1.0",
)


@app.post("/v1/set", response_model=SetResponse)
async def set_value(request: SetRequest) -> SetResponse:
    set_key(request.key, request.value, request.ttl_seconds)
    return SetResponse(key=request.key, stored=True)


@app.get("/v1/get/{key}", response_model=GetResponse)
async def get_value(key: str) -> GetResponse:
    entry = get_key(key)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Key not found: {key}")
    return GetResponse(key=entry.key, value=entry.value, ttl_remaining=entry.ttl_remaining)


@app.delete("/v1/delete/{key}", response_model=DeleteResponse)
async def delete_value(key: str) -> DeleteResponse:
    deleted = delete_key(key)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Key not found: {key}")
    return DeleteResponse(key=key, deleted=True)


@app.get("/v1/keys", response_model=KeyListResponse)
async def get_keys(prefix: str | None = Query(default=None)) -> KeyListResponse:
    keys = list_keys(prefix)
    return KeyListResponse(keys=keys, total=len(keys))


@app.post("/v1/flush", response_model=FlushResponse)
async def flush() -> FlushResponse:
    count = flush_all()
    return FlushResponse(deleted=count)


@app.get("/v1/stats", response_model=StatsResponse)
async def get_stats() -> StatsResponse:
    s = stats()
    return StatsResponse(**s)
