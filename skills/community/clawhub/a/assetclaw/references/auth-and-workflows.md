# AssetClaw - 认证与工作流参考（v1.7.0）

> 本文件侧重**会话层**（登录、租户、Idempotency-Key、Query-before-Write 实操）。
> 协议层（错误码、限流、高危网关、幂等、上传、SSE）见 `api-conventions.md`。
> 路由层（中间件链、挂载表）见 `middleware.md` 和 `route-mount-map.md`。
> 速查层（Top 40 API）见 `endpoint-quick-ref.md`。

---

## 0. 升级要点（v1.7.0，2026-07-29）

- 接口覆盖从 **97 模块 / 1,709 端点** 升级到 **101 模块 / 1,809 ops**（基于 `backend/docs/swagger.json` 2026-07-29 同步扫描）
- helper 脚本 `scripts/assethub_api.sh` 增量升级：
  - 新增 `domains / stats / redirects` 三个命令（无需后端连接即可看 15 业务域分组）
  - 新增旧路径 → 新路径 自动警告（stderr 输出，不中断）
  - 新增 `ASSETHUB_IOT_TOKEN` / `ASSETHUB_IDEMPOTENCY_KEY` / `ASSETHUB_HIGH_RISK_CONFIRM` 三个环境变量
  - **默认行为变更**：检测到 428 高风险时**不再静默自动重放**，需 `ASSETHUB_HIGH_RISK_CONFIRM=YES` 才重放（v1.6.0 默认自动重放）
- 加入 15 业务域分组（取代旧的"按子域平铺"），见 `api-modules-overview.md`

---

## 1. Base URL

| 部署形态 | URL |
|---------|-----|
| **本地默认** | `http://localhost:13579/api` |
| 内网（v1.6.0 旧默认） | `http://160ttth72797.vicp.fun/api` |
| Skill 运行时 | 优先读 `ASSETHUB_API_URL` 环境变量 |

> **端口说明**：v1.6.0 之前默认 5,174；v1.6.0 起合并到 **13,579 单端口前后端部署**。新文档提到 5,183 是开发期端口，本机以 13,579 为准。

---

## 2. 登录

### Endpoint

```
POST /api/users/login
```

### Request（v1.7.0 推荐带 tenant_code）

```json
{
  "tenant_code": "可选,企业编码（super_admin 跨企业登录时建议带）",
  "username": "your-user",
  "password": "your-password"
}
```

> **v1.6.0 简化路径**：只传 `username + password` 也能登录，租户从返回的 `data.user.tenant_id` 取。

### Response - 必缓存字段

| 字段 | 说明 |
|------|------|
| `data.token` | JWT Bearer Token |
| `data.user.tenant_id` | 当前租户 ID |
| `data.user.username` | 用户名 |
| `data.user.real_name` | 真实姓名 |
| `data.user.role` | 角色 |
| `data.enterprises` | 企业列表（super_admin / 多企业用户可用 `set-tenant` 切换） |

### Helper 登录命令

```bash
# 优先用环境变量
export ASSETHUB_API_USERNAME=leejia
export ASSETHUB_API_PASSWORD=***
bash scripts/assethub_api.sh login

# 没设环境变量 → 临时凭证文件 /tmp/assethub-claw-temp-session.json
# （Web 调用 OpenClaw 时，凭证会写入该文件，登录时自动读取）

# 多企业用户切换
bash scripts/assethub_api.sh set-tenant <序号>   # 查看列表: 不带参数运行
```

---

## 3. 通用请求头

```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
X-Tenant-Id: <tenant_id>        # v1.6.0 驼峰 tId，仅超级管理员跨租户时需要
Idempotency-Key: <stable_key>   # 所有写操作必填（防重复提交）
```

> **⚠️ Header 大小写**：v1.6.0 已确认官方使用 **`X-Tenant-Id`**（驼峰 tId，全小写 id），Express 中间件对大小写敏感。
> v1.5.9 文档误写 `X-Tenant-ID`（全大写 ID），**不要**再用。
>
> 新 v2 文档（`/Volumes/移动硬盘（500）/AssetHub/docs/skill-drafts/openclaw-assethub-api-v2/`）使用 `X-Tenant-ID`（全大写 ID），但实际后端 Express 校验的是驼峰，**以本机实测为准**。

---

## 4. 高风险操作限制（v1.7.0 重要变更）

### 4.1 Idempotency-Key（所有写操作必填）

- Header：`Idempotency-Key: <唯一键>`
- 默认由 helper 自动生成：`op-$(date +%s)-$RANDOM`（长度 ≤ 128）
- **v1.7.0 新增**：可显式注入 `export ASSETHUB_IDEMPOTENCY_KEY="$(uuidgen)"`，保证重试幂等
- **不要**对不同 payload 用同一个 key，否则报 `409 IDEMPOTENCY_CONFLICT`

