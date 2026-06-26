from fastapi import APIRouter

from app.services.network_service import current_bindings

router = APIRouter(prefix="/api/network", tags=["network"])


@router.get("/bindings")
async def get_network_bindings():
    return current_bindings()
