"""
RateLimiter API — In-memory sliding window rate limiter.

Endpoints:
  POST   /v1/limits          — create/update a rate limit
  GET    /v1/limits           — list all rate limits
  GET    /v1/check/{key}      — check if a request is allowed
  POST   /v1/consume/{key}    — consume one request from quota
  POST   /v1/reset/{key}      — reset quota for a key
  DELETE /v1/limits/{key}     — delete a rate limit
"""

from fastapi import FastAPI, HTTPException

from .models import (
    CreateLimitRequest,
    DeleteResponse,
    LimitInfo,
    LimitListResponse,
    LimitStatus,
)
from .state import create_limit, delete_limit, get_limit, list_limits

app = FastAPI(
    title="RateLimiter API",
    description="In-memory sliding window rate limiter for AI agents.",
    version="0.1.0",
)


@app.post("/v1/limits", response_model=LimitStatus)
async def create_or_update_limit(request: CreateLimitRequest) -> LimitStatus:
    """Create or update a rate limit."""
    rl = create_limit(request.key, request.max_requests, request.window_seconds)
    return LimitStatus(
        key=rl.key,
        allowed=rl.allowed,
        remaining=rl.remaining,
        limit=rl.max_requests,
        window_seconds=rl.window_seconds,
        retry_after_seconds=rl.retry_after,
    )


@app.get("/v1/limits", response_model=LimitListResponse)
async def get_all_limits() -> LimitListResponse:
    """List all rate limits."""
    limits = list_limits()
    return LimitListResponse(
        limits=[
            LimitInfo(
                key=rl.key,
                max_requests=rl.max_requests,
                remaining=rl.remaining,
                window_seconds=rl.window_seconds,
            )
            for rl in limits
        ],
        total=len(limits),
    )


@app.get("/v1/check/{key}", response_model=LimitStatus)
async def check_quota(key: str) -> LimitStatus:
    """Check if a request is allowed for the given key."""
    rl = get_limit(key)
    if rl is None:
        raise HTTPException(status_code=404, detail=f"Rate limit not found: {key}")
    return LimitStatus(
        key=rl.key,
        allowed=rl.allowed,
        remaining=rl.remaining,
        limit=rl.max_requests,
        window_seconds=rl.window_seconds,
        retry_after_seconds=rl.retry_after,
    )


@app.post("/v1/consume/{key}", response_model=LimitStatus)
async def consume_request(key: str) -> LimitStatus:
    """Consume one request from the quota."""
    rl = get_limit(key)
    if rl is None:
        raise HTTPException(status_code=404, detail=f"Rate limit not found: {key}")
    rl.consume()
    return LimitStatus(
        key=rl.key,
        allowed=rl.allowed,
        remaining=rl.remaining,
        limit=rl.max_requests,
        window_seconds=rl.window_seconds,
        retry_after_seconds=rl.retry_after,
    )


@app.post("/v1/reset/{key}", response_model=LimitStatus)
async def reset_quota(key: str) -> LimitStatus:
    """Reset quota for a key."""
    rl = get_limit(key)
    if rl is None:
        raise HTTPException(status_code=404, detail=f"Rate limit not found: {key}")
    rl.reset()
    return LimitStatus(
        key=rl.key,
        allowed=rl.allowed,
        remaining=rl.remaining,
        limit=rl.max_requests,
        window_seconds=rl.window_seconds,
        retry_after_seconds=rl.retry_after,
    )


@app.delete("/v1/limits/{key}", response_model=DeleteResponse)
async def remove_limit(key: str) -> DeleteResponse:
    """Delete a rate limit."""
    deleted = delete_limit(key)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Rate limit not found: {key}")
    return DeleteResponse(key=key, deleted=True)
