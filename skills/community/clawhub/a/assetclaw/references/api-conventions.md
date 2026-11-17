# AssetHub API 全局约定

> 本文件汇总 AssetHub 后端全局生效的请求/响应/安全约定。覆盖范围：`backend/server.js` 路由挂载、`backend/middleware/*` 中间件、错误处理与高危网关。
>
> 与 `auth-and-workflows.md` 互补：本文件侧重**协议层**（错误码、限流、高危网关、幂等、统一响应），后者侧重**会话层**（登录、租户、Idempotency-Key 实操）。

---

## 1. Base URL

- **业务接口前缀**：`/api`（开发示例：`http://localhost:5183/api`，内网示例：`http://localhost:13579/api`）
- **健康检查例外**：无 `/api` 前缀，根路径直接挂载
  - `GET /alive` —— 服务存活
  - `GET /ready` —— 服务就绪
  - `GET /health` —— 基础健康检查
  - `GET /health/detailed` —— 详细健康检查
  - `GET /api/circuit-breakers` —— 熔断器状态
  - `GET /api/metrics` —— Prometheus 指标
- **Skill 运行时优先读取环境变量** `ASSETHUB_API_URL`（helper 脚本已实现）

---

## 2. 认证方式

| 接口类型 | 认证方式 |
|----------|----------|
| 大多数业务接口 | `Authorization: Bearer <JWT>`，由 `authenticate` 中间件校验 |
| 登录/注册/刷新 Token | 公开，部分限流（见第 5 节） |
| IoT 设备上行 | 设备 Token + `X-IoT-Token` Header，**不使用** 用户 JWT |
| 公开分享链接 | `GET /api/assets/share/:token` 无需 JWT |
| 公开招标/供应商 | `/api/tendering/public/*` 无需 JWT |
| 飞书事件订阅 | `/api/feishu-binding/event`（公开 webhook） |

---

## 3. 租户上下文（多租户隔离）

### 3.1 普通用户

- 租户从 JWT 推断，无需额外头
- 所有查询自动带 `tenant_id` 行级过滤

### 3.2 `super_admin`

- 必须通过查询参数 `?tenant_id=<id>` 或请求头 `X-Tenant-Id: <id>` 显式指定租户（**v1.6.0 修正**：驼峰 tId，旧文档误写 `X-Tenant-ID`）
- 否则后端返回 `400 TENANT_REQUIRED`
- 业务查询前调用 `assethub_validate_tenant` 或 `GET /api/tenants/current/info`

### 3.3 写入端点

- 大多数挂载 `requireTenantId` 中间件，缺租户上下文直接返回 400
- 资产 CRUD 写入**必须** `requireTenantId`
- 资产查询接口仅 `authenticate`
- 分类 CRUD 仅 `requireSystemAdmin`（租户/角色/菜单管理）

---

## 4. 统一响应格式

```json
{
  "success": true,
  "data": { /* payload */ },
  "timestamp": "2026-04-02T10:00:00.000Z"
}
```

```json
{
  "success": false,
  "message": "错误信息（人类可读）",
  "code": "ERROR_CODE",
  "path": "/api/xxx",
  "method": "POST"
}
```

### 4.1 列表端点的两种形状

```json
// 形状 A：嵌套 pagination
{ "success": true, "data": { "list": [...], "total": 1234 }, "pagination": { "page": 1, "pageSize": 20 } }

// 形状 B：data 内嵌分页
{ "success": true, "data": { ...payload..., "pagination": { "page": 1, "pageSize": 20, "total": 1234 } } }
```

**客户端处理建议**：先尝试 `data.list`，再尝试 `data.records`，最后兜底 `data` 本身（视其为数组）。

### 4.2 高危网关响应（428）

```json
{
  "success": false,
  "code": "HIGH_RISK_CONFIRMATION_REQUIRED",
  "message": "该操作影响 N 条记录，需要显式确认",
  "data": {
    "action": "scrapping:approve",
    "target": { "id": "SR-2026-0007" },
    "hint": "请在确认后重试，并携带相同的 Idempotency-Key"
  }
}
```

