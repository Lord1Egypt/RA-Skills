# OpenClaw AssetHub API 业务域速查表

> 基于 2026-07-29 同步的 `backend/docs/swagger.json`(1,381 paths / 1,809 operations)。
> 完整的程序化 API 列表见 `api-catalog.json`(本目录)。
> 本表只列**业务域**和每个域的**代表操作**(精选 5-8 个),不平铺所有 1,809 个 endpoint。

## 阅读指引

| 标记 | 含义 |
| --- | --- |
| `Method` | HTTP 方法 |
| `Path` | 完整路径(包含 `/api` 前缀,`{param}` 为路径参数) |
| `Summary` | 自动生成的占位摘要为 `查询 /xxx`,手写 JSDoc 才有真实摘要 |
| `✍️` | 有手写 JSDoc,描述较准确 |
| `🤖` | 自动 catalog 生成的占位文档(基于路由声明) |
| `⚠️` | **已弃用/迁移到新路径**,仅作历史兼容保留,新建 skill **不要**引用 |

## 关键路径消歧

| 业务 | ✅ 新路径 | ❌ 已弃用路径 |
| --- | --- | --- |
| 维修 | `/api/maintenance-management/*` | `/api/maintenance/*`(已迁移) |
| 不良事件 | `/api/adverse-reaction/*` | `/api/adverse-events/*`(已删除) |
| 资产调拨 | `/api/asset-allocation/*` | `/api/transfer/*` `/api/assets/transfer-requests`(已弃用) |
| 重点设备 | `/api/key-equipment/*` | `/api/compliance/special-equipment/*`(已删除) |
| 员工资质 | `/api/staff/*` | `/api/compliance/staff-qualification/*`(已删除) |
| 开机率 | `/api/uptime/*` | `/api/compliance/uptime-statistics/*`(已删除) |
| 安全检查 | `/api/safety-inspection/*` | `/api/compliance/safety-inspection/*`(已删除) |
| IoT 设备 | `/api/iot/devices/*` | `/api/iot-devices/*`(已迁移) |
| IoT 位置 | `/api/iot/locations/*` | `/api/asset-location/*`(已迁移) |
| 资产图片 | `/api/assets/images/*` | `/api/asset-images/*`(已迁移) |
| 资产标签 | `/api/assets/labels/*` | `/api/asset-labels/*`(已迁移) |
| 采购申请 | `/api/tendering/procurement-requests` | `/api/procurement/*`(已迁移) |
| 验收 | `/api/acceptance-management/*` | `/api/acceptance/*`(已迁移) |
| AI 助手 | `/api/asset-ai-assistant/*` | `/api/ai/*` `/api/chat/*`(已弃用) |

---

## 核心资产

**说明**:资产的全生命周期(列表/详情/创建/更新/调拨/报废/闲置/扫码/标签打印)。注:`/api/asset-allocation` 是新路径,`/api/transfer` 和 `/api/assets/transfer-requests` 已弃用。

### `assets` (36 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/assets` | 获取资产列表 | ✍️ |
| `GET` | `/api/assets` | 获取资产列表 | ✍️ |
| `GET` | `/assets/{id}` | 获取资产详情 | ✍️ |
| `GET` | `/assets/export` | 导出资产Excel | ✍️ |
| `GET` | `/api/assets/all` | 全量查询资产列表（不分页） | ✍️ |
| `GET` | `/api/assets/{id}` | 获取资产详情 | ✍️ |

### `asset-allocation` (9 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/asset-allocation` | 查询 /api/asset-allocation | 🤖 |
| `GET` | `/api/asset-allocation/{id}` | 查询 /api/asset-allocation/{id} | 🤖 |
| `GET` | `/api/asset-allocation/export` | 查询 /api/asset-allocation/export | 🤖 |
| `GET` | `/api/asset-allocation/statistics` | 查询 /api/asset-allocation/statistics | 🤖 |
| `PUT` | `/api/asset-allocation/{id}/reject` | 更新 /api/asset-allocation/{id}/reject | 🤖 |
| `PUT` | `/api/asset-allocation/{id}/approve` | 更新 /api/asset-allocation/{id}/approve | 🤖 |

### `transfer` (9 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/transfer` | 查询 /api/transfer | 🤖 |
| `GET` | `/api/transfer/{id}` | 查询 /api/transfer/{id} | 🤖 |
| `GET` | `/api/transfer/export` | 查询 /api/transfer/export | 🤖 |
| `GET` | `/api/transfer/statistics` | 查询 /api/transfer/statistics | 🤖 |
| `PUT` | `/api/transfer/{id}/reject` | 更新 /api/transfer/{id}/reject | 🤖 |
| `PUT` | `/api/transfer/{id}/approve` | 更新 /api/transfer/{id}/approve | 🤖 |

### `asset-usage` (9 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/asset-usage` | 查询 /api/asset-usage | 🤖 |
| `GET` | `/api/asset-usage/health` | 查询 /api/asset-usage/health | 🤖 |
| `GET` | `/api/asset-usage/records` | 查询 /api/asset-usage/records | 🤖 |
| `GET` | `/api/asset-usage/statistics` | 查询 /api/asset-usage/statistics | 🤖 |
| `GET` | `/api/asset-usage/records/{id}` | 查询 /api/asset-usage/records/{id} | 🤖 |
| `GET` | `/api/asset-usage/user/{userId}/records` | 查询 /api/asset-usage/user/{userId}/records | 🤖 |

### `idle` (11 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/idle` | 查询 /api/idle | 🤖 |
| `GET` | `/api/idle/{id}` | 查询 /api/idle/{id} | 🤖 |
| `GET` | `/api/idle/health` | 查询 /api/idle/health | 🤖 |
| `GET` | `/api/idle/statistics` | 查询 /api/idle/statistics | 🤖 |
| `DELETE` | `/api/idle/batch` | 删除 /api/idle/batch | 🤖 |
| `PUT` | `/api/idle/{id}/cancel` | 更新 /api/idle/{id}/cancel | 🤖 |

### `scrapping` (14 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/scrapping` | 查询 /api/scrapping | 🤖 |
| `GET` | `/api/scrapping/{id}` | 查询 /api/scrapping/{id} | 🤖 |
| `GET` | `/api/scrapping/stats` | 查询 /api/scrapping/stats | 🤖 |
| `GET` | `/api/scrapping/statistics/summary` | 查询 /api/scrapping/statistics/summary | 🤖 |
| `POST` | `/api/scrapping/{id}/files` | 创建/提交 /api/scrapping/{id}/files | 🤖 |
| `POST` | `/api/scrapping/{id}/reject` | 创建/提交 /api/scrapping/{id}/reject | 🤖 |

### `asset-images` (5 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/asset-images/asset-images` | 查询 /api/asset-images/asset-images | 🤖 |
| `GET` | `/api/asset-images/assets/{assetId}/images` | 查询 /api/asset-images/assets/{assetId}/images | 🤖 |
| `PUT` | `/api/asset-images/assets/images/{imageId}` | 更新 /api/asset-images/assets/images/{imageId} | 🤖 |

### `asset-labels` (13 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/asset-labels/templates` | 获取标签模板列表 | ✍️ |
| `GET` | `/api/asset-labels/print-queue` | 获取打印队列 | ✍️ |
| `GET` | `/api/asset-labels/templates/{id}` | 获取标签模板详情 | ✍️ |
| `GET` | `/api/asset-labels/generate-zpl/:templateId/:assetCode` | 生成ZPL标签 | ✍️ |
| `POST` | `/api/asset-labels/print` | 打印标签 | ✍️ |
| `POST` | `/api/asset-labels/generate-zpl-batch` | 批量生成ZPL标签 | ✍️ |

### `temp-assets` (5 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/temp-assets` | 查询 /api/temp-assets | 🤖 |
| `GET` | `/api/temp-assets/{id}` | 查询 /api/temp-assets/{id} | 🤖 |

### `asset-location` (13 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/asset-location` | 查询 /api/asset-location | 🤖 |
| `GET` | `/api/asset-location/devices` | 查询 /api/asset-location/devices | 🤖 |
| `GET` | `/api/asset-location/beacon-assets` | 查询 /api/asset-location/beacon-assets | 🤖 |
| `GET` | `/api/asset-location/assets/{assetIdOrCode}/devices` | 查询 /api/asset-location/assets/{assetIdOrCode}/devices | 🤖 |
| `GET` | `/api/asset-location/assets/{assetIdOrCode}/location` | 查询 /api/asset-location/assets/{assetIdOrCode}/location | 🤖 |
| `GET` | `/api/asset-location/assets/{assetIdOrCode}/location/history` | 查询 /api/asset-location/assets/{assetIdOrCode}/location/history | 🤖 |

