# AssetHub 模块概览（101 模块 / 1,809 ops，v1.7.0）

> **v1.7.0 升级（2026-07-29）**：模块数从 97 升级到 **101**，端点数从 1,709 升级到 **1,809 ops / 1,381 paths**。
>
> 数据来源：`backend/docs/swagger.json` (2.60 MB / 1,381 paths / 1,809 operations) 2026-07-29 同步扫描，`backend/docs/api-catalog.json` (312 KB / 1,777 endpoints / 101 modules)。
>
> 本文件按 **15 业务域** 分组列出所有 101 模块，每个模块给出**入口前缀 / 典型端点数量 / 核心场景**。
>
> 完整端点矩阵：
> - 静态快照：`references/api-catalog-2026-07-29/`（含 API 接口总览 + 端点目录）
> - 动态生成：`bash scripts/assethub_api.sh modules / module <path> / domains / stats / redirects`

---

## 关键路径消歧（v1.7.0 必须看）

| 业务 | ✅ 新路径 | ❌ 已弃用路径 |
|------|----------|--------------|
| 维修 | `/api/maintenance-management/*` | `/api/maintenance/*`（已迁移，132 ops 但已弃用） |
| 不良事件 | `/api/adverse-reaction/*` | `/api/adverse-events/*`（已删除） |
| 资产调拨 | `/api/asset-allocation/*` | `/api/transfer/*`（已弃用）/ `/api/assets/transfer-requests`（已弃用） |
| 重点设备 | `/api/key-equipment/*` | `/api/compliance/special-equipment/*`（已删除） |
| 员工资质 | `/api/staff/*` | `/api/compliance/staff-qualification/*`（已删除） |
| 开机率 | `/api/uptime/*` | `/api/compliance/uptime-statistics/*`（已删除） |
| 安全检查 | `/api/safety-inspection/*` | `/api/compliance/safety-inspection/*`（已删除） |
| IoT 设备 | `/api/iot/devices/*` | `/api/iot-devices/*`（已迁移） |
| IoT 位置 | `/api/iot/locations/*` | `/api/asset-location/*`（已迁移） |
| 资产图片 | `/api/assets/images/*` | `/api/asset-images/*`（已迁移） |
| 资产标签 | `/api/assets/labels/*` | `/api/asset-labels/*`（已迁移） |
| 采购申请 | `/api/tendering/procurement-requests` | `/api/procurement/*`（已迁移） |
| 验收 | `/api/acceptance-management/*` | `/api/acceptance/*`（已迁移） |
| AI 助手 | `/api/asset-ai-assistant/*` | `/api/ai/*` `/api/chat/*` `/api/asset-ai-analysis/*`（已弃用） |
| 折旧 | `/api/depreciation/*` | `/api/asset-depreciation/*`（已迁移） |

> **新规则**：调用任何接口前先 `bash scripts/assethub_api.sh redirects` 看完整映射表。脚本会自动警告用错路径（stderr）。

---

## 1. 核心资产（12 模块 / 136 ops）

### 1.1 资产管理 `/api/assets`（核心）

- **端点数量**：36 ops
- **核心场景**：资产 CRUD、查询、统计、导入/导出、变更日志、状态流转
- **关键端点**：
  - `GET /api/assets` —— 列表（分页/过滤）
  - `GET /api/assets/all` —— 全量（无分页）
  - `POST /api/assets` —— 创建（需 `Idempotency-Key`，可能 428）
  - `GET /api/assets/{id}` —— 详情（ID 或 asset_code）
  - `PUT /api/assets/{id}` —— 更新（高风险）
  - `DELETE /api/assets/{id}` —— 删除（高风险，必 428）
  - `GET /api/assets/statistics` —— 统计概览
  - `POST /api/assets/import` —— 导入（multipart）
  - `GET /api/assets/export` —— 导出（Excel）

### 1.2 调拨 `/api/asset-allocation`（新路径）

- **端点数量**：9 ops
- **关键端点**：
  - `POST /api/asset-allocation/transfer-apply` —— 提交调拨（需 `Idempotency-Key`）
  - `POST /api/asset-allocation/transfer-requests/{id}/approve` —— 审批（高风险，必 428）
  - `POST /api/asset-allocation/transfer-requests/{id}/reject` —— 驳回（高风险，必 428）

### 1.3 报废 `/api/scrapping`

- **端点数量**：14 ops
- **核心场景**：报废申请、审批、处置

### 1.4 闲置 `/api/idle`

- **端点数量**：11 ops
- **核心场景**：闲置资产发布、再利用申请

### 1.5 资产使用 `/api/asset-usage`

- **端点数量**：9 ops
- **核心场景**：使用量追踪、科室使用率

