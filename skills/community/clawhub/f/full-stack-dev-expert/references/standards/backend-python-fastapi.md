# Python / FastAPI 编码规范（后端工程师实现必读）

适用：Python 3.11+ / FastAPI / Pydantic v2 / SQLAlchemy 2.x 或 SQLModel。

## 1. 工程结构

```
app/
├── main.py               # 应用工厂：路由挂载、中间件、异常处理器注册
├── core/                 # 配置（pydantic-settings）、安全、日志
├── api/v1/               # 路由层：只做依赖注入 + 校验 + 调 service
├── services/             # 业务层：业务规则与事务
├── models/               # ORM 模型
├── schemas/              # Pydantic 请求/响应模型（DTO）
├── deps/                 # 依赖注入（DB 会话、当前用户）
└── tests/
```

依赖方向：api → services → models；api 禁止直接 import models 做查询。

## 2. 类型与模型

- 全量类型注解；`mypy --strict`（或 pyright strict）无 ERROR。
- Pydantic 模型三分离：`XxxCreate`（请求）/ `XxxUpdate`（PATCH）/ `XxxRead`（响应）；
  响应模型显式 `response_model=`，防泄漏内部字段。
- ORM 模型与 Pydantic DTO 严格分离，转换用显式 `model_validate`/工厂方法。
- `BaseSettings` 管配置：环境变量覆盖默认值，启动时校验，缺失密钥快速失败。

## 3. 分层与依赖注入

- DB 会话用 `Depends(get_db)` 注入，请求级生命周期，用完自动关闭。
- 认证依赖 `Depends(get_current_user)` 组合权限检查；路由声明权限需求。
- Service 函数显式接收 `session` 参数，事务边界在 service
  （`with session.begin():` 或显式 commit/rollback）。

## 4. 异步纪律

- 路由函数统一 async；`async def` 内禁止阻塞调用（同步 DB 驱动、requests、time.sleep），
  阻塞库要么换异步版（httpx、asyncpg/SQLAlchemy async）要么 `run_in_threadpool`。
- SQLAlchemy 2.x async + asyncpg；连接池参数外置配置。
- CPU 密集任务走后台任务/任务队列，不在请求路径执行。

## 5. 错误处理

- 业务异常自定义 `BizError(code, message)`，全局 exception_handler 统一映射契约错误结构。
- 校验交给 Pydantic（422 由框架处理），自定义校验规则放 schema validator。
- 不捕获后 `pass`；不向客户端暴露 traceback（日志里留全栈）。

## 6. 测试与质量

- pytest + httpx `AsyncClient`：路由层集成测试走依赖注入覆盖（override get_db 用测试库），
  service 层单测覆盖业务规则；`pytest -q` 全过。
- 质量命令（提交前全过）：

```bash
ruff check app tests && ruff format --check app tests
mypy app
pytest -q
```

- 依赖锁文件（uv.lock / requirements.txt + hashes）提交；禁止装未登记包。
