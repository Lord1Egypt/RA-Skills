# AssetHub 资产管理系统 — API 接口总览（面向 OpenClaw）

> ⚠️ **快照时间**：2026-07-19T15:12:38.578Z
> 数据来源：server.js route mounts + recursive regex scan of route files
> 后端服务端口：**5183** ｜ Base URL：**http://localhost:5183/api**
> 接口总数：**1709** ｜ 模块数：**97**

## 一、通用调用约定

### 1. 认证（Bearer Token）

所有接口（除 `GET /api/health`、`/api/alive`、`/api/ready` 等健康检查外）均需在请求头携带 JWT：

| Header | 说明 | 示例 |
|--------|------|------|
| `Authorization` | Bearer 令牌 | `Bearer eyJhbGciOiJIUzI1Ni... ` |
| `X-Tenant-Id` | 租户隔离标识（多租户必填） | `999001` |
| `Content-Type` | 请求体格式 | `application/json` |

> ⚠️ **租户 Header 名称**：官方规格使用 `X-Tenant-Id`（驼峰 tId）；旧文档误写为 `X-Tenant-ID`（全大写 ID），部分客户端/代理对大小写敏感，请以小写 `Id` 为准。

### 2. 统一响应结构

```json
{
  "success": true,
  "message": "操作成功",
  "data": { },
  "pagination": { "page": 1, "pageSize": 20, "total": 100, "totalPages": 5 }
}
```

### 3. 基础 curl 模板

```bash
curl -X <METHOD> "http://localhost:5183/api/<module>/<path>" \
  -H "Authorization: Bearer <JWT>" \
  -H "X-Tenant-Id: <TENANT_ID>" \
  -H "Content-Type: application/json" \
  -d '{ <json-body> }'
```

### 4. 高风险接口网关（high-risk-action-gate）

对写入类接口（POST/PUT/PATCH/DELETE，且路径命中资产/合同等前缀，或含审批关键字），除鉴权外还需：

- 请求头 `Idempotency-Key: <uuid>`（幂等防重）
- 二次确认头 `X-Risk-Confirm-Token: <token>`

> 注：纯只读型辅助 POST（如 AI 识别、计量报告分析）已被网关豁免，无需带 `Idempotency-Key`。

---

## 二、模块清单（97 个，按字母排序）

```
/api                                /api/agent-mesh
/api/acceptance                     /api/ai
/api/acceptance-management          /api/ai-assistant
/api/adverse-reaction               /api/analysis
/api/api-documentation              /api/asset-ai-analysis
/api/asset-ai-assistant             /api/asset-allocation
/api/asset-depreciation             /api/asset-images
/api/asset-labels                   /api/asset-location
/api/asset-usage                    /api/assets
/api/assets/statistics              /api/audit-logs
/api/backup                         /api/barcode-scan
/api/chat                           /api/cloud-sync
/api/compliance                     /api/contracts
/api/dashboard                      /api/dashboard-configs
/api/departments                    /api/desktop-preferences
/api/depreciation                   /api/emergency-allocation
/api/enhanced-permissions           /api/event-reminder
/api/feishu                         /api/finance
/api/form-customization             /api/i18n
/api/idle                           /api/in-app-notifications
/api/inspection                     /api/intelligent-alerts
/api/inventory                      /api/inventory-discrepancies
/api/inventory-plans                /api/inventory-reports
/api/inventory-tasks                /api/iot
/api/iot-devices                    /api/knowledge-base
/api/large-equipment                /api/location-alerts
/api/location-codes                 /api/maintenance
/api/maintenance-management         /api/maintenance-temporary
/api/maintenance/ai                 /api/materials
/api/metrology                      /api/module-configs
/api/modules                        /api/notification-preferences
/api/notifications                  /api/page-views
/api/pdca                           /api/poct-quality-control
/api/preventive-maintenance         /api/quality-assurance
/api/quality-control                /api/recipient-strategies
/api/risk                           /api/roles-permissions
/api/safety-inspection              /api/scrapping
/api/sms-verification               /api/spare-parts
/api/special-equipment              /api/staff
/api/supplier                       /api/system-config
/api/technical-documents            /api/technical-documents/ai
/api/technical-documents/enhanced   /api/temp-assets
/api/tenant-access-url              /api/tenant-association
/api/tenant-module-config           /api/tenant-role-config
/api/tenants                        /api/tendering
/api/transfer                       /api/uptime
/api/users                          /api/warranty
/api/wechat-mp                      /api/workflow
/api/wx-cloud
```

---

## 三、模块端点数（Top 30，按规模）

