# 后端深度 Playbook

> 整合自 `api-design`、`backend-patterns`、`database-design`、`fastapi-python` 四份子技能。本文件是后端决策与落地的深层参考，按需读取。

## 1. API 设计（api-design）

### 风格选择

| 场景 | 推荐 | 理由 |
|------|------|------|
| 通用 CRUD、多端消费 | REST | 简单、生态成熟、缓存友好 |
| 强类型、复杂图、前端驱动取数 | GraphQL | 避免过度/欠获取，按需取字段 |
| 内部服务间高频调用、流式 | gRPC | 高性能、强契约、双向流 |

### 稳定性原则（REST）

- **名词复数**：`/users` `/orders`；避免 `/getUser` `/createOrder`。
- **HTTP 语义**：GET 查询 / POST 创建 / PUT 全量更新 / PATCH 部分更新 / DELETE 删除；不要全用 POST。
- **状态码精确**：200/201/400/401/403/404/409/500；不要全部 200 + 业务 code。
- **统一分页**：`?page=1&limit=20` + `Link` header；每端点保持一致。
- **错误可调试**：
  ```json
  { "error": { "code": "INVALID_EMAIL", "message": "邮箱格式不合法", "field": "email" } }
  ```
  不要返回 HTML 或裸文本。

### 版本与弃用

- 版本方案：URL 路径（`/v1/users`）最直观，header 最干净；**选定后全仓库一致**。
- 向后兼容优先于破坏性变更；必须破坏时：新版本 + 旧版本并行 + 明确弃用时间表 + `Deprecation` header。

### 文档驱动

- 用 OpenAPI 3.0 定义契约，自动生成文档与 Mock。起点见 [assets/openapi-spec-template.yaml](../assets/openapi-spec-template.yaml)。

## 2. 架构模式（backend-patterns）

### 分层

```
Controller → Service → Repository → DB
```
- **Repository Pattern**：数据访问抽象，替换 ORM/数据库不影响业务逻辑。
- **依赖注入**：DB session、认证、权限以依赖链注入，便于测试与替换。
- **Middleware Chain**：认证 / 日志 / 限流 / CORS 可插拔。

### 关键模式速查

| 模式 | 适用 | 收益 |
|------|------|------|
| Repository | 数据访问抽象 | 业务逻辑与存储解耦 |
| Middleware Chain | 请求管线 | 横切关注点可插拔 |
| CQRS | 读写负载差异大 | 读/写各自优化 |
| Circuit Breaker | 调用外部服务 | 防止级联故障 |
| Idempotency Key | 支付/订单接口 | 防止重复提交 |

### 安全加固（OWASP 视角）

- 输入验证（Pydantic / schema 校验）、SQL 注入防护（参数化查询，禁字符串拼接）、CORS 白名单、Rate Limiting、输出编码。
- 细节配合 `security-guardian` 做专项审计。

### 性能优化

- 消除 N+1（eager load / 批量查询）、连接池调优、响应压缩、读路径加缓存。
- 缓存聚焦应用层（进程内 / 短 TTL），Redis 集群运维不在本技能范围。

## 3. 数据库设计（database-design）

### Schema 检查清单

```
[ ] 主键：UUID vs SERIAL vs ULID（分布式用 UUID/ULID，自增用 SERIAL）
[ ] 时间戳：created_at / updated_at / deleted_at
[ ] 软删除 vs 硬删除（合规/可恢复选软删）
[ ] 外键：CASCADE / SET NULL / RESTRICT
[ ] 字段类型：TEXT vs VARCHAR、INT vs BIGINT、JSONB 合理使用
[ ] 枚举：DB enum vs 应用常量
[ ] 唯一约束：业务唯一键 + 唯一索引
[ ] 默认值：避免无意义 NULL
```

### 范式 vs 反范式

- OLTP 默认 3NF；读多写少、报表类可适度反范式（冗余字段、物化视图）换读性能。
- 不要为反范式而反范式——先定位真实瓶颈。

### 索引策略

- B-Tree 通用；GIN 用于 JSONB / 数组 / 全文；复合索引**最左前缀**匹配，顺序按区分度高的列在前。
- 覆盖索引避免回表；但过度索引拖慢写入，按真实查询模式建。
- 慢查询先用 `EXPLAIN (ANALYZE, BUFFERS)` 读执行计划，再决定加索引还是改写法。

### ORM 选型

| ORM | 生态 | 适用 |
|-----|------|------|
| Prisma | TS/JS 一等公民，迁移体验好 | Node 全栈、类型安全优先 |
| Drizzle | 轻量、SQL 亲近、类型强 | 想要手写感又不想裸 SQL |
| SQLAlchemy 2.0 async | Python 事实标准 | FastAPI 后端 |
| TypeORM | 老牌、装饰器风格 | 既有 TypeORM 项目维护 |

