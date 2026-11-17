# AssetHub 路由挂载总览

> **v1.6.0 更新（2026-07-19）**：基于自动化扫描（`server.js route mounts + recursive regex scan`），后端当前共有 **1709 端点 / 97 模块**。完整目录快照见 `references/api-catalog-2026-07-19/`。
>
> 来源：`backend/server.js` 路由挂载 + `backend/modules/*/routes/*`。本文件汇总所有路由前缀与对应文件，便于定位端点源码、排查行为不一致、新增端点同步文档。
>
> 凡是发现本表与实际后端行为不一致，**以 `backend/server.js` 与路由文件源码为准**，并同步更新本文档。

---

## 1. 直接挂载（顶级路由）

| 前缀 | 文件 |
|------|------|
| `/api/roles-permissions` | `backend/routes/roles-permissions.js` |
| `/api/enhanced-permissions` | `backend/routes/enhanced-permissions.js` |
| `/api/system-config` | `backend/routes/system-config.js` |
| `/api/tenants` | `backend/routes/tenants.js` |
| `/api/tenant-access-url` | `backend/routes/tenant-access-url.js` |
| `/api/tenant-association` | `backend/routes/tenant-association.js` |
| `/api/tenant-module-config` | `backend/routes/tenant-module-config.js` |
| `/api/modules` | `backend/routes/modules.js` |
| `/api/module-configs` | `backend/routes/module-configs.js` |
| `/api/audit-logs` | `backend/routes/audit-logs.js` |
| `/api/audit-logs-enhanced` | `backend/routes/audit-logs-enhanced.js` |
| `/api/backup` | `backend/routes/backup.js` |
| `/api/workflow` | `backend/routes/workflow.js` |
| `/api/i18n` | `backend/routes/i18n.routes.js` |
| `/api/api-documentation` | `backend/routes/api-documentation.js` |
| `/api/agent-mesh` | `backend/routes/agent-mesh.js` |
| `/api/dashboard` | `backend/routes/dashboard.js` |
| `/api/dashboard-configs` | `backend/routes/dashboard-configs.js` |
| `/api/desktop-preferences` | `backend/routes/desktop-preferences.js` |
| `/api/page-views` | `backend/routes/page-views.js` |
| `/api/analysis` | `backend/routes/analysis.js` |
| `/api/wx-cloud` | `backend/routes/wx-cloud.js` |
| `/api/menus` | `backend/routes/menus.js` |
| `/api/maintenance-ai` | `backend/routes/maintenance-ai.js` |
| `/api/maintenance` | `backend/routes/maintenance.js`（兼容入口）+ 子路由 `maintenance/*.router.js` |
| `/api/technical-documents` | `backend/routes/technical-documents.js` |
| `/api/technical-documents-enhanced` | `backend/routes/technical-documents-enhanced.js` |
| `/api/technical-documents-ai` | `backend/routes/technical-documents-ai.js` |
| `/api/asset-ai-analysis` | `backend/routes/asset-ai-analysis.js` |
| `/api/asset-images` | `backend/routes/asset-images.js` |
| `/api/asset-labels` | `backend/routes/asset-labels.js` |
| `/api/asset-location` | `backend/routes/asset-location.js` |
| `/api/asset-depreciation` | `backend/routes/asset-depreciation.js` |
| `/api/temp-assets` | `backend/routes/temp-assets.js` |
| `/api/barcode-scan` | `backend/routes/barcode-scan.js` |
| `/api/intelligent-alerts` | `backend/routes/intelligent-alerts.js` |
| `/api/idle` | `backend/routes/idle.js` |
| `/api/scrapping` | `backend/routes/scrapping.js` |
| `/api/transfer` | `backend/routes/transfer.js` |
| `/api/depreciation` | `backend/routes/depreciation.js` |
| `/api/inventory` | `backend/routes/inventory.js` |
| `/api/inventory-plans` | `backend/routes/inventory-plans.js` |
| `/api/inventory-tasks` | `backend/routes/inventory-tasks.js` |
| `/api/inventory-reports` | `backend/routes/inventory-reports.js` |
| `/api/inventory-discrepancies` | `backend/routes/inventory-discrepancies.js` |
| `/api/quality-control` | `backend/routes/quality-control.js` |
| `/api/quality` | `backend/routes/quality.js`（兼容，部分入口） |
| `/api/procurement` | `backend/routes/procurement.js` |
| `/api/acceptance` | `backend/routes/acceptance.js` |
| `/api/adverse-reaction` | `backend/routes/adverse-reaction.js` |
| `/api/adverse-events` | `backend/routes/adverse-events.js` |
| `/api/ai` | `backend/routes/ai.js` |
| `/api/ai-assistant` | `backend/routes/ai-assistant.js` |
| `/api/chat` | `backend/routes/ai.js`（alias） |
| `/api/materials` | `backend/routes/materials.js` |
| `/api/sms-verification` | `backend/routes/sms-verification.js` |
| `/api/cloud-sync` | `backend/routes/cloud-sync.js` |
| `/api/location-codes` | `backend/routes/location-codes.js` |
| `/api/location-alerts` | `backend/routes/location-alerts.js` |
| `/api/integration` | `backend/routes/integration.js` |
| `/api/integration-channels` | `backend/routes/integration-channels.js` |
| `/api/message-integration` | `backend/routes/message-integration.js` |
| `/api/feishu` | `backend/modules/feishu-binding/routes/index.js` |
| `/api/health` | `backend/routes/health.js` |
| `/api/circuit-breakers` | `backend/routes/circuit-breakers.js` |
| `/api/metrics` | `backend/routes/metrics.js` |