| 排名 | 模块 | 端点数 |
|------|------|--------|
| 1 | `/api/compliance` | 37 |
| 1 | `/api/acceptance-management` | 37 |
| 3 | `/api/assets` | 31 |
| 4 | `/api/adverse-reaction` | 28 |
| 4 | `/api/contracts` | 27 |
| 6 | `/api/inventory-tasks` | 21 |
| 7 | `/api/acceptance` | 20 |
| 8 | `/api/depreciation` | 19 |
| 9 | `/api/users` | 17+（含用户认证/审批/角色申请等） |
| 10 | `/api/asset-depreciation` | 16 |
| 11 | `/api/maintenance` | 15+ |
| 12 | `/api/inventory-plans` | 15 |
| 13 | `/api/iot-devices` | 14 |
| 14 | `/api/asset-location` | 13 |
| 14 | `/api` | 13 |
| 16 | `/api/inventory-reports` | 13 |
| 17 | `/api/asset-labels` | 12 |
| 18 | `/api/agent-mesh` | 10 |
| 18 | `/api/asset-ai-analysis` | 10 |
| 20 | `/api/asset-ai-assistant` | 9 |
| 20 | `/api/asset-usage` | 9 |
| 20 | `/api/asset-allocation` | 9 |
| 23 | `/api/audit-logs` | 9 |
| 24 | `/api/intelligent-alerts` | 9 |
| 25 | `/api/inventory` | 8 |
| 25 | `/api/inventory-discrepancies` | 8 |
| 27 | `/api/cloud-sync` | 7 |
| 28 | `/api/warranty` | 7 |
| 29 | `/api/backup` | 6 |
| 30 | `/api/feishu` | 6 |

> 完整模块端点清单见 `api-catalog.json`（按模块分组）。

---

## 四、典型端点示例（按业务域）

### 4.1 健康检查（公开）

```bash
curl -X GET "http://localhost:5183/api/health"
curl -X GET "http://localhost:5183/api/alive"
curl -X GET "http://localhost:5183/api/ready"
curl -X GET "http://localhost:5183/api/metrics"
```

### 4.2 资产核心

```bash
# 列表（分页）
curl -X GET "http://localhost:5183/api/assets?page=1&pageSize=20" \
  -H "Authorization: Bearer <JWT>" -H "X-Tenant-Id: <TENANT_ID>"

# 详情
curl -X GET "http://localhost:5183/api/assets/{id}" \
  -H "Authorization: Bearer <JWT>" -H "X-Tenant-Id: <TENANT_ID>"

# 创建
curl -X POST "http://localhost:5183/api/assets" \
  -H "Authorization: Bearer <JWT>" -H "X-Tenant-Id: <TENANT_ID>" \
  -H "Content-Type: application/json" \
  -d '{ "asset_name": "...", "category_id": 1, ... }'

# 统计
curl -X GET "http://localhost:5183/api/assets/statistics/overview" \
  -H "Authorization: Bearer <JWT>" -H "X-Tenant-Id: <TENANT_ID>"
```

### 4.3 维修（AI 安全入口 vs 普通入口）

```bash
# AI 安全入口（推荐，不触发 high-risk 网关）
curl -X POST "http://localhost:5183/api/maintenance/ai/submit-request" \
  -H "Authorization: Bearer <JWT>" -H "X-Tenant-Id: <TENANT_ID>" \
  -H "Idempotency-Key: $(uuidgen)" \
  -H "Content-Type: application/json" \
  -d '{ "asset_code": "ASSET-001", "fault_description": "..." }'

# 普通入口（触发二次确认网关）
curl -X POST "http://localhost:5183/api/maintenance-management/requests" \
  -H "Authorization: Bearer <JWT>" -H "X-Tenant-Id: <TENANT_ID>" \
  -H "Idempotency-Key: $(uuidgen)" \
  -H "X-Risk-Confirm-Token: <token>" \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

### 4.4 仪表盘

```bash
curl -X GET "http://localhost:5183/api/dashboard" \
  -H "Authorization: Bearer <JWT>" -H "X-Tenant-Id: <TENANT_ID>"
```

---

## 五、变更摘要（vs v1.5.9 / 2026-04-22）

| 类别 | v1.5.9 | v1.6.0（本次） |
|------|--------|---------------|
| 端点总数 | ~688 | **1709** |
| 模块数 | 60+ | **97** |
| 租户 Header | `X-Tenant-ID`（旧） | `X-Tenant-Id`（**官方**） |
| 高危网关 | 仅 `Idempotency-Key` | `Idempotency-Key` + `X-Risk-Confirm-Token` 双重 |
| 文档来源 | 人工维护 | 自动化扫描（route mounts + regex scan） |
| 新模块 | — | acceptance-management, agent-mesh, asset-ai-analysis, asset-ai-assistant, contracts, dashboard-configs, feishu, finance, inspection, intelligent-alerts, knowledge-base, large-equipment, maintenance-management, maintenance-temporary, metrology, pdca, poct-quality-control, quality-assurance, recipient-strategies, safety-inspection, spare-parts, special-equipment, staff, supplier, tendering, warranty, wechat-mp, wx-cloud 等 |

---

## 六、参考来源

- `backend/server.js` —— 路由挂载入口
- `backend/routes/*` + `backend/modules/*/routes/*`
- 自动化扫描脚本输出（route mounts + recursive regex scan）
- 生成时间：2026-07-19T15:12:38.578Z
