# 常见问题与解决方案

---

## 问题分类说明

**简单问题（1-2步排查）**：安装错误、导入问题等
**中等问题（3-5步排查）**：路由冲突、请求验证失败等
**复杂问题（5-10步排查）**：性能问题、部署故障等

---

## 安装问题

### 1. pip install fastapi 失败【简单问题】

**问题描述**: 使用 pip 安装 FastAPI 时报错

**排查步骤**:
```bash
# 检查 Python 版本（需要 3.8+）
python --version

# 检查 pip 版本
pip --version
```

**常见原因**:
- Python 版本低于 3.8 (40%)
- 网络连接问题 (30%)
- pip 版本过低 (20%)
- 虚拟环境未激活 (10%)

**解决方案**:

**方案A（推荐）**: 使用虚拟环境安装
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
pip install "fastapi[standard]"
```

**方案B**: 升级 pip 后重试
```bash
python -m pip install --upgrade pip
pip install fastapi
```

---

### 2. uvicorn 命令找不到【简单问题】

**问题描述**: 安装 FastAPI 后运行 `uvicorn` 提示 command not found

**排查步骤**:
```bash
# 检查 uvicorn 是否安装
pip list | grep uvicorn

# 检查 PATH
which uvicorn
```

**常见原因**:
- 未安装 uvicorn (50%)
- 虚拟环境未激活 (30%)
- PATH 未包含 pip 安装目录 (20%)

**解决方案**:

**方案A（推荐）**: 安装完整依赖
```bash
pip install "fastapi[standard]"
```

**方案B**: 使用 python -m 方式运行
```bash
python -m uvicorn main:app --reload
```

---

## 开发问题

### 3. 路由 404 Not Found【中等问题】

**问题描述**: 请求 API 端点返回 404

**排查步骤**:
```bash
# 查看所有已注册路由
python -c "
from main import app
for route in app.routes:
    if hasattr(route, 'methods'):
        print(f'{route.methods} {route.path}')
"
```

**常见原因**:
- 路径拼写错误或缺少前缀斜杠 (35%)
- 路由器未注册到 app (25%)
- HTTP 方法不匹配 (20%)
- 路径参数类型不匹配 (20%)

**解决方案**:

**方案A**: 检查路由注册
```python
# 确保路由器已 include
from fastapi import FastAPI
from routers import users

app = FastAPI()
app.include_router(users.router, prefix="/users")
```

**方案B**: 检查路径参数类型
```python
# 错误：路径顺序导致冲突
@app.get("/users/{user_id}")  # 这个会捕获 /users/me
@app.get("/users/me")

# 正确：具体路径放前面
@app.get("/users/me")
@app.get("/users/{user_id}")
```

---

### 4. 请求体验证失败 422 Unprocessable Entity【中等问题】

**问题描述**: POST/PUT 请求返回 422 验证错误

**排查步骤**:
```bash
# 检查请求体格式
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "price": 10.5}'
```

**常见原因**:
- 请求体缺少必填字段 (35%)
- 字段类型不匹配 (30%)
- 未设置 Content-Type: application/json (20%)
- Pydantic 模型定义错误 (15%)

**解决方案**:

**方案A**: 检查 Pydantic 模型定义
```python
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None  # 可选字段需要默认值
```

**方案B**: 查看详细错误信息
```python
# 422 响应体包含详细的验证错误
# 检查 response.json()["detail"] 获取具体哪个字段出错
```

---

### 5. 异步数据库操作阻塞【中等问题】

**问题描述**: 使用同步数据库驱动导致 API 响应缓慢

**排查步骤**:
```python
# 检查是否在 async 函数中使用了同步操作
import asyncio
# 如果事件循环被阻塞，其他请求会等待
```

**常见原因**:
- 在 async 路由中使用同步数据库驱动 (50%)
- 未使用连接池 (30%)
- CPU 密集型操作在主线程 (20%)

**解决方案**:

**方案A（推荐）**: 使用异步数据库驱动
```python
# 使用 databases 或 SQLAlchemy async
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine("postgresql+asyncpg://...")
```

**方案B**: 同步操作改用普通函数（FastAPI 自动在线程池运行）
```python
# FastAPI 会自动将 def 路由放入线程池
@app.get("/items/")
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

---

## 部署问题

### 6. CORS 跨域请求被拒绝【简单问题】

**问题描述**: 前端请求 API 报 CORS 错误

**排查步骤**:
```bash
# 检查响应头是否包含 CORS 头
curl -I -X OPTIONS http://localhost:8000/api/items \
  -H "Origin: http://localhost:3000"
```

**常见原因**:
- 未添加 CORS 中间件 (60%)
- allowed_origins 配置错误 (25%)
- 预检请求未处理 (15%)

**解决方案**:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 生产环境使用具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 7. 生产环境部署 uvicorn workers 配置【中等问题】

**问题描述**: 单 worker 无法充分利用多核 CPU

**排查步骤**:
```bash
# 检查 CPU 核心数
python -c "import multiprocessing; print(multiprocessing.cpu_count())"

# 检查当前 worker 数
ps aux | grep uvicorn
```

**常见原因**:
- 默认单 worker 运行 (50%)
- worker 数设置过多导致内存不足 (30%)
- 未使用进程管理器 (20%)

**解决方案**:

**方案A（推荐）**: 使用 gunicorn + uvicorn workers
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

**方案B**: 直接使用 uvicorn 多 worker
```bash
uvicorn main:app --workers 4 --host 0.0.0.0 --port 8000
```

---

### 8. 静态文件无法访问【简单问题】

**问题描述**: 挂载的静态文件目录返回 404

**排查步骤**:
```bash
# 确认静态文件目录存在
ls -la static/

# 确认挂载顺序（静态文件应在最后挂载）
```

**常见原因**:
- 目录路径错误 (40%)
- 挂载顺序在 API 路由之前 (30%)
- 文件权限问题 (30%)

**解决方案**:

```python
from fastapi.staticfiles import StaticFiles

# 注意：静态文件挂载应在所有 API 路由之后
app.mount("/static", StaticFiles(directory="static"), name="static")
```

---

## 性能问题

### 9. 依赖注入每次请求重新创建【中等问题】

**问题描述**: 数据库连接等资源每次请求都重新创建，导致性能下降

**排查步骤**:
```python
# 检查依赖函数是否正确使用 yield
# 检查是否使用了 lru_cache 缓存重量级依赖
```

**常见原因**:
- 未使用 yield 管理资源生命周期 (40%)
- 未缓存配置类依赖 (35%)
- 每次请求创建新的数据库引擎 (25%)

**解决方案**:

**方案A**: 使用 yield 依赖管理连接
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**方案B**: 缓存配置依赖
```python
from functools import lru_cache

@lru_cache
def get_settings():
    return Settings()
```

---

### 10. Swagger 文档页面加载缓慢【简单问题】

**问题描述**: /docs 页面在生产环境加载很慢

**排查步骤**:
```bash
# 检查是否从 CDN 加载 Swagger UI 资源
curl -I https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js
```

**常见原因**:
- CDN 资源在国内访问慢 (60%)
- 路由数量过多导致 OpenAPI schema 太大 (30%)
- 未设置 CDN 镜像 (10%)

**解决方案**:

**方案A**: 使用本地静态文件
```python
from fastapi.openapi.docs import get_swagger_ui_html

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API Docs",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )
```

**方案B**: 生产环境禁用文档
```python
app = FastAPI(docs_url=None, redoc_url=None)  # 生产环境
```
