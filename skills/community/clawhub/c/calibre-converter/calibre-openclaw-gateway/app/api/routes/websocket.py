from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import asyncio
import hmac
import json
from datetime import datetime

from app.api.routes.stats import get_database_stats, get_query_stats
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections for real-time updates."""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to a specific WebSocket, checking if still connected."""
        try:
            if websocket.client_state.name != 'DISCONNECTED':
                await websocket.send_text(message)
            else:
                logger.warning("Attempted to send to disconnected WebSocket")
                return False
            return True
        except Exception as e:
            logger.error(f"Error sending to WebSocket: {e}")
            return False
    
    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients."""
        if self.active_connections:
            message_str = json.dumps(message)
            disconnected = set()
            
            for connection in self.active_connections:
                try:
                    if connection.client_state.name != 'DISCONNECTED':
                        await connection.send_text(message_str)
                    else:
                        disconnected.add(connection)
                except Exception as e:
                    logger.error(f"Error sending to WebSocket: {e}")
                    disconnected.add(connection)
            
            # Remove disconnected clients
            for connection in disconnected:
                self.active_connections.discard(connection)


manager = ConnectionManager()


def websocket_api_key(websocket: WebSocket) -> str:
    auth_header = websocket.headers.get("authorization", "")
    if auth_header.lower().startswith("bearer "):
        return auth_header[7:].strip()
    return (
        websocket.headers.get("x-api-key", "").strip()
        or websocket.query_params.get("api_key", "").strip()
    )


async def require_websocket_api_key(websocket: WebSocket) -> bool:
    if settings.ALLOW_UNAUTHENTICATED:
        return True
    configured_key = settings.api_key_value
    supplied_key = websocket_api_key(websocket)
    if configured_key and supplied_key and hmac.compare_digest(supplied_key, configured_key):
        return True
    await websocket.close(code=1008, reason="Authentication required")
    return False


@router.websocket("/ws/stats")
async def websocket_stats(websocket: WebSocket):
    """WebSocket endpoint for real-time statistics updates.
    
    Optimized to connect immediately and fetch data in parallel.
    """
    client_host = websocket.client.host if websocket.client else "unknown"
    logger.info(f"[{client_host}] WebSocket connection attempt started")
    
    if not await require_websocket_api_key(websocket):
        logger.warning(f"[{client_host}] WebSocket authentication failed")
        return
    
    logger.info(f"[{client_host}] WebSocket authentication successful, connecting...")
    await manager.connect(websocket)
    logger.info(f"[{client_host}] WebSocket connected successfully")
    
    try:
        # Send connection acknowledgment immediately
        ack_message = {
            "type": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
        logger.debug(f"[{client_host}] Sending connection acknowledgment")
        sent = await manager.send_personal_message(json.dumps(ack_message), websocket)
        if not sent:
            logger.warning(f"[{client_host}] Failed to send connection ack, closing connection")
            return
        logger.debug(f"[{client_host}] Connection acknowledgment sent successfully")
        
        # Fetch initial stats in parallel
        logger.debug(f"[{client_host}] Starting to fetch initial stats in parallel")
        try:
            import time
            start_time = time.time()
            
            db_stats, query_stats = await asyncio.gather(
                get_database_stats(),
                get_query_stats()
            )
            
            fetch_time = time.time() - start_time
            logger.info(f"[{client_host}] Initial stats fetched in {fetch_time:.3f}s")
            
            initial_message = {
                "type": "initial",
                "data": {
                    "database": db_stats,
                    "queries": query_stats,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
            logger.debug(f"[{client_host}] Sending initial message (size: {len(json.dumps(initial_message))} bytes)")
            sent = await manager.send_personal_message(json.dumps(initial_message), websocket)
            if not sent:
                logger.warning(f"[{client_host}] Failed to send initial message, closing connection")
                return
            logger.info(f"[{client_host}] Initial message sent successfully")
        except Exception as e:
            logger.error(f"[{client_host}] Error fetching initial stats: {e}", exc_info=True)
            error_message = {
                "type": "error",
                "error": "Failed to fetch initial statistics",
                "timestamp": datetime.utcnow().isoformat()
            }
            await manager.send_personal_message(json.dumps(error_message), websocket)
            logger.warning(f"[{client_host}] Error message sent, keeping connection alive for retries")
            # Don't close connection, allow periodic updates to try again
        
        # Send periodic updates every 5 seconds
        update_count = 0
        while True:
            await asyncio.sleep(5)
            update_count += 1
            logger.debug(f"[{client_host}] Starting periodic update #{update_count}")
            
            try:
                # Fetch stats in parallel
                import time
                start_time = time.time()
                
                db_stats, query_stats = await asyncio.gather(
                    get_database_stats(),
                    get_query_stats()
                )
                
                fetch_time = time.time() - start_time
                logger.debug(f"[{client_host}] Update #{update_count} stats fetched in {fetch_time:.3f}s")
                
                update_message = {
                    "type": "update",
                    "data": {
                        "database": db_stats,
                        "queries": query_stats,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
                sent = await manager.send_personal_message(json.dumps(update_message), websocket)
                if not sent:
                    logger.warning(f"[{client_host}] Failed to send update message #{update_count}, closing connection")
                    break
                logger.debug(f"[{client_host}] Update #{update_count} sent successfully")
            except Exception as e:
                logger.error(f"[{client_host}] Error fetching stats for update #{update_count}: {e}", exc_info=True)
                # Send error message but keep connection alive
                error_message = {
                    "type": "error",
                    "error": "Failed to fetch statistics",
                    "timestamp": datetime.utcnow().isoformat()
                }
                await manager.send_personal_message(json.dumps(error_message), websocket)
                
    except asyncio.CancelledError:
        logger.info(f"[{client_host}] WebSocket connection cancelled during shutdown")
        manager.disconnect(websocket)
        raise
    except WebSocketDisconnect as e:
        logger.info(f"[{client_host}] WebSocket client disconnected (code: {e.code}, reason: {e.reason})")
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"[{client_host}] WebSocket error: {e}", exc_info=True)
        manager.disconnect(websocket)
