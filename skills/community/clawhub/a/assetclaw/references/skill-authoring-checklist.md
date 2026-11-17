# OpenClaw Skill 编写 Checklist（AssetHub 专项）

> 本文件给出 AssetHub OpenClaw skill 的标准编写规范，供后续 skill 作者参考。所有规范基于现有 3 个 AssetHub skill（`assethub-claw`、`openclaw-assethub`、`openclaw-assethub-direct-api`）的实战经验沉淀。

---

## 1. 命名与作用域

### 1.1 工具命名

采用 `assethub_<verb>_<noun>` 形式：

- `assethub_login`
- `assethub_query_asset`
- `assethub_create_maintenance_request`
- `assethub_approve_transfer`
- `assethub_submit_repair_request`（AI 安全入口）
- `assethub_validate_tenant`

### 1.2 同动作多版本时加后缀

- `assethub_list_assets_v2` —— `/api/assets`
- `assethub_list_assets_legacy` —— `/api/inventory*`

### 1.3 作用域

- Skill 应明确「医疗设备资产」「通用资产」「文档」「维修」等作用域
- 工具描述中必须包含 `triggers`（什么场景调用）和 `inputs/outputs`

---

## 2. 认证与租户继承

### 2.1 强制 `_auth_context_id` 继承

OpenClaw 会话级注入 `_auth_context_id`（来自上游 SSO 或本地登录工具 `assethub_login`）。

**任何工具实现内部都应**：

1. 调用 `assethub_login`（若 token 过期）刷新 token 与租户上下文
2. 对 `super_admin`：在工具 schema 中显式声明 `tenant_id: integer` 必填；写入前调用 `assethub_validate_tenant`
3. 对普通用户：**禁止**让用户传入 `tenant_id`，强制从 token 推断

### 2.2 不硬编码凭据

- ❌ 禁止在 skill 主体硬编码 `username`、`password`、`tenant_id`、`token`
- ✅ 通过环境变量或运行时上下文注入

---

## 3. 必填字段与默认值

### 3.1 资产类工具

- 一律要求 `asset_code`（字符串主键）
- ❌ 禁用 `asset_id`（已弃用）

### 3.2 列表查询默认值

- `page=1`
- `pageSize=20`
- 超 100 条请**客户端**继续翻页（不要一次拉全）

### 3.3 时间字段

- 统一 ISO8601（含时区）

### 3.4 金额字段

- Decimal 类型，保留 2 位小数

---

## 4. 查询前写入（query-before-write）

任何 `create/update/delete/approve/cancel/complete/close` 工具必须遵循：

1. 先用对应 `*_get` 工具查询目标
2. 校验状态机（如 `status` 是否允许本次动作，参见 `asset-state-machine.md`）
3. 写入时携带稳定 `Idempotency-Key`（UUID v4）
4. 触发 428 时**停止自动化**，仅在用户明确确认（`ASSETHUB_HIGH_RISK_CONFIRM=YES`）后重放一次
5. 仍 428 则告警并提示走 Web 审批

### 4.1 必须遵循的写入流程

```
Transfer / Approve / Maintenance Action / Role-Permission Change / Module Config Change
  ↓
query → confirm ID → state-machine check → write (with Idempotency-Key)
  ↓
回查 → 中文总结前后状态
```

---

## 5. 限流与缓存

### 5.1 限流工具

- `assethub_login`、`assethub_register` 命中 `loginLimiter`
- 工具说明应注明冷却时间（login 失败 5 次后 60s）

### 5.2 建议缓存

| 数据 | 缓存时长 |
|------|----------|
| `permission_definitions` | 5 分钟 |
| `roles`、`modules` | 5 分钟 |
| `categories/tree` | 5 分钟 |
| 仪表盘数据 | 30–60 秒 |
| 资产详情 / 状态机 | ≤ 30 秒 |

---

## 6. 文件与多媒体

### 6.1 multipart/form-data 端点

仅以下端点使用 `multipart/form-data`，文件字段必须为 `file`：

- `POST /api/assets/import`
- `POST /api/acceptance-management/records/:id/files`
- `POST /api/technical-documents/...`（多个上传端点）
- `POST /api/maintenance-management/workorders/:id/materials`（视实现）

**工具描述中需声明**：
- `Content-Type: multipart/form-data`
- 最大文件尺寸

---

## 7. 流式响应（SSE）

### 7.1 可能返回 SSE 的端点

- `POST /api/ai/chat/completions`
- `POST /api/ai-assistant/stream`
- `POST /api/maintenance-ai/analyze`