---

## 2. 模块挂载（按业务域组织）

### 2.1 用户管理

| 前缀 | 模块文件 |
|------|----------|
| `/api/users` | `backend/modules/user-management/routes/users.js` + `backend/routes/users.js` |

### 2.2 部门管理

| 前缀 | 模块文件 |
|------|----------|
| `/api/departments` | `backend/modules/department-management/routes/departments.js` |

### 2.3 资产管理

| 前缀 | 模块文件 |
|------|----------|
| `/api/assets` | `backend/routes/assets/index.js`（聚合）+ `asset.{mutation,query,category,statistics,share,transfer,import-export}.js` + `backend/modules/asset-management/routes/*.js` |

### 2.4 合规管理

| 前缀 | 模块文件 |
|------|----------|
| `/api/compliance` | `backend/routes/compliance/index.js` + `compliance/{maintenance-level,uptime-statistics,safety-inspection,special-equipment,staff-qualification}.js` + `backend/modules/compliance-management/routes/*` |
| `/api/safety-inspection` | safety 子模块 |
| `/api/special-equipment` | special 子模块 |
| `/api/staff` | 旧路径，主体已迁移至 `compliance/staff-qualification` 与 `staff-qualification` 模块 |
| `/api/uptime` | 旧路径，主体已迁移至 `compliance/uptime-statistics` 与 `uptime-management` 模块 |
| `/api/risk` | 旧路径，主体已迁移至 `asset-risk-management` |

### 2.5 IoT 与资产监测

| 前缀 | 模块文件 |
|------|----------|
| `/api/iot` | `backend/modules/iot-management/routes/*`（含 `asset-monitoring`、`environment-monitoring`、`zone-location`、`patient-volume`、`iot-devices`、`asset-location`）+ 子模块 `iot-asset-monitoring-management`、`iot-environment-monitoring-management`、`iot-geo-location-management`、`iot-zone-location-management` |
| `/api/iot-devices` | `backend/modules/iot-management/routes/iot-devices.js` |
| `/api/asset-location` | `backend/modules/iot-management/routes/asset-location.js` |

### 2.6 文档管理

| 前缀 | 模块文件 |
|------|----------|
| `/api/technical-documents` | `backend/modules/technical-documents/routes/*` |

### 2.7 维修与使用

| 前缀 | 模块文件 |
|------|----------|
| `/api/asset-usage` | `backend/modules/asset-usage-management/routes/*` |
| `/api/preventive-maintenance` | `backend/modules/preventive-maintenance-management/routes/*` |
| `/api/maintenance-management` | `backend/modules/maintenance-management/routes/*` |

### 2.8 质量与采购

| 前缀 | 模块文件 |
|------|----------|
| `/api/acceptance-management` | `backend/modules/acceptance-management/routes/*` |
| `/api/quality-assurance` | `backend/modules/quality-assurance-management/routes/*` |
| `/api/quality-common` | `backend/modules/quality-common/routes/*` |

### 2.9 AI 助手

| 前缀 | 模块文件 |
|------|----------|
| `/api/asset-ai-assistant` | `backend/modules/asset-ai-assistant/routes/*` |
| `/api/ct-maintenance-assistant-management` | `backend/modules/ct-maintenance-assistant-management/routes/*` |

### 2.10 集成

| 前缀 | 模块文件 |
|------|----------|
| `/api/tendering` | `backend/modules/tendering-management/routes/*` |
| `/api/dingtalk-binding` | `backend/modules/dingtalk-binding/routes/*` |
| `/api/wechat-binding` | `backend/modules/wechat-binding/routes/*` |

---

## 3. 端点总数（v1.6.0）

- 直接挂载路由：约 75+ 个前缀文件
- 模块挂载路由：约 35+ 个业务模块
- **总端点**：**1709 个**
- **覆盖模块数**：**97**

> 来源：自动化扫描（`server.js route mounts + recursive regex scan`），快照时间 2026-07-19T15:12:38.578Z。完整目录见 `references/api-catalog-2026-07-19/`。

---

## 4. 命名约定

### 4.1 路由命名

- 资源路由：`/api/<resource>`（如 `/api/assets`）
- 子资源路由：`/api/<resource>/:id/<verb>`（如 `/api/assets/:id/transfer-apply`）
- 批量操作：`/api/<resource>/batch-<verb>`（如 `/api/inventory-discrepancies/batch-handle`）
- 嵌套资源：`/api/<parent>/<parent_id>/<child>`（如 `/api/users/:id/roles`）