### 迁移管理

- 迁移文件版本化、可幂等、可回滚；大表变更走**零停机**（加列→双写→回填→切读→删旧）。
- 不替代 DBA 的生产环境调优。

## 4. FastAPI 开发（fastapi-python）

### 项目骨架

```
app/
├── main.py            # FastAPI app + lifespan
├── config.py          # pydantic-settings
├── models/            # SQLAlchemy models
├── schemas/           # Pydantic schemas
├── api/v1/            # 路由
├── services/          # 业务逻辑
├── dependencies.py    # 依赖注入
└── tests/
```

### 要点

- **异步**：`async def` 端点、`BackgroundTasks`、StreamingResponse。IO 密集（外部 API、文件）用 async 收益最大。
- **Pydantic 验证**：请求/响应模型分离，嵌套 Schema + 自定义 validator。
- **依赖注入**：DB session、当前用户、权限检查都走 `Depends`，利于测试 mock。
- **中间件**：CORS、请求日志、startup/shutdown 生命周期。
- **测试**：`TestClient` + pytest，异步用 `httpx.AsyncClient` + `anyio`；DB 用事务回滚或测试库。

### 工作流

```
项目初始化 → 模型设计(Pydantic→SQLAlchemy→迁移) → 路由开发(CRUD+DI+异常) → 中间件 → 测试
```

## 5. 高频踩坑速查

线上后端问题多数不是「不知道该怎么写」，而是**症状与根因错位**。下表按症状反查：

| 现象 | 根因 | 修法 |
|------|------|------|
| 本地正常，线上偶发 500，日志只有 ORM 异常栈 | 唯一键/外键冲突未映射成业务错误，异常直接冒泡 | service 层捕获完整性错误 → 409 + 业务 code（错误体格式见第 1 节） |
| 列表接口随数据量变慢，DB CPU 不高但查询数暴涨 | N+1：序列化时逐行懒加载关联对象 | 预加载（`selectinload` / `JOIN`）；测试里加 **SQL 查询数断言**防回归 |
| 建了索引，`EXPLAIN` 仍走全表扫 | 条件列被函数包裹或类型不匹配（`lower(email)=`、字符串比数字），索引失效 | 建表达式索引，或让参数类型与列类型严格一致 |
| 分页翻到深页越来越慢 | `OFFSET N` 需扫过并丢弃前 N 行 | 改 keyset/游标分页：`WHERE id < :last_id ORDER BY id DESC LIMIT n` |
| 客户端超时重试后出现重复订单 | POST 无幂等键，重试产生第二条记录 | `Idempotency-Key` + 唯一索引；重复请求返回首次结果 |
| 端点写了 `async def` 反而更慢 | 协程里调用同步阻塞 IO（`requests`、同步 ORM），阻塞事件循环 | 换 async 客户端；或退回 `def` 端点交线程池，或 `run_in_executor` |
| 迁移本地秒过、生产锁表 | 大表 `ALTER`/加非空默认列触发全表重写与长事务锁 | 拆成「加可空列 → 分批回填 → 加约束」；并设 `lock_timeout` |
| 改了响应模型但接口仍返回旧字段/多余字段 | 未声明 `response_model`，或直接返回 ORM 实例绕过序列化 | 显式声明 `response_model`，禁止直接返回 ORM 对象 |

### 诊断命令

```bash
# 读执行计划：判断索引是否真的被用上
psql -c "EXPLAIN (ANALYZE, BUFFERS) SELECT ...;"

# 找最慢语句（需启用 pg_stat_statements）
psql -c "SELECT mean_exec_time, calls, query FROM pg_stat_statements
         ORDER BY mean_exec_time DESC LIMIT 10;"

# 查长事务与阻塞——迁移锁表时的第一现场
psql -c "SELECT pid, state, wait_event_type, now()-xact_start AS age, query
         FROM pg_stat_activity WHERE state <> 'idle' ORDER BY age DESC;"
```

## 后端决策速查

- 新建 Python API → FastAPI + SQLAlchemy 2.0 async + Pydantic v2。
- 新建 Node API → Express + Repository + 依赖注入。
- 接口混乱 → 先按第 1 节统一契约与状态码。
- 慢查询 → 第 3 节索引 + EXPLAIN。
- 架构坏味 → 第 2 节分层与模式。

> 具体技能调用：设计接口 → [skills/api-design](../skills/api-design/SKILL.md)；架构重构 → [skills/backend-patterns](../skills/backend-patterns/SKILL.md)；Schema/索引 → [skills/database-design](../skills/database-design/SKILL.md)；FastAPI 落地 → [skills/fastapi-python](../skills/fastapi-python/SKILL.md)。