### 1.6 资产标签 `/api/assets/labels`、`资产图片 /api/assets/images`、`条码扫描 /api/barcode-scan`

- **端点数量**：13 + 5 + 5 ops
- **核心场景**：标签模板/批量生成、图片上传、扫码盘点

### 1.7 临时资产 `/api/temp-assets`、`位置编码 /api/location-codes`、`云同步 /api/cloud-sync`（已弃用）

---

## 2. 维修与保养（7 模块 / 261 ops）

> **v1.7.0 重要**：`maintenance` 模块虽还有 132 ops（最大），但已标注 ⚠️ 弃用。新代码**必须**用 `/api/maintenance-management/*`。

### 2.1 维修管理（新）`/api/maintenance-management`

- **端点数量**：47 ops
- **核心场景**：工单/审批/费用/派工/完工
- **关键端点**：
  - `GET /api/maintenance-management/work-orders?status=in_progress` —— 工单列表
  - `GET /api/maintenance-management/requests?status=pending` —— 申请列表
  - `POST /api/maintenance-management/requests` —— 手动提交申请（需 `Idempotency-Key`，可能 428）
  - `POST /api/maintenance-management/work-orders/{id}/dispatch` —— 派工（高风险）
  - `POST /api/maintenance-management/work-orders/{id}/complete` —— 完工（高风险，可能 428）

### 2.2 维修管理（旧，已弃用）`/api/maintenance` ⚠️

- **端点数量**：132 ops（最大但已迁移）
- **保留原因**：历史兼容，**新建 skill 不要引用**
- **AI 安全入口（推荐）**：`POST /api/maintenance/ai/submit-request`（白名单免 428）

### 2.3 保修 `/api/warranty`

- **端点数量**：41 ops
- **核心场景**：保修期管理、索赔、保修策略

### 2.4 日常保养 `/api/daily-maintenance`

- **端点数量**：18 ops
- **核心场景**：日常巡检维护记录

### 2.5 维修成本 `/api/maintenance-cost`

- **端点数量**：11 ops
- **核心场景**：维修费用统计、成本分析

### 2.6 预防性维护 `/api/preventive-maintenance`

- **端点数量**：6 ops
- **核心场景**：设备预防性维护计划（PM）

### 2.7 临时维修 `/api/maintenance-temporary`（已弃用）

---

## 3. 采购/合同/供应商（4 模块 / 276 ops）

### 3.1 招标采购 `/api/tendering`（新路径）

- **端点数量**：169 ops（最大业务域）
- **核心场景**：招标项目、投标、合同、预算
- **关键端点**：
  - `GET /api/tendering/projects?status=in_progress` —— 项目列表
  - `GET /api/tendering/procurement-requests?status=pending` —— 采购申请列表
  - `POST /api/tendering/procurement-requests` —— 创建采购申请（需 `Idempotency-Key`）

### 3.2 供应商 `/api/supplier`

- **端点数量**：62 ops
- **核心场景**：资质、评价、管理
- **关键端点**：
  - `GET /api/supplier?keyword=西门子&status=active`

### 3.3 合同管理 `/api/contracts`

- **端点数量**：27 ops
- **核心场景**：资产/维修/配件合同
- **关键端点**：合同 CRUD、到期提醒、付款记录

### 3.4 采购 `/api/procurement`（已弃用）

- **端点数量**：18 ops
- **替代路径**：`/api/tendering/procurement-requests`

---

## 4. 质量管理（5 模块 / 112 ops）

### 4.1 质量控制 `/api/quality-control`

- **端点数量**：32 ops
- **关键端点**：
  - `GET /api/quality-control/records?department=检验科`

### 4.2 POCT 质控 `/api/poct-quality-control`

- **端点数量**：28 ops
- **关键端点**：
  - `GET /api/poct-quality-control/records?date=2026-07-29`

### 4.3 不良事件 `/api/adverse-reaction`（新路径）

- **端点数量**：28 ops
- **关键端点**：
  - `GET /api/adverse-reaction?status=pending`
  - `POST /api/adverse-reaction` —— 上报不良事件（需 `Idempotency-Key`，可能 428）

### 4.4 质量保证 `/api/quality-assurance`

- **端点数量**：21 ops

### 4.5 计量 `/api/metrology`

- **端点数量**：3 ops
- **核心场景**：器具、校准、检定

---

## 5. 巡检/合规/安全（7 模块 / 204 ops）

### 5.1 巡检 `/api/inspection`

- **端点数量**：47 ops
- **关键端点**：
  - `GET /api/inspection/tasks?status=pending`
  - `GET /api/inspection/issues?status=open`

### 5.2 员工资质 `/api/staff`（新路径）

