---
name: fastapi-backend
description: "FastAPI 后端开发最佳实践框架。涵盖 FastAPI + SQLAlchemy 2.0 (async) + Alembic 迁移 + Pydantic v2 的完整技术栈。当用户需要：创建 API/后端服务、搭建 Web 服务、设计 RESTful 接口、配置数据库连接、编写 CRUD 操作、实现认证授权、处理异步请求、部署 Python Web 应用、使用 SQLAlchemy ORM、配置 Alembic 数据库迁移时，立即使用此技能。即使用户只说'写个接口'、'做个后端'、'连数据库'，也应触发此技能。"
version: 1.0.0
---

# FastAPI Backend — 后端开发最佳实践

## 技术栈

| 组件 | 版本 | 用途 |
|------|------|------|
| FastAPI | 0.110+ | Web 框架 |
| SQLAlchemy | 2.0+ | ORM（异步） |
| Alembic | 1.13+ | 数据库迁移 |
| Pydantic | 2.0+ | 数据验证 |
| uvicorn | 0.27+ | ASGI 服务器 |

---

## 一、项目结构

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── dependencies.py      # 依赖注入
│   ├── models/              # SQLAlchemy 模型
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/             # Pydantic 模型
│   │   ├── __init__.py
│   │   └── user.py
│   ├── api/                 # 路由
│   │   ├── __init__.py
│   │   ├── deps.py          # API 依赖
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── users.py
│   ├── core/                # 核心功能
│   │   ├── __init__.py
│   │   ├── security.py      # 认证/授权
│   │   └── exceptions.py    # 自定义异常
│   └── crud/                # CRUD 操作
│       ├── __init__.py
│       └── user.py
├── alembic/                 # 迁移文件
│   ├── versions/
│   └── env.py
├── alembic.ini
├── tests/
│   ├── conftest.py
│   └── test_users.py
├── requirements.txt
└── .env
```

---

## 二、核心配置

### 2.1 配置管理 (config.py)

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # 应用
    APP_NAME: str = "My API"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    
    # 数据库
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/dbname"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    
    # 认证
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24h
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    model_config = {"env_file": ".env", "case_sensitive": True}

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

### 2.2 数据库连接 (database.py)

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,  # 自动重连
    echo=settings.DEBUG,
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncSession:
    """依赖注入：获取数据库会话"""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

---

## 三、模型定义 (SQLAlchemy 2.0)

### 3.1 基础模型

```python
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.database import Base

class TimestampMixin:
    """时间戳混入"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

class IDMixin:
    """ID 混入"""
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
```

### 3.2 业务模型

```python
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.mixins import TimestampMixin, IDMixin

class User(TimestampMixin, IDMixin, Base):
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # 关系
    posts: Mapped[list["Post"]] = relationship(back_populates="author", lazy="selectin")

class Post(TimestampMixin, IDMixin, Base):
    __tablename__ = "posts"
    
    title: Mapped[str] = mapped_column(String(200), index=True)
    content: Mapped[str] = mapped_column(String(10000))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    
    author: Mapped["User"] = relationship(back_populates="posts")
```

---

## 四、Pydantic Schemas

### 4.1 基础 Schema

```python
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime
```

---

## 五、CRUD 操作

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return list(result.scalars().all())

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user

async def update_user(db: AsyncSession, db_user: User, user_in: UserUpdate) -> User:
    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    for field, value in update_data.items():
        setattr(db_user, field, value)
    await db.flush()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int) -> bool:
    user = await get_user(db, user_id)
    if not user:
        return False
    await db.delete(user)
    await db.flush()
    return True
```

---

## 六、API 路由

### 6.1 路由定义

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import user as user_crud
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.api.deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await user_crud.get_users(db, skip=skip, limit=limit)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    # 检查邮箱是否已存在
    existing = await user_crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await user_crud.create_user(db, user_in)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    user = await user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    user = await user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # 权限检查
    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    return await user_crud.update_user(db, user, user_in)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    deleted = await user_crud.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
```

### 6.2 主应用入口

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.api.v1 import users

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由
app.include_router(users.router, prefix=settings.API_V1_PREFIX)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
```

---

## 七、认证与授权

### 7.1 JWT 认证

```python
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import get_settings
from app.database import get_db
from app.crud import user as user_crud

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: int, expires_delta: timedelta | None = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return jwt.encode({"sub": str(subject), "exp": expire}, settings.SECRET_KEY, algorithm="HS256")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await user_crud.get_user(db, user_id)
    if user is None:
        raise credentials_exception
    return user
```

---

## 八、Alembic 迁移

### 8.1 初始化

```bash
# 初始化 Alembic
alembic init -t async alembic

# 配置 alembic.ini
# sqlalchemy.url = postgresql+asyncpg://user:pass@localhost/dbname

# 配置 alembic/env.py (见下方)
```

### 8.2 alembic/env.py 配置

```python
from app.config import get_settings
from app.database import Base
from app.models import user  # 导入所有模型

config = context.config
target_metadata = Base.metadata

# 使用异步引擎
async def run_migrations_online():
    connectable = create_async_engine(get_settings().DATABASE_URL)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()
```

### 8.3 常用命令

```bash
# 创建迁移
alembic revision --autogenerate -m "add users table"

# 应用迁移
alembic upgrade head

# 回滚一个版本
alembic downgrade -1

# 查看迁移历史
alembic history

# 查看当前版本
alembic current
```

---

## 九、异常处理

```python
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# 使用
raise AppException(status_code=404, detail="Resource not found")
```

---

## 十、测试

### 10.1 conftest.py

```python
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/test_db"

@pytest.fixture
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    session_maker = async_sessionmaker(engine, class_=AsyncSession)
    async with session_maker() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()
```

### 10.2 测试用例

```python
import pytest

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post("/api/v1/users/", json={
        "email": "test@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_create_user_duplicate_email(client):
    # 先创建一个
    await client.post("/api/v1/users/", json={
        "email": "test@example.com",
        "password": "securepassword"
    })
    # 尝试重复创建
    response = await client.post("/api/v1/users/", json={
        "email": "test@example.com",
        "password": "anotherpassword"
    })
    assert response.status_code == 400
```

---

## 十一、性能优化清单

- [ ] 使用 `selectinload` 或 `joinedload` 预加载关系
- [ ] 为频繁查询的字段添加索引
- [ ] 使用连接池（已配置）
- [ ] 启用 `pool_pre_ping` 防止连接失效
- [ ] 使用 `limit` 和 `offset` 分页
- [ ] 避免在循环中执行数据库查询
- [ ] 使用 `EXPLAIN ANALYZE` 分析慢查询
- [ ] 考虑使用 Redis 缓存热点数据

---

## 十二、部署

```bash
# 生产环境启动
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# 或使用 gunicorn + uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 快速参考

| 场景 | 解决方案 |
|------|---------|
| 添加新接口 | `api/v1/` 下创建路由，注册到 `main.py` |
| 添加新模型 | `models/` 下定义，运行 `alembic revision --autogenerate` |
| 添加认证 | 使用 `get_current_user` 依赖 |
| 分页查询 | 使用 `offset` + `limit` |
| 错误处理 | 使用 `HTTPException` 或自定义 `AppException` |
| 测试 | 使用 `pytest-asyncio` + `httpx.AsyncClient` |