### `barcode-scan` (5 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/barcode-scan` | 条码扫描API信息 | ✍️ |
| `GET` | `/api/barcode-scan/logs` | 获取扫码日志 | ✍️ |
| `GET` | `/api/barcode-scan/generate/{asset_code}` | 生成资产二维码 | ✍️ |
| `POST` | `/api/barcode-scan/verify` | 扫码验证资产 | ✍️ |
| `POST` | `/api/barcode-scan/inventory` | 扫码进行盘点 | ✍️ |

### `cloud-sync` (7 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/cloud-sync/events` | 获取同步事件列表 | ✍️ |
| `GET` | `/api/cloud-sync/sources` | 获取同步源列表 | ✍️ |
| `GET` | `/api/cloud-sync/events/stream` | 订阅同步事件流 | ✍️ |
| `PUT` | `/api/cloud-sync/sources/{id}` | 更新同步源 | ✍️ |
| `POST` | `/api/cloud-sync/webhook/{sourceId}` | 接收云同步Webhook事件 | ✍️ |

---

## 维修与保养

**说明**:日常维修工单/审批/费用/评价、日常保养、预防性维护、临时保养、保修合同。`/api/maintenance-management` 是新模块化路径,`/api/maintenance` 旧路径仍兼容。

### `maintenance-management` (47 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/maintenance-management` | 查询 /api/maintenance-management | 🤖 |
| `GET` | `/api/maintenance-management/logs` | 查询 /api/maintenance-management/logs | 🤖 |
| `GET` | `/api/maintenance-management/plans` | 查询 /api/maintenance-management/plans | 🤖 |
| `GET` | `/api/maintenance-management/costs` | 查询 /api/maintenance-management/costs | 🤖 |
| `GET` | `/api/maintenance-management/usage` | 查询 /api/maintenance-management/usage | 🤖 |
| `GET` | `/api/maintenance-management/health` | 查询 /api/maintenance-management/health | 🤖 |

### `maintenance` (132 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/maintenance/logs` | 获取维护日志列表 | ✍️ |
| `GET` | `/maintenance/requests` | 获取维修申请列表 | ✍️ |
| `GET` | `/maintenance/logs/{id}` | 获取维护日志详情 | ✍️ |
| `GET` | `/maintenance/statistics` | 获取维护统计 | ✍️ |
| `GET` | `/maintenance/requests/{id}` | 获取维修申请详情 | ✍️ |
| `GET` | `/api/maintenance/ai/pending` | 获取AI待处理请求 | ✍️ |

### `maintenance-cost` (11 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/maintenance-cost/costs` | 查询 /api/maintenance-cost/costs | 🤖 |
| `GET` | `/api/maintenance-cost/costs/trend` | 查询 /api/maintenance-cost/costs/trend | 🤖 |
| `GET` | `/api/maintenance-cost/costs/analysis` | 查询 /api/maintenance-cost/costs/analysis | 🤖 |
| `GET` | `/api/maintenance-cost/costs/department` | 查询 /api/maintenance-cost/costs/department | 🤖 |
| `GET` | `/api/maintenance-cost/costs/asset-type` | 查询 /api/maintenance-cost/costs/asset-type | 🤖 |
| `GET` | `/api/maintenance-cost/costs/maintenance-type` | 查询 /api/maintenance-cost/costs/maintenance-type | 🤖 |

### `daily-maintenance` (18 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/daily-maintenance` | 查询 /api/daily-maintenance | 🤖 |
| `GET` | `/api/daily-maintenance/plans` | 查询 /api/daily-maintenance/plans | 🤖 |
| `GET` | `/api/daily-maintenance/health` | 查询 /api/daily-maintenance/health | 🤖 |
| `GET` | `/api/daily-maintenance/templates` | 查询 /api/daily-maintenance/templates | 🤖 |
| `GET` | `/api/daily-maintenance/reminders` | 查询 /api/daily-maintenance/reminders | 🤖 |
| `GET` | `/api/daily-maintenance/plans/{id}` | 查询 /api/daily-maintenance/plans/{id} | 🤖 |

### `preventive-maintenance` (6 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/preventive-maintenance` | 查询 /api/preventive-maintenance | 🤖 |
| `GET` | `/api/preventive-maintenance/health` | 查询 /api/preventive-maintenance/health | 🤖 |
| `GET` | `/api/preventive-maintenance/efficiency/overview` | 查询 /api/preventive-maintenance/efficiency/overview | 🤖 |
| `GET` | `/api/preventive-maintenance/efficiency/technician` | 查询 /api/preventive-maintenance/efficiency/technician | 🤖 |
| `GET` | `/api/preventive-maintenance/efficiency/response-time` | 查询 /api/preventive-maintenance/efficiency/response-time | 🤖 |
| `GET` | `/api/preventive-maintenance/efficiency/asset-frequency` | 查询 /api/preventive-maintenance/efficiency/asset-frequency | 🤖 |

### `maintenance-temporary` (6 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/maintenance-temporary` | 查询 /api/maintenance-temporary | 🤖 |
| `GET` | `/api/maintenance-temporary/health` | 查询 /api/maintenance-temporary/health | 🤖 |
| `GET` | `/api/maintenance-temporary/efficiency/overview` | 查询 /api/maintenance-temporary/efficiency/overview | 🤖 |
| `GET` | `/api/maintenance-temporary/efficiency/technician` | 查询 /api/maintenance-temporary/efficiency/technician | 🤖 |
| `GET` | `/api/maintenance-temporary/efficiency/response-time` | 查询 /api/maintenance-temporary/efficiency/response-time | 🤖 |
| `GET` | `/api/maintenance-temporary/efficiency/asset-frequency` | 查询 /api/maintenance-temporary/efficiency/asset-frequency | 🤖 |

### `warranty` (41 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/warranty/info` | 查询 /api/warranty/info | 🤖 |
| `GET` | `/api/warranty/history` | 查询 /api/warranty/history | 🤖 |
| `GET` | `/api/warranty/invoices` | 查询 /api/warranty/invoices | 🤖 |
| `GET` | `/api/warranty/payments` | 查询 /api/warranty/payments | 🤖 |
| `GET` | `/api/warranty/archives` | 查询 /api/warranty/archives | 🤖 |
| `GET` | `/api/warranty/contracts` | 查询 /api/warranty/contracts | 🤖 |

---

## 采购/合同/供应商

**说明**:招标项目/投标/评标/合同/预算池/采购申请,供应商资质,统一合同管理。`/api/tendering/procurement-requests` 替代旧 `/api/procurement`。

### `tendering` (169 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/tendering` | 查询 /api/tendering | 🤖 |
| `GET` | `/api/tendering/dict` | 查询 /api/tendering/dict | 🤖 |
| `GET` | `/api/tendering/health` | 查询 /api/tendering/health | 🤖 |
| `GET` | `/api/tendering/audits` | 查询 /api/tendering/audits | 🤖 |
| `GET` | `/api/tendering/projects` | 查询 /api/tendering/projects | 🤖 |
| `GET` | `/api/tendering/invoices` | 查询 /api/tendering/invoices | 🤖 |

### `procurement` (18 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/procurement` | 获取采购申请列表 | ✍️ |
| `GET` | `/procurement/stats` | 获取采购统计 | ✍️ |
| `GET` | `/procurement/requests` | 获取采购单列表 | ✍️ |
| `GET` | `/procurement/requests/{id}/files` | 获取采购单附件列表 | ✍️ |
| `PUT` | `/procurement/requests/{id}` | 更新采购单 | ✍️ |
| `PUT` | `/api/procurement/{id}/approve` | 审批采购申请 | ✍️ |

### `supplier` (62 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/supplier/{id}` | 查询 /api/supplier/{id} | 🤖 |
| `GET` | `/api/supplier/dict` | 查询 /api/supplier/dict | 🤖 |
| `GET` | `/api/supplier/list` | 查询 /api/supplier/list | 🤖 |
| `GET` | `/api/supplier/health` | 查询 /api/supplier/health | 🤖 |
| `GET` | `/api/supplier/export` | 查询 /api/supplier/export | 🤖 |
| `GET` | `/api/supplier/blacklist` | 查询 /api/supplier/blacklist | 🤖 |

