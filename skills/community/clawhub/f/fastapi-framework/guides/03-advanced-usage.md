# 高级用法

**适用场景**: 构建生产级 FastAPI 应用，涉及模块化路由、依赖注入、认证、数据库集成、中间件等

---

## 一、模块化项目结构（APIRouter）

### 推荐项目结构

```
app/
├── __init__.py
├── main.py              # 应用入口
├── dependencies.py      # 公共依赖
├── core/
│   ├── __init__.py
│   ├── config.py        # 配置管理
│   └── security.py      # 安全工具函数
├── models/
│   ├── __init__.py
│   └── user.py          # Pydantic 模型
├── routers/
│   ├── __init__.py
│   ├── users.py
│   └── items.py
└── crud/
    ├── __init__.py
    └── user.py
```

### 定义路由器

**AI 执行说明**: AI 可以自动生成路由器模块代码

```python
# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", summary="获取用户列表")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/me", summary="获取当前用户")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user

@router.get("/{username}", summary="根据用户名获取用户")
async def read_user(username: str):
    return {"username": username}
```

```python
# app/routers/items.py
from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_token_header

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],  # 路由器级别依赖
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

@router.get("/")
async def read_items():
    return fake_items_db

@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}
```

### 主应用注册路由器

```python
# app/main.py
from fastapi import FastAPI
from .routers import users, items

app = FastAPI(
    title="My API",
    description="Production FastAPI Application",
    version="1.0.0",
)

# 注册路由器
app.include_router(users.router)
app.include_router(items.router)

# 还可以在注册时覆盖前缀和 tags
app.include_router(
    users.router,
    prefix="/api/v2",
    tags=["users-v2"],
)

@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to My API"}
```

---

## 二、依赖注入系统

### 基础依赖

**AI 执行说明**: AI 可以自动识别公共逻辑并封装为依赖函数

```python
# app/dependencies.py
from typing import Annotated
from fastapi import Depends, HTTPException, Header

# 公共查询参数
async def common_parameters(
    q: str | None = None,
    skip: int = 0,
    limit: int = 100,
):
    return {"q": q, "skip": skip, "limit": limit}

CommonsDep = Annotated[dict, Depends(common_parameters)]

# Token 验证依赖
async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

# 使用类作为依赖（可缓存）
class DatabaseDep:
    def __init__(self, db_url: str = "sqlite:///./test.db"):
        self.db_url = db_url

    def __call__(self):
        # 返回数据库连接
        return {"url": self.db_url}

db_dependency = DatabaseDep()
```

### 带 yield 的依赖（资源管理）

适用于数据库会话、文件句柄等需要在请求结束后释放的资源：

```python
from sqlmodel import Session, create_engine

engine = create_engine("sqlite:///./database.db")

def get_session():
    with Session(engine) as session:
        yield session  # FastAPI 在请求结束后自动关闭 session

SessionDep = Annotated[Session, Depends(get_session)]
```

### 子依赖（依赖链）

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    if current_user.get("disabled"):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# 在路由中使用
@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[dict, Depends(get_current_active_user)]
):
    return current_user
```

---

## 三、中间件

### 自定义 HTTP 中间件

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# 日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Response status: {response.status_code}")
    return response
```

### CORS 配置

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com", "https://www.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time"],
)

# 开发环境允许所有来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### GZip 压缩中间件

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

---

## 四、JWT 认证实现

### 安装依赖

```bash
pip install pyjwt "pwdlib[argon2]"
```

### 完整认证实现

```python
# app/core/security.py
from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from pydantic import BaseModel

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 数据模型
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

# 模拟用户数据库
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": password_hash.hash("secret"),
        "disabled": False,
    }
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def get_user(db, username: str) -> UserInDB | None:
    if username in db:
        return UserInDB(**db[username])
    return None

def authenticate_user(db, username: str, password: str) -> UserInDB | bool:
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = {**data}
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

```python
# app/main.py（认证相关路由）
from fastapi import FastAPI, Depends
from .core.security import (
    Token, User, authenticate_user, create_access_token,
    get_current_active_user, fake_users_db, ACCESS_TOKEN_EXPIRE_MINUTES
)
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated

app = FastAPI()

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
```

---

## 五、数据库集成（SQLModel）

### 安装和配置

```bash
pip install sqlmodel
```

```python
# app/database.py
from typing import Annotated
from fastapi import Depends
from sqlmodel import Field, Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
```

### 模型定义（继承模式）

```python
# app/models/hero.py
from sqlmodel import Field, SQLModel

# 共享基础字段
class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)

# 数据库表模型
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str  # 敏感字段，不对外暴露

# 创建请求模型
class HeroCreate(HeroBase):
    secret_name: str

# 公开响应模型（不含敏感字段）
class HeroPublic(HeroBase):
    id: int

# 更新请求模型（所有字段可选）
class HeroUpdate(SQLModel):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None
```

### CRUD 路由实现

```python
# app/routers/heroes.py
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from ..database import SessionDep
from ..models.hero import Hero, HeroCreate, HeroPublic, HeroUpdate

router = APIRouter(prefix="/heroes", tags=["heroes"])

@router.post("/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@router.get("/", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

@router.get("/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@router.patch("/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db

@router.delete("/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
```

---

## 六、应用生命周期事件

使用 `lifespan` 管理应用启动和关闭资源：

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时：初始化数据库、连接缓存等
    print("Application starting up...")
    create_db_and_tables()
    # 也可以初始化 ML 模型
    # app.state.model = load_model()

    yield  # 应用运行中

    # 关闭时：释放资源
    print("Application shutting down...")
    # await cache.close()

app = FastAPI(lifespan=lifespan)
```

---

## 七、后台任务

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message + "\n")

async def send_email(email: str, message: str):
    # 模拟发送邮件
    print(f"Sending email to {email}: {message}")

@app.post("/send-notification/{email}")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    background_tasks.add_task(send_email, email, "You have a notification!")
    return {"message": "Notification sent in the background"}
```

---

## 八、WebSocket 支持

```python
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except Exception:
        await websocket.close()
```

---

## 九、环境配置管理

```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    debug: bool = False
    database_url: str = "sqlite:///./database.db"
    secret_key: str
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

```bash
# .env
APP_NAME=Production API
DEBUG=false
DATABASE_URL=postgresql://user:pass@localhost/mydb
SECRET_KEY=super-secret-key
```

```bash
pip install pydantic-settings
```

---

## 十、API 版本控制

```python
# 方式 1：URL 前缀版本
from fastapi import FastAPI
from .routers.v1 import users as users_v1
from .routers.v2 import users as users_v2

app = FastAPI()
app.include_router(users_v1.router, prefix="/api/v1")
app.include_router(users_v2.router, prefix="/api/v2")

# 方式 2：独立子应用挂载
from fastapi import FastAPI

v1 = FastAPI()
v2 = FastAPI()

@v1.get("/users/")
async def read_users_v1():
    return {"version": "v1"}

@v2.get("/users/")
async def read_users_v2():
    return {"version": "v2", "features": ["new_feature"]}

app = FastAPI()
app.mount("/api/v1", v1)
app.mount("/api/v2", v2)
```

---

## 十一、生产部署

### 使用 Gunicorn + Uvicorn

```bash
pip install gunicorn

# 启动多进程服务
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# 构建并运行
docker build -t my-fastapi-app .
docker run -d -p 8000:8000 my-fastapi-app
```

---

## 完成确认

### 检查清单

- [ ] 路由器模块化，按业务功能划分
- [ ] 依赖注入封装了数据库会话和用户认证
- [ ] JWT 认证流程正常（登录获取 token，请求携带 token）
- [ ] 数据库 CRUD 操作正常
- [ ] 中间件按预期执行
- [ ] 生命周期事件正确初始化/清理资源
- [ ] 生产环境配置（多进程、环境变量）就绪

### 下一步

查阅 [常见问题](../troubleshooting.md) 了解常见错误的解决方案