- **端点数量**：52 ops
- **替代路径**：`/api/compliance/staff-qualification`（已删除）

### 5.3 合规 `/api/compliance`

- **端点数量**：25 ops
- **核心场景**：合规检查、报告

### 5.4 风险评估 `/api/risk`

- **端点数量**：25 ops

### 5.5 重点设备 `/api/key-equipment`（新路径）

- **端点数量**：24 ops
- **替代路径**：`/api/compliance/special-equipment`（已删除）

### 5.6 开机率 `/api/uptime`（新路径）

- **端点数量**：18 ops
- **替代路径**：`/api/compliance/uptime-statistics`（已删除）

### 5.7 安全检查 `/api/safety-inspection`（新路径）

- **端点数量**：13 ops
- **替代路径**：`/api/compliance/safety-inspection`（已删除）

---

## 6. 设备/备件/技术资料（8 模块 / 216 ops）

### 6.1 技术文档 `/api/technical-documents`

- **端点数量**：64 ops
- **核心场景**：上传、解析、AI 问答

### 6.2 IoT `/api/iot`（新路径）

- **端点数量**：56 ops
- **关键端点**：
  - `GET /api/iot/devices?status=online`
  - `GET /api/iot/locations?asset_id=123`
  - `POST /api/iot/locations/ingest` —— IoT 位置上报（需 IoT token）

### 6.3 大型设备 `/api/large-equipment`

- **端点数量**：29 ops

### 6.4 备件库 `/api/spare-parts`

- **端点数量**：27 ops
- **关键端点**：入库、出库、统计

### 6.5 知识库 `/api/knowledge-base`

- **端点数量**：19 ops
- **核心场景**：CRUD、AI 问答

### 6.6 IoT 设备（已弃用）`/api/iot-devices` ⚠️、位置编码 `/api/location-codes`、位置预警 `/api/location-alerts`

---

## 7. 验收/事件/PDCA（6 模块 / 138 ops）

### 7.1 验收管理 `/api/acceptance-management`（新路径）

- **端点数量**：39 ops
- **关键端点**：
  - `GET /api/acceptance-management/applications?status=pending`
  - `POST /api/acceptance-management/applications` —— 提交验收（需 `Idempotency-Key`）

### 7.2 PDCA `/api/pdca`

- **端点数量**：30 ops

### 7.3 验收（已弃用）`/api/acceptance` ⚠️

- **端点数量**：20 ops
- **替代路径**：`/api/acceptance-management/*`

### 7.4 事件提醒 `/api/event-reminder`

- **端点数量**：20 ops

### 7.5 应急调配 `/api/emergency-allocation`

- **端点数量**：20 ops

### 7.6 表单定制 `/api/form-customization`

- **端点数量**：9 ops

---

## 8. 用户/权限/组织（12 模块 / 143 ops）

### 8.1 用户 `/api/users`

- **端点数量**：27 ops
- **关键端点**：
  - `POST /api/users/login` —— 登录
  - `GET /api/users/me` —— 当前用户
  - `GET /api/users?status=active&role=department_admin`

### 8.2 模块配置 `/api/module-configs`

- **端点数量**：22 ops

### 8.3 角色权限 `/api/roles-permissions`

- **端点数量**：19 ops
- **关键端点**：角色、按钮、菜单
- **写操作**：高风险（角色变更）

### 8.4 模块列表 `/api/modules`

- **端点数量**：16 ops

### 8.5 增强权限 `/api/enhanced-permissions`

- **端点数量**：12 ops

### 8.6 部门 `/api/departments`

- **端点数量**：8 ops

### 8.7 菜单 `/api/menus`、`租户 `/api/tenants`、`租户模块配置`、`租户角色配置`、`租户访问 URL`、`租户关联`

---

## 9. 财务/折旧（2 模块 / 32 ops）

### 9.1 折旧 `/api/depreciation`（新路径）

- **端点数量**：17 ops
- **核心场景**：折旧计算与统计

### 9.2 财务 `/api/finance`

- **端点数量**：15 ops

---

## 10. 通知/消息（5 模块 / 58 ops）

### 10.1 通知 `/api/notifications`

- **端点数量**：17 ops

### 10.2 智能预警 `/api/intelligent-alerts`

- **端点数量**：14 ops

### 10.3 站内消息 `/api/in-app-notifications`

- **端点数量**：12 ops
- **关键端点**：`GET /api/in-app-notifications?status=unread`

### 10.4 收件人策略 `/api/recipient-strategies`

- **端点数量**：8 ops

### 10.5 通知偏好 `/api/notification-preferences`

- **端点数量**：7 ops

---

## 11. 工作流/审计/分析（11 模块 / 72 ops）