---

## 5. 限流

| 限流器 | 触发端点 | 触发响应 |
|--------|----------|----------|
| `loginLimiter` | `/api/users/login`、`/api/users/refresh-token` | `429 RATE_LIMITED` |
| `registerLimiter` | `/api/users/register` | `429 RATE_LIMITED` |
| `apiLimiter` | 全局 API（每分钟请求数受环境变量控制） | `429 RATE_LIMITED` |

### 5.1 429 响应

```json
{ "success": false, "code": "RATE_LIMITED", "message": "请求过于频繁" }
```

### 5.2 处理建议

- 退避重试（指数回退 1s → 2s → 4s）
- helper 脚本登录命令失败时**不要**立即重试，等待 30–60 秒
- 工具描述中应注明冷却时间，便于模型降频

---

## 6. 高危操作网关（highRiskActionGate / high-risk-action-gate）

> **v1.6.0 升级**：网关现在采用双重保护。除原有的 `Idempotency-Key` 外，新增 `X-Risk-Confirm-Token` 请求头校验。
> 数据来源：`references/api-catalog-2026-07-19/API接口总览.md`（扫描时间 2026-07-19T15:12:38.578Z）。

### 6.1 触发条件

通过后端中间件对**破坏性/跨表写入**做二次确认：

- 删除（资产/工单/记录）
- 报废审批
- 资产转移
- 角色/权限变更
- 跨租户切换
- 备份恢复
- 合同/资产关联写入

### 6.2 触发响应

- HTTP 状态：**428 Precondition Required**
- 响应字段：`code: "HIGH_RISK_CONFIRMATION_REQUIRED"`、`data.action`、`data.target`、`data.hint`

### 6.3 客户端回放

1. 必须携带显式确认标记（环境变量 `ASSETHUB_HIGH_RISK_CONFIRM=YES` 或 body/header `confirm: true`）
2. **v1.6.0 新增**：请求头 `X-Risk-Confirm-Token: <token>`（由 helper 脚本自动生成）
3. 同一 `Idempotency-Key` **仅可重放一次**
4. helper 脚本已实现一次自动重放（需要显式开启环境变量）

### 6.4 维修申请安全入口（不走网关）

- `POST /api/maintenance/ai/submit-request` **不触发** `highRiskActionGate`
- AI / skill / MCP 提交的报修都走这个入口
- 提交后申请固定为 `待审批` 状态
- 仍需要 `Idempotency-Key` Header（防重复）

### 6.5 兜底策略

如果同一 `Idempotency-Key` 重放后仍返回 428：

- **停止自动化**
- 告诉用户：查询 API 仍可用，写入必须到 Web 管理后台走人工审批

---

## 7. 审计日志

### 7.1 触发

- `auditLogger(action, resource)` 中间件记录关键写操作
- 覆盖：创建/更新/删除/审批/转移/报废

### 7.2 查询端点

- `GET /api/audit-logs` —— 列表（分页/过滤）
- `GET /api/audit-logs/:id` —— 详情
- `GET /api/audit-logs/stats` —— 统计
- `GET /api/audit-logs-enhanced` —— 增强查询（多维过滤、导出）

### 7.3 数据写入位置

- `audit_logs` 表（行级带 `tenant_id`）
- 字段：`user_id`、`action`、`resource`、`resource_id`、`payload`、`created_at`

---

## 8. 缓存与幂等

### 8.1 服务端缓存

- 列表/统计接口**默认无服务端缓存**
- OpenClaw skill 端建议本地缓存以下低频变更数据：
  - `permission_definitions`（5 分钟）
  - `roles`、`modules`（5 分钟）
  - `categories/tree`（5 分钟）
  - 仪表盘数据（30–60 秒）
  - 资产详情/状态机（≤ 30 秒）

### 8.2 客户端幂等