### `contracts` (27 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/contracts/asset` | 查询 /api/contracts/asset | 🤖 |
| `GET` | `/api/contracts/parts` | 查询 /api/contracts/parts | 🤖 |
| `GET` | `/api/contracts/asset/{id}` | 查询 /api/contracts/asset/{id} | 🤖 |
| `GET` | `/api/contracts/parts/{id}` | 查询 /api/contracts/parts/{id} | 🤖 |
| `GET` | `/api/contracts/asset/stats` | 查询 /api/contracts/asset/stats | 🤖 |
| `GET` | `/api/contracts/maintenance` | 查询 /api/contracts/maintenance | 🤖 |

---

## 质量管理

**说明**:质控记录/报告、POCT 临床质控(早中晚班+签名)、计量器具/校准/检定、不良事件上报/审批/根因分析。

### `quality-control` (32 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/quality-control/metrology` | 获取计量记录列表 | ✍️ |
| `GET` | `/quality-control/metrology/{id}` | 获取计量记录详情 | ✍️ |
| `GET` | `/quality-control/quality-control` | 获取质量控制记录列表 | ✍️ |
| `GET` | `/quality-control/quality-control/{id}` | 获取质量控制记录详情 | ✍️ |
| `GET` | `/quality-control/quality-control/statistics` | 获取质量控制统计 | ✍️ |
| `GET` | `/api/quality-control` | 查询 /api/quality-control | 🤖 |

### `quality-assurance` (21 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/quality-assurance` | 查询 /api/quality-assurance | 🤖 |
| `GET` | `/api/quality-assurance/{id}` | 查询 /api/quality-assurance/{id} | 🤖 |
| `GET` | `/api/quality-assurance/health` | 查询 /api/quality-assurance/health | 🤖 |
| `GET` | `/api/quality-assurance/expiring` | 查询 /api/quality-assurance/expiring | 🤖 |
| `GET` | `/api/quality-assurance/templates` | 查询 /api/quality-assurance/templates | 🤖 |
| `GET` | `/api/quality-assurance/statistics` | 查询 /api/quality-assurance/statistics | 🤖 |

### `poct-quality-control` (28 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/poct-quality-control/health` | 查询 /api/poct-quality-control/health | 🤖 |
| `GET` | `/api/poct-quality-control/shifts` | 查询 /api/poct-quality-control/shifts | 🤖 |
| `GET` | `/api/poct-quality-control/records` | 查询 /api/poct-quality-control/records | 🤖 |
| `GET` | `/api/poct-quality-control/subjects` | 查询 /api/poct-quality-control/subjects | 🤖 |
| `GET` | `/api/poct-quality-control/schedules` | 查询 /api/poct-quality-control/schedules | 🤖 |
| `GET` | `/api/poct-quality-control/reminders` | 查询 /api/poct-quality-control/reminders | 🤖 |

### `metrology` (3 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/metrology` | 查询 /api/metrology | 🤖 |
| `GET` | `/api/metrology/info` | 查询 /api/metrology/info | 🤖 |
| `GET` | `/api/metrology/health` | 查询 /api/metrology/health | 🤖 |

### `adverse-reaction` (28 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/adverse-reaction` | 查询 /api/adverse-reaction | 🤖 |
| `GET` | `/api/adverse-reaction/{id}` | 查询 /api/adverse-reaction/{id} | 🤖 |
| `GET` | `/api/adverse-reaction/health` | 查询 /api/adverse-reaction/health | 🤖 |
| `GET` | `/api/adverse-reaction/export/excel` | 查询 /api/adverse-reaction/export/excel | 🤖 |
| `GET` | `/api/adverse-reaction/{id}/workflow` | 查询 /api/adverse-reaction/{id}/workflow | 🤖 |
| `GET` | `/api/adverse-reaction/alerts/overdue` | 查询 /api/adverse-reaction/alerts/overdue | 🤖 |

---

## 巡检/合规/安全

**说明**:巡检模板/任务/异常整改、合规检查、风险评估、重点设备(原特种设备)、员工资质、设备开机率。

### `inspection` (47 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/inspection` | 查询 /api/inspection | 🤖 |
| `GET` | `/api/inspection/tasks` | 查询 /api/inspection/tasks | 🤖 |
| `GET` | `/api/inspection/plans` | 查询 /api/inspection/plans | 🤖 |
| `GET` | `/api/inspection/status` | 查询 /api/inspection/status | 🤖 |
| `GET` | `/api/inspection/health` | 查询 /api/inspection/health | 🤖 |
| `GET` | `/api/inspection/issues` | 查询 /api/inspection/issues | 🤖 |

### `compliance` (25 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/compliance` | 查询 /api/compliance | 🤖 |
| `GET` | `/api/compliance/health` | 查询 /api/compliance/health | 🤖 |
| `GET` | `/api/compliance/status` | 查询 /api/compliance/status | 🤖 |
| `GET` | `/api/compliance/departments` | 查询 /api/compliance/departments | 🤖 |
| `GET` | `/api/compliance/dashboard-stats` | 查询 /api/compliance/dashboard-stats | 🤖 |
| `GET` | `/api/compliance/maintenance-plans` | 查询 /api/compliance/maintenance-plans | 🤖 |

### `risk` (25 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/risk` | 查询 /api/risk | 🤖 |
| `GET` | `/api/risk/health` | 查询 /api/risk/health | 🤖 |
| `GET` | `/api/risk/status` | 查询 /api/risk/status | 🤖 |
| `GET` | `/api/risk/controls` | 查询 /api/risk/controls | 🤖 |
| `GET` | `/api/risk/standards` | 查询 /api/risk/standards | 🤖 |
| `GET` | `/api/risk/dashboard` | 查询 /api/risk/dashboard | 🤖 |

### `key-equipment` (24 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/key-equipment` | 查询 /api/key-equipment | 🤖 |
| `GET` | `/api/key-equipment/{id}` | 查询 /api/key-equipment/{id} | 🤖 |
| `GET` | `/api/key-equipment/certs` | 查询 /api/key-equipment/certs | 🤖 |
| `GET` | `/api/key-equipment/status` | 查询 /api/key-equipment/status | 🤖 |
| `GET` | `/api/key-equipment/health` | 查询 /api/key-equipment/health | 🤖 |
| `GET` | `/api/key-equipment/export` | 查询 /api/key-equipment/export | 🤖 |

### `safety-inspection` (13 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/safety-inspection` | 查询 /api/safety-inspection | 🤖 |
| `GET` | `/api/safety-inspection/{id}` | 查询 /api/safety-inspection/{id} | 🤖 |
| `GET` | `/api/safety-inspection/status` | 查询 /api/safety-inspection/status | 🤖 |
| `GET` | `/api/safety-inspection/health` | 查询 /api/safety-inspection/health | 🤖 |
| `GET` | `/api/safety-inspection/issues` | 查询 /api/safety-inspection/issues | 🤖 |
| `GET` | `/api/safety-inspection/expiring` | 查询 /api/safety-inspection/expiring | 🤖 |

### `staff` (52 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/staff` | 查询 /api/staff | 🤖 |
| `GET` | `/api/staff/status` | 查询 /api/staff/status | 🤖 |
| `GET` | `/api/staff/health` | 查询 /api/staff/health | 🤖 |
| `GET` | `/api/staff/training` | 查询 /api/staff/training | 🤖 |
| `GET` | `/api/staff/engineers` | 查询 /api/staff/engineers | 🤖 |
| `GET` | `/api/staff/statistics` | 查询 /api/staff/statistics | 🤖 |

### `uptime` (18 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/uptime` | 查询 /api/uptime | 🤖 |
| `GET` | `/api/uptime/status` | 查询 /api/uptime/status | 🤖 |
| `GET` | `/api/uptime/config` | 查询 /api/uptime/config | 🤖 |
| `GET` | `/api/uptime/health` | 查询 /api/uptime/health | 🤖 |
| `GET` | `/api/uptime/statistics` | 查询 /api/uptime/statistics | 🤖 |
| `GET` | `/api/uptime/operation-logs` | 查询 /api/uptime/operation-logs | 🤖 |

---

## 设备/备件/技术资料

**说明**:大型设备台账/巡检/校准、备件入库出库、IoT 设备/位置/环境监测、技术文档上传/AI 问答、知识库。

