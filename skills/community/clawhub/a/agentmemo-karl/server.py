"""agentMemo v3.0.0 — Semantic Memory Mesh for AI Agents (formerly AgentVault)."""
from __future__ import annotations
import asyncio
import logging
import os
import time
from collections import defaultdict
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, Request, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2 import Environment, FileSystemLoader
from sse_starlette.sse import EventSourceResponse

import database as db
import embeddings
from events import event_bus
from models import (
    ApiKeyCreate, ApiKeyResponse, BatchRequest, BatchResponse,
    EventCreate, EventResponse, ExportResponse, HealthResponse,
    ImportRequest, ImportResponse, MemoryCreate, MemoryCreateResponse,
    MemoryResponse, MemorySearchResponse, MemorySearchResult,
    MemoryUpdate, MemoryVersionResponse, MetricsResponse,
    NamespaceInfo, StatsResponse,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("agentmemo")

VERSION = "3.0.0"
SERVICE_NAME = "agentMemo"


def _env(key: str, default=None):
    """Read env var — AGENTMEMO_* preferred, AGENTVAULT_* fallback for backward compat."""
    new_key = key.replace("AGENTVAULT_", "AGENTMEMO_")  # backward compat: migrate old key names
    val = os.environ.get(new_key)
    if val is not None:
        return val
    val = os.environ.get(key)
    if val is not None:
        logger.warning("⚠️  Deprecated env var '%s' — please migrate to '%s'", key, new_key)
        return val
    return default


ADMIN_KEY = _env("AGENTMEMO_ADMIN_KEY")
if not ADMIN_KEY:
    logger.error("❌ AGENTMEMO_ADMIN_KEY (or AGENTVAULT_ADMIN_KEY) is required. "  # fallback: AGENTVAULT_ADMIN_KEY still works
                 "Set it to enable RBAC auth. Refusing to start without auth.")
    raise SystemExit(1)
AUTH_ENABLED = True
START_TIME = time.time()
REQUEST_COUNT = 0
RATE_LIMITS: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT_RPM = int(_env("AGENTMEMO_RATE_LIMIT", "120"))


async def _prune_loop():
    while True:
        await asyncio.sleep(60)
        try:
            pruned = await db.prune_expired()
            if pruned:
                logger.info("TTL auto-expire: pruned %d memories", pruned)
        except Exception as e:
            logger.error("Prune error: %s", e)


async def _prewarm_hnsw():
    """Load all embeddings into HNSW index on startup, chunked to avoid blocking the event loop."""
    count = 0
    cursor = None
    chunk_size = 500
    while True:
        memories, next_cursor = await db.get_all_memories(limit=chunk_size, cursor=cursor)
        for mem in memories:
            if mem.get("embedding"):
                embeddings.hnsw_index.add(mem["id"], mem["embedding"])
                count += 1
        if not next_cursor:
            break
        cursor = next_cursor
        await asyncio.sleep(0)  # yield to event loop between chunks
    logger.info("HNSW index prewarmed with %d vectors", count)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()
    embeddings.get_model()
    await _prewarm_hnsw()
    logger.info("🧠 %s v%s ready on port %s (auth=%s)", SERVICE_NAME, VERSION, _env("AGENTMEMO_PORT", "8790"), AUTH_ENABLED)
    prune_task = asyncio.create_task(_prune_loop())
    yield
    prune_task.cancel()
    try:
        await prune_task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="agentMemo",
    description="Semantic Memory Mesh for AI Agents",
    version=VERSION,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Environment(loader=FileSystemLoader(Path(__file__).parent / "templates"), autoescape=True)


# --- RBAC Middleware ---

async def check_auth(request: Request) -> Optional[dict]:
    if not AUTH_ENABLED:
        return None
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")
    if api_key == ADMIN_KEY:
        return {"key": ADMIN_KEY, "name": "admin", "namespaces": ["*"]}
    key_data = await db.get_api_key(api_key)
    if not key_data:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return key_data


def _check_namespace_access(key_data: Optional[dict], namespace: str):
    if key_data is None:
        return
    if "*" in key_data["namespaces"]:
        return
    if namespace not in key_data["namespaces"]:
        raise HTTPException(status_code=403, detail=f"No access to namespace '{namespace}'")


_RATE_LIMIT_LAST_EVICT = 0.0
_RATE_LIMIT_EVICT_INTERVAL = 300  # evict stale keys every 5 minutes


@app.middleware("http")
async def timing_and_rate_limit(request: Request, call_next):
    global REQUEST_COUNT, _RATE_LIMIT_LAST_EVICT
    REQUEST_COUNT += 1
    start = time.perf_counter()

    if AUTH_ENABLED and request.url.path.startswith("/v1/"):
        api_key = request.headers.get("X-API-Key", "anonymous")
        now = time.time()
        RATE_LIMITS[api_key] = [t for t in RATE_LIMITS[api_key] if now - t < 60]
        if len(RATE_LIMITS[api_key]) >= RATE_LIMIT_RPM:
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
        RATE_LIMITS[api_key].append(now)

        # Periodically evict idle keys to prevent unbounded dict growth
        if now - _RATE_LIMIT_LAST_EVICT > _RATE_LIMIT_EVICT_INTERVAL:
            _RATE_LIMIT_LAST_EVICT = now
            stale = [k for k, ts in RATE_LIMITS.items() if not ts or now - ts[-1] > 120]
            for k in stale:
                del RATE_LIMITS[k]

    response = await call_next(request)
    elapsed = (time.perf_counter() - start) * 1000
    response.headers["X-Response-Time"] = f"{elapsed:.1f}ms"
    return response


# --- Health & Metrics ---

@app.get("/health", response_model=HealthResponse)
async def health_check():
    db_ok = True
    try:
        async with db.pooled() as conn:
            await conn.execute("SELECT 1")
    except Exception:
        db_ok = False
    return HealthResponse(
        status="healthy" if db_ok else "degraded",
        version=VERSION,
        uptime_seconds=round(time.time() - START_TIME, 2),
        db_ok=db_ok,
        embedding_model_loaded=embeddings._model is not None,
    )


@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    stats = await db.get_stats()
    return MetricsResponse(
        uptime_seconds=round(time.time() - START_TIME, 2),
        total_requests=REQUEST_COUNT,
        requests_per_minute=round(REQUEST_COUNT / max((time.time() - START_TIME) / 60, 0.01), 2),
        total_memories=stats["total_memories"],
        total_events=stats["total_events"],
        total_namespaces=stats["total_namespaces"],
        storage_size_bytes=stats["storage_size_bytes"],
        embedding_cache_size=embeddings.embedding_cache.size,
        embedding_cache_hits=embeddings.embedding_cache.hits,
        embedding_cache_misses=embeddings.embedding_cache.misses,
        hnsw_index_size=embeddings.hnsw_index.size,
        active_websockets=event_bus.active_websocket_count,
    )


# --- Memory Endpoints ---

@app.post("/v1/memories", response_model=MemoryCreateResponse, status_code=201)
async def create_memory(body: MemoryCreate, request: Request):
    key_data = await check_auth(request)
    _check_namespace_access(key_data, body.namespace)
    embedding = embeddings.embed_text(body.text)
    result = await db.create_memory(
        text=body.text, namespace=body.namespace, importance=body.importance,
        half_life_hours=body.half_life_hours, ttl_seconds=body.ttl_seconds,
        metadata=body.metadata, embedding=embedding, tags=body.tags,
    )
    embeddings.hnsw_index.add(result["id"], embedding)
    await event_bus.publish({"type": "memory.created", "namespace": body.namespace,
                             "payload": {"id": result["id"], "text": body.text[:100]}})
    return MemoryCreateResponse(id=result["id"], embedding_dim=384)


@app.get("/v1/memories/search", response_model=MemorySearchResponse)
async def search_memories(
    request: Request,
    q: str = Query(..., min_length=1),
    namespace: Optional[str] = None,
    limit: int = Query(default=10, ge=1, le=100),
    budget_tokens: Optional[int] = Query(default=None, ge=1),
    min_score: float = Query(default=0.3, ge=0.0, le=1.0),
    mode: str = Query(default="semantic", pattern="^(semantic|keyword|hybrid)$"),
    tags: Optional[str] = Query(default=None, description="Comma-separated tags filter"),
    cursor: Optional[str] = Query(default=None),
):
    key_data = await check_auth(request)
    if namespace:
        _check_namespace_access(key_data, namespace)
    tag_list = [t.strip() for t in tags.split(",")] if tags else None
    memories, next_cursor = await db.get_all_memories(namespace=namespace, tags=tag_list)
    results, total_tokens = embeddings.search_memories(q, memories, limit=limit, min_score=min_score,
                                                        budget_tokens=budget_tokens, mode=mode)
    return MemorySearchResponse(results=results, total_tokens=total_tokens, budget_tokens=budget_tokens,
                                 mode=mode, cursor=next_cursor)


@app.get("/v1/memories/count")
async def count_memories(request: Request, namespace: Optional[str] = None):
    key_data = await check_auth(request)
    if namespace:
        _check_namespace_access(key_data, namespace)
    count = await db.count_memories(namespace=namespace)
    return {"count": count, "namespace": namespace}


@app.get("/v1/memories/{memory_id}", response_model=MemoryResponse)
async def get_memory(memory_id: str, request: Request):
    key_data = await check_auth(request)
    mem = await db.get_memory(memory_id)
    if not mem:
        raise HTTPException(status_code=404, detail="Memory not found")
    _check_namespace_access(key_data, mem["namespace"])
    return MemoryResponse(
        id=mem["id"], text=mem["text"], namespace=mem["namespace"],
        importance=mem["importance"], effective_importance=round(mem["effective_importance"], 4),
        ttl_seconds=mem["ttl_seconds"], metadata=mem["metadata"], tags=mem.get("tags", []),
        embedding_dim=384, created_at=mem["created_at"], age_hours=round(mem["age_hours"], 2),
        version=mem.get("version", 1),
    )


@app.put("/v1/memories/{memory_id}", response_model=MemoryResponse)
async def update_memory(memory_id: str, body: MemoryUpdate, request: Request):
    key_data = await check_auth(request)
    existing = await db.get_memory(memory_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Memory not found")
    _check_namespace_access(key_data, existing["namespace"])

    new_embedding = None
    if body.text is not None and body.text != existing["text"]:
        new_embedding = embeddings.embed_text(body.text)

    updated = await db.update_memory(
        memory_id, text=body.text, importance=body.importance,
        ttl_seconds=body.ttl_seconds, metadata=body.metadata,
        half_life_hours=body.half_life_hours, tags=body.tags,
        new_embedding=new_embedding,
    )
    if not updated:
        raise HTTPException(status_code=500, detail="Update failed")

    if new_embedding:
        embeddings.hnsw_index.remove(memory_id)
        embeddings.hnsw_index.add(memory_id, new_embedding)

    await event_bus.publish({"type": "memory.updated", "namespace": existing["namespace"],
                             "payload": {"id": memory_id, "version": updated.get("version", 1)}})
    return MemoryResponse(
        id=updated["id"], text=updated["text"], namespace=updated["namespace"],
        importance=updated["importance"], effective_importance=round(updated["effective_importance"], 4),
        ttl_seconds=updated["ttl_seconds"], metadata=updated["metadata"], tags=updated.get("tags", []),
        embedding_dim=384, created_at=updated["created_at"], age_hours=round(updated["age_hours"], 2),
        version=updated.get("version", 1),
    )


@app.get("/v1/memories/{memory_id}/versions", response_model=list[MemoryVersionResponse])
async def get_memory_versions(memory_id: str, request: Request):
    key_data = await check_auth(request)
    existing = await db.get_memory(memory_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Memory not found")
    _check_namespace_access(key_data, existing["namespace"])
    versions = await db.get_memory_versions(memory_id)
    return [MemoryVersionResponse(**v) for v in versions]


@app.post("/v1/memories/{memory_id}/rollback", response_model=MemoryResponse)
async def rollback_memory(memory_id: str, request: Request, version: Optional[int] = Query(default=None)):
    key_data = await check_auth(request)
    existing = await db.get_memory(memory_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Memory not found")
    _check_namespace_access(key_data, existing["namespace"])
    result = await db.rollback_memory(memory_id, target_version=version)
    if not result:
        raise HTTPException(status_code=404, detail="No version to rollback to")

    if result.get("embedding"):
        embeddings.hnsw_index.remove(memory_id)
        embeddings.hnsw_index.add(memory_id, result["embedding"])

    await event_bus.publish({"type": "memory.rollback", "namespace": existing["namespace"],
                             "payload": {"id": memory_id, "version": result.get("version", 1)}})
    return MemoryResponse(
        id=result["id"], text=result["text"], namespace=result["namespace"],
        importance=result["importance"], effective_importance=round(result["effective_importance"], 4),
        ttl_seconds=result["ttl_seconds"], metadata=result["metadata"], tags=result.get("tags", []),
        embedding_dim=384, created_at=result["created_at"], age_hours=round(result["age_hours"], 2),
        version=result.get("version", 1),
    )


@app.delete("/v1/memories/{memory_id}", status_code=204)
async def delete_memory(memory_id: str, request: Request):
    key_data = await check_auth(request)
    existing = await db.get_memory(memory_id)
    if existing:
        _check_namespace_access(key_data, existing["namespace"])
    if not await db.delete_memory(memory_id):
        raise HTTPException(status_code=404, detail="Memory not found")
    embeddings.hnsw_index.remove(memory_id)


# --- Batch API ---

@app.post("/v1/memories/batch", response_model=BatchResponse)
async def batch_operations(body: BatchRequest, request: Request):
    key_data = await check_auth(request)
    response = BatchResponse()

    # Batch create — use single-transaction batch
    if body.create:
        texts = [item.text for item in body.create]
        embs = embeddings.embed_batch(texts)
        items = []
        for item, emb in zip(body.create, embs):
            _check_namespace_access(key_data, item.namespace)
            items.append({
                "text": item.text, "namespace": item.namespace, "importance": item.importance,
                "half_life_hours": item.half_life_hours, "ttl_seconds": item.ttl_seconds,
                "metadata": item.metadata, "embedding": emb, "tags": item.tags,
            })
        results = await db.batch_create_memories(items)
        for result, emb in zip(results, embs):
            embeddings.hnsw_index.add(result["id"], emb)
            response.created.append(MemoryCreateResponse(id=result["id"], embedding_dim=384))

    # Batch delete
    for item in body.delete:
        if await db.delete_memory(item.id):
            embeddings.hnsw_index.remove(item.id)
            response.deleted.append(item.id)

    # Batch search — group by namespace to avoid redundant DB fetches
    if body.search:
        ns_memory_cache: dict[str | None, list] = {}
        for item in body.search:
            if item.namespace:
                _check_namespace_access(key_data, item.namespace)
            ns_key = item.namespace
            if ns_key not in ns_memory_cache:
                ns_memories, _ = await db.get_all_memories(namespace=ns_key)
                ns_memory_cache[ns_key] = ns_memories
            results, total_tokens = embeddings.search_memories(
                item.q, ns_memory_cache[ns_key], limit=item.limit, min_score=item.min_score, mode=item.mode)
            response.searches.append(MemorySearchResponse(results=results, total_tokens=total_tokens, mode=item.mode))

    return response


# --- Event Endpoints ---

@app.post("/v1/events", response_model=EventResponse, status_code=201)
async def create_event(body: EventCreate, request: Request):
    key_data = await check_auth(request)
    _check_namespace_access(key_data, body.namespace)
    result = await db.create_event(type_=body.type, payload=body.payload, namespace=body.namespace)
    await event_bus.publish(result)
    return EventResponse(**result)


@app.get("/v1/events/stream")
async def stream_events(request: Request, namespace: Optional[str] = None):
    await check_auth(request)
    return EventSourceResponse(event_bus.subscribe(namespace=namespace))


# --- WebSocket ---

@app.websocket("/v1/ws")
async def websocket_endpoint(websocket: WebSocket, namespace: Optional[str] = None):
    if AUTH_ENABLED:
        api_key = websocket.query_params.get("api_key")
        if not api_key:
            await websocket.close(code=4001, reason="Missing api_key")
            return
        if api_key != ADMIN_KEY:
            key_data = await db.get_api_key(api_key)
            if not key_data:
                await websocket.close(code=4001, reason="Invalid API key")
                return
    await event_bus.ws_subscribe(websocket, namespace=namespace)


# --- Import/Export ---

@app.post("/v1/import", response_model=ImportResponse)
async def import_memories(body: ImportRequest, request: Request):
    key_data = await check_auth(request)
    texts = [m.text for m in body.memories]
    embs = embeddings.embed_batch(texts)
    items = []
    for mem, emb in zip(body.memories, embs):
        _check_namespace_access(key_data, mem.namespace)
        items.append({
            "text": mem.text, "namespace": mem.namespace, "importance": mem.importance,
            "half_life_hours": mem.half_life_hours, "ttl_seconds": mem.ttl_seconds,
            "metadata": mem.metadata, "embedding": emb, "tags": mem.tags,
        })
    results = await db.batch_create_memories(items)
    ids = [r["id"] for r in results]
    for result, emb in zip(results, embs):
        embeddings.hnsw_index.add(result["id"], emb)
    return ImportResponse(imported=len(ids), ids=ids)


@app.get("/v1/export", response_model=ExportResponse)
async def export_memories(request: Request, namespace: Optional[str] = None):
    key_data = await check_auth(request)
    if namespace:
        _check_namespace_access(key_data, namespace)
    memories = await db.export_memories(namespace=namespace)
    return ExportResponse(memories=memories, exported=len(memories), namespace=namespace)


# --- Info Endpoints ---

@app.get("/v1/namespaces", response_model=list[NamespaceInfo])
async def list_namespaces(request: Request):
    await check_auth(request)
    return [NamespaceInfo(**ns) for ns in await db.get_namespaces()]


@app.get("/v1/stats", response_model=StatsResponse)
async def get_stats(request: Request):
    await check_auth(request)
    return StatsResponse(**await db.get_stats())


# --- API Key Management (admin only) ---

@app.post("/v1/api-keys", response_model=ApiKeyResponse, status_code=201)
async def create_api_key(body: ApiKeyCreate, request: Request):
    if not AUTH_ENABLED:
        raise HTTPException(status_code=404, detail="Auth not enabled")
    api_key = request.headers.get("X-API-Key")
    if api_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Admin key required")
    result = await db.create_api_key(body.name, body.namespaces)
    return ApiKeyResponse(**result)


@app.get("/v1/api-keys", response_model=list[ApiKeyResponse])
async def list_api_keys(request: Request):
    if not AUTH_ENABLED:
        raise HTTPException(status_code=404, detail="Auth not enabled")
    api_key = request.headers.get("X-API-Key")
    if api_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Admin key required")
    keys = await db.list_api_keys()
    return [ApiKeyResponse(**k) for k in keys]


@app.delete("/v1/api-keys/{key}", status_code=204)
async def delete_api_key(key: str, request: Request):
    if not AUTH_ENABLED:
        raise HTTPException(status_code=404, detail="Auth not enabled")
    api_key = request.headers.get("X-API-Key")
    if api_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Admin key required")
    if not await db.delete_api_key(key):
        raise HTTPException(status_code=404, detail="API key not found")


# --- Dashboard ---

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    tmpl = templates.get_template("dashboard.html")
    return tmpl.render(version=VERSION)


if __name__ == "__main__":
    import uvicorn
    port = int(_env("AGENTMEMO_PORT", "8790"))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
