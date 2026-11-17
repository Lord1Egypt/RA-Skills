# AssetHub 中间件速查

> 来源：`backend/middleware/*.js` 实际实现。本文件列出每个中间件的行为、典型触发场景、客户端应对方式。
>
> 阅读路径：先看「认证 & 租户」→ 再看「权限 & 角色」→ 最后看「业务增强」（上传/审计/限流/高危）。

---

## 1. 总览

| 中间件 | 来源文件 | 作用 |
|--------|----------|------|
| `authenticate` | `auth.js` | 校验 JWT，写入 `req.user` |
| `requireTenantId` | `tenant.js` | 强制租户上下文，缺则 400 |
| `requireSystemAdmin` | `roles.js` | 限定 `system_admin` 角色 |
| `requireSuperAdmin` | `roles.js` | 限定平台 `super_admin`（仅系统级） |
| `authorize(permission)` | `roles.js` | 单权限码校验 |
| `authorize([...])` | `roles.js` | 多权限码 OR 校验 |
| `auditLogger(action, resource)` | `audit.js` | 写入审计日志 |
| `highRiskActionGate` | `risk.js` | 二次确认（HTTP 428） |
| `apiLimiter` / `loginLimiter` / `registerLimiter` | `rateLimit.js` | 触发 429 |
| `upload.single(field)` | `upload.js` | multipart 单文件上传 |
| `fileSecurity()` | `upload.js` | 文件类型/大小校验 |
| `moduleGuard` | `moduleGuard.js` | 模块启用校验 |

---

## 2. 认证中间件

### `authenticate`

- 校验 `Authorization: Bearer <JWT>`
- 解析后写入 `req.user`（含 `user_id`、`tenant_id`、`role`、`permissions`）
- 失败响应：`401 UNAUTHORIZED`
- 大多数业务路由**必须**挂载此中间件

**公开端点（不挂载 authenticate）**：

- `POST /api/users/login`
- `POST /api/users/register`
- `POST /api/users/refresh-token`（部分）
- `GET /api/tendering/public/*`
- `GET /api/assets/share/:token`
- `/api/feishu-binding/event`（公开 webhook）
- `GET /alive` / `GET /ready` / `GET /health`

---

## 3. 租户中间件

### `requireTenantId`

- 强制请求携带租户上下文
- **触发场景**：资产 CRUD 写入、维修创建、采购申请等
- **缺失响应**：`400 TENANT_REQUIRED`
- **普通用户**：从 JWT 自动注入
- **`super_admin`**：必须显式传 `?tenant_id=` 或 `X-Tenant-Id`

---

## 4. 角色权限中间件

### `requireSystemAdmin`

- 限定当前用户角色 = `system_admin`
- 失败响应：`403 FORBIDDEN`
- **典型用途**：分类 CRUD、租户 CRUD、模块开关、菜单权限

### `requireSuperAdmin`

- 限定平台级 `super_admin`
- **典型用途**：数据库连接、备份恢复、跨租户数据迁移

### `authorize(permission)`

- 校验单个权限码（如 `asset.create`、`maintenance.approve`）
- 失败响应：`403 FORBIDDEN`

### `authorize([...])`

- 校验多个权限码，OR 关系
- 失败响应：`403 FORBIDDEN`

---

## 5. 业务增强中间件

### `auditLogger(action, resource)`

- 在请求完成后（成功或失败）写入审计日志
- **action 枚举示例**：
  - `asset.create` / `asset.update` / `asset.delete`
  - `maintenance.request.create` / `maintenance.request.approve`
  - `transfer.apply` / `transfer.approve`
  - `scrapping.apply` / `scrapping.approve`
- **resource 枚举示例**：`asset`、`maintenance_request`、`workorder`、`transfer`、`scrapping`、`role`、`user`
- 数据落表：`audit_logs`（行级 `tenant_id`）

### `highRiskActionGate`

- 见 `api-conventions.md` 第 6 节
- 触发条件：删除 / 报废审批 / 转移 / 跨租户写入
- 响应：`428 HIGH_RISK_CONFIRMATION_REQUIRED`
- 回放：必须带 `Idempotency-Key` + 确认标记

### `apiLimiter` / `loginLimiter` / `registerLimiter`

