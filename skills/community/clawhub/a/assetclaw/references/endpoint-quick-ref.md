# AssetHub API Top 40 速查（v1.7.0）

> 最高频 40 个 API 的 1 行速查。完整 1,809 ops 见 `api-modules-overview.md`。
> 数据来源：`backend/docs/swagger.json` 2026-07-29 同步扫描（基于 1,381 paths / 1,809 operations）。

## 关键标识

| 标识 | 含义 |
| --- | --- |
| `Idempotency-Key 必填` | POST/PUT/DELETE 必须带稳定的 `Idempotency-Key` header |
| `高风险` | 可能返回 `428 HIGH_RISK_CONFIRMATION_REQUIRED`，需用户明确确认后用 `X-Risk-Confirm-Token` 重放 |
| `白名单` | 已配置为免 428（如 `/maintenance/ai/submit-request`） |
| `新路径` | v1.7.0 新模块化路径，优先于旧路径 |

---

## 认证 / 自描述

| Method | Path | 说明 | 关键参数/Header |
| --- | --- | --- | --- |
| `POST` | `/api/users/login` | 用户登录，获取 JWT token | body: `{username, password, tenant_code?}` → `data.token` |
| `GET` | `/api/users/me` | 当前登录用户信息 | `Authorization: Bearer <token>` |
| `GET` | `/api/api-documentation/modules` | 运行时获取全部 101 个模块列表 | 无参数 |
| `GET` | `/api/api-documentation/module/{path}` | 运行时获取单个模块的接口详情 | `path={assets\|maintenance-management\|...}`（不含 `/api` 前缀） |
| `GET` | `/api/api-documentation/endpoints` | 运行时获取全部 1,809 endpoints | 无参数 |
| `GET` | `/api/health` | 服务健康检查（免认证） | 无参数 |

## 资产

| Method | Path | 说明 | 关键参数/Header |
| --- | --- | --- | --- |
| `GET` | `/api/assets` | 资产列表（分页+筛选） | `?page=1&pageSize=20&keyword=CT&status=在用&department=放射科` |
| `GET` | `/api/assets/all` | 资产全量列表（不分页） | `?keyword=&status=`（慎用，大数据量） |
| `GET` | `/api/assets/{id}` | 资产详情（ID 或 asset_code） | `path={id\|asset_code}` |
| `POST` | `/api/assets` | 创建资产 | `Idempotency-Key 必填`；body 必填 `asset_code/asset_name/category_id` |
| `PUT` | `/api/assets/{id}` | 更新资产 | `Idempotency-Key 必填`；`高风险`，可能 428 |
| `DELETE` | `/api/assets/{id}` | 删除资产 | `Idempotency-Key 必填`；`高风险`，必 428 |
| `GET` | `/api/assets/statistics` | 资产统计概览 | 无参数 |
| `GET` | `/api/assets/export` | 导出 Excel | `?keyword=&status=` |

## 维修（新模块化路径）

| Method | Path | 说明 | 关键参数/Header |
| --- | --- | --- | --- |
| `GET` | `/api/maintenance-management/work-orders` | 维修工单列表 | `?status=in_progress&page=1&pageSize=20` |
| `GET` | `/api/maintenance-management/requests` | 维修申请列表 | `?status=pending` |
| `POST` | `/api/maintenance/ai/submit-request` | AI 提交维修申请（`白名单`免 428） | body: `{asset_code, fault_description, source, intent}` |
| `POST` | `/api/maintenance-management/requests` | 手动提交维修申请 | `Idempotency-Key 必填`；body: `{asset_id, fault_description, ...}` |
| `POST` | `/api/maintenance-management/work-orders/{id}/dispatch` | 派工 | `高风险`，可能 428 |
| `POST` | `/api/maintenance-management/work-orders/{id}/complete` | 完工 | `高风险`，可能 428 |

## 调拨（`新路径`）

| Method | Path | 说明 | 关键参数/Header |
| --- | --- | --- | --- |
| `GET` | `/api/asset-allocation` | 调拨记录列表 | `?status=pending&page=1` |
| `POST` | `/api/asset-allocation/transfer-apply` | 提交调拨申请 | `Idempotency-Key 必填`；body: `{asset_id, to_department_id, reason}` |
| `POST` | `/api/asset-allocation/transfer-requests/{request_id}/approve` | 审批调拨 | `高风险`，必 428 |
| `POST` | `/api/asset-allocation/transfer-requests/{request_id}/reject` | 驳回调拨 | `高风险`，必 428 |

## 采购

| Method | Path | 说明 | 关键参数/Header |
| --- | --- | --- | --- |
| `GET` | `/api/tendering/projects` | 招标项目列表 | `?status=in_progress` |
| `GET` | `/api/tendering/procurement-requests` | 采购申请列表 | `?status=pending` |
| `POST` | `/api/tendering/procurement-requests` | 创建采购申请 | `Idempotency-Key 必填` |
| `GET` | `/api/supplier` | 供应商列表 | `?keyword=西门子&status=active` |
| `GET` | `/api/contracts` | 合同列表 | `?status=active&type=asset` |