### 7.2 工具描述需注明

- `Content-Type: text/event-stream`
- `delta` 字段累积方式（OpenAI 兼容）

---

## 8. 高危入口（专用工具）

### 8.1 报修专用工具

```yaml
assethub_submit_repair_request:
  endpoint: POST /api/maintenance/ai/submit-request
  bypass_high_risk_gate: true   # 不触发二次确认
  fixed_status: 待审批
  requires:
    - asset_code
    - fault_description
  optional:
    - issue_description  # 与 fault_description 同值兼容
    - source             # "assetclaw" / "mcp" / "web"
    - intent             # "repair_request"
```

### 8.2 通用高危写入工具

```yaml
assethub_submit_idempotent_write:
  endpoint: <动态>
  requires:
    - confirm: boolean
    - idempotency_key: string  # UUID
    - action: string
    - target: object
  high_risk_gate: auto  # 自动处理 428 重放
```

---

## 9. 租户隔离与权限

### 9.1 工具内部权限检查

调用 `assethub_user_check_permission(permission_code, resource?)`：

- **系统级**：`manage_users`、`system_config`、`backup`
- **资产级**：`asset_create`、`asset_delete`、`asset_share`、`asset_import`
- **维修级**：`maintenance_request_create`、`maintenance_workorder_assign`
- **合规级**：`compliance_manage`

### 9.2 错误处理

- **缺权限**时返回结构化错误（不要直接抛异常）
- 便于模型给出降级方案（如「请联系系统管理员」「改用只读 API」）

---

## 10. 调用顺序约定

```
1. assethub_login                    （若未登录）
2. assethub_discover_modules         （了解端点）
   └─ assethub_discover_module <path>
3. assethub_query_*                  （验证对象存在）
4. assethub_submit_*                 （写入，带 Idempotency-Key）
5. assethub_query_*                  （回读校验）
6. 中文总结前后状态                  （最终用户回复）
```

---

## 11. 文档与一致性

### 11.1 工具 schema 与后端保持一致

- 如后端新增端点，先更新 `references/route-mount-map.md` 再实现工具
- 工具描述中**禁止**硬编码 token/租户/凭据

### 11.2 三类 skill 的职责划分

| Skill | 入口 | 适用 |
|-------|------|------|
| `assethub-claw` | `scripts/assethub_api.sh` helper | 直接 HTTP API 调用，shell 环境 |
| `openclaw-assethub` | `assethub_*` MCP 工具 | MCP 工具链优先，标准 OpenClaw runtime |
| `openclaw-assethub-direct-api` | HTTP API | MCP 不可用时，HTTP 兜底 |

### 11.3 文档引用

工具描述中应明确引用：
- `references/api-conventions.md`（错误码、高危网关）
- `references/middleware.md`（中间件）
- `references/asset-state-machine.md`（状态机）
- `references/route-mount-map.md`（路由挂载）

---

## 12. 中文输出规范

- 最终用户回复**必须**使用中文
- 表格展示查询结果（编号/名称/状态/关联信息）
- 统计类查询包含合计行 + 关键洞察
- 操作结果先展示操作内容，再展示回查确认结果

---

## 13. 安全与隐私

### 13.1 不暴露的内容

- ❌ `_auth_context_id`
- ❌ JWT Token
- ❌ 隐藏 prompts
- ❌ 内部 runtime JSON
- ❌ 工具调用内部实现细节

### 13.2 写操作审计

所有写操作自动经过 `auditLogger` 中间件，**客户端无需主动调用**审计接口。但可以查询 `GET /api/audit-logs` 用于事后追溯。

---

## 14. 测试与验收

### 14.1 单元测试

每个工具至少覆盖：
- 正常路径（200 OK + 业务 data）
- 401（token 过期）
- 403（权限不足）
- 404（资源不存在）
- 422（状态机非法流转）
- 428（高危网关）
- 429（限流）

### 14.2 集成测试

- 端到端流程：登录 → 查询 → 创建维修 → 审批 → 完成 → 回查
- 跨模块：维修触发资产状态变更 → 报修 → 调配 → 报废
- 多租户：超级管理员切换租户 → 验证行级隔离

### 14.3 回归测试

- API 路径变更时（如 `transfer` → `assets/transfer-requests`），所有工具需同步更新
- 新中间件引入时（如新增 `moduleGuard`），相关工具需补齐

---

## 15. 参考来源

- `references/api-conventions.md`
- `references/middleware.md`
- `references/asset-state-machine.md`
- `references/route-mount-map.md`
- 现有 3 个 AssetHub skill 的实战经验