- 全局限流，每分钟请求数受环境变量配置
- 触发响应：`429 RATE_LIMITED`
- **典型冷却时间**：
  - login：失败 5 次后冷却 60 秒
  - register：失败 3 次后冷却 5 分钟
  - api：100 req/min（默认）

### `upload.single(field)`

- multipart/form-data 单文件上传
- **field 名约定**：`file`（绝大多数端点）
- 与 `fileSecurity()` 配合使用

### `fileSecurity()`

- 校验文件类型（白名单：pdf、doc、docx、xls、xlsx、png、jpg 等）
- 校验文件大小（默认 ≤ 50 MB）
- 文件名安全检查（防路径穿越）
- 失败响应：`400 VALIDATION_ERROR`

### `moduleGuard`

- 校验目标模块在当前租户**已启用**
- 触发条件：调用方传入 `?module=xxx` 或路由挂载时硬编码
- 失败响应：`403 MODULE_DISABLED`
- **典型场景**：招投标 `GET /api/tendering/projects` 需 `tendering` 模块启用

---

## 6. 中间件组合模式

### 6.1 普通用户写资产

```js
router.post('/assets',
  authenticate,        // 1. JWT 校验
  requireTenantId,     // 2. 强制租户
  authorize('asset.create'), // 3. 权限码校验
  auditLogger('asset.create', 'asset'), // 4. 审计
  highRiskActionGate,  // 5. 高危二次确认（仅删除时）
  upload.single('file'),  // 6. 可选文件上传
  fileSecurity(),
  handler
)
```

### 6.2 超级管理员跨租户

```js
router.get('/assets',
  authenticate,
  requireTenantId,  // super_admin 必须显式带 ?tenant_id=
  handler
)
```

### 6.3 公开端点（无认证）

```js
router.post('/users/login',
  loginLimiter,  // 仅限流
  handler
)
```

---

## 7. 客户端应对矩阵

| 中间件触发 | 客户端动作 |
|------------|-----------|
| `authenticate` 失败（401） | 删除会话文件，重新登录 |
| `requireTenantId` 失败（400） | 显式传 `?tenant_id=` 或 `X-Tenant-Id`（仅 super_admin） |
| `authorize` 失败（403） | 停止写操作，告知用户权限不足 |
| `requireSystemAdmin` 失败（403） | 提示「需要系统管理员角色」 |
| `requireSuperAdmin` 失败（403） | 提示「需要平台超级管理员」 |
| `auditLogger` | 客户端无感（仅记录） |
| `highRiskActionGate` 428 | 询问用户是否确认；如确认则带同一 Idempotency-Key + `ASSETHUB_HIGH_RISK_CONFIRM=YES` 重放一次；仍 428 则停止自动化 |
| `apiLimiter` 429 | 退避重试（指数回退） |
| `upload` 失败 | 检查 `Content-Type: multipart/form-data`、字段名 `file`、文件大小 |
| `fileSecurity` 失败 | 替换为白名单文件类型、压缩文件 |
| `moduleGuard` 失败 | 提示「模块未启用，需联系管理员」 |

---

## 8. 权限码速查（部分）

| 权限 | 说明 |
|------|------|
| `asset.view_all` | 查看所有资产 |
| `asset.create` | 创建资产 |
| `asset.edit` | 编辑资产 |
| `asset.delete` | 删除资产 |
| `asset.import` | 导入资产 |
| `asset.share` | 生成分享链接 |
| `maintenance.add` | 创建维修申请 |
| `maintenance.approve` | 审批维修 |
| `maintenance.execute` | 执行维修 |
| `inventory.view` | 查看盘点 |
| `inventory.execute` | 执行盘点 |
| `transfer.approve` | 审批调配 |
| `compliance.manage` | 管理合规 |
| `user.manage` | 管理用户 |
| `role.manage` | 管理角色权限 |
| `system.config` | 系统配置 |
| `backup.manage` | 备份恢复 |

> 完整权限列表：`GET /api/roles-permissions/permissions/list` 或 `permissions/definitions`

---

## 9. 参考来源

- `backend/middleware/auth.js`
- `backend/middleware/tenant.js`
- `backend/middleware/roles.js`
- `backend/middleware/audit.js`
- `backend/middleware/risk.js`
- `backend/middleware/rateLimit.js`
- `backend/middleware/upload.js`
- `backend/middleware/moduleGuard.js`