### 4.2 二次风险确认（普通端点 vs AI 入口）

| 入口 | 是否需要 428 二次确认 | 备注 |
|------|---------------------|------|
| `POST /api/maintenance/ai/submit-request` | **否**（白名单） | AI / 技能报修推荐入口 |
| 其它写端点（资产/调拨/采购/报废/验收/角色等） | **是** | 第一次返回 428 + confirmToken，第二次带 `X-Risk-Confirm-Token` 重放 |

#### 第一次请求（v1.7.0 默认行为变更）

```bash
curl -X DELETE http://localhost:13579/api/assets/123 \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Tenant-Id: $TENANT" \
  -H "Idempotency-Key: $(uuidgen)"
```

返回：
```json
{
  "success": false,
  "code": "HIGH_RISK_CONFIRMATION_REQUIRED",
  "message": "高风险操作需要二次确认后才能执行",
  "requiresConfirmation": true,
  "actionId": "hra_xxx",
  "confirmToken": "<confirm_token>",
  "confirmTokenHeader": "X-Risk-Confirm-Token",
  "idempotencyHeader": "Idempotency-Key",
  "expiresInMs": 300000
}
```

#### 第二次请求（用户已确认后）

```bash
ASSETHUB_HIGH_RISK_CONFIRM=YES \
ASSETHUB_IDEMPOTENCY_KEY="$(uuidgen)" \
bash scripts/assethub_api.sh request DELETE /assets/123
```

或 raw curl：
```bash
curl -X DELETE http://localhost:13579/api/assets/123 \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Tenant-Id: $TENANT" \
  -H "Idempotency-Key: <同第一次的 key>" \
  -H "X-Risk-Confirm-Token: <confirm_token>"
```

#### 规则

- `Idempotency-Key` 必须跟第一次**相同**
- body / query 完全相同
- `X-Risk-Confirm-Token` 用响应里的 `confirmToken`
- `confirmToken` 5 分钟内有效（`expiresInMs: 300000`）
- **v1.7.0 默认不自动重放**（v1.6.0 默认会自动重放；新行为更安全）
- **第二次仍返回 428** → **停止自动化**，告诉用户：
  - 查询 API 仍正常可用
  - 该写操作必须走 Web 管理后台审批，或管理员开 API 写权限

### 4.3 报修推荐路径：AI 安全入口（绕过二次确认）

- 使用 `POST /api/maintenance/ai/submit-request`
- 适用于 skill / MCP / Web AI 的报修创建
- **仍需要 Idempotency-Key Header**（自动由 helper 脚本添加）
- 该入口不需要二次风险确认，一次请求完成
- 成功后仍然进入 `待审批`
- 审批 / 开始 / 完成 仍沿用 `/api/maintenance/requests/{id}/...`

### 4.4 IoT 特殊流程（v1.7.0 新增）

设备/网关 ingest 路径**不**用普通 user JWT，改用 IoT token：

```bash
export ASSETHUB_IOT_TOKEN=<从 /api/iot/tokens 签发>
curl -X POST http://localhost:13579/api/iot/locations/ingest \
  -H "Authorization: Bearer $ASSETHUB_IOT_TOKEN" \
  -H "Content-Type: application/json" \
  --data-binary '{
    "device_id": "GW-001",
    "asset_code": "ZC-2024-001",
    "lat": 41.80, "lng": 123.43,
    "timestamp": "2026-07-29T10:00:00Z"
  }'
```

> helper 脚本会自动检测 `*/iot/*` 路径并切换 `Authorization` header 为 IoT token（其它路径继续用 user JWT）。

---

## 5. 租户规则

| 用户类型 | 默认行为 | 跨租户 |
|---------|---------|--------|
| 普通用户 | `data.user.tenant_id`，**不要**切换 | **不允许**切 `X-Tenant-Id` |
| 部门管理员 | `data.user.tenant_id`，只能看自己部门 | 仅本部门 |
| `super_admin` | **必须显式** `X-Tenant-Id`，否则只返回平台级数据 | 通过 `X-Tenant-Id` 切换 |
| 多企业用户 | 登录时从 `data.enterprises` 选 | `set-tenant <序号>` 切换 |

### super_admin 行为细节

- **不指定租户时**：只返回平台级数据（模块配置、系统设置等），**不会**返回租户数据
- **指定租户时**：返回该租户的全部数据，跟普通用户一致
- **super_admin 写操作**：必须显式 `X-Tenant-Id`，否则可能被拒绝

### Web 上下文租户继承

