"""
Production-ready REST API template using FastAPI.
Includes pagination, filtering, error handling, and best practices.
"""

from fastapi import FastAPI, HTTPException, Query, Path, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List, Any, Generic, TypeVar
from datetime import datetime
from enum import Enum

# App setup
app = FastAPI(
    title="API Template",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Models
# ============================================================================

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class UserCreate(BaseModel):
    """Request body for creating a user."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)


class UserUpdate(BaseModel):
    """Request body for updating a user (partial)."""
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[UserStatus] = None


class User(BaseModel):
    """User response model."""
    id: str
    email: str
    name: str
    status: UserStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# Pagination
# ============================================================================

T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1


# ============================================================================
# Error Handling
# ============================================================================

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str
    code: str


class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[List[ErrorDetail]] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    content = {
        "error": exc.__class__.__name__,
        "message": exc.detail if isinstance(exc.detail, str) else exc.detail.get("message", "Error"),
        "timestamp": datetime.now().isoformat()
    }
    if isinstance(exc.detail, dict) and "details" in exc.detail:
        content["details"] = exc.detail["details"]
    
    return JSONResponse(status_code=exc.status_code, content=content)


def raise_not_found(resource: str, resource_id: str):
    """Raise 404 with consistent format."""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": f"{resource} not found", "resource_id": resource_id}
    )


def raise_conflict(message: str, field: str = None):
    """Raise 409 conflict."""
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail={"message": message, "field": field}
    )


# ============================================================================
# Endpoints
# ============================================================================

@app.get("/api/users", response_model=PaginatedResponse[User], tags=["Users"])
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[UserStatus] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search by name/email"),
    sort: Optional[str] = Query("-created_at", description="Sort field (prefix - for desc)")
):
    """
    List users with pagination, filtering, and sorting.
    
    - **page**: Page number (1-indexed)
    - **page_size**: Number of items per page (max 100)
    - **status**: Filter by user status
    - **search**: Search in name and email
    - **sort**: Sort field, prefix with - for descending
    """
    # Implementation: Replace with actual database query
    total = 100
    items = []  # fetch_users(...)
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size
    )


@app.post(
    "/api/users",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"]
)
async def create_user(user: UserCreate):
    """
    Create a new user.
    
    Returns 201 Created with the new user.
    Returns 409 Conflict if email already exists.
    """
    # Check for existing user
    # if await user_exists(user.email):
    #     raise_conflict("Email already registered", "email")
    
    # Create and return user
    return User(
        id="new-id",
        email=user.email,
        name=user.name,
        status=UserStatus.ACTIVE,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@app.get("/api/users/{user_id}", response_model=User, tags=["Users"])
async def get_user(user_id: str = Path(..., description="User ID")):
    """
    Get user by ID.
    
    Returns 404 if user not found.
    """
    # user = await fetch_user(user_id)
    # if not user:
    #     raise_not_found("User", user_id)
    # return user
    raise_not_found("User", user_id)


@app.patch("/api/users/{user_id}", response_model=User, tags=["Users"])
async def update_user(
    user_id: str = Path(..., description="User ID"),
    update: UserUpdate = ...
):
    """
    Partially update user.
    
    Only provided fields are updated.
    """
    # existing = await fetch_user(user_id)
    # if not existing:
    #     raise_not_found("User", user_id)
    # 
    # update_data = update.model_dump(exclude_unset=True)
    # updated = await update_user_in_db(user_id, update_data)
    # return updated
    raise_not_found("User", user_id)


@app.delete(
    "/api/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Users"]
)
async def delete_user(user_id: str = Path(..., description="User ID")):
    """
    Delete user.
    
    Returns 204 No Content on success.
    Returns 404 if user not found.
    """
    # if not await fetch_user(user_id):
    #     raise_not_found("User", user_id)
    # await delete_user_from_db(user_id)
    pass


# ============================================================================
# Health Checks
# ============================================================================

@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/health/ready", tags=["Health"])
async def readiness_check():
    """Detailed readiness check with dependency status."""
    checks = {
        "database": True,  # await check_database()
        "cache": True,     # await check_redis()
    }
    all_healthy = all(checks.values())
    
    return {
        "status": "ready" if all_healthy else "not_ready",
        "checks": checks,
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# Run
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