### `large-equipment` (29 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/large-equipment` | 查询 /api/large-equipment | 🤖 |
| `GET` | `/api/large-equipment/{id}` | 查询 /api/large-equipment/{id} | 🤖 |
| `GET` | `/api/large-equipment/status` | 查询 /api/large-equipment/status | 🤖 |
| `GET` | `/api/large-equipment/health` | 查询 /api/large-equipment/health | 🤖 |
| `GET` | `/api/large-equipment/export` | 查询 /api/large-equipment/export | 🤖 |
| `GET` | `/api/large-equipment/inspections` | 查询 /api/large-equipment/inspections | 🤖 |

### `spare-parts` (27 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/spare-parts` | 查询 /api/spare-parts | 🤖 |
| `GET` | `/api/spare-parts/{id}` | 查询 /api/spare-parts/{id} | 🤖 |
| `GET` | `/api/spare-parts/status` | 查询 /api/spare-parts/status | 🤖 |
| `GET` | `/api/spare-parts/health` | 查询 /api/spare-parts/health | 🤖 |
| `GET` | `/api/spare-parts/approvals` | 查询 /api/spare-parts/approvals | 🤖 |
| `GET` | `/api/spare-parts/adjustments` | 查询 /api/spare-parts/adjustments | 🤖 |

### `iot` (56 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/iot` | 查询 /api/iot | 🤖 |
| `GET` | `/api/iot/health` | 查询 /api/iot/health | 🤖 |
| `GET` | `/api/iot/devices` | 查询 /api/iot/devices | 🤖 |
| `GET` | `/api/iot/devices/{id}` | 查询 /api/iot/devices/{id} | 🤖 |
| `GET` | `/api/iot/devices/{deviceId}/assets` | 查询 /api/iot/devices/{deviceId}/assets | 🤖 |
| `GET` | `/api/iot/patient-volume/records/all` | 查询 /api/iot/patient-volume/records/all | 🤖 |

### `iot-devices` (11 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/iot-devices` | 查询 /api/iot-devices | 🤖 |
| `GET` | `/api/iot-devices/{id}` | 查询 /api/iot-devices/{id} | 🤖 |
| `GET` | `/api/iot-devices/{deviceId}/data` | 查询 /api/iot-devices/{deviceId}/data | 🤖 |
| `GET` | `/api/iot-devices/{deviceId}/assets` | 查询 /api/iot-devices/{deviceId}/assets | 🤖 |
| `GET` | `/api/iot-devices/assets/{assetCode}/devices` | 查询 /api/iot-devices/assets/{assetCode}/devices | 🤖 |
| `POST` | `/api/iot-devices/assets/{assetCode}/link` | 创建/提交 /api/iot-devices/assets/{assetCode}/link | 🤖 |

### `location-codes` (5 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/location-codes` | 查询 /api/location-codes | 🤖 |
| `GET` | `/api/location-codes/{id}` | 查询 /api/location-codes/{id} | 🤖 |

### `location-alerts` (5 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/location-alerts` | 获取位置告警列表 | ✍️ |
| `GET` | `/api/location-alerts/stats` | 获取位置告警统计 | ✍️ |
| `DELETE` | `/api/location-alerts/{id}` | 删除位置告警 | ✍️ |
| `PUT` | `/api/location-alerts/{id}/handle` | 处理位置告警 | ✍️ |
| `POST` | `/api/location-alerts/batch/handle` | 批量处理位置告警 | ✍️ |

### `technical-documents` (64 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/technical-documents` | 获取技术资料列表 | ✍️ |
| `GET` | `/api/technical-documents/assets/{assetId}` | 获取资产的技术资料列表 | ✍️ |
| `GET` | `/api/technical-documents/{id}` | 查询 /api/technical-documents/{id} | 🤖 |
| `GET` | `/api/technical-documents/stats` | 查询 /api/technical-documents/stats | 🤖 |
| `GET` | `/api/technical-documents/health` | 查询 /api/technical-documents/health | 🤖 |
| `GET` | `/api/technical-documents/pending` | 查询 /api/technical-documents/pending | 🤖 |

### `knowledge-base` (19 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/knowledge-base/health` | 查询 /api/knowledge-base/health | 🤖 |
| `GET` | `/api/knowledge-base/settings` | 查询 /api/knowledge-base/settings | 🤖 |
| `GET` | `/api/knowledge-base/documents` | 查询 /api/knowledge-base/documents | 🤖 |
| `GET` | `/api/knowledge-base/qa-records` | 查询 /api/knowledge-base/qa-records | 🤖 |
| `GET` | `/api/knowledge-base/documents/{id}` | 查询 /api/knowledge-base/documents/{id} | 🤖 |
| `GET` | `/api/knowledge-base/knowledge-bases` | 查询 /api/knowledge-base/knowledge-bases | 🤖 |

---

## 验收/事件/PDCA

**说明**:验收申请/审批/报告、通用事件提醒、PDCA 模板/记录、应急设备租借/计费、schema 表单设计器。

### `acceptance-management` (39 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/acceptance-management` | 查询 /api/acceptance-management | 🤖 |
| `GET` | `/api/acceptance-management/health` | 查询 /api/acceptance-management/health | 🤖 |
| `GET` | `/api/acceptance-management/templates` | 查询 /api/acceptance-management/templates | 🤖 |
| `GET` | `/api/acceptance-management/reminders` | 查询 /api/acceptance-management/reminders | 🤖 |
| `GET` | `/api/acceptance-management/applications` | 查询 /api/acceptance-management/applications | 🤖 |
| `GET` | `/api/acceptance-management/reports/{id}` | 查询 /api/acceptance-management/reports/{id} | 🤖 |

### `acceptance` (20 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/acceptance/records` | 查询 /api/acceptance/records | 🤖 |
| `GET` | `/api/acceptance/templates` | 查询 /api/acceptance/templates | 🤖 |
| `GET` | `/api/acceptance/statistics` | 查询 /api/acceptance/statistics | 🤖 |
| `GET` | `/api/acceptance/records/{id}` | 查询 /api/acceptance/records/{id} | 🤖 |
| `GET` | `/api/acceptance/records/{id}/files` | 查询 /api/acceptance/records/{id}/files | 🤖 |
| `GET` | `/api/acceptance/files/{id}/download` | 查询 /api/acceptance/files/{id}/download | 🤖 |

### `event-reminder` (20 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/event-reminder` | 查询 /api/event-reminder | 🤖 |
| `GET` | `/api/event-reminder/health` | 查询 /api/event-reminder/health | 🤖 |
| `GET` | `/api/event-reminder/status` | 查询 /api/event-reminder/status | 🤖 |
| `GET` | `/api/event-reminder/events` | 查询 /api/event-reminder/events | 🤖 |
| `GET` | `/api/event-reminder/upcoming` | 查询 /api/event-reminder/upcoming | 🤖 |
| `GET` | `/api/event-reminder/calendar` | 查询 /api/event-reminder/calendar | 🤖 |

### `pdca` (30 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/pdca` | 查询 /api/pdca | 🤖 |
| `GET` | `/api/pdca/health` | 查询 /api/pdca/health | 🤖 |
| `GET` | `/api/pdca/status` | 查询 /api/pdca/status | 🤖 |
| `GET` | `/api/pdca/records` | 查询 /api/pdca/records | 🤖 |
| `GET` | `/api/pdca/overview` | 查询 /api/pdca/overview | 🤖 |
| `GET` | `/api/pdca/templates` | 查询 /api/pdca/templates | 🤖 |

### `emergency-allocation` (20 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/emergency-allocation` | 查询 /api/emergency-allocation | 🤖 |
| `GET` | `/api/emergency-allocation/pools` | 查询 /api/emergency-allocation/pools | 🤖 |
| `GET` | `/api/emergency-allocation/health` | 查询 /api/emergency-allocation/health | 🤖 |
| `GET` | `/api/emergency-allocation/status` | 查询 /api/emergency-allocation/status | 🤖 |
| `GET` | `/api/emergency-allocation/orders` | 查询 /api/emergency-allocation/orders | 🤖 |
| `GET` | `/api/emergency-allocation/pools/{id}` | 查询 /api/emergency-allocation/pools/{id} | 🤖 |

### `form-customization` (9 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/form-customization` | 查询 /api/form-customization | 🤖 |
| `GET` | `/api/form-customization/health` | 查询 /api/form-customization/health | 🤖 |
| `GET` | `/api/form-customization/status` | 查询 /api/form-customization/status | 🤖 |
| `GET` | `/api/form-customization/schemas` | 查询 /api/form-customization/schemas | 🤖 |
| `GET` | `/api/form-customization/schemas/{id}` | 查询 /api/form-customization/schemas/{id} | 🤖 |
| `GET` | `/api/form-customization/schemas/code/{code}` | 查询 /api/form-customization/schemas/code/{code} | 🤖 |