### 4.2 HTTP 方法语义

- `GET`：查询（幂等）
- `POST`：创建 / 触发动作
- `PUT`：整体更新
- `PATCH`：部分更新（部分端点使用）
- `DELETE`：删除

### 4.3 兼容路由与新路由

- 大量模块同时存在新/旧两套路由（如 `transfer` vs `assets/transfer-requests`）
- **优先使用新路由**，旧路由仅用于历史兼容
- 部分路由已标记 `410 GONE`（参见 `api-conventions.md` 第 9 节）

---

## 5. 路由与权限的对应

每个路由挂载的中间件决定了访问权限（参见 `middleware.md`）：

- `authenticate` —— 大多数 GET
- `authenticate + requireTenantId` —— 资产/维修写入
- `authenticate + requireSystemAdmin` —— 分类/角色/模块
- `authenticate + requireSuperAdmin` —— 数据库/备份
- `authenticate + authorize('xxx')` —— 单权限校验

---

## 6. 路由调试

### 6.1 helper 脚本（推荐）

```bash
# 列出所有模块
bash scripts/assethub_api.sh modules

# 查看某模块的端点
bash scripts/assethub_api.sh module assets
bash scripts/assethub_api.sh module maintenance
```

### 6.2 直接 curl

```bash
curl -sS "http://localhost:13579/api/assets?page=1&pageSize=20" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "X-Tenant-Id: <TENANT_ID>"
```

### 6.3 健康检查

```bash
# 服务存活
curl http://localhost:13579/alive

# 服务就绪
curl http://localhost:13579/ready

# 详细健康
curl http://localhost:13579/api/health/detailed
```

---

## 7. 路径变更日志（v1.7.0，重要！）

> **v1.7.0 变更**：v1.6.0 中列出的"路径变更日志"已被新扫描覆盖。
> 完整重定向表运行 `bash scripts/assethub_api.sh redirects` 获取。

### 7.1 v1.7.0 关键变更（2026-07-29）

| 旧路径 | 新路径 | 状态 |
|--------|--------|------|
| `/api/maintenance` (132 ops) | `/api/maintenance-management` (47 ops) | ⚠️ 旧路径仍存在但已弃用 |
| `/api/adverse-events` | `/api/adverse-reaction` | ✅ 已删除 |
| `/api/transfer` | `/api/asset-allocation` | ⚠️ 旧路径仍存在但已弃用 |
| `/api/assets/transfer-requests` | `/api/asset-allocation` | ⚠️ 旧路径已弃用 |
| `/api/compliance/special-equipment` | `/api/key-equipment` | ✅ 已删除 |
| `/api/compliance/staff-qualification` | `/api/staff` | ✅ 已删除 |
| `/api/compliance/uptime-statistics` | `/api/uptime` | ✅ 已删除 |
| `/api/compliance/safety-inspection` | `/api/safety-inspection` | ✅ 已删除 |
| `/api/iot-devices` | `/api/iot/devices` | ⚠️ 旧路径已迁移 |
| `/api/asset-location` | `/api/iot/locations` | ⚠️ 旧路径已迁移 |
| `/api/asset-images` | `/api/assets/images` | ⚠️ 旧路径已迁移 |
| `/api/asset-labels` | `/api/assets/labels` | ⚠️ 旧路径已迁移 |
| `/api/procurement` | `/api/tendering/procurement-requests` | ⚠️ 旧路径已迁移 |
| `/api/acceptance` | `/api/acceptance-management` | ⚠️ 旧路径已迁移 |
| `/api/ai`、`/api/chat`、`/api/asset-ai-analysis` | `/api/asset-ai-assistant` | ⚠️ 旧路径已弃用 |
| `/api/asset-depreciation` | `/api/depreciation` | ⚠️ 旧路径已迁移 |
| `/api/sms-verification` | (已删除) | ✅ 已删除 |

### 7.2 v1.6.0 历史变更（已不再参考，仅作记录）

| 旧路径 | 新路径 | 备注 |
|--------|--------|------|
| `/api/transfer` (v1.6.0 当时) | `/api/assets/transfer-requests` (v1.6.0 当时) | **v1.7.0 又改了一次** → 现在是 `/api/asset-allocation` |
| `/api/inventory` | `/api/inventory-plans` + `/api/inventory-tasks` + `/api/inventory-discrepancies` | 整体已弃用，改用 `/api/inspection/tasks` |
| `/api/preventive-maintenance` | `/api/maintenance-management` (v1.7.0) | 仍有效，`maintenance-management` 已包含 PM |

> **运维提示**：**永远以 v1.7.0 表为准**，不要相信 v1.6.0 的变更日志。

---

## 8. 参考来源

- `backend/server.js` —— 路由挂载入口
- `backend/routes/` —— 直接挂载路由
- `backend/modules/*/routes/` —— 模块路由
- `docs/API_全量接口说明_供AI读取.md` —— 运行时汇总