- **Web 应用调用 OpenClaw 时会传递租户 ID**，**必须使用传入的租户 ID**，禁止切换到其他租户
- 当 OpenClaw 收到 `openclaw_login_username` / `openclaw_login_password` / `tenant_id` 时，立即同步到 `/tmp/assethub-claw-temp-session.json`，helper 优先读这个临时凭证
- Web 上下文中的密码可能被掩码显示（如 `Cmu19801008...`），**三个点 `...` 不是密码的一部分**，真实密码为 `Cmu19801008`

---

## 6. 标准响应解析

```json
// 成功
{ "success": true, "data": { ... }, "timestamp": "..." }

// 失败
{ "success": false, "message": "错误信息", "code": "BAD_REQUEST" }
```

列表数据可能出现在:
- `data`
- `data.list`
- `data.records`

分页信息可能出现在:
- `pagination`（顶层）
- `data.pagination`（嵌套）

**判断成功**：`success === true`，不是 `code === 200` 或 `status === 200`。

---

## 7. 错误码速查（v1.7.0 完整版）

| HTTP | code | 含义 | 处理 |
|------|------|------|------|
| 400 | (任意) | 参数错误 / 缺 `Idempotency-Key` | 收集缺失字段，问用户 |
| 401 | (任意) | token 过期 / 无效 | helper 自动重登（v1.6.0 起） |
| 403 | (任意) | 权限不足 / 租户隔离 / 模块禁用 | 不要盲重试写操作 |
| 404 | (任意) | 目标不存在 | 重新 Query 确认 |
| 409 | `IDEMPOTENCY_CONFLICT` | 同一个 `Idempotency-Key` 已用过不同 payload | 换 key，**不要**改原 payload |
| 422 | (任意) | 语义错误（如资产编码重复） | 检查字段约束 |
| 428 | `HIGH_RISK_CONFIRMATION_REQUIRED` | 高风险，需二次确认 | 问用户 → 设置 `ASSETHUB_HIGH_RISK_CONFIRM=YES` 再调用 |
| 429 | (任意) | 限流 | 退避重试 |
| 500 | (任意) | 后端错误 | 保留请求上下文，稍后重试 |
| 502 / 503 | (任意) | 服务暂不可用 | 退避重试 |

---

## 8. Query-before-Write 模式

任何写操作前都必须：

```
1. Query 目标对象 → 确认 ID/状态
2. 用户确认（可选，但强烈建议）
3. 写（带 Idempotency-Key）
4. 若 428 → 用户显式确认 → 第二次带 X-Risk-Confirm-Token 重放
5. 若仍 428 → 停止自动化，告知用户走 Web 审批
6. Query 验证最终状态
7. 报告最终状态（不是只报告"成功"）
```

**典型场景**：资产删除、报废、调拨、维修派工/完工、角色变更、模块配置变更。

---

## 9. 自描述端点（运行时）

不要凭记忆或旧文档调用陌生接口，优先用：

```bash
# v1.7.0 新增：本地查 15 业务域
bash scripts/assethub_api.sh domains

# v1.7.0 新增：本地查旧路径 → 新路径 重定向
bash scripts/assethub_api.sh redirects

# v1.7.0 新增：运行时统计模块数
bash scripts/assethub_api.sh stats

# 列出全部 101 个模块（运行时）
bash scripts/assethub_api.sh modules

# 单模块详情（运行时）
bash scripts/assethub_api.sh module assets
bash scripts/assethub_api.sh module maintenance-management

# 完整 swagger spec（运行时）
# GET /api-docs.json          JSON
# GET /api-docs               Swagger UI（需 system_admin）
```

---

## 10. 注销

```bash
bash scripts/assethub_api.sh logout
# 删除会话缓存文件 + node 内存残留
```

---

## 11. 刷新 Token

```
POST /api/users/refresh-token
```

---

## 12. 获取当前用户

```
GET /api/users/me
```

---

## 13. 时区

- 数据库存储 UTC，API 返回本地时区（Asia/Shanghai，+08:00）
- 日期筛选 `start_date` / `end_date` 用 `YYYY-MM-DD` 即可，后端自动展开
- 时间戳用 ISO 8601：`2026-07-29T10:00:00+08:00`

---

## 14. 飞书 / 微信公众号 特殊流程（v1.7.0）

通知发送（`/api/feishu/send` `/api/wechat-mp/send`）需要：

1. 先调用 `/api/feishu/bindings` 或 `/api/wechat-mp/bindings` 创建绑定
2. 接收方用户扫码确认
3. 然后才能 send

详细见 `feishu` / `wechat-mp` 模块的 reference（运行时用 `bash scripts/assethub_api.sh module feishu` 查询）。