---

## 用户/权限/组织

**说明**:用户管理、部门组织、租户/模块/角色配置、菜单权限、按钮级权限。

### `users` (27 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `POST` | `/api/users/login` | 用户登录 | ✍️ |
| `POST` | `/api/users/refresh-token` | 刷新令牌 | ✍️ |
| `GET` | `/api/users` | 查询 /api/users | 🤖 |
| `GET` | `/api/users/{id}` | 查询 /api/users/{id} | 🤖 |
| `GET` | `/api/users/roles` | 查询 /api/users/roles | 🤖 |
| `GET` | `/api/users/health` | 查询 /api/users/health | 🤖 |

### `departments` (8 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/departments` | 查询 /api/departments | 🤖 |
| `GET` | `/api/departments/tree` | 查询 /api/departments/tree | 🤖 |
| `GET` | `/api/departments/{id}` | 查询 /api/departments/{id} | 🤖 |
| `GET` | `/api/departments/health` | 查询 /api/departments/health | 🤖 |
| `GET` | `/api/departments/search` | 查询 /api/departments/search | 🤖 |

### `tenants` (7 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/tenants` | 查询 /api/tenants | 🤖 |
| `GET` | `/api/tenants/{id}(\\d+)` | 查询 /api/tenants/{id}(\\d+) | 🤖 |
| `GET` | `/api/tenants/current/info` | 查询 /api/tenants/current/info | 🤖 |
| `POST` | `/api/tenants/verify` | 创建/提交 /api/tenants/verify | 🤖 |

### `tenant-access-url` (4 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/tenant-access-url/{tenantId}` | 查询 /api/tenant-access-url/{tenantId} | 🤖 |
| `GET` | `/api/tenant-access-url/_debug/build-url` | 查询 /api/tenant-access-url/_debug/build-url | 🤖 |

### `tenant-association` (3 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/tenant-association/my-tenant` | 查询 /api/tenant-association/my-tenant | 🤖 |
| `POST` | `/api/tenant-association/join` | 创建/提交 /api/tenant-association/join | 🤖 |
| `POST` | `/api/tenant-association/create` | 创建/提交 /api/tenant-association/create | 🤖 |

### `tenant-module-config` (10 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/tenant-module-config/logs` | 获取配置变更日志 | ✍️ |
| `GET` | `/api/tenant-module-config/tenants` | 获取企业空间列表 | ✍️ |
| `GET` | `/api/tenant-module-config/modules` | 获取所有可用模块 | ✍️ |
| `GET` | `/api/tenant-module-config/modules/{moduleId}/menus` | 获取指定模块的菜单列表 | ✍️ |
| `GET` | `/api/tenant-module-config/tenants/{tenantId}/modules` | 获取指定企业空间的模块配置 | ✍️ |
| `GET` | `/api/tenant-module-config/modules/{moduleId}/dependencies` | 获取指定模块的依赖关系 | ✍️ |

### `tenant-role-config` (7 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/tenant-role-config/roles` | 查询 /api/tenant-role-config/roles | 🤖 |
| `GET` | `/api/tenant-role-config/roles/{role}/menus` | 查询 /api/tenant-role-config/roles/{role}/menus | 🤖 |
| `GET` | `/api/tenant-role-config/roles/{role}/data-scope` | 查询 /api/tenant-role-config/roles/{role}/data-scope | 🤖 |
| `GET` | `/api/tenant-role-config/roles/{role}/permissions` | 查询 /api/tenant-role-config/roles/{role}/permissions | 🤖 |

### `modules` (16 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/modules` | 获取模块清单 | ✍️ |
| `GET` | `/modules/{moduleId}/dependencies` | 获取模块依赖 | ✍️ |
| `GET` | `/api/modules` | 查询 /api/modules | 🤖 |
| `GET` | `/api/modules/list` | 查询 /api/modules/list | 🤖 |
| `GET` | `/api/modules/{moduleId}` | 查询 /api/modules/{moduleId} | 🤖 |
| `GET` | `/api/modules/{moduleId}/logs` | 查询 /api/modules/{moduleId}/logs | 🤖 |

### `module-configs` (22 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/module-configs/list` | 获取租户模块配置列表 | ✍️ |
| `GET` | `/module-configs/{moduleId}` | 获取单模块租户配置 | ✍️ |
| `GET` | `/module-configs/{moduleId}/menus` | 获取模块菜单启用状态 | ✍️ |
| `POST` | `/module-configs/enable` | 启用模块 | ✍️ |
| `POST` | `/module-configs/disable` | 停用模块 | ✍️ |
| `GET` | `/api/module-configs/list` | 查询 /api/module-configs/list | 🤖 |

### `menus` (8 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/menus/menus` | 查询 /api/menus/menus | 🤖 |
| `GET` | `/api/menus/menu-tree` | 查询 /api/menus/menu-tree | 🤖 |
| `GET` | `/api/menus/builtin-menus` | 查询 /api/menus/builtin-menus | 🤖 |
| `GET` | `/api/menus/default-menus` | 查询 /api/menus/default-menus | 🤖 |
| `GET` | `/api/menus/_debug-labels` | 查询 /api/menus/_debug-labels | 🤖 |
| `GET` | `/api/menus/display-settings` | 查询 /api/menus/display-settings | 🤖 |

### `roles-permissions` (19 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/roles-permissions/user/menus` | 获取当前用户菜单权限 | ✍️ |
| `GET` | `/api/roles-permissions/roles` | 查询 /api/roles-permissions/roles | 🤖 |
| `GET` | `/api/roles-permissions/menus/list` | 查询 /api/roles-permissions/menus/list | 🤖 |
| `GET` | `/api/roles-permissions/user/menus` | 查询 /api/roles-permissions/user/menus | 🤖 |
| `GET` | `/api/roles-permissions/permissions/list` | 查询 /api/roles-permissions/permissions/list | 🤖 |
| `GET` | `/api/roles-permissions/user/permissions` | 查询 /api/roles-permissions/user/permissions | 🤖 |

### `enhanced-permissions` (12 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/enhanced-permissions/audit-logs` | 查询 /api/enhanced-permissions/audit-logs | 🤖 |
| `GET` | `/api/enhanced-permissions/data-scopes/definitions` | 查询 /api/enhanced-permissions/data-scopes/definitions | 🤖 |
| `GET` | `/api/enhanced-permissions/roles/{role}/data-scope` | 查询 /api/enhanced-permissions/roles/{role}/data-scope | 🤖 |
| `GET` | `/api/enhanced-permissions/users/{userId}/data-scope` | 查询 /api/enhanced-permissions/users/{userId}/data-scope | 🤖 |
| `GET` | `/api/enhanced-permissions/users/{userId}/permissions` | 查询 /api/enhanced-permissions/users/{userId}/permissions | 🤖 |
| `GET` | `/api/enhanced-permissions/users/{userId}/menu-permissions` | 查询 /api/enhanced-permissions/users/{userId}/menu-permissions | 🤖 |

---

## 财务/折旧

**说明**:预算/收支/财务报表、资产折旧。

### `finance` (15 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/finance/budgets` | 获取预算列表 | ✍️ |
| `GET` | `/api/finance/costs` | 查询 /api/finance/costs | 🤖 |
| `GET` | `/api/finance/costs/stats` | 查询 /api/finance/costs/stats | 🤖 |
| `GET` | `/api/finance/transactions` | 查询 /api/finance/transactions | 🤖 |
| `GET` | `/api/finance/budgets/export` | 查询 /api/finance/budgets/export | 🤖 |
| `GET` | `/api/finance/budgets/summary` | 查询 /api/finance/budgets/summary | 🤖 |

### `depreciation` (17 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/depreciation` | 获取折旧列表 | ✍️ |
| `GET` | `/api/depreciation/{id}` | 获取资产折旧详情 | ✍️ |
| `GET` | `/api/depreciation/export` | 导出折旧数据 | ✍️ |
| `GET` | `/api/depreciation/methods` | 获取折旧方法列表 | ✍️ |
| `GET` | `/api/depreciation/summary/by-type` | 按类型汇总折旧数据 | ✍️ |
| `GET` | `/api/depreciation/summary/by-month` | 按月份查看折旧趋势 | ✍️ |