## 巡检 / 验收 / 质控

| Method | Path | 说明 | 关键参数/Header |
| --- | --- | --- | --- |
| `GET` | `/api/inspection/tasks` | 巡检任务列表 | `?status=pending` |
| `GET` | `/api/inspection/issues` | 巡检异常/整改 | `?status=open` |
| `GET` | `/api/acceptance-management/applications` | 验收申请列表 | `?status=pending` |
| `POST` | `/api/acceptance-management/applications` | 提交验收申请 | `Idempotency-Key 必填` |
| `GET` | `/api/quality-control/records` | 质控记录 | `?department=检验科` |
| `GET` | `/api/poct-quality-control/records` | POCT 质控（早中晚班） | `?date=2026-07-29` |

## 不良事件（`新路径`）

| Method | Path | 说明 | 关键参数/Header |
| --- | --- | --- | --- |
| `GET` | `/api/adverse-reaction` | 不良事件列表 | `?status=pending` |
| `POST` | `/api/adverse-reaction` | 上报不良事件 | `Idempotency-Key 必填`；body: `{event_type, asset_id, description, severity}` |

## IoT

| Method | Path | 说明 | 关键参数/Header |
| --- | --- | --- | --- |
| `GET` | `/api/iot/devices` | IoT 设备列表 | `?status=online` |
| `GET` | `/api/iot/locations` | IoT 位置列表 | `?asset_id=123` |
| `POST` | `/api/iot/locations/ingest` | IoT 位置上报 | 需 `ASSETHUB_IOT_TOKEN`（不用 user JWT） |

## 用户 / 部门 / 角色

| Method | Path | 说明 | 关键参数/Header |
| --- | --- | --- | --- |
| `GET` | `/api/users` | 用户列表 | `?status=active&role=department_admin` |
| `GET` | `/api/departments` | 部门列表 | `?status=active` |
| `GET` | `/api/roles-permissions/roles` | 角色列表 | 无参数 |

## 系统 / 通知

| Method | Path | 说明 | 关键参数/Header |
| --- | --- | --- | --- |
| `GET` | `/api/tenants` | 租户列表（仅 super_admin） | 无参数 |
| `GET` | `/api/audit-logs` | 审计日志 | `?user_id=&start_date=&end_date=` |
| `GET` | `/api/in-app-notifications` | 站内消息 | `?status=unread` |

## AI

| Method | Path | 说明 | 关键参数/Header |
| --- | --- | --- | --- |
| `POST` | `/api/asset-ai-assistant/chat` | AI 助手对话 | body: `{message, session_id}` |
| `POST` | `/api/asset-ai-assistant/asset-query` | AI 资产查询 | body: `{natural_language_query}` |

## 第三方集成

| Method | Path | 说明 | 关键参数/Header |
| --- | --- | --- | --- |
| `GET` | `/api/feishu/bindings` | 飞书绑定查询 | 无参数 |
| `POST` | `/api/feishu/send` | 飞书发送通知 | body: `{binding_id, content}`（需先 bindings） |
| `POST` | `/api/wechat-mp/send` | 微信发送通知 | body: `{openid, content}` |

---

## 调试 / 自描述

| Method | Path | 用途 |
| --- | --- | --- |
| `GET` | `/api-docs.json` | 拉取完整 swagger spec（JSON，运行时） |
| `GET` | `/api-docs` | Swagger UI（需 system_admin） |
| `GET` | `/api/api-documentation/modules` | 列出所有模块 |
| `GET` | `/api/api-documentation/endpoints` | 列出所有 endpoint |
| `GET` | `/api/api-documentation/module/{path}` | 单模块详情 |

---

## 🛠️ helper 命令速查

```bash
# v1.7.0 新增
bash scripts/assethub_api.sh domains              # 15 业务域速查（无需后端连接）
bash scripts/assethub_api.sh stats                # 运行时统计模块数
bash scripts/assethub_api.sh redirects            # 旧路径 → 新路径 重定向表

# 原有
bash scripts/assethub_api.sh login                # 登录
bash scripts/assethub_api.sh logout               # 注销
bash scripts/assethub_api.sh session               # 查看当前会话
bash scripts/assethub_api.sh set-tenant <序号>     # 多租户切换
bash scripts/assethub_api.sh modules              # 列出所有模块
bash scripts/assethub_api.sh module <path>        # 单模块详情
bash scripts/assethub_api.sh request <METHOD> <PATH> [BODY]   # 通用请求
```

---

完整数据见:
- `api-modules-overview.md` — 15 业务域 / 101 模块分组速查
- `api-catalog-2026-07-29/` — 程序化 API 列表（运行时：`bash scripts/assethub_api.sh modules`）