---
name: fastapi
description: FastAPI - 高性能 Python Web API 框架
version: 0.1.0
metadata:
  openclaw:
    requires:
      - fastapi
      - uvicorn
    emoji: ⚡
    homepage: https://fastapi.tiangolo.com
---

# FastAPI 高性能 Python Web API 框架

## 技能概述

本技能帮助开发者使用 FastAPI 构建现代化、高性能的 Web API，支持以下场景：

- **REST API 开发**: 快速构建符合 OpenAPI 标准的 RESTful 接口
- **数据验证**: 基于 Pydantic 的自动请求/响应数据验证
- **自动文档**: 自动生成 Swagger UI 和 ReDoc 交互式 API 文档
- **异步支持**: 原生支持 async/await，处理高并发场景
- **依赖注入**: 强大的依赖注入系统，简化认证、数据库连接等公共逻辑
- **安全认证**: 内置 OAuth2、JWT、API Key 等认证方案

**技术基础**: FastAPI 构建于 Starlette（Web 框架层）和 Pydantic（数据验证层）之上，性能接近 NodeJS 和 Go。

## 架构概览

```
FastAPI 应用架构
├── app/
│   ├── main.py              # 应用入口，注册路由和中间件
│   ├── dependencies.py      # 公共依赖（认证、数据库会话等）
│   ├── models/              # Pydantic 数据模型
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/             # 路由模块（按业务划分）
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── crud/                # 数据库操作层
│   │   ├── __init__.py
│   │   └── user.py
│   └── core/                # 核心配置
│       ├── config.py
│       └── security.py
```

## 核心概念

| 概念 | 说明 |
|------|------|
| **路径操作** | 使用 `@app.get/post/put/delete` 装饰器定义 API 端点 |
| **路径参数** | URL 中的变量，如 `/items/{item_id}` |
| **查询参数** | URL 查询字符串，如 `/items?skip=0&limit=10` |
| **请求体** | 通过 Pydantic 模型接收 JSON 数据 |
| **依赖注入** | 通过 `Depends()` 注入可复用的依赖函数 |
| **中间件** | 处理每个请求/响应的通用逻辑 |
| **路由器** | `APIRouter` 将路由按模块组织，类似 Flask Blueprint |

## 使用流程

AI 助手将引导你完成以下步骤：

1. 安装 FastAPI 及依赖（uvicorn、pydantic 等）
2. 创建应用入口文件 `main.py`
3. 定义 Pydantic 数据模型
4. 编写路径操作函数（路由处理器）
5. 配置依赖注入和中间件
6. 启动开发服务器并验证 API 文档

## 关键章节导航

- [安装指南](./guides/01-installation.md)
- [快速开始](./guides/02-quickstart.md)
- [高级用法](./guides/03-advanced-usage.md)
- [常见问题](./troubleshooting.md)

## AI 助手能力

当你向 AI 描述需求时，AI 会：

- **自动生成** 路由处理函数和 Pydantic 数据模型
- **自动配置** 依赖注入（数据库会话、用户认证）
- **自动搭建** 项目骨架结构（models、routers、crud 分层）
- **自动实现** JWT 认证和 OAuth2 安全方案
- **自动集成** SQLAlchemy/SQLModel 数据库操作
- **自动编写** 测试用例（pytest + httpx）
- **自动处理** CORS 配置和自定义中间件

## 核心功能

- ✅ 基于 Python 类型提示的自动数据验证
- ✅ 自动生成 OpenAPI/Swagger 交互式文档
- ✅ 原生 async/await 异步支持
- ✅ 强大的依赖注入系统
- ✅ 内置安全认证（OAuth2、JWT、API Key、HTTP Basic）
- ✅ 支持 WebSocket 实时通信
- ✅ 支持 GraphQL（通过 Strawberry 集成）
- ✅ 支持后台任务（BackgroundTasks）
- ✅ 支持文件上传和静态文件服务
- ✅ 支持中间件和 CORS 配置

## 快速示例

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

```bash
# 启动开发服务器
fastapi dev main.py

# 或使用 uvicorn
uvicorn main:app --reload
```

访问 `http://127.0.0.1:8000/docs` 查看自动生成的交互式 API 文档。

## 扩展点

- **中间件**: 实现日志、限流、请求追踪等横切关注点
- **依赖注入**: 封装数据库连接、权限校验等可复用逻辑
- **事件处理**: `startup`/`shutdown` 生命周期钩子
- **自定义响应**: 支持 `JSONResponse`、`HTMLResponse`、`FileResponse` 等
- **插件生态**: 支持 SQLAlchemy、Celery、Redis、S3 等主流库

## 环境要求

- Python 3.8 或更高版本（推荐 3.11+）
- pip 包管理器
- （可选）虚拟环境工具（venv、conda、uv）

## 许可证

MIT License

## 项目链接

- GitHub: https://github.com/tiangolo/fastapi
- 官网: https://fastapi.tiangolo.com
- 文档: https://fastapi.tiangolo.com/tutorial/
- PyPI: https://pypi.org/project/fastapi/