---

## 通知/消息

**说明**:通知发送记录/配置、站内消息中心、用户通知偏好、动态收件人策略。

### `notifications` (17 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/notifications/logs` | 查询 /api/notifications/logs | 🤖 |
| `GET` | `/api/notifications/rules` | 查询 /api/notifications/rules | 🤖 |
| `GET` | `/api/notifications/retries` | 查询 /api/notifications/retries | 🤖 |
| `GET` | `/api/notifications/metadata` | 查询 /api/notifications/metadata | 🤖 |
| `GET` | `/api/notifications/templates` | 查询 /api/notifications/templates | 🤖 |
| `GET` | `/api/notifications/rules/{id}` | 查询 /api/notifications/rules/{id} | 🤖 |

### `in-app-notifications` (12 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/in-app-notifications` | 查询 /api/in-app-notifications | 🤖 |
| `GET` | `/api/in-app-notifications/{id}/detail` | 查询 /api/in-app-notifications/{id}/detail | 🤖 |
| `GET` | `/api/in-app-notifications/admin/stats` | 查询 /api/in-app-notifications/admin/stats | 🤖 |
| `GET` | `/api/in-app-notifications/unread-count` | 查询 /api/in-app-notifications/unread-count | 🤖 |
| `DELETE` | `/api/in-app-notifications/{id}` | 删除 /api/in-app-notifications/{id} | 🤖 |
| `DELETE` | `/api/in-app-notifications/batch` | 删除 /api/in-app-notifications/batch | 🤖 |

### `notification-preferences` (7 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/notification-preferences/me` | 查询 /api/notification-preferences/me | 🤖 |
| `GET` | `/api/notification-preferences/meta` | 查询 /api/notification-preferences/meta | 🤖 |
| `GET` | `/api/notification-preferences/me/effective` | 查询 /api/notification-preferences/me/effective | 🤖 |
| `GET` | `/api/notification-preferences/user/{userId}` | 查询 /api/notification-preferences/user/{userId} | 🤖 |
| `POST` | `/api/notification-preferences` | 创建/提交 /api/notification-preferences | 🤖 |
| `DELETE` | `/api/notification-preferences/{id}` | 删除 /api/notification-preferences/{id} | 🤖 |

### `recipient-strategies` (8 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/recipient-strategies` | 查询 /api/recipient-strategies | 🤖 |
| `GET` | `/api/recipient-strategies/meta` | 查询 /api/recipient-strategies/meta | 🤖 |
| `GET` | `/api/recipient-strategies/event/{eventCode}` | 查询 /api/recipient-strategies/event/{eventCode} | 🤖 |
| `PUT` | `/api/recipient-strategies/{id}` | 更新 /api/recipient-strategies/{id} | 🤖 |
| `POST` | `/api/recipient-strategies/preview` | 创建/提交 /api/recipient-strategies/preview | 🤖 |
| `POST` | `/api/recipient-strategies/batch-delete` | 创建/提交 /api/recipient-strategies/batch-delete | 🤖 |

### `intelligent-alerts` (14 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/intelligent-alerts` | 获取预警列表 | ✍️ |
| `GET` | `/api/intelligent-alerts/safety` | 安全检测到期预警 | ✍️ |
| `GET` | `/api/intelligent-alerts/uptime` | 开机率异常预警 | ✍️ |
| `GET` | `/api/intelligent-alerts/overview` | 获取预警概览统计 | ✍️ |
| `GET` | `/api/intelligent-alerts/settings` | 获取用户预警设置 | ✍️ |
| `GET` | `/api/intelligent-alerts/maintenance` | 保养到期预警 | ✍️ |

---

## 工作流/审计/分析

**说明**:通用审批工作流引擎、操作审计日志、数据备份恢复、数据分析、首页仪表盘。

### `workflow` (19 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/workflow` | 工作流API信息 | ✍️ |
| `GET` | `/api/workflow/states` | 获取工作流状态列表 | ✍️ |
| `GET` | `/api/workflow/default` | 获取默认工作流ID | ✍️ |
| `GET` | `/api/workflow/transitions` | 获取工作流迁移规则 | ✍️ |
| `POST` | `/api/workflow/transition/{assetId}` | 执行状态迁移 | ✍️ |
| `GET` | `/api/workflow/health` | 查询 /api/workflow/health | 🤖 |

### `audit-logs` (9 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/audit-logs` | 获取操作日志列表 | ✍️ |
| `GET` | `/api/audit-logs/{id}` | 获取操作日志详情 | ✍️ |
| `GET` | `/api/audit-logs/stats` | 获取操作日志统计 | ✍️ |
| `GET` | `/api/audit-logs/export` | 查询 /api/audit-logs/export | 🤖 |
| `GET` | `/api/audit-logs/enhanced` | 查询 /api/audit-logs/enhanced | 🤖 |
| `GET` | `/api/audit-logs/statistics` | 查询 /api/audit-logs/statistics | 🤖 |

### `backup` (6 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/backup` | 获取备份列表 | ✍️ |
| `GET` | `/api/backup/{id}/download` | 下载备份文件 | ✍️ |
| `DELETE` | `/api/backup/{id}` | 删除备份文件 | ✍️ |
| `POST` | `/api/backup/{id}/restore` | 恢复数据库备份 | ✍️ |
| `POST` | `/api/backup/add-tenant-id` | 为表添加tenant_id字段 | ✍️ |

### `analysis` (3 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/analysis` | 获取资产综合分析数据 | ✍️ |
| `GET` | `/api/analysis/depreciation` | 获取资产折旧分析 | ✍️ |
| `GET` | `/api/analysis/value-distribution` | 获取资产价值分布分析 | ✍️ |

### `dashboard` (3 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/dashboard` | 获取仪表盘统计数据 | ✍️ |
| `GET` | `/api/dashboard/realtime` | 获取实时统计数据 | ✍️ |
| `GET` | `/api/dashboard/stats` | 查询 /api/dashboard/stats | 🤖 |

### `dashboard-configs` (7 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/dashboard-configs` | 查询 /api/dashboard-configs | 🤖 |
| `GET` | `/api/dashboard-configs/{id}` | 查询 /api/dashboard-configs/{id} | 🤖 |
| `GET` | `/api/dashboard-configs/active` | 查询 /api/dashboard-configs/active | 🤖 |
| `GET` | `/api/dashboard-configs/{id}/data` | 查询 /api/dashboard-configs/{id}/data | 🤖 |

### `desktop-preferences` (5 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/desktop-preferences/preferences` | 查询 /api/desktop-preferences/preferences | 🤖 |
| `PATCH` | `/api/desktop-preferences/preferences/hide` | 局部更新 /api/desktop-preferences/preferences/hide | 🤖 |
| `PATCH` | `/api/desktop-preferences/preferences/show` | 局部更新 /api/desktop-preferences/preferences/show | 🤖 |
| `PUT` | `/api/desktop-preferences/preferences/layout` | 更新 /api/desktop-preferences/preferences/layout | 🤖 |

### `page-views` (2 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/page-views/{pageKey}` | 获取页面访问量 | ✍️ |

### `i18n` (4 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/i18n/locales` | 获取支持的语言列表 | ✍️ |
| `GET` | `/api/i18n/messages/{locale}` | 获取指定语言的翻译消息 | ✍️ |
| `POST` | `/api/i18n/switch` | 切换用户语言偏好（需要登录） | ✍️ |
| `POST` | `/api/i18n/translate` | 翻译文本 | ✍️ |

### `api-documentation` (4 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/api-documentation` | 查询 /api/api-documentation | 🤖 |
| `GET` | `/api/api-documentation/modules` | 查询 /api/api-documentation/modules | 🤖 |
| `GET` | `/api/api-documentation/endpoints` | 查询 /api/api-documentation/endpoints | 🤖 |
| `GET` | `/api/api-documentation/module/{path}` | 查询 /api/api-documentation/module/{path} | 🤖 |

### `agent-mesh` (10 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/agent-mesh/topology` | 获取 Agent Mesh 拓扑结构 | ✍️ |
| `GET` | `/api/agent-mesh/microservice/events` | 获取事件契约清单 | ✍️ |
| `GET` | `/api/agent-mesh/microservice/roadmap` | 获取微服务拆分路线图 | ✍️ |
| `POST` | `/api/agent-mesh/init` | 初始化对话会话 | ✍️ |
| `POST` | `/api/agent-mesh/message` | 发送消息 | ✍️ |
| `POST` | `/api/agent-mesh/intelligence/risk-score` | 风险评分计算 | ✍️ |

