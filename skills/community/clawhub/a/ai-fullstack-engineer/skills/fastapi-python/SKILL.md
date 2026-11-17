---
name: fastapi-python
description: FastAPI Python 开发：异步 API、Pydantic 验证、依赖注入、测试与部署
source:
  type: derived
  repo: skills-repo/ai-fullstack-engineer
  path: skills/fastapi-python/SKILL.md
  url: https://skills.sh/mindrally/skills/fastapi-python
  version: 1.0.0
  updated: 2026-07-30
metadata:
  author: hope
  category: 开发
  platform: Python
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-30
tags:
  - fastapi
  - python
  - async
  - pydantic
  - api
---

# FastAPI Python — 异步后端开发

> Python 后端也可以快。FastAPI 凭借原生 async/await、自动 OpenAPI 文档和 Pydantic 验证，让 Python 成为高性能 API 的有力竞争者。

## 能力

- **异步 API 开发**：async def、后台任务、StreamingResponse
- **Pydantic 数据验证**：请求/响应模型、嵌套 Schema、自定义验证器
- **依赖注入**：数据库会话、认证、权限的依赖链管理
- **中间件与事件**：CORS、请求日志、startup/shutdown 生命周期
- **测试**：TestClient + pytest、异步测试、数据库 mock

## 使用方式

在 Claude Code 中使用 `/fastapi-python` 调用。

```
/fastapi-python 帮我搭建一个 FastAPI 项目骨架（含数据库和认证）
/fastapi-python 这个 Pydantic 模型如何设计嵌套验证？
/fastapi-python 如何优化这个端点的并发性能？
```

## 工作流

1. **项目初始化** — 目录结构、配置管理、环境变量
2. **模型设计** — Pydantic Schema → SQLAlchemy Model → 迁移
3. **路由开发** — CRUD 端点、依赖注入、异常处理
4. **中间件集成** — CORS、认证、限流、日志
5. **测试编写** — 单元测试、集成测试、性能测试

## FastAPI 项目骨架

```
app/
├── main.py           # FastAPI app + lifespan
├── config.py         # Settings (pydantic-settings)
├── models/           # SQLAlchemy models
├── schemas/          # Pydantic schemas
├── api/              # Route handlers
│   └── v1/
├── services/         # Business logic
├── dependencies.py   # Dependency injection
└── tests/
```

## 适用场景

- Python 开发者构建高性能 REST API
- 从 Flask/Django REST 迁移到 FastAPI
- 需要自动生成 OpenAPI 文档的项目
- 异步 IO 密集型应用（文件处理、外部 API 调用）

## 限制

- 不涉及 Django/Flask 等其他 Python 框架
- WebSocket 支持有限（复杂场景建议用 Socket.IO）
- ORM 推荐 SQLAlchemy 2.0 async，不覆盖 Tortoise/Peewee 等替代方案
- 部署建议配合 Uvicorn + Gunicorn，不覆盖 Docker/K8s 编排

## 相关参考（Playbook）

本子技能落地"FastAPI 异步后端"，跨栈方法论见下列 `references/`（按需读取）：

- 后端深度 playbook（FastAPI / 异步 / 依赖注入 / 踩坑速查）：[references/backend-playbook.md](../../references/backend-playbook.md)
- AI-native 全栈工作流（契约优先 → 前后端并行联调）：[references/fullstack-workflow.md](../../references/fullstack-workflow.md)