- **所有写操作必须携带 `Idempotency-Key` Header**
- 推荐 UUID v4 或 `op-$(date +%s)-$RANDOM`（长度 ≤ 128）
- 跨重试保持**同一 Idempotency-Key + 同一 Body**，避免重复创建
- helper 脚本自动添加 Idempotency-Key 到所有写操作

### 8.3 不同负载**不要**复用同一 Idempotency-Key

---

## 9. HTTP 状态码速查

| 状态 | 含义 | 响应 `code` | 处理 |
|------|------|------------|------|
| 200 | 成功 | — | 解析 `data` |
| 400 | 参数错误 / 缺租户 | `VALIDATION_ERROR` / `TENANT_REQUIRED` | 补全字段；不要盲重试 |
| 401 | 缺/失效 JWT | `UNAUTHORIZED` | 删除会话文件 → 重新登录 |
| 403 | 权限不足 / 跨租户 | `FORBIDDEN` / `requireSystemAdmin` 失败 | 确认权限；停止写操作 |
| 404 | 资源/路径不存在 | `NOT_FOUND` | 回查确认 ID |
| 409 | 唯一键冲突（`asset_code`、`username` 等） | `CONFLICT` | 重新查询，选用新编码 |
| 410 | 资源已废弃（旧路由下线） | `GONE` | 改用新路径 |
| 422 | 业务规则不满足（状态机非法流转） | `UNPROCESSABLE_ENTITY` | 检查 `status` |
| 428 | **高危操作需二次确认** | `HIGH_RISK_CONFIRMATION_REQUIRED` | 见第 6 节 |
| 429 | 限流触发 | `RATE_LIMITED` | 退避重试 |
| 500 | 服务内部异常 | `INTERNAL_ERROR` | 保留上下文，稍后重试 |
| 503 | 数据库不可用 / 熔断 | `SERVICE_UNAVAILABLE` | 等待恢复后重试 |

---

## 10. 数据库连接

- **不硬编码**任何连接字符串
- 统一读取 `backend/.env`（参见 `project_rules.md`）
- 数据库名（默认）：`zcgl`
- 连接测试端点：`POST /api/system-config/database/test`（`requireSuperAdmin`）

---

## 11. 文件上传约定

仅以下端点使用 `multipart/form-data`，文件字段必须为 `file`：

- `POST /api/assets/import`（导入资产）
- `POST /api/acceptance-management/records/:id/files`（验收文件）
- `POST /api/technical-documents/...`（技术资料多个上传端点）
- `POST /api/maintenance-management/workorders/:id/materials`（工单物料，视实现）
- `POST /api/procurement/:id/files`（采购附件）

**Content-Type**：`multipart/form-data`
**最大尺寸**：通常 ≤ 50 MB（视具体中间件配置）

---

## 12. 流式响应（SSE）

以下 AI 端点可能返回 SSE：

- `POST /api/ai/chat/completions`
- `POST /api/ai-assistant/stream`
- `POST /api/maintenance-ai/analyze`

**响应头**：`Content-Type: text/event-stream`
**字段**：增量 `delta`（OpenAI 兼容格式）

OpenClaw skill 实现时需用流式解析器累积 `delta` 字段。

---

## 13. 公共响应最佳实践

- 优先从 `data` 取业务数据，从顶层取 `success`、`code`、`message`
- 分页信息统一从 `pagination` 或 `data.pagination` 取
- 时间字段默认 ISO8601（含时区）
- 金额字段保留 2 位小数（Decimal）

---

## 14. 参考来源

- `backend/server.js` —— 路由挂载入口
- `backend/middleware/auth.js` —— JWT 校验
- `backend/middleware/tenant.js` —— 多租户隔离
- `backend/middleware/roles.js` —— 角色权限
- `backend/middleware/risk.js` —— 高危网关
- `backend/middleware/audit.js` —— 审计日志
- `backend/middleware/rateLimit.js` —— 限流
- `backend/middleware/upload.js` —— 文件上传 + fileSecurity
- `docs/API_全量接口说明_供AI读取.md` —— 运行时汇总