---

## AI 智能

**说明**:AI 对话式资产助手、AI 资产数据分析。`/api/asset-ai-assistant` 是新模块化路径,`/api/ai` `/api/chat` 旧路径已弃用。

### `asset-ai-assistant` (9 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/asset-ai-assistant` | 查询 /api/asset-ai-assistant | 🤖 |
| `GET` | `/api/asset-ai-assistant/config` | 查询 /api/asset-ai-assistant/config | 🤖 |
| `GET` | `/api/asset-ai-assistant/status` | 查询 /api/asset-ai-assistant/status | 🤖 |
| `GET` | `/api/asset-ai-assistant/health` | 查询 /api/asset-ai-assistant/health | 🤖 |
| `GET` | `/api/asset-ai-assistant/sessions/{sessionId}/history` | 查询 /api/asset-ai-assistant/sessions/{sessionId}/history | 🤖 |
| `POST` | `/api/asset-ai-assistant/message` | 创建/提交 /api/asset-ai-assistant/message | 🤖 |

### `asset-ai-analysis` (8 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/asset-ai-analysis/dimensions` | 查询 /api/asset-ai-analysis/dimensions | 🤖 |
| `GET` | `/api/asset-ai-analysis/datasources` | 查询 /api/asset-ai-analysis/datasources | 🤖 |
| `GET` | `/api/asset-ai-analysis/reports/{id}` | 查询 /api/asset-ai-analysis/reports/{id} | 🤖 |
| `GET` | `/api/asset-ai-analysis/analysis-history` | 查询 /api/asset-ai-analysis/analysis-history | 🤖 |
| `GET` | `/api/asset-ai-analysis/question-records` | 查询 /api/asset-ai-analysis/question-records | 🤖 |
| `POST` | `/api/asset-ai-analysis/analyze-assets` | 创建/提交 /api/asset-ai-analysis/analyze-assets | 🤖 |

### `ai` (3 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/ai/config` | 获取AI配置信息 | ✍️ |
| `POST` | `/api/ai/chat/completions` | AI对话补全 | ✍️ |
| `POST` | `/api/ai/completions` | 创建/提交 /api/ai/completions | 🤖 |

### `ai-assistant` (5 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/ai-assistant/modes` | 查询 /api/ai-assistant/modes | 🤖 |
| `GET` | `/api/ai-assistant/config` | 查询 /api/ai-assistant/config | 🤖 |
| `GET` | `/api/ai-assistant/quick-questions` | 查询 /api/ai-assistant/quick-questions | 🤖 |
| `POST` | `/api/ai-assistant/query` | 创建/提交 /api/ai-assistant/query | 🤖 |
| `POST` | `/api/ai-assistant/history` | 创建/提交 /api/ai-assistant/history | 🤖 |

### `chat` (6 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/chat/config` | 查询 /chat/config | 🤖 |
| `GET` | `/api/chat/config` | 查询 /api/chat/config | 🤖 |
| `POST` | `/chat/completions` | 创建/提交 /chat/completions | 🤖 |
| `POST` | `/api/chat/completions` | 创建/提交 /api/chat/completions | 🤖 |
| `POST` | `/chat/chat/completions` | 创建/提交 /chat/chat/completions | 🤖 |
| `POST` | `/api/chat/chat/completions` | 创建/提交 /api/chat/chat/completions | 🤖 |

---

## 第三方集成

**说明**:飞书机器人/通知/绑定、微信公众号通知/绑定、微信小程序云函数。

### `feishu` (12 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/feishu` | 查询 /api/feishu | 🤖 |
| `GET` | `/api/feishu/health` | 查询 /api/feishu/health | 🤖 |
| `GET` | `/api/feishu/diagnostic` | 查询 /api/feishu/diagnostic | 🤖 |
| `GET` | `/api/feishu/binding/list` | 查询 /api/feishu/binding/list | 🤖 |
| `GET` | `/api/feishu/binding/status` | 查询 /api/feishu/binding/status | 🤖 |
| `GET` | `/api/feishu/binding/auth-url` | 查询 /api/feishu/binding/auth-url | 🤖 |

### `wechat-mp` (12 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/wechat-mp` | 查询 /api/wechat-mp | 🤖 |
| `GET` | `/api/wechat-mp/event` | 查询 /api/wechat-mp/event | 🤖 |
| `GET` | `/api/wechat-mp/health` | 查询 /api/wechat-mp/health | 🤖 |
| `GET` | `/api/wechat-mp/binding/list` | 查询 /api/wechat-mp/binding/list | 🤖 |
| `GET` | `/api/wechat-mp/binding/status` | 查询 /api/wechat-mp/binding/status | 🤖 |
| `GET` | `/api/wechat-mp/binding/auth-url` | 查询 /api/wechat-mp/binding/auth-url | 🤖 |

### `wx-cloud` (8 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/wx-cloud/status` | 获取微信云开发连接状态 | ✍️ |
| `GET` | `/api/wx-cloud/collections` | 获取集合列表 | ✍️ |
| `POST` | `/api/wx-cloud/add` | 新增记录 | ✍️ |
| `POST` | `/api/wx-cloud/query` | 查询记录 | ✍️ |
| `POST` | `/api/wx-cloud/count` | 统计记录数 | ✍️ |
| `POST` | `/api/wx-cloud/update` | 更新记录 | ✍️ |

### `sms-verification` (3 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `POST` | `/api/sms-verification/send-code` | 创建/提交 /api/sms-verification/send-code | 🤖 |
| `POST` | `/api/sms-verification/verify-code` | 创建/提交 /api/sms-verification/verify-code | 🤖 |
| `POST` | `/api/sms-verification/login-with-code` | 创建/提交 /api/sms-verification/login-with-code | 🤖 |

---

## 认证/系统

**说明**:登录/Token 管理、Service Token 签发/吊销、K8s 探针、Prometheus 指标、熔断器状态。

### `auth` (4 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/auth/service-tokens` | 查询 /api/auth/service-tokens | 🤖 |
| `GET` | `/api/auth/service-tokens/scopes` | 查询 /api/auth/service-tokens/scopes | 🤖 |
| `POST` | `/api/auth/service-tokens/{id}/revoke` | 创建/提交 /api/auth/service-tokens/{id}/revoke | 🤖 |

### `health` (9 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/health` | 服务健康检查 | ✍️ |
| `GET` | `/api/health` | 健康检查 | ✍️ |
| `GET` | `/api/health/ready` | 就绪检查 | ✍️ |
| `GET` | `/api/health/alive` | 存活检查 | ✍️ |
| `GET` | `/api/health/metrics` | 获取监控指标 | ✍️ |
| `GET` | `/api/health/detailed` | 详细健康状态 | ✍️ |

### `ready` (1 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/ready` | 查询 /api/ready | 🤖 |

### `alive` (1 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/alive` | 查询 /api/alive | 🤖 |

### `metrics` (1 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/metrics` | 查询 /api/metrics | 🤖 |

### `circuit-breakers` (2 ops)

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/circuit-breakers` | 查询 /api/circuit-breakers | 🤖 |
| `POST` | `/api/circuit-breakers/{name}/reset` | 创建/提交 /api/circuit-breakers/{name}/reset | 🤖 |

---

## 已弃用/迁移

**说明**:已迁移/弃用的旧路径,**不要**在新建 skill 时引用。保留仅作历史兼容。

### `inventory` (18 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/inventory` | 查询 /api/inventory | 🤖 |
| `GET` | `/api/inventory/{id}` | 查询 /api/inventory/{id} | 🤖 |
| `GET` | `/api/inventory/statistics` | 查询 /api/inventory/statistics | 🤖 |
| `GET` | `/api/inventory/self/assets` | 查询 /api/inventory/self/assets | 🤖 |
| `GET` | `/api/inventory/self/windows` | 查询 /api/inventory/self/windows | 🤖 |
| `GET` | `/api/inventory/{id}/scan-logs` | 查询 /api/inventory/{id}/scan-logs | 🤖 |

### `inventory-plans` (9 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/inventory-plans` | 获取盘点计划列表 | ✍️ |
| `GET` | `/api/inventory-plans/{id}` | 获取盘点计划详情 | ✍️ |
| `PUT` | `/api/inventory-plans/{id}/cancel` | 取消盘点计划 | ✍️ |
| `PUT` | `/api/inventory-plans/{id}/activate` | 激活盘点计划 | ✍️ |
| `PUT` | `/api/inventory-plans/{id}/complete` | 完成盘点计划 | ✍️ |
| `GET` | `/api/inventory-plans/statistics` | 查询 /api/inventory-plans/statistics | 🤖 |

