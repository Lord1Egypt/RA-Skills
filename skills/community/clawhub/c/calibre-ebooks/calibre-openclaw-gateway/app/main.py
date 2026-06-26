from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import uuid
import hmac
from contextlib import asynccontextmanager

from app.config import settings
from app.database.postgres_db import postgres_db
from app.utils.logger import setup_logger, get_logger
from app.api.routes import books, search, embeddings, stats, websocket, downloads
from app.services.book_service import book_service

# Setup logger
setup_logger()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("Starting Calibre OpenClaw Server...")
    settings.validate_security()
    postgres_db.initialize_pool()
    logger.info("PostgreSQL connection pool initialized")
    
    # Background sync task
    async def background_sync():
        """Run book sync in background thread with periodic checks."""
        from pathlib import Path
        import asyncio
        from app.database.calibre_db import CalibreMetadataDBUnavailable, diagnose_calibre_db
        from app.services.embedding_service import embedding_service
        try:
            if settings.RAG_RECONCILE_ON_START:
                try:
                    result = await asyncio.to_thread(
                        embedding_service.reconcile_embedding_version
                    )
                    logger.info(f"Embedding version reconciliation: {result}")
                except Exception as e:
                    logger.error(f"Embedding version reconciliation failed: {e}")

            calibre_db_path = Path(settings.CALIBRE_DB_PATH)
            diagnostic = diagnose_calibre_db()
            
            # Initial sync
            if diagnostic["status"] == "available":
                current_mtime = calibre_db_path.stat().st_mtime
                stored_mtime = postgres_db.get_calibre_db_mtime()
                
                if stored_mtime is None:
                    logger.info("First run - syncing all books from Calibre in background")
                    synced_count = await asyncio.to_thread(book_service.sync_books_from_calibre)
                    postgres_db.set_calibre_db_mtime(current_mtime)
                    logger.info(f"Initial sync completed: {synced_count} books")
                elif current_mtime > stored_mtime:
                    logger.info(f"Calibre DB updated (old: {stored_mtime}, new: {current_mtime}) - syncing in background")
                    synced_count = await asyncio.to_thread(book_service.sync_books_from_calibre)
                    postgres_db.set_calibre_db_mtime(current_mtime)
                    logger.info(f"Sync completed: {synced_count} books")
                else:
                    logger.info("Calibre DB is up to date - no sync needed")
            else:
                logger.warning(
                    "Calibre metadata.db unavailable at startup: %s",
                    diagnostic,
                )
            
            # Periodic sync check every 60 seconds
            while True:
                await asyncio.sleep(60)

                diagnostic = diagnose_calibre_db()
                if diagnostic["status"] != "available":
                    logger.warning(
                        "Calibre metadata.db unavailable during periodic sync: %s",
                        diagnostic,
                    )
                    continue

                try:
                    current_mtime = calibre_db_path.stat().st_mtime
                    stored_mtime = postgres_db.get_calibre_db_mtime()
                    
                    if stored_mtime is None or current_mtime > stored_mtime:
                        logger.info(f"Calibre DB updated detected (old: {stored_mtime}, new: {current_mtime}) - syncing")
                        synced_count = await asyncio.to_thread(book_service.sync_books_from_calibre)
                        postgres_db.set_calibre_db_mtime(current_mtime)
                        logger.info(f"Periodic sync completed: {synced_count} books")
                except CalibreMetadataDBUnavailable as e:
                    logger.warning(
                        "Calibre metadata.db became unavailable during sync: %s",
                        e.diagnostic,
                    )
                    
        except asyncio.CancelledError:
            logger.info("Background sync cancelled during shutdown")
            raise
        except Exception as e:
            logger.error(f"Background sync failed: {e}", exc_info=True)
    
    # Start background tasks and store references
    import asyncio
    sync_task = asyncio.create_task(background_sync())
    network_task = None
    if settings.ENABLE_NETWORK_BINDINGS_MONITOR:
        from app.services.network_service import monitor_network_bindings
        network_task = asyncio.create_task(monitor_network_bindings())
    
    # Print server information
    print("\n" + "="*60)
    print("CALIBRE OPENCLAW SERVER")
    print("="*60)
    print(f"Version: 1.0.0")
    print(f"Host: {settings.SERVER_HOST}")
    print(f"Port: {settings.SERVER_PORT}")
    print(f"\nServer URL: http://{settings.SERVER_HOST}:{settings.SERVER_PORT}")
    print(f"\nAPI Documentation:")
    print(f"  - Swagger UI: http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/docs")
    print(f"  - ReDoc: http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/redoc")
    print(f"  - OpenAPI JSON: http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/openapi.json")
    print(f"\nMain Endpoints:")
    print(f"  - GET  /api/books              - List all books")
    print(f"  - GET  /api/books/sync         - Sync books from Calibre")
    print(f"  - GET  /api/books/sync/status  - Check sync status")
    print(f"  - GET  /api/books/{{id}}         - Get book details")
    print(f"  - GET  /api/books/{{id}}/formats - Get available book formats")
    print(f"  - GET  /api/books/{{id}}/cover   - Get book cover (JPG)")
    print(f"  - GET  /api/books/{{id}}/file    - Get selected available book file")
    print(f"  - GET  /api/books/{{id}}/pdf     - Get complete PDF")
    print(f"  - GET  /api/books/{{id}}/markdown - Get book as Markdown")
    print(f"  - POST /api/books/upload         - Upload ebook file with validation")
    print(f"  - POST /api/books/convert-format - Convert and register a book format")
    print(f"  - GET  /api/search              - Search by metadata")
    print(f"  - POST /api/search/content      - Semantic content search")
    print(f"  - GET  /api/embeddings/status/{{id}} - Check embedding status")
    print(f"  - POST /api/embeddings/generate/{{id}} - Generate embeddings")
    print(f"  - GET  /api/embeddings/queue    - Get processing queue")
    print(f"  - GET  /api/stats/database      - Database statistics")
    print(f"  - GET  /api/stats/library       - Library and RAG summary")
    print(f"  - GET  /api/stats/queries       - Query statistics")
    print(f"  - GET  /api/stats/overview     - Overview statistics")
    if settings.ENABLE_NETWORK_BINDINGS_ENDPOINT:
        print(f"  - GET  /api/network/bindings    - Active network interface URLs")
    print(f"  - WS   /ws/stats                - Real-time statistics updates")
    print(f"  - GET  /dashboard               - Real-time dashboard UI")
    print("="*60 + "\n")
    
    logger.info(f"Server starting on {settings.SERVER_HOST}:{settings.SERVER_PORT}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Calibre OpenClaw Server...")
    
    # Cancel background sync task if still running
    if sync_task and not sync_task.done():
        logger.info("Cancelling background sync task...")
        sync_task.cancel()
        try:
            await asyncio.wait_for(sync_task, timeout=5.0)
        except asyncio.CancelledError:
            logger.info("Background sync task cancelled")
        except asyncio.TimeoutError:
            logger.warning("Background sync task did not cancel in time")
        except Exception as e:
            logger.error(f"Error cancelling sync task: {e}")

    if network_task and not network_task.done():
        logger.info("Cancelling network binding monitor...")
        network_task.cancel()
        try:
            await asyncio.wait_for(network_task, timeout=5.0)
        except asyncio.CancelledError:
            logger.info("Network binding monitor cancelled")
        except asyncio.TimeoutError:
            logger.warning("Network binding monitor did not cancel in time")
        except Exception as e:
            logger.error(f"Error cancelling network binding monitor: {e}")
    
    postgres_db.close_pool()
    logger.info("PostgreSQL connection pool closed")
    logger.info("Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="Calibre OpenClaw Server",
    description="REST API for managing Calibre library with semantic search capabilities",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins_list,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _request_api_key(request: Request) -> str:
    auth_header = request.headers.get("authorization", "")
    if auth_header.lower().startswith("bearer "):
        return auth_header[7:].strip()
    return request.headers.get("x-api-key", "").strip() or request.query_params.get("api_key", "").strip()


def _auth_required(path: str) -> bool:
    return not (path == "/health" and settings.PUBLIC_HEALTHCHECK)


@app.middleware("http")
async def require_api_key(request: Request, call_next):
    """Require API key authentication unless explicitly disabled for local use."""
    if request.method == "OPTIONS" or not _auth_required(request.url.path):
        return await call_next(request)
    if not settings.ALLOW_UNAUTHENTICATED:
        configured_key = settings.api_key_value
        supplied_key = _request_api_key(request)
        if not configured_key or not supplied_key or not hmac.compare_digest(supplied_key, configured_key):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authentication required"},
                headers={"WWW-Authenticate": "Bearer"},
            )
    return await call_next(request)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault("Cache-Control", "no-store")
    response.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; "
        "connect-src 'self' ws: wss:; img-src 'self' data:; object-src 'none'; base-uri 'self'",
    )
    return response


# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log all requests with terminal-friendly details."""
    request_id = request.headers.get("x-request-id") or uuid.uuid4().hex[:12]
    start_time = time.time()
    client_ip = request.client.host if request.client else None
    query = str(request.url.query) if request.url.query else None
    user_agent = request.headers.get("user-agent")
    
    logger.info(
        f"Request started: {request.method} {request.url.path}",
        extra={
            "request_id": request_id,
            "method": request.method,
            "endpoint": str(request.url.path),
            "query": query,
            "ip": client_ip,
            "operation": "http_request_start",
        },
    )
    
    try:
        response = await call_next(request)
    except Exception:
        duration_ms = round((time.time() - start_time) * 1000, 2)
        logger.error(
            f"Request failed: {request.method} {request.url.path}",
            exc_info=True,
            extra={
                "request_id": request_id,
                "method": request.method,
                "endpoint": str(request.url.path),
                "query": query,
                "ip": client_ip,
                "duration_ms": duration_ms,
                "operation": "http_request_error",
            },
        )
        raise

    duration_ms = round((time.time() - start_time) * 1000, 2)
    response.headers["X-Request-ID"] = request_id
    content_length = response.headers.get("content-length")
    logger.info(
        f"Request completed: {request.method} {request.url.path} -> {response.status_code}",
        extra={
            "request_id": request_id,
            "method": request.method,
            "endpoint": str(request.url.path),
            "query": query,
            "ip": client_ip,
            "status_code": response.status_code,
            "duration": duration_ms / 1000,
            "duration_ms": duration_ms,
            "bytes": content_length,
            "operation": "http_request_end",
        },
    )

    if user_agent:
        logger.debug(
            "Request user agent",
            extra={
                "request_id": request_id,
                "endpoint": str(request.url.path),
                "operation": "http_request_user_agent",
            },
        )

    return response