### 11.1 工作流 `/api/workflow`

- **端点数量**：19 ops

### 11.2 智能体网络 `/api/agent-mesh`

- **端点数量**：10 ops

### 11.3 审计日志 `/api/audit-logs`

- **端点数量**：9 ops
- **关键端点**：`GET /api/audit-logs?user_id=&start_date=&end_date=`

### 11.4 仪表盘配置 `/api/dashboard-configs`、备份 `/api/backup`、桌面偏好 `/api/desktop-preferences`、国际化 `/api/i18n`、API 文档 `/api/api-documentation`、分析 `/api/analysis`、仪表盘 `/api/dashboard`、页面访问 `/api/page-views`

---

## 12. AI 智能（5 模块 / 31 ops）

### 12.1 资产 AI 助手 `/api/asset-ai-assistant`（新路径，**推荐**）

- **端点数量**：9 ops
- **关键端点**：
  - `POST /api/asset-ai-assistant/chat` —— body: {message, session_id}
  - `POST /api/asset-ai-assistant/asset-query` —— body: {natural_language_query}

### 12.2 其它 AI 模块（已弃用）⚠️

- `asset-ai-analysis` (8 ops) → 用 `asset-ai-assistant`
- `chat` (6 ops) → 用 `asset-ai-assistant`
- `ai-assistant` (5 ops) → 用 `asset-ai-assistant`
- `ai` (3 ops) → 用 `asset-ai-assistant`

---

## 13. 第三方集成（4 模块 / 35 ops）

### 13.1 飞书 `/api/feishu`

- **端点数量**：12 ops
- **关键端点**：
  - `GET /api/feishu/bindings` —— 创建/查询绑定
  - `POST /api/feishu/send` —— 发送通知（需先 bindings）

### 13.2 微信公众号 `/api/wechat-mp`

- **端点数量**：12 ops

### 13.3 微信云 `/api/wx-cloud`

- **端点数量**：8 ops

### 13.4 短信验证 `/api/sms-verification`（已删除）

---

## 14. 认证/系统（6 模块 / 18 ops）

### 14.1 健康检查 `/api/health`（免认证）

### 14.2 认证 `/api/auth`、`熔断器 /api/circuit-breakers`、就绪 `/api/ready`、存活 `/api/alive`、指标 `/api/metrics`

---

## 15. 已弃用/迁移（7 模块 / 64 ops，**勿引用**）

> 这些模块已在 v1.7.0 标注 ⚠️，**新建 skill 不要引用**。
> helper 脚本会自动检测旧路径并警告（stderr）。

- `inventory` (18 ops) → 用 `/api/inspection/tasks`
- `materials` (11 ops) → 用 `/api/spare-parts`
- `inventory-tasks/plans/reports/discrepancies` → 用 `/api/inspection/*`
- `sms-verification` (3 ops) → 已删除

---

## 📋 业务域速查表（一张图）

| # | 业务域 | 模块数 | ops | 主入口路径 |
|---|--------|------:|----:|----------|
| 1 | 核心资产 | 12 | 136 | `/api/assets`, `/api/asset-allocation` |
| 2 | 维修与保养 | 7 | 261 | `/api/maintenance-management`, `/api/warranty` |
| 3 | 采购/合同/供应商 | 4 | 276 | `/api/tendering`, `/api/supplier`, `/api/contracts` |
| 4 | 质量管理 | 5 | 112 | `/api/quality-control`, `/api/poct-quality-control` |
| 5 | 巡检/合规/安全 | 7 | 204 | `/api/inspection`, `/api/key-equipment` |
| 6 | 设备/备件/技术资料 | 8 | 216 | `/api/iot`, `/api/technical-documents` |
| 7 | 验收/事件/PDCA | 6 | 138 | `/api/acceptance-management` |
| 8 | 用户/权限/组织 | 12 | 143 | `/api/users`, `/api/roles-permissions` |
| 9 | 财务/折旧 | 2 | 32 | `/api/depreciation`, `/api/finance` |
| 10 | 通知/消息 | 5 | 58 | `/api/notifications`, `/api/in-app-notifications` |
| 11 | 工作流/审计/分析 | 11 | 72 | `/api/workflow`, `/api/audit-logs` |
| 12 | AI 智能 | 5 | 31 | `/api/asset-ai-assistant` |
| 13 | 第三方集成 | 4 | 35 | `/api/feishu`, `/api/wechat-mp` |
| 14 | 认证/系统 | 6 | 18 | `/api/health`, `/api/auth` |
| 15 | 已弃用/迁移 | 7 | 64 | ⚠️ 勿引用 |
| **合计** | **15** | **101** | **1,809** | — |