### `inventory-tasks` (10 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/inventory-tasks` | 获取盘点任务列表 | ✍️ |
| `GET` | `/api/inventory-tasks/{id}` | 获取盘点任务详情 | ✍️ |
| `GET` | `/api/inventory-tasks/my/tasks` | 获取我的任务 | ✍️ |
| `PUT` | `/api/inventory-tasks/{id}/start` | 开始盘点任务 | ✍️ |
| `PUT` | `/api/inventory-tasks/{id}/assign` | 分配盘点任务 | ✍️ |
| `PUT` | `/api/inventory-tasks/{id}/cancel` | 取消盘点任务 | ✍️ |

### `inventory-reports` (7 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/inventory-reports` | 查询 /api/inventory-reports | 🤖 |
| `GET` | `/api/inventory-reports/dashboard` | 查询 /api/inventory-reports/dashboard | 🤖 |
| `GET` | `/api/inventory-reports/export/inventory-tasks` | 查询 /api/inventory-reports/export/inventory-tasks | 🤖 |
| `GET` | `/api/inventory-reports/export/inventory-plans` | 查询 /api/inventory-reports/export/inventory-plans | 🤖 |
| `GET` | `/api/inventory-reports/export/inventory-records` | 查询 /api/inventory-reports/export/inventory-records | 🤖 |
| `GET` | `/api/inventory-reports/export/inventory-discrepancies` | 查询 /api/inventory-reports/export/inventory-discrepancies | 🤖 |

### `inventory-discrepancies` (6 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/inventory-discrepancies` | 获取盘点差异列表 | ✍️ |
| `GET` | `/api/inventory-discrepancies/{id}` | 获取盘点差异详情 | ✍️ |
| `GET` | `/api/inventory-discrepancies/{inventory_id}/statistics` | 获取盘点差异统计 | ✍️ |
| `PUT` | `/api/inventory-discrepancies/{id}/handle` | 处理盘点差异 | ✍️ |
| `POST` | `/api/inventory-discrepancies/batch-handle` | 批量处理盘点差异 | ✍️ |
| `POST` | `/api/inventory-discrepancies/generate-from-details` | 自动生成盘点差异记录 | ✍️ |

### `materials` (11 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `GET` | `/api/materials` | 查询 /api/materials | 🤖 |
| `GET` | `/api/materials/inventory` | 查询 /api/materials/inventory | 🤖 |
| `GET` | `/api/materials/transactions` | 查询 /api/materials/transactions | 🤖 |
| `GET` | `/api/materials/maintenance-requirements` | 查询 /api/materials/maintenance-requirements | 🤖 |
| `PUT` | `/api/materials/{id}` | 更新 /api/materials/{id} | 🤖 |
| `POST` | `/api/materials/inventory/inbound` | 创建/提交 /api/materials/inventory/inbound | 🤖 |

### `sms-verification` (3 ops) ⚠️

| Method | Path | Summary | 类型 |
| --- | --- | --- | --- |
| `POST` | `/api/sms-verification/send-code` | 创建/提交 /api/sms-verification/send-code | 🤖 |
| `POST` | `/api/sms-verification/verify-code` | 创建/提交 /api/sms-verification/verify-code | 🤖 |
| `POST` | `/api/sms-verification/login-with-code` | 创建/提交 /api/sms-verification/login-with-code | 🤖 |

---

## 附录:全部 101 个模块速查

按业务域分组的 module 路径前缀(用于 `bash scripts/api.sh module <path>`):

**核心资产** (12 模块 / 136 ops)

- `assets` — 36 ops
- `scrapping` — 14 ops
- `asset-labels` — 13 ops
- `asset-location` — 13 ops ⚠️
- `idle` — 11 ops
- `asset-allocation` — 9 ops
- `transfer` — 9 ops ⚠️
- `asset-usage` — 9 ops
- `cloud-sync` — 7 ops ⚠️
- `asset-images` — 5 ops
- `temp-assets` — 5 ops
- `barcode-scan` — 5 ops ⚠️

**维修与保养** (7 模块 / 261 ops)

- `maintenance` — 132 ops ⚠️
- `maintenance-management` — 47 ops
- `warranty` — 41 ops
- `daily-maintenance` — 18 ops
- `maintenance-cost` — 11 ops
- `preventive-maintenance` — 6 ops
- `maintenance-temporary` — 6 ops ⚠️

**采购/合同/供应商** (4 模块 / 276 ops)

- `tendering` — 169 ops
- `supplier` — 62 ops
- `contracts` — 27 ops
- `procurement` — 18 ops ⚠️

**质量管理** (5 模块 / 112 ops)

- `quality-control` — 32 ops
- `poct-quality-control` — 28 ops
- `adverse-reaction` — 28 ops
- `quality-assurance` — 21 ops
- `metrology` — 3 ops

**巡检/合规/安全** (7 模块 / 204 ops)

- `staff` — 52 ops
- `inspection` — 47 ops
- `compliance` — 25 ops
- `risk` — 25 ops
- `key-equipment` — 24 ops
- `uptime` — 18 ops
- `safety-inspection` — 13 ops

**设备/备件/技术资料** (8 模块 / 216 ops)

- `technical-documents` — 64 ops
- `iot` — 56 ops
- `large-equipment` — 29 ops
- `spare-parts` — 27 ops
- `knowledge-base` — 19 ops
- `iot-devices` — 11 ops ⚠️
- `location-codes` — 5 ops
- `location-alerts` — 5 ops

**验收/事件/PDCA** (6 模块 / 138 ops)

- `acceptance-management` — 39 ops
- `pdca` — 30 ops
- `acceptance` — 20 ops ⚠️
- `event-reminder` — 20 ops
- `emergency-allocation` — 20 ops
- `form-customization` — 9 ops

**用户/权限/组织** (12 模块 / 143 ops)

- `users` — 27 ops
- `module-configs` — 22 ops
- `roles-permissions` — 19 ops
- `modules` — 16 ops
- `enhanced-permissions` — 12 ops
- `tenant-module-config` — 10 ops
- `departments` — 8 ops
- `menus` — 8 ops
- `tenants` — 7 ops
- `tenant-role-config` — 7 ops
- `tenant-access-url` — 4 ops
- `tenant-association` — 3 ops

**财务/折旧** (2 模块 / 32 ops)

- `depreciation` — 17 ops
- `finance` — 15 ops

**通知/消息** (5 模块 / 58 ops)

- `notifications` — 17 ops
- `intelligent-alerts` — 14 ops
- `in-app-notifications` — 12 ops
- `recipient-strategies` — 8 ops
- `notification-preferences` — 7 ops

**工作流/审计/分析** (11 模块 / 72 ops)

- `workflow` — 19 ops
- `agent-mesh` — 10 ops
- `audit-logs` — 9 ops
- `dashboard-configs` — 7 ops
- `backup` — 6 ops
- `desktop-preferences` — 5 ops
- `i18n` — 4 ops
- `api-documentation` — 4 ops
- `analysis` — 3 ops
- `dashboard` — 3 ops
- `page-views` — 2 ops

**AI 智能** (5 模块 / 31 ops)

- `asset-ai-assistant` — 9 ops
- `asset-ai-analysis` — 8 ops ⚠️
- `chat` — 6 ops ⚠️
- `ai-assistant` — 5 ops ⚠️
- `ai` — 3 ops ⚠️

**第三方集成** (4 模块 / 35 ops)

- `feishu` — 12 ops
- `wechat-mp` — 12 ops
- `wx-cloud` — 8 ops
- `sms-verification` — 3 ops ⚠️

**认证/系统** (6 模块 / 18 ops)

- `health` — 9 ops
- `auth` — 4 ops
- `circuit-breakers` — 2 ops
- `ready` — 1 ops
- `alive` — 1 ops
- `metrics` — 1 ops

**已弃用/迁移** (7 模块 / 64 ops)

- `inventory` — 18 ops ⚠️
- `materials` — 11 ops ⚠️
- `inventory-tasks` — 10 ops ⚠️
- `inventory-plans` — 9 ops ⚠️
- `inventory-reports` — 7 ops ⚠️
- `inventory-discrepancies` — 6 ops ⚠️
- `sms-verification` — 3 ops ⚠️