# Include routers
app.include_router(books.router)
app.include_router(search.router)
app.include_router(embeddings.router)
app.include_router(stats.router)
app.include_router(websocket.router)
app.include_router(downloads.router)
if settings.ENABLE_NETWORK_BINDINGS_ENDPOINT:
    from app.api.routes import network
    app.include_router(network.router)


# Root endpoint - Serve dashboard
@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint serves the dashboard."""
    from pathlib import Path
    dashboard_path = Path(__file__).parent / "dashboard.html"
    return FileResponse(dashboard_path)


# API info endpoint
@app.get("/api")
async def api_info():
    """API information endpoint."""
    return {
        "name": "Calibre OpenClaw Server",
        "version": "1.0.0",
        "description": "REST API for managing Calibre library with semantic search",
        "docs": "/docs",
        "openapi": "/openapi.json",
        "dashboard": "/"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        from app.database.calibre_db import diagnose_calibre_db
        # Check database connection
        postgres_db.get_all_books(limit=1)
        calibre_diagnostic = diagnose_calibre_db()
        status_value = "healthy" if calibre_diagnostic["status"] == "available" else "degraded"
        status_code = 200 if status_value == "healthy" else 503
        return JSONResponse(
            status_code=status_code,
            content={
                "status": status_value,
                "database": "connected",
                "calibre_metadata_db": calibre_diagnostic,
            },
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected"}
        )


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=False,
        log_config=None  # Use our custom logger
    )
