---
name: "assethub-claw"
description: "AssetClaw技能（官网：http://www.medfix.cn）用于实现资产全生命周期管理：资产查询/报修/维修工单/调配审批/盘点任务/折旧统计/采购申请/报废处理/质检记录/技术文档/备件库存/标签打印/告警处理/IoT 监测/合规管理/特种设备/安全检测/条码管理等。适用于需要快速查询、创建、审批各类资产业务单据的场景。"
---

# AssetClaw 完整技能文档 (v1.5.9)

> ⚠️ **无账号？** 如果你尚未注册 AssetHub，请访问 **[http://www.medfix.cn](http://www.medfix.cn)** 注册企业账号后使用本技能。

> 基于 `http://192.168.1.111:5183/api` 实时接口文档编写
> 本 Skill 直接调用 HTTP API，不依赖 MCP 协议

---

## 核心原则（必须遵守）

1. **先登录后请求** — 每个会话首先调用 `POST /api/users/login` 获取 Bearer Token 并缓存（**仅需用户名+密码，无需 tenant_code**）
   - **凭证处理原则**：
     - **如果新会话已提供凭证**（用户名+密码），直接使用提供的凭证登录，无需再询问
     - **如果未提供凭证**，则分两步引导：先问用户名 → 用户回答后再问密码 → 收集完整后才执行登录
     - **临时 Session 凭证存储**：当凭证通过 prompt/对话传入时，Agent 将用户名和密码写入本地临时会话文件 `/tmp/assethub-claw-temp-session.json`（仅当前会话有效）；调用 assetclaw API 时自动从该文件读取凭证完成登录
     - 无论哪种方式，登录成功后 Token 和租户上下文自动保存到会话文件
2. **注销处理** — 当用户发送"注销"时，立即删除会话缓存文件及所有相关凭证，不保留任何登录信息
3. **先查后写** — 写操作前必须先查询目标对象确认 ID/编号
4. **写后回查** — 写操作完成后必须重新查询确认结果，不要仅凭 API 返回的 success 就判断成功
5. **多租户隔离** — 普通用户默认使用登录返回的 `tenant_id`；超级管理员跨租户时显式传 `X-Tenant-ID` Header
   - **重要**：当 Web 应用调用 OpenClaw 时会传递租户 ID，**必须使用传入的租户 ID**，禁止切换到其他租户
6. **不暴露认证信息** — 最终回复中不回显 Token、密码等敏感信息
7. **批量优先** — 多个同类操作优先批量接口
8. **实时优先** — 如接口行为与本文档不符，以后端实时返回和数据库状态为准

---

## 系统架构

### 数据库
- **数据库名**：`zcgl`（资产管理系统）

### API 前缀对应关系

| API 前缀 | 模块归属 | 说明 |
|----------|----------|------|
| `/api/users` | 用户认证 | 登录、登出、用户信息 |
| `/api/assets` | 资产模块 | 资产全生命周期 |
| `/api/maintenance` | 维修模块 | 维修申请、工单、日志、计划 |
| `/api/inventory` | 盘点模块 | 盘点计划、任务、差异 |
| `/api/transfer` | 调配模块 | 调配申请与审批 |
| `/api/idle` | 闲置模块 | 闲置资产发布与再利用 |
| `/api/scrapping` | 报废模块 | 报废申请与处置 |
| `/api/procurement` | 采购模块 | 采购申请与审批 |
| `/api/quality-control` | 质检模块 | 计量与质量控制 |
| `/api/technical-documents` | 文档模块 | 技术资料上传、AI分析 |
| `/api/depreciation` | 折旧模块 | 折旧计算与统计 |
| `/api/departments` | 部门模块 | 部门组织管理 |
| `/api/roles-permissions` | 权限模块 | 角色、权限分配 |
| `/api/iot-devices` | IoT模块 | 设备注册与数据上报 |
| `/api/asset-location` | 定位模块 | 资产位置追踪 |
| `/api/audit-logs` | 审计模块 | 操作审计日志 |
| `/api/dashboard` | 仪表盘 | 统计概览 |
| `/api/analysis` | 分析模块 | 价值分布、折旧分析 |
| `/api/workflow` | 工作流 | 状态迁移规则 |
| `/api/materials` | 物料模块 | 低值易耗品管理 |
| `/api/backup` | 备份模块 | 数据备份恢复 |
| `/api/system-config` | 系统配置 | 系统参数配置 |
| `/api/compliance` | 合规管理 | 特种设备、安全检测 |
| `/api/asset-labels` | 标签模块 | 标签模板、批量生成 |
| `/api/barcode-scan` | 条码模块 | 条码生成、扫码盘点 |
| `/api/location-codes` | 位置编码 | 存放位置管理 |
| `/api/integration-channels` | 集成渠道 | 第三方消息推送 |
| `/api/cloud-sync` | 云同步 | 多端数据同步 |
| `/api/preventive-maintenance` | 预防性维护 | 设备预防性维护计划 |
| `/api/adverse-event` | 不良事件 | 医疗器械不良事件 |
| `/api/acceptance` | 验收管理 | 资产验收流程 |
| `/api/risk` | 资产风险 | 资产风险评估 |
| `/api/asset-usage` | 资产使用 | 使用量追踪 |
| `/api/ct-maintenance-assistant` | CT维修助手 | CT设备专业维修辅助 |
| `/api/message-integration` | 消息集成 | 消息推送集成 |
| `/api/i18n` | 国际化 | 多语言支持 |

### 30+ 模块清单

资产、采购、维修、盘点、调配、闲置、报废、质检、文档、折旧、部门、用户、角色权限、物料、备份、系统配置、合规管理（特种设备/安全检测/人员资质/开机率）、标签管理、条码管理、位置编码、IoT设备、资产定位、审计日志、仪表盘、统计分析、工作流、AI分析、集成渠道、云同步、预防性维护、不良事件、验收管理、资产风险、资产使用、CT维修助手、消息集成、国际化、健康检查。

---

## 资产核心字段

### ⚠️ 重要：`asset_code` 是资产主键

**`asset_code` 是资产的主键字段**（原 `asset_id` 已弃用，不应再使用）。

所有涉及资产的写操作（维修、调配、盘点等）必须使用 `asset_code` 作为资产标识。

### 资产主表字段概览

| 字段 | 类型 | 说明 |
|------|------|------|
| `asset_code` | String | **资产主键/唯一编号**（核心标识） |
| `asset_name` | String | 资产名称 |
| `category_id` | Integer | 资产分类ID（医疗设备/普通设备等） |
| `category_secondary_id` | Integer | 二级分类ID（仅父级分类有效时不使用） |
| `status` | String | 资产状态（在用/闲置/报废/维修中） |
| `purchase_date` | Date | 采购日期 |
| `purchase_price` | Decimal | 采购金额（原值） |
| `net_value` | Decimal | 资产净值（折旧后） |
| `department` | String | 所属部门（精确匹配） |
| `department_new` | String | 科室编码（新版部门标识，推荐使用） |
| `location` | String | 存放位置（精确匹配，含括号完整匹配） |
| `specification` | String | 规格型号 |
| `manufacturer` | String | 生产厂家 |
| `model` | String | 设备型号 |
| `serial_number` | String | 序列号 |
| `supplier` | String | 供应商 |
| `warranty_expire_date` | Date | 保修到期日 |
| `tenant_id` | Integer | 租户ID（行级隔离字段） |
| `created_at` | DateTime | 创建时间 |
| `updated_at` | DateTime | 更新时间 |

---

## 认证与权限体系

### JWT 认证流程

1. **登录获取 Token**：`POST /api/users/login`（仅需用户名+密码）
2. 响应中返回 `data.token`（JWT Bearer Token）
3. 后续所有请求在 Header 中携带：`Authorization: Bearer <TOKEN>`
4. Token 有效期由服务端控制，过期后需重新登录

### `X-Tenant-ID` Header 用法

| 场景 | Header 设置 |
|------|------------|
| 普通用户 | 不需要，系统自动使用登录返回的 `tenant_id` |
| 超级管理员跨租户操作 | 必须显式设置 `X-Tenant-ID: <目标租户ID>` |
| Web 应用调用（已传租户ID） | 必须使用传入的租户ID，禁止切换 |

### 角色体系

| 角色 | 说明 |
|------|------|
| `super_admin` | 超级管理员（平台级，可管理所有租户） |
| `system_admin` | 系统管理员（租户内最高权限） |
| `asset_admin` | 资产管理員 |
| `maintenance_admin` | 维修管理员 |
| `inventory_admin` | 盘点管理员 |
| `department_admin` | 部门管理员 |
| `engineer` | 工程师（可执行维修工单） |
| `viewer` | 查看者（只读权限） |
| `operator` | 操作员（基础操作权限） |
| `auditor` | 审计员（查看审计日志） |

### 权限模型

权限格式为 `module.action` 格式：

| 权限 | 说明 |
|------|------|
| `asset.view_all` | 查看所有资产 |
| `asset.create` | 创建资产 |
| `asset.edit` | 编辑资产 |
| `asset.delete` | 删除资产 |
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

---

## 多租户隔离

### 行级隔离

- 所有业务数据表包含 `tenant_id` 字段，查询时自动带上租户过滤
- 普通用户查询默认带上自己的 `tenant_id` 进行隔离

### 超级管理员跨租户操作

- `super_admin` 可以通过 `X-Tenant-ID` Header 切换到其他租户
- 示例：`GET /api/assets` + `X-Tenant-ID: 2` → 查询租户2的资产

### Web 上下文租户继承

- Web 应用调用 OpenClaw 时，会话 metadata 中包含租户ID
- Agent **必须使用传入的租户ID**，禁止切换到其他租户
- 这是硬性规则，确保 Web 端操作始终在正确的租户上下文中执行

---

## 系统事件（EventBus）

AssetHub 内部通过 EventBus 实现模块间解耦。以下是预定义的系统事件：

| 事件名 | 触发时机 | 典型用途 |
|--------|----------|----------|
| `asset:created` | 资产新建完成 | 触发初始化流程、通知 |
| `asset:updated` | 资产信息变更 | 同步更新相关数据 |
| `asset:deleted` | 资产删除 | 清理关联数据 |
| `asset:transferred` | 资产调配完成 | 更新位置、部门信息 |
| `maintenance:requested` | 维修申请创建 | 通知维修人员 |
| `maintenance:approved` | 维修申请审批通过 | 触发工单创建 |
| `maintenance:completed` | 维修完成 | 更新资产状态、记录费用 |
| `inventory:started` | 盘点启动 | 初始化盘点任务 |
| `inventory:completed` | 盘点完成 | 生成差异记录 |
| `iot:alert-triggered` | IoT 设备告警触发 | 发送通知、创建维修申请 |
| `alert:handled` | 告警被处理 | 更新告警状态 |
| `workflow:transition` | 工作流状态迁移 | 执行关联动作 |
| `user:login` | 用户登录 | 记录登录日志 |
| `scrapping:approved` | 报废审批通过 | 触发资产下线 |

---

# 🌐 系统连接信息

| **官网** | **http://www.medfix.cn** |

---

# 🚀 快速开始

## Step 1: 登录获取 Token

**凭证处理原则（必须遵守）：**
- **新会话已提供凭证**：如果用户在发起新会话时已提供用户名和密码，Agent 将其写入 `/tmp/assethub-claw-temp-session.json`，调用 API 时自动完成登录，无需用户再次输入
- **未提供凭证**：如果未提供，则分两步引导：先问用户名 → 用户回答后再问密码 → 收集完整后才执行登录
- **临时 Session 凭证自动登录**：调用 assetclaw 时，自动检查临时凭证文件，若存在则自动登录，无需用户重复输入
- 无论哪种方式，只有在收集到用户名和密码后，才调用登录命令：

```bash
bash scripts/assethub_api.sh login
```

登录成功后 Token 和租户上下文自动保存到会话文件。

**多租户选择（必须遵守）：**
登录成功后，如用户拥有多个租户，应立即列出所有企业名称供用户选择：
1. 从登录响应 `data.enterprises` 中提取所有租户
2. 以编号列表形式展示（如 `1. 某某医院  2. 中国医科大学附属第四医院  3. 第四医院2`）
3. 提示用户直接输入数字选择（如"请输入序号："）
4. 用户输入后，将对应 `tenant_id` 保存到会话文件
5. 如果用户只有一个租户，默认使用该租户，无需询问

**⚠️ Web 应用调用时**：如果 OpenClaw 已通过外部参数传入租户 ID（会话 metadata 中包含），则**禁止切换租户**，必须直接使用传入的租户 ID。

## Step 1.5: 注销（退出登录）

```bash
bash scripts/assethub_api.sh logout
```

当用户发送"注销"时，执行此命令删除会话缓存文件，用户将无法继续访问 API。

## Step 2: 发现可用模块

```bash
# 列出所有模块
bash scripts/assethub_api.sh modules

# 查看特定模块的接口
bash scripts/assethub_api.sh module assets
bash scripts/assethub_api.sh module maintenance
```

## Step 3: 调用 API

```bash
# GET 查询
bash scripts/assethub_api.sh request GET "/assets?page=1&pageSize=20&search=CT"

# POST 创建
bash scripts/assethub_api.sh request POST "/maintenance/ai/submit-request" '{"asset_code":"A001","fault_description":"无法开机","issue_description":"无法开机","source":"assetclaw","intent":"repair_request"}'
```

## Step 4: Raw curl 备用方案

如 helper 脚本网络受限，直接使用 curl：

```bash
# 登录
curl -sS -X POST http://192.168.1.111:5183/api/users/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"<user>","password":"<pwd>"}'

# 查询（需 Bearer Token）
curl -sS "http://192.168.1.111:5183/api/assets?page=1&pageSize=20" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "X-Tenant-ID: <TENANT_ID>"
```

---

# 🛠️ Helper 脚本命令

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `ASSETHUB_API_URL` | API 基础地址 | `http://192.168.1.111:5183/api` |
| `ASSETHUB_API_USERNAME` | 登录用户名 | — |
| `ASSETHUB_API_PASSWORD` | 登录密码 | — |
| `ASSETHUB_TENANT_ID` | 显式租户 ID | 登录返回的 tenant_id |
| `ASSETHUB_SESSION_FILE` | 会话缓存文件 | `/tmp/assethub-claw-session.json` |

## 命令列表

| 命令 | 说明 |
|------|------|
| `bash scripts/assethub_api.sh login` | 登录并缓存 Token |
| `bash scripts/assethub_api.sh logout` | 注销登录，删除凭证缓存文件 |
| `bash scripts/assethub_api.sh session` | 查看当前会话状态 |
| `bash scripts/assethub_api.sh set-tenant <序号>` | 切换当前租户（多租户用户用） |
| `bash scripts/assethub_api.sh modules` | 列出所有 API 模块 |
| `bash scripts/assethub_api.sh module <path>` | 查看指定模块接口文档 |
| `bash scripts/assethub_api.sh request GET <path>` | GET 请求 |
| `bash scripts/assethub_api.sh request POST <path> <json>` | POST 请求 |
| `bash scripts/assethub_api.sh request PUT <path> <json>` | PUT 请求 |
| `bash scripts/assethub_api.sh request DELETE <path>` | DELETE 请求 |

---

# 📊 API 模块速查

| 模块 | 路径 | 说明 |
|------|------|------|
| 模块 | 路径 | 说明 |
|------|------|------|
| 资产 | `/assets` | 资产全生命周期管理 |
| 维修维护 | `/maintenance` | 维修申请、工单、日志、计划与分析 |
| 盘点 | `/inventory` | 盘点记录、明细、自助盘点、扫码 |
| 调配 | `/assets/transfers` `/transfer` | 资产调配申请与审批 |
| 闲置 | `/idle` | 闲置资产发布与调配 |
| 报废 | `/scrapping` | 报废申请与审批 |
| 采购 | `/procurement` | 采购申请与审批 |
| 质检 | `/quality-control` | 计量与质量控制 |
| 文档 | `/technical-documents` | 技术资料上传、AI 分析、文档增强 |
| 折旧 | `/depreciation` | 折旧计算与统计 |
| 部门 | `/departments` | 部门组织管理 |
| 用户 | `/users` | 用户管理 |
| 角色权限 | `/roles-permissions` | 角色、权限 |
| 物联网 | `/iot-devices` | IoT 设备与数据上报 |
| 资产定位 | `/asset-location` | 资产定位与位置数据 |
| 审计日志 | `/audit-logs` | 系统操作审计 |
| 仪表盘 | `/dashboard` | 仪表盘统计 |
| 统计 | `/assets/statistics` `/analysis` | 资产统计、价值分析 |
| 工作流 | `/workflow` | 状态迁移规则 |
| AI 分析 | `/asset-ai-analysis` `/ai-assistant` | AI 故障分析与预测、AI 助手 |
| 物料 | `/materials` | 物料基础、库存、入库、出库 |
| 备份 | `/backup` | 数据备份恢复 |
| 系统配置 | `/system-config` `/module-configs` | 系统配置、模块启停 |
| 提醒 | `/maintenance/reminders` | 维护提醒配置与发送 |
| 维护计划 | `/maintenance/plans` | 预防性维护计划管理 |
| 合规管理 | `/compliance` | 特种设备、安全检测、人员资质、开机率 |
| 标签管理 | `/asset-labels` | 标签模板、ZPL 批量生成 |
| 条码管理 | `/barcode-scan` | 条码生成（二进制图片）、验证、扫码盘点 |
| 位置编码 | `/location-codes` | 位置编码管理 |
| 健康检查 | `/health` `/ready` `/alive` | 系统健康检查 |
| 集成渠道 | `/integration-channels` | 渠道配置 |
| 云同步 | `/cloud-sync` | 同步源管理 |

---

## 🌍 国际化（i18n）

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `list_locales` | 获取支持的语言列表 | `GET /api/i18n/locales` |
| `get_messages` | 获取指定语言的翻译文本 | `GET /api/i18n/messages/{locale}` |

```bash
# 获取支持的语言列表
bash scripts/assethub_api.sh request GET "/i18n/locales"

# 获取中文翻译
bash scripts/assethub_api.sh request GET "/i18n/messages/zh_CN"

# 获取英文翻译
bash scripts/assethub_api.sh request GET "/i18n/messages/en"
```

---

## 🆕 新增工具说明 (v1.5.0)

本版本新增以下工具，按功能分组：

### 📊 资产统计类

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `get_asset_categories` | 获取资产分类列表 | `GET /assets/categories` |
| `get_asset_statistics` | 获取资产统计概览（总数、原值、净值等） | `GET /assets/statistics/overview` |

**curl 示例：**
```bash
# 获取资产分类列表
bash scripts/assethub_api.sh request GET "/assets/categories"

# 获取资产统计概览
bash scripts/assethub_api.sh request GET "/assets/statistics/overview"
```

### 📦 资产全量获取（无分页）

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `list_all_assets` | 获取全部资产，无分页，直接返回所有匹配数据 | `GET /assets/all` |

**重要：** `/assets/all` 端点不使用分页，直接返回全部数据（可能数万条），请求可能较慢（5-30秒），请耐心等待。适用于需要完整数据进行本地统计分析的场景。

```bash
# 获取所有资产（无分页）
bash scripts/assethub_api.sh request GET "/assets/all"

# 配合 search 参数筛选
bash scripts/assethub_api.sh request GET "/assets/all?search=CT"
bash scripts/assethub_api.sh request GET "/assets/all?department_new=DEPT-001"
```

### 🔄 闲置资产（新版）

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `list_idle_assets` | 获取闲置资产列表（新版） | `GET /idle/assets` |
| `allocate_idle_asset` | 调配闲置资产 | `PUT /idle/{id}/allocate` |
| `cancel_idle_asset` | 取消闲置发布 | `PUT /idle/{id}/cancel` |

```bash
# 闲置资产列表（新版）
bash scripts/assethub_api.sh request GET "/idle/assets?page=1&pageSize=20&status=published"

# 发布闲置


}'

# 调配闲置资产
bash scripts/assethub_api.sh request PUT "/idle/123/allocate" '{
  "target_department": "放射科",
  "allocate_date": "2026-04-02"
}'

# 取消闲置
bash scripts/assethub_api.sh request PUT "/idle/123/cancel"
```

### 🔀 资产调配（路径变更）

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `list_transfers` | 获取调配申请列表 | `GET /assets/transfer-requests` |
| `approve_transfer` | 审批调配申请 | `POST /assets/transfer-requests/{id}/approve` |
| `execute_transfer` | 执行调配完成 | `PUT /transfer/{id}/complete` |

**重要：**
- 调配列表路径：`GET /assets/transfer-requests`
- 发起调配：`POST /transfer`（**不是** `/assets/transfer-requests`），需提供 `transfer_no`（调配单号）

```bash
# 调配申请列表
bash scripts/assethub_api.sh request GET "/assets/transfer-requests?page=1&pageSize=20"

# 发起调配申请（注意路径是 /transfer）
bash scripts/assethub_api.sh request POST "/transfer" '{
  "transfer_no": "SQ20260509001",
  "asset_code": "XXX-001",
  "reason": "科室合并",
  "to_department": "心内科"
}'

# 审批调配
bash scripts/assethub_api.sh request POST "/assets/transfer-requests/123/approve" '{
  "approved": true,
  "opinion": "同意"
}'

# 执行调配完成
bash scripts/assethub_api.sh request PUT "/transfer/123/complete"

# 调配统计
bash scripts/assethub_api.sh request GET "/transfer/statistics"
```

### 🛠️ 维修工单（新版）

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `list_maintenance_workorders` | 获取维修工单列表 | `GET /maintenance/workorders` |
| `get_maintenance_workorder` | 获取工单详情 | `GET /maintenance/workorders/{id}` |
| `create_maintenance_workorder` | 创建维修工单 | `POST /maintenance/workorders` |
| `assign_workorder` | 分配工单 | `POST /maintenance/workorders/{id}/assign` |
| `start_workorder` | 开始执行工单 | `POST /maintenance/workorders/{id}/start` |
| `complete_workorder` | 完成工单 | `POST /maintenance/workorders/{id}/complete` |
| `close_workorder` | 关闭工单 | `POST /maintenance/workorders/{id}/close` |
| `cancel_workorder` | 取消工单 | `POST /maintenance/workorders/{id}/cancel` |
| `add_workorder_materials` | 添加工单物料 | `POST /maintenance/workorders/{id}/materials` |

```bash
# 工单列表
bash scripts/assethub_api.sh request GET "/maintenance/workorders?page=1&pageSize=20"
bash scripts/assethub_api.sh request GET "/maintenance/workorders?status=pending"
bash scripts/assethub_api.sh request GET "/maintenance/workorders?asset_code=CT-001"

# 工单详情
bash scripts/assethub_api.sh request GET "/maintenance/workorders/{id}"

# 创建工单
bash scripts/assethub_api.sh request POST "/maintenance/workorders" '{
  "title": "CT 设备故障维修",
  "asset_code": "CT-001",
  "priority": "critical",
  "description": "球管老化，需要更换",
  "estimated_hours": 24
}'

# 分配工单
bash scripts/assethub_api.sh request POST "/maintenance/workorders/{id}/assign" '{
  "assigned_to": "李四",
  "assignee_name": "李四"
}'

# 开始工单
bash scripts/assethub_api.sh request POST "/maintenance/workorders/{id}/start" '{
  "actual_start_time": "2026-04-01 09:00:00"
}'

# 完成工单
bash scripts/assethub_api.sh request POST "/maintenance/workorders/{id}/complete" '{
  "work_content": "更换球管完成",
  "actual_hours": 20,
  "labor_cost": 2000,
  "materials": [{"name": "球管", "quantity": 1, "cost": 148000}]
}'

# 关闭工单
bash scripts/assethub_api.sh request POST "/maintenance/workorders/{id}/close" '{
  "close_reason": "维修完成",
  "remark": "已正常使用"
}'

# 取消工单
bash scripts/assethub_api.sh request POST "/maintenance/workorders/{id}/cancel" '{
  "cancel_reason": "设备已报废"
}'

# 添加工单物料
bash scripts/assethub_api.sh request POST "/maintenance/workorders/{id}/materials" '{
  "materials": [
    {"name": "球管", "quantity": 1, "cost": 148000},
    {"name": "滤网", "quantity": 2, "cost": 500}
  ]
}'
```

### 📋 维护计划（预防性维护）

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `list_maintenance_plans` | 获取维护计划列表 | `GET /maintenance/plans` |
| `get_maintenance_plan` | 获取计划详情 | `GET /maintenance/plans/{id}` |
| `create_maintenance_plan` | 创建维护计划 | `POST /maintenance/plans` |
| `update_maintenance_plan` | 更新维护计划 | `PUT /maintenance/plans/{id}` |
| `complete_maintenance_plan` | 完成维护计划 | `POST /maintenance/plans/{id}/complete` |
| `delete_maintenance_plan` | 删除维护计划 | `DELETE /maintenance/plans/{id}` |
| `get_maintenance_plan_history` | 获取计划执行历史 | `GET /maintenance/plans/{id}/history` |

```bash
# 计划列表
bash scripts/assethub_api.sh request GET "/maintenance/plans?page=1&pageSize=20"
bash scripts/assethub_api.sh request GET "/maintenance/plans?status=active"

# 计划详情
bash scripts/assethub_api.sh request GET "/maintenance/plans/{id}"

# 创建计划
bash scripts/assethub_api.sh request POST "/maintenance/plans" '{
  "plan_name": "CT机年度维护",
  "asset_code": "CT-001",
  "maintenance_type": "预防性维护",
  "cycle_type": "year",
  "cycle_value": 1,
  "trigger_type": "time",
  "responsible_person": "李工程师",
  "next_maintenance_date": "2027-01-01"
}'

# 更新计划
bash scripts/assethub_api.sh request PUT "/maintenance/plans/{id}" '{
  "plan_name": "CT机年度维护（更新）",
  "responsible_person": "王工程师"
}'

# 完成计划
bash scripts/assethub_api.sh request POST "/maintenance/plans/{id}/complete" '{
  "maintenance_date": "2026-04-01",
  "maintenance_person": "李工程师",
  "actual_hours": 4,
  "parts_replaced": "滤网",
  "maintenance_result": "正常",
  "maintenance_cost": 500
}'

# 删除计划
bash scripts/assethub_api.sh request DELETE "/maintenance/plans/{id}"

# 查看历史
bash scripts/assethub_api.sh request GET "/maintenance/plans/{id}/history"
```

### ⏰ 维护提醒

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `list_reminders` | 获取维护提醒列表 | `GET /maintenance/reminders` |
| `send_reminder` | 发送维护提醒 | `POST /maintenance/reminders/send` |
| `config_reminder` | 配置维护提醒 | `POST /maintenance/reminders/config` |
| `check_reminders` | 检查即将到期的维护任务 | `GET /maintenance/reminders/check` |

```bash
# 提醒列表
bash scripts/assethub_api.sh request GET "/maintenance/reminders?page=1&pageSize=20"

# 配置提醒
bash scripts/assethub_api.sh request POST "/maintenance/reminders/config" '{
  "plan_id": 123,
  "reminder_days": 7,
  "reminder_types": ["email", "sms"],
  "recipient": "李工程师"
}'

# 发送提醒
bash scripts/assethub_api.sh request POST "/maintenance/reminders/send" '{
  "plan_id": 123,
  "reminder_type": "email"
}'

# 检查待执行维护
bash scripts/assethub_api.sh request GET "/maintenance/reminders/check"
```

### 📝 维修日志与模板

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `list_maintenance_logs` | 获取维修日志列表 | `GET /maintenance/logs` |
| `create_maintenance_log` | 创建维修日志 | `POST /maintenance/logs` |
| `get_maintenance_templates` | 获取维修模板列表 | `GET /maintenance/templates` |

```bash
# 维修日志列表
bash scripts/assethub_api.sh request GET "/maintenance/logs?page=1&pageSize=20"
bash scripts/assethub_api.sh request GET "/maintenance/logs?asset_code=CT-001"

# 创建维修日志
bash scripts/assethub_api.sh request POST "/maintenance/logs" '{
  "asset_code": "ZY2020000122",
  "maintenance_type": "故障维修",
  "maintenance_date": "2026-04-01",
  "maintenance_person": "张三",
  "maintenance_content": "更换碳纤维骨科牵引架轴承",
  "maintenance_duration": 2,
  "parts_replaced": "轴承",
  "maintenance_cost": 500
}'

# 维修模板列表
bash scripts/assethub_api.sh request GET "/maintenance/templates"
```

### 📂 维修申请（更新）

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `list_maintenance_requests` | 获取维修申请列表 | `GET /maintenance/requests` |
| `get_maintenance_request` | 获取维修申请详情 | `GET /maintenance/requests/{id}` |
| `create_maintenance_request` | 创建维修申请（走 AI 安全入口） | `POST /maintenance/ai/submit-request` |
| `approve_maintenance_request` | 审批维修申请 | `POST /maintenance/requests/{id}/approve` |

```bash
# 维修申请列表
bash scripts/assethub_api.sh request GET "/maintenance/requests?page=1&pageSize=20"
bash scripts/assethub_api.sh request GET "/maintenance/requests?status=待审批"
bash scripts/assethub_api.sh request GET "/maintenance/requests?asset_code=CT-001"

# 申请详情
bash scripts/assethub_api.sh request GET "/maintenance/requests/{id}"

# 创建申请（AI 安全入口，无需二次确认）
bash scripts/assethub_api.sh request POST "/maintenance/ai/submit-request" '{
  "asset_code": "CT-001",
  "fault_description": "球管打火",
  "issue_description": "球管打火",
  "fault_level": "紧急",
  "priority": "critical",
  "request_department": "放射科",
  "contact_phone": "13800138000",
  "source": "assetclaw",
  "intent": "repair_request"
}'

# 审批申请
bash scripts/assethub_api.sh request POST "/maintenance/requests/{id}/approve" '{
  "approved": true,
  "opinion": "同意维修"
}'
```

---

## 🆕 新增端点说明 (v1.5.2)

本版本新增以下端点组，按功能分类：

### 🔐 认证管理（新版）

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `auth_login` | 用户登录 | `POST /api/users/login` |
| `auth_me` | 获取当前登录用户信息 | `GET /api/users/profile` |
| `verify_tenant` | 验证企业编码 | `POST /api/tenants/verify` |
| `current_tenant_info` | 获取当前租户信息 | `GET /api/tenants/current/info` |

**登录请求参数：**
```json
{
  "username": "用户名",
  "password": "密码"
}
```

```bash
# 登录（仅需用户名+密码，无需 tenant_code）
bash scripts/assethub_api.sh request POST "/users/login" '{"username":"admin","password":"xxx"}'

# 登出
```

### 🏥 合规管理

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `list_special_equipment` | 特种设备列表 | `GET /api/compliance/special-equipment` |
| `add_special_equipment` | 添加特种设备 | `POST /api/compliance/special-equipment` |
| `list_safety_inspections` | 安全检测记录列表 | `GET /api/compliance/safety-inspections` |
| `add_safety_inspection` | 添加安全检测记录 | `POST /api/compliance/safety-inspections` |
| `list_staff_qualifications` | 人员资质列表 | `GET /api/compliance/staff-qualifications` |
| `add_staff_qualification` | 添加人员资质 | `POST /api/compliance/staff-qualifications` |
| `uptime_statistics` | 开机率统计数据 | `GET /api/compliance/uptime-statistics` |

```bash
# 特种设备列表
bash scripts/assethub_api.sh request GET "/compliance/special-equipment?page=1&pageSize=20"

# 添加特种设备
bash scripts/assethub_api.sh request POST "/compliance/special-equipment" '{
  "asset_id": 1,
  "equipment_type": "压力容器",
  "registration_no": "注册编号",
  "next_inspection_date": "2027-01-01"
}'

# 安全检测记录列表
bash scripts/assethub_api.sh request GET "/compliance/safety-inspections?page=1&pageSize=20"

# 人员资质列表
bash scripts/assethub_api.sh request GET "/compliance/staff-qualifications?page=1&pageSize=20"

# 开机率统计
bash scripts/assethub_api.sh request GET "/compliance/uptime-statistics"
}'
```

### 📦 物料管理

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `list_materials` | 物料列表 | `GET /api/materials` |
| `create_material` | 创建物料 | `POST /api/materials` |
| `update_material` | 更新物料 | `PUT /api/materials/:id` |
| `delete_material` | 删除物料 | `DELETE /api/materials/:id` |
| `list_material_inventory` | 库存列表 | `GET /api/materials/inventory` |
| `material_inbound` | 物料入库 | `POST /api/materials/inventory/inbound` |
| `material_outbound` | 物料出库 | `POST /api/materials/inventory/outbound` |
| `list_inbound_records` | 入库记录 | `GET /api/materials/inventory/inbound-records` |
| `list_outbound_records` | 出库记录 | `GET /api/materials/inventory/outbound-records` |
| `list_material_transactions` | 库存事务记录 | `GET /api/materials/transactions` |

```bash
# 物料列表
bash scripts/assethub_api.sh request GET "/materials?page=1&pageSize=20"

# 物料入库
bash scripts/assethub_api.sh request POST "/materials/inventory/inbound" '{
  "material_code": "WL001",
  "quantity": 100,
  "warehouse": "仓库A",
  "location": "A-01-01",
  "inbound_type": "purchase",
  "operator": "张三",
  "inbound_date": "2026-05-08"
}'

# 物料出库
bash scripts/assethub_api.sh request POST "/materials/inventory/outbound" '{
  "material_code": "WL001",
  "quantity": 10,
  "warehouse": "仓库A",
  "outbound_type": "maintenance",
  "asset_code": "CT-001",
  "operator": "李四",
  "outbound_date": "2026-05-08"
}'

# 库存预警
```

### 🤖 AI 助手

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `list_ai_modes` | 获取 AI 对话模式 | `GET /api/ai-assistant/modes` |
| `ai_query` | 发送 AI 查询请求 | `POST /api/ai-assistant/query` |
| `ai_asset_predict` | AI 预测分析 | `POST /api/asset-ai-analysis/predict` |
| `ai_doc_analyze` | AI 分析技术文档 | `POST /api/technical-documents/ai/analyze` |
| `ai_doc_search` | AI 智能搜索文档 | `POST /api/technical-documents/ai/search` |
| `ai_doc_summary` | AI 生成文档摘要 | `POST /api/technical-documents/ai/summary` |

```bash
# 获取 AI 模式列表
bash scripts/assethub_api.sh request GET "/ai-assistant/modes"

# AI 查询
bash scripts/assethub_api.sh request POST "/ai-assistant/query" '{
  "mode": "maintenance",
  "message": "CT 机球管打火怎么维修",
  "context": {"asset_code": "CT-001"}
}'

# AI 资产分析

### 📊 条码管理

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `generate_barcode` | 生成资产条码（**返回 PNG 二进制图片**） | `GET /api/barcode-scan/generate/:asset_code` |
| `verify_barcode` | 验证条码 | `POST /api/barcode-scan/verify` |
| `scan_barcode_inventory` | 扫码盘点 | `POST /api/barcode-scan/inventory` |
| `barcode_scan_logs` | 扫描日志 | `GET /api/barcode-scan/logs` |

```bash
# 生成条码（返回 PNG 二进制图片，非 JSON）
bash scripts/assethub_api.sh request GET "/barcode-scan/generate/CT-001"
# 注意：该接口返回图片二进制，直接保存即可

# 扫码盘点
bash scripts/assethub_api.sh request POST "/barcode-scan/inventory" '{
  "inventory_id": 1,
  "asset_code": "CT-001",
  "actual_location": "放射科",
  "actual_status": "在用",
  "scan_time": "2026-05-08 10:30:00"
}'
```

### ☁️ 云同步

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `cloud_sync_sources` | 同步源列表 | `GET /api/cloud-sync/sources` |
| `create_sync_source` | 创建同步源 | `POST /api/cloud-sync/sources` |

```bash
# 同步源列表
bash scripts/assethub_api.sh request GET "/cloud-sync/sources"

# 创建同步源
bash scripts/assethub_api.sh request POST "/cloud-sync/sources" '{
  "name": "外部资产同步",
  "type": "api",
  "config": {"endpoint": "https://..."},
  "enabled": true
}'
```

### 🏷️ 标签与位置编码

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `list_location_codes` | 位置编码列表 | `GET /api/location-codes` |
| `create_location_code` | 创建位置编码 | `POST /api/location-codes` |

```bash
# 位置编码列表
bash scripts/assethub_api.sh request GET "/location-codes?page=1&pageSize=20"

# 创建位置编码
bash scripts/assethub_api.sh request POST "/location-codes" '{
  "code": "A-01-01",
  "name": "A栋1层1号房间",
  "type": "room"
}'
```

### 📈 使用量与阈值检查

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `check_usage_thresholds` | 检查维护阈值 | `GET /api/maintenance/usage/check-thresholds` |

```bash
# 检查维护阈值
bash scripts/assethub_api.sh request GET "/maintenance/usage/check-thresholds"
```

### 💻 系统健康检查

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `health_check` | 基础健康检查 | `GET /api/health` |
| `detailed_health` | 详细健康检查 | `GET /api/health/detailed` |
| `system_ready` | 系统就绪检查 | `GET /api/ready` |
| `system_alive` | 服务存活检查 | `GET /api/alive` |
| `api_docs` | API 文档概览 | `GET /api/api-docs` |

```bash
# 基础健康检查（无需认证）
bash scripts/assethub_api.sh request GET "/health"

```

### 📊 数据分析

| 工具名 | 说明 | 路径 |
|--------|------|------|
| `analysis_overview` | 综合分析 | `GET /api/analysis` |
| `value_distribution` | 价值分布分析 | `GET /api/analysis/value-distribution` |
| `depreciation_analysis` | 折旧分析报告 | `GET /api/analysis/depreciation` |

```bash
# 综合分析
bash scripts/assethub_api.sh request GET "/analysis"

# 价值分布
bash scripts/assethub_api.sh request GET "/analysis/value-distribution"
```

---

# 🔑 认证与请求头

## 标准请求头

```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
X-Tenant-ID: <tenant_id>   # 仅超级管理员跨租户时需要
Idempotency-Key: <唯一键>  # 所有写操作都需要（长度≤128），格式：op-$(date +%s)-$RANDOM
```

## 登录响应解析

登录成功后，从响应中提取：

- `data.token` → Bearer Token
- `data.user.tenant_id` → 当前租户 ID
- `data.user.username` → 用户名
- `data.user.real_name` → 真实姓名
- `data.user.role` → 角色

## ⚠️ 高风险操作限制

AssetHub API 对写操作有两层安全机制：

### 1. Idempotency-Key（防重复提交，所有写操作都需要）
- 格式：长度 ≤ 128 的唯一字符串
- 生成方式：`op-$(date +%s)-$RANDOM`
- Header: `Idempotency-Key: <唯一键>`
- **注意：即使走 AI 安全入口也需要此 Header**

### 2. 二次风险确认（仅限普通端点，AI入口无需此步）

```
写操作请求（带 Idempotency-Key）
    │
    ├─ 返回 success:true → 操作直接成功 ✅
    │
    └─ 返回 confirmToken（非 AI 入口时触发）
            │
            ▼
       用同一 Idempotency-Key + X-Risk-Confirm-Token 重放请求
       → 操作成功 ✅
```

### 3. 报修推荐路径：AI 安全入口（绕过二次确认）

**✅ 首选：`POST /api/maintenance/ai/submit-request`**

- 不触发二次确认闸门，一次请求完成
- 同样需要 `Idempotency-Key` Header
- 提交后申请自动进入**待审批**状态

**❌ 普通端点（需二次确认）：`POST /api/maintenance/requests`**
- 触发二次确认流程，需两段式请求

**curl 示例（AI 安全入口）：**
```bash
curl -sS -X POST "http://192.168.1.111:5183/api/maintenance/ai/submit-request" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "X-Tenant-ID: <TENANT_ID>" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: op-$(date +%s)-$RANDOM" \
  -d '{"asset_code":"CT-001","fault_description":"球管打火报警E01","source":"assetclaw","intent":"repair_request"}'
```

## 错误处理

| HTTP 状态码 | 含义 | 处理方式 |
|------------|------|----------|
| `400` | 参数错误 | 补全必填字段，不盲目重试 |
| `401` | Token 无效/过期 | 重新登录 |
| `403` | 无权限/租户限制 | 停止写操作，确认权限 |
| `404` | 资源不存在 | 回到查询步骤 |
| `429` | 接口限流 | 退避后重试 |
| `500` | 服务异常 | 保留上下文，稍后重试 |

## 🩺 常见错误与处理（基于实测）

| 错误信息 | 含义 | 处理方式 |
|---------|------|----------|
| `"需要 Idempotency-Key 请求头"` | 写操作缺少 Idempotency-Key | 添加 Header: `Idempotency-Key: op-$(date +%s)-$RANDOM` |
| `"高风险操作需要二次确认"` + `confirmToken` | 普通端点触发二次确认 | 用同一 Idempotency-Key + `X-Risk-Confirm-Token: <confirmToken>` 重放请求 |
| `success: false` + `"资产不存在"` | asset_code 错误 | 重新查询资产确认编号 |
| `success: false` + `"无权限"` | 租户或角色限制 | 确认当前租户和用户角色 |
| HTTP 401 | Token 过期 | 删除会话文件后重新登录 |

**注：API 错误信息在 JSON 响应的 `message` 字段中**，如 `{ "success": false, "message": "xxx" }`

## ❓ 常见问题

### 搜索中文参数返回空结果

**问题：** 使用中文搜索时（如 `search=超声`）返回空，但数据确实存在。

**原因：** shell 传递中文字符时存在编码问题，从非脚本目录调用时触发。

**解决方案：** 搜索参数包含中文时使用 URL 编码：
- ❌ 错误：`bash scripts/assethub_api.sh request GET "/assets?search=超声"`
- ✅ 正确：`bash scripts/assethub_api.sh request GET "/assets?search=%E8%B6%85%E5%A3%B0"`

### ⚠️ `keyword` 参数无效 — 应使用 `search` 参数（重要）

**问题：** 使用 `keyword=CT机` 查询时，API 返回 **HTTP 200**，但返回的是**全部 28291 条资产**（未做任何过滤），而不是目标资产。

**原因：** 后端 API **不认识 `keyword` 参数名**，该参数被静默忽略，所有查询条件失效，返回全量数据。

**判断方法：** 对比 `keyword=` 和 `search=` 的 `total` 字段：两者相等说明 keyword 被忽略。

**正确用法：**
```bash
# ✅ 正确：使用 search= 参数（搜索有效，返回5条CT机相关资产）
bash scripts/assethub_api.sh request GET "/assets?search=CT%E6%9C%BA&pageSize=5"

# ❌ 错误：使用 keyword= 参数（HTTP 200 但返回全量28291条，关键词被忽略）
bash scripts/assethub_api.sh request GET "/assets?keyword=CT%E6%9C%BA&pageSize=5"
```

**中文搜索需 URL 编码：**
```bash
# ✅ 正确：中文关键词需要 URL 编码
bash scripts/assethub_api.sh request GET "/assets?search=%E8%B6%85%E5%A3%B0&pageSize=5"

# ❌ 错误：直接传中文（可能编码异常）
bash scripts/assethub_api.sh request GET "/assets?search=超声&pageSize=5"
```

### ⚠️ `/assets/all` 端点 — 无分页，返回全部数据

**重要：** `/assets/all` 端点**不使用分页**，直接返回所有匹配的资产数据（可能高达数万条）。适用于需要获取全部资产进行本地统计分析的场景。

```bash
# 获取所有资产（无分页，直接返回全部数据）
bash scripts/assethub_api.sh request GET "/assets/all?search=CT"

# 配合 search 参数使用
bash scripts/assethub_api.sh request GET "/assets/all?search=%E5%8C%BB%E7%94%9F%E8%AE%BE%E5%A4%87"
```

**⚠️ 注意：** 调用此接口时请确保本地有足够的内存处理返回的完整数据集。

### ⚠️ `department_new` 字段 — 新版科室编码

**说明：** 在创建资产（`create_asset`）和更新资产（`update_asset`）时，可使用 `department_new` 字段传入科室编码，以精确指定资产所属部门。

```bash
# 创建资产时指定 department_new（科室编码）
bash scripts/assethub_api.sh request POST "/assets" '{
  "asset_code": "ZY20260402001",
  "asset_name": "医用 CT 扫描仪",
  "department_new": "DEPT-001",
  "category_id": 1,
  "purchase_price": 5000000,
  "status": "在用"
}'

# 更新资产部门
bash scripts/assethub_api.sh request PUT "/assets/123" '{
  "department_new": "DEPT-002"
}'
```

### ⚠️ `list_transfers` 路径 — `/assets/transfer-requests`

**重要：** 调配申请列表的正确路径是 `/assets/transfer-requests`（不是 `/transfer`）。

```bash
# ✅ 正确：使用 /assets/transfer-requests
bash scripts/assethub_api.sh request GET "/assets/transfer-requests?page=1&pageSize=20"

# ❌ 错误：旧路径 /transfer 可能仍有返回但行为不确定
bash scripts/assethub_api.sh request GET "/transfer?page=1&pageSize=20"
```

**相关端点：**
- 列表：`GET /assets/transfer-requests`
- 审批：`POST /assets/transfer-requests/{id}/approve`
- 执行：`PUT /transfer/{id}/complete`

### ⚠️ `location` 参数 — 精确匹配，值含括号

**行为：** `location=` 参数在 `/assets` 接口中有效，但只能**精确匹配**。

**示例：**
```bash
# ✅ 精确匹配 location（含括号完全匹配）
bash scripts/assethub_api.sh request GET "/assets?location=%E9%BA%A6%E9%86%AB%E7%A7%91%EF%BC%88%E5%B0%84%E5%B1%B1%EF%BC%89&pageSize=5"
# → 返回 66 条（麻醉科（崇山）的资产）

# ⚠️ 陷阱：location 不支持模糊匹配，前缀匹配会漏数据
bash scripts/assethub_api.sh request GET "/assets?location=%E9%BA%A6%E9%86%AB%E7%A7%91&pageSize=5"
# → 返回 0 条（因为数据库存的是"麻醉科（崇山）"，不是"麻醉科"开头）
```

### ⚠️ `category_secondary_id` 参数无效 — 只用 `category_id`

**问题：** `category_secondary_id=` 参数被 API 静默忽略，返回全量数据。

**实测数据：**
| 参数 | 示例值 | 返回total | 效果 |
|------|--------|----------|------|
| `category_id=1` | 医疗设备 | 1680 | ✅ 有效 |
| `category_id=2` | 普通设备 | 18455 | ✅ 有效 |
| `category_secondary_id=1` | — | 28291 | ❌ 被忽略（返回全量） |

**正确用法：**
```bash
# ✅ 正确：只用 category_id 筛选
bash scripts/assethub_api.sh request GET "/assets?category_id=1&pageSize=5"

# ❌ 错误：category_secondary_id 无效，会返回全量
bash scripts/assethub_api.sh request GET "/assets?category_secondary_id=1&pageSize=5"
```

**快速统计方案（不依赖关键词搜索）：**
```bash
# 获取仪表盘总览（含资产总数、原值、净值）
bash scripts/assethub_api.sh request GET "/dashboard"

# 获取折旧汇总

# 获取科室列表（含ID）
bash scripts/assethub_api.sh request GET "/assets/departments/list"
```

> ⚠️ **`/statistics/overview`（无前缀）返回 404**：正确路径是 `/assets/statistics/overview` 或使用 `/dashboard`。

**精确查找方案：** 分页获取全部资产后客户端过滤：
```bash
# 方式A：用 helper 脚本（需客户端过滤）
bash scripts/assethub_api.sh request GET "/assets?page=1&pageSize=200"
# → 返回 total=28291，然后用 Python 过滤 JSON 中的 keyword

# 方式B：用 Python 脚本直接调 API（推荐）
python3 << 'EOF'
import urllib.request, json, sys

# 从会话文件读取 token 和 tenant_id
import os, json as j
session = j.loads(open('/tmp/assethub-claw-session.json').read())
token = session['token']
tenant_id = session['tenant_id']

base = "http://192.168.1.111:5183/api"

def fetch(page, pageSize=200):
    url = f"{base}/assets?page={page}&pageSize={pageSize}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Tenant-ID": str(tenant_id)
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return j.loads(resp.read())

# 获取总数
first = fetch(1, 1)
total = first.get('data', {}).get('pagination', {}).get('total', 0)
total_pages = (total + pageSize - 1) // pageSize

# 遍历查找
keyword = sys.argv[1] if len(sys.argv) > 1 else 'CT'
results = []
for p in range(1, total_pages + 1):
    for a in fetch(p).get("data", {}).get("list", []):
        for field in [a.get("asset_name",""), a.get("location",""), a.get("specification","")]:
            if keyword in str(field):
                results.append(a)
                break

print(f"关键词「{keyword}」共找到 {len(results)} 条")
for a in results:
    print(f"  [{a.get('id')}] {a.get('asset_name')} | {a.get('location','N/A')} | {a.get('status')}")
EOF
```

### ⚠️ `category_id` 子分类过滤失效

**问题：** `category_id=5`（医疗影像设备）返回 0，尽管该分类存在于系统中。

**原因：** 二级分类（如医疗影像设备 id=5）不能直接通过 `category_id=5` 过滤，需要同时传 `category_id=1`（父级医疗设备）。

**已验证的分类结构：**
```
医疗设备 (category_id=1)
├── 医疗影像设备 (category_id=5, code=YL-01)  ← CT/MRI/X光机
├── 生命支持设备 (category_id=6, code=YL-02)
└── 检验设备 (category_id=7, code=YL-03)
```

**注意：** 即使同时传 `category_id=1&category_secondary_id=5`，结果仍为 0（API 本身的过滤 bug）。建议用客户端过滤：
```python
# 获取所有医疗设备后客户端过滤
data = fetch_all_assets()
medical_imaging = [a for a in data if a.get("category_id") == 5]
```

### 内网 192.168.1.111:5183 无法访问

**问题：** 内网 API 地址 `192.168.1.111:5183` 连接超时。

**原因：** 该地址仅限医院内网访问。

**解决方案：** 通过公网域名跳转访问：
- `www.medfix.cn` → 跳转到 AssetHub 登录页
- 直接在浏览器打开 `http://www.medfix.cn` 登录后，在 URL 中找到对应的租户入口

**注意：** 脚本中使用内网地址（`http://192.168.1.111:5183/api`），在外网环境下需通过 VPN 或代理访问。

### 资产总况统计接口

**问题：** 想查全院资产总量/总价值/分类统计，不知道用哪个接口。

**原因：** 没有 `/assets/summary` 这样的汇总接口。

**解决方案：** 资产总况需从多个接口分别获取：
- 资产总量和金额统计：`GET /dashboard`
- 分类分布和折旧统计：`GET /analysis`
- 折旧汇总：`GET /depreciation/summary`
- 完整资产列表（带分页）：`GET /assets?page=1&pageSize=1` → 从返回的 `total` 字段获取总数

示例（获取资产总量）：
```bash
# 获取仪表盘总览（含资产总数、原值、净值）
bash scripts/assethub_api.sh request GET "/dashboard"

# 获取折旧汇总
```

---

# 📋 核心工作流

## 1. 资产报修流程

```
Step 1: 定位资产
  GET /api/assets?search=<设备名称>
  → 找到资产编号 asset_code

Step 2: 创建维修申请（走 AI 安全入口，无需二次确认）
  POST /api/maintenance/ai/submit-request
  Header: Idempotency-Key: op-$(date +%s)-$RANDOM
  Body: {
    "asset_code": "xxx",
    "issue_description": "故障描述",
    "fault_description": "故障描述",
    "fault_level": "一般/紧急",
    "priority": "normal/critical",
    "request_department": "报修科室",
    "contact_phone": "电话",
    "source": "assetclaw",
    "intent": "repair_request"
  }
  注意：AI 安全入口一次请求完成，无需二次确认；成功后申请状态为待审批

Step 3: 查询确认
  GET /api/maintenance/requests?asset_code=xxx

Step 4: (可选) 审批维修申请
  POST /api/maintenance/requests/{id}/approve
  Body: {"approved": true, "opinion": "同意"}

Step 5: (可选) 开始执行
  POST /api/maintenance/requests/{id}/start
  Body: {"repair_person": "维修人员"}

Step 6: (可选) 完成维修
  POST /api/maintenance/requests/{id}/complete
  Body: {"repair_content": "维修内容", "repair_cost": 1000, "parts_replaced": "更换零件"}
```

## 2. 资产调配流程

```
Step 1: 查询资产确认
  GET /api/assets/{id}
  → 确认资产编号和当前部门

Step 2: 提交调配申请
  POST /api/transfer
  Body: {
    "asset_code": "xxx",
    "reason": "调配原因",
    "to_department": "目标科室"
  }
  或使用旧版路径:
  POST /api/assets/{id}/transfer-apply
  Body: {"reason": "调配原因", "target_department": "目标科室"}

Step 3: 查询调配记录
  GET /api/transfer

Step 4: 审批调配
  PUT /api/transfer/{id}/approve
  Body: {"approved": true, "opinion": "同意"}

Step 5: 执行完成
  PUT /api/transfer/{id}/complete
```

## 3. 盘点完整流程

```
Step 1: 创建盘点计划
  POST /api/inventory-plans
  Body: {
    "plan_name": "全院资产盘点",
    "plan_no": "PD20260402001",
    "start_date": "2026-04-02",
    "end_date": "2026-04-09",
    "remark": "备注"
  }

Step 2: 激活计划
  PUT /api/inventory-plans/{id}/activate

Step 3: 创建盘点任务
  POST /api/inventory-tasks
  Body: {
    "inventory_plan_id": 计划ID,
    "task_name": "科室盘点任务",
    "assignee": "负责人用户名",
    "assignee_name": "负责人姓名",
    "location": "科室位置"
  }

Step 4: 执行盘点
  PUT /api/inventory-tasks/{id}/start

Step 5: 完成盘点
  PUT /api/inventory-tasks/{id}/complete
  Body: {"actual_count": 100}

Step 6: 生成差异
  POST /api/inventory-discrepancies/generate-from-details
  或基于盘点明细:
  POST /api/inventory-discrepancies
  Body: {"inventory_id": 计划ID, "asset_code": "xxx", "discrepancy_type": "missing"}

Step 7: 处理差异
  PUT /api/inventory-discrepancies/{id}/handle
  Body: {"handling_status": "已处理", "handling_method": "盘亏报废"}

Step 8: 批量处理差异
  POST /api/inventory-discrepancies/batch-handle
  Body: {"ids": [ID1, ID2], "handling_status": "已处理", "handling_method": "正常"}

Step 9: 完成计划
  PUT /api/inventory-plans/{id}/complete
```

## 4. 闲置资产发布流程

```
Step 1: 发布闲置
  Body: {
    "asset_code": "xxx",
    "publish_person": "发布人",
    "publish_reason": "科室合并"
  }

Step 2: 查询闲置列表
  GET /api/idle/assets?status=published

Step 3: 调配闲置资产
  PUT /api/idle/{id}/allocate
  Body: {"target_department": "目标科室", "allocate_date": "2026-04-02"}

Step 4: 取消闲置发布
  PUT /api/idle/{id}/cancel

Step 5: 查看闲置统计
  GET /api/idle/statistics
```

## 4.1 资产调配流程（新版）

```
Step 1: 查询资产确认
  GET /api/assets?search=<资产编码或名称>
  → 找到资产编号 asset_code 和当前部门

Step 2: 提交调配申请（注意路径变更）
  POST /api/assets/transfer-requests
  Body: {
    "asset_code": "xxx",
    "reason": "调配原因",
    "to_department": "目标科室"
  }

Step 3: 查询调配记录
  GET /api/assets/transfer-requests

Step 4: 审批调配
  POST /api/assets/transfer-requests/{id}/approve
  Body: {"approved": true, "opinion": "同意"}

Step 5: 执行完成
  PUT /api/transfer/{id}/complete

Step 6: 查看调配统计
  GET /api/transfer/statistics
```

## 5. 报废申请流程

```
Step 1: 创建报废申请
  POST /api/scrapping
  Body: {
    "asset_code": "xxx",
    "asset_name": "资产名称",
    "applicant": "申请人",
    "scrapping_reason": "报废原因",
    "estimated_value": 5000
  }

Step 2: 查询报废记录
  GET /api/scrapping

Step 3: 审批报废
  POST /api/scrapping/{id}/approve
  Body: {"approved": true, "opinion": "同意"}

Step 4: 完成报废
  POST /api/scrapping/{id}/complete
```

## 6. 采购申请流程

```
Step 1: 创建采购申请
  POST /api/procurement/requests
  Body: {
    "title": "采购标题",
    "department": "需求部门",
    "applicant": "申请人",
    "budget": 150000,
    "remark": "备注"
  }

Step 2: 查询采购列表
  GET /api/procurement/requests

Step 3: 审批采购
  PUT /api/procurement/requests/{id}/approve
  Body: {"approved": true, "opinion": "同意"}

Step 4: 执行采购
  Body: {"completed": true, "result": "已完成采购"}

Step 5: 验收
```

## 7. 文档上传审核流程

```
Step 1: 上传文档
  POST /api/technical-documents
  Body (form-data):
    file: <文件>
    title: "资料标题"
    category: "技术资料"
    asset_code: "xxx"

Step 2: 审核文档
  POST /api/technical-documents/{id}/review
  Body: {"status": "approved", "comment": "审核通过"}

Step 3: 创建分享链接
  POST /api/technical-documents/{id}/share
  Body: {"expires_days": 30, "supplier_name": "供应商"}

Step 4: AI 问答
  POST /api/technical-documents/ai/ask
  Body: {"question": "问题", "document_ids": [ID1, ID2]}
```

## 8. 预防性维护流程（新版维护计划）

```
Step 1: 创建维护计划
  POST /api/maintenance/plans
  Body: {
    "plan_name": "CT机年度维护",
    "asset_code": "xxx",
    "maintenance_type": "预防性维护",
    "cycle_type": "year",
    "cycle_value": 1,
    "trigger_type": "time",
    "responsible_person": "负责人",
    "next_maintenance_date": "2027-01-01"
  }

Step 2: 配置提醒
  POST /api/maintenance/reminders/config
  Body: {
    "plan_id": 计划ID,
    "reminder_days": 7,
    "reminder_types": ["email", "sms"],
    "recipient": "工程师"
  }

Step 3: 检查待执行维护
  GET /api/maintenance/reminders/check

Step 4: 发送维护提醒
  POST /api/maintenance/reminders/send
  Body: {"plan_id": 计划ID, "reminder_type": "email"}

Step 5: 执行维护
  POST /api/maintenance/plans/{id}/complete
  Body: {
    "maintenance_date": "2026-04-01",
    "maintenance_person": "张三",
    "actual_hours": 4,
    "parts_replaced": "滤网",
    "maintenance_result": "正常",
    "maintenance_cost": 500
  }

Step 6: 查看维护历史
  GET /api/maintenance/plans/{id}/history

Step 7: 查看维修工单列表
  GET /api/maintenance/workorders?status=pending

Step 8: 创建维修工单
  POST /api/maintenance/workorders
  Body: {
    "title": "设备维修",
    "asset_code": "xxx",
    "priority": "critical",
    "description": "故障描述",
    "estimated_hours": 24
  }

Step 9: 分配工单
  POST /api/maintenance/workorders/{id}/assign
  Body: {"assigned_to": "李四", "assignee_name": "李四"}

Step 10: 开始工单
  POST /api/maintenance/workorders/{id}/start

Step 11: 完成工单
  POST /api/maintenance/workorders/{id}/complete
  Body: {
    "work_content": "维修完成",
    "actual_hours": 20,
    "labor_cost": 2000,
    "materials": [{"name": "球管", "quantity": 1, "cost": 148000}]
  }

Step 12: 关闭工单
  POST /api/maintenance/workorders/{id}/close
  Body: {"close_reason": "维修完成", "remark": "已正常使用"}
```

## 9. IoT 设备注册与数据上报

```
Step 1: 注册 IoT 设备
  POST /api/iot/devices
  Body: {
    "device_name": "温湿度传感器-001",
    "device_type": "environment_sensor",
    "device_id": "ENV-001",
    "asset_code": "ASSET-001",
    "manufacturer": "小米"
  }

Step 2: 上报设备位置
  POST /api/iot/location/assets/{assetCode}/location
  Body: {"latitude": 31.23, "longitude": 121.47, "location_code": "L001"}

Step 3: 批量上报区域定位
  POST /api/iot/zone-location/ingest/batch
  Body: {
    "events": [
      {
        "device_id": "BEACON-001",
        "asset_code": "ASSET-001",
        "event_time": "2026-04-01T10:00:00Z",
        "location_code": "L001",
        "rssi": -65
      }
    ]
  }

Step 4: 查询最新位置
  GET /api/iot/zone-location/assets/{assetCode}/latest

Step 5: 查询位置历史
  GET /api/iot/location/assets/{assetCode}/location/history
```

## 10. 质检记录流程

```
Step 1: 创建计量记录
  POST /api/quality-control/metrology
  Body: {
    "asset_code": "xxx",
    "metrology_type": "年度计量",
    "metrology_date": "2026-04-01",
    "result": "合格"
  }

Step 2: 创建质量控制记录
  POST /api/quality-control/quality-control
  Body: {
    "asset_code": "xxx",
    "qc_type": "性能检测",
    "qc_date": "2026-04-01",
    "result": "合格",
    "finding": "无异常"
  }

Step 3: 查询质检历史
  GET /api/quality-control/asset/{assetCode}/history

Step 4: 统计查询
  GET /api/quality-control/metrology/statistics
  GET /api/quality-control/quality-control/statistics
```

---

# 🔍 查询决策树

## "查某类设备"问题

```
用户要查某类设备（未限定科室）
  │
  └─ GET /api/assets?search=<设备名称>&pageSize=50 ✅
     (不要用 keyword 参数，会被忽略返回全量28291条数据)
```

## "查询科室资产"问题 ⚠️ 重要

```
用户要查某科室资产（如"检验科资产"、"病理科资产"）
  │
  ├─ ⚠️ 陷阱1：department参数只能精确匹配 department 字段
  │         科室信息也可能存在 location 字段中
  │         例："检验科"资产在 department="检验科" 有543条
  │                     在 location="检验科（崇山）" 有12条
  │
  ├─ ⚠️ 陷阱2：location参数也只能精确匹配
  │         例：location=检验科 返回12条（含括号变体仍只有12条）
  │
  └─ ✅ 正确做法：
       方案A（精确）：同时查询 department=科室名 和 location=科室名，合并去重
       方案B（完整）：全量扫描，在代码中过滤 department / location / department_new 字段
       注：department字段有数据（不是全量），location字段数据较少但仍需覆盖
```

## "查询调配记录"问题

```
用户要查询调配
  │
  └─ GET /api/transfer 或 GET /api/assets/transfer-requests
```

## "查询盘点状态"问题

```
用户要查盘点
  │
  ├─ 盘点计划列表: GET /api/inventory-plans         # 有效，但当前租户下可能无数据
  ├─ 盘点任务列表: GET /api/inventory-tasks         # 有效，但当前租户下可能无数据
  ├─ 盘点差异记录: GET /api/inventory-discrepancies # 有效，但当前租户下可能无数据
  │
  └─ 盘点详情: GET /api/inventory/{id}             # ⚠️ 有SQL BUG，返回500错误
```

## "查询维修记录"问题

```
用户要查维修
  │
  ├─ 维修申请: GET /api/maintenance/requests
  ├─ 维修工单: GET /api/maintenance/workorders
  └─ 维修日志: GET /api/maintenance/logs
```

## "查询资产详情"问题

```
已知资产 ID（数字）
  └─ GET /api/assets/{id}  (id 为数字 ID)

已知资产编码（asset_code）
  或先 GET /api/assets?search=<asset_code> 找到 id
```

## ⚠️ 全量扫描规范（适用于全面统计场景）

当用户要求"全院某类资产统计"、科室资产统计等需要完整数据时：

```
1. 分页遍历：总资产 28291 条，每页 300 条，共 95 页
   → 必须遍历所有页，不能只取前几页

2. 关键词过滤：在 Python 脚本中遍历所有资产，对所有文本字段
   （asset_name / location / department / use_department / department_new 等）
   进行关键词匹配

3. 科室查询示例（以"检验科"为例）：
   - ❌ 错误：只查 department='检验科' → 漏掉 415 件
   - ✅ 正确：遍历所有资产，对所有字段匹配 '检验科'
     → 匹配到 550 件（分布在 location/department 等多字段）

4. 统计输出：
   - 按 location 分组汇总（location 含科室信息最多）
   - 计算每组数量、总价值、状态分布
   - 输出高价值资产（>5万或>10万）
   - 输出品牌/类型分布
```

---

# 📖 常用 API 调用示例

## 资产操作

```bash
# 资产列表（模糊搜索）
bash scripts/assethub_api.sh request GET "/assets?page=1&pageSize=20&search=监护仪"

# ⚠️ 按科室查询资产——重要提醒：
# department 参数只能精确匹配 department 字段（需 URL 编码中文）
# 科室信息大量存储在 location / use_department / department_new 字段
# 如需完整科室资产，必须同时查询 department 和 location 再合并去重
bash scripts/assethub_api.sh request GET "/assets?page=1&pageSize=20&department=%E6%A3%80%E9%AA%8C%E7%A7%91"

# 科室名完整查询（同时匹配 department + location 字段，Python脚本）
python3 << 'PYEOF'
import urllib.request, json, sys, urllib.parse

session = json.loads(open('/tmp/assethub-claw-session.json').read())
token = session['token']; tenant_id = session['tenant_id']
base = "http://192.168.1.111:5183/api"

def fetch(path):
    url = f"{base}{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Tenant-ID": str(tenant_id)
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

DEPT = sys.argv[1] if len(sys.argv) > 1 else "内科"
seen = {}
for field in ["department", "location"]:
    data = fetch(f"/assets?page=1&pageSize=1&{field}={urllib.parse.quote(DEPT)}")
    total = data.get("data", {}).get("pagination", {}).get("total", 0)
    if total > 0:
        page_count = min((total + 199) // 200, 50)
        for p in range(1, page_count + 1):
            for a in fetch(f"/assets?page={p}&pageSize=200&{field}={urllib.parse.quote(DEPT)}").get("data",{}).get("list",[]):
                key = a.get("id")
                if key and key not in seen:
                    seen[key] = a

print(f"科室「{DEPT}」共 {len(seen)} 条资产（合并 department + location）")
for a in list(seen.values())[:10]:
    print(f"  [{a.get('id')}] {a.get('asset_name')} | {a.get('department')} | {a.get('location')}")
PYEOF

# 资产列表（按状态筛选）
bash scripts/assethub_api.sh request GET "/assets?page=1&pageSize=20&status=在用"

# 资产详情
bash scripts/assethub_api.sh request GET "/assets/123"

# 创建资产（支持 department_new 科室编码字段）
bash scripts/assethub_api.sh request POST "/assets" '{
  "asset_code": "ZY20260402001",
  "asset_name": "医用 CT 扫描仪",
  "category_id": 1,
  "purchase_price": 5000000,
  "status": "在用",
  "department_new": "DEPT-001",
  "department_id": 3
}'

# 更新资产（支持 department_new 字段）
bash scripts/assethub_api.sh request PUT "/assets/123" '{
  "asset_name": "医用 CT 扫描仪（新）",
  "status": "维修",
  "department_new": "DEPT-002"
}'

# 资产变更日志
bash scripts/assethub_api.sh request GET "/assets/123/change-logs"

# 导出资产（返回 Excel 二进制文件，非 JSON）
bash scripts/assethub_api.sh request GET "/assets/export?status=在用"
# 注意：该接口返回 Excel 文件二进制数据，需指定输出文件名

# 获取全部资产（无分页，直接返回全部数据，适用于统计分析）
bash scripts/assethub_api.sh request GET "/assets/all?search=CT"
bash scripts/assethub_api.sh request GET "/assets/all?department_new=DEPT-001"

# 获取资产详情（支持 id 或 asset_code）
bash scripts/assethub_api.sh request GET "/assets/123"

# 创建资产（支持 department_new 字段）
bash scripts/assethub_api.sh request POST "/assets" '{
  "asset_code": "ZY20260402001",
  "asset_name": "医用 CT 扫描仪",
  "category_id": 1,
  "purchase_price": 5000000,
  "status": "在用",
  "department_new": "DEPT-001"
}'

# 更新资产（支持 department_new 字段）
bash scripts/assethub_api.sh request PUT "/assets/123" '{
  "asset_name": "医用 CT 扫描仪（新）",
  "status": "维修",
  "department_new": "DEPT-002"
}'

# 资产变更日志
bash scripts/assethub_api.sh request GET "/assets/123/change-logs"

# 获取资产分类列表
bash scripts/assethub_api.sh request GET "/assets/categories"

# 获取资产统计（总数、原值、净值等）
bash scripts/assethub_api.sh request GET "/assets/statistics/overview"
```

## 维修管理

### 维修申请状态流转

维修申请从创建到完成经历以下状态：

```
[新建/待审批] → [已批准] → [维修中] → [已完成]
     ↓
  [已拒绝]     (维修过程中可暂停)
```

- **待审批**：提交后等待管理员审批（API筛选用 `status=待审批`）
- **已批准**：审批通过，等待派工（API筛选用 `status=已批准`）
- **维修中**：维修人员已开始处理（API筛选用 `status=维修中`）
- **已完成**：维修完成（API筛选用 `status=已完成`）
- **已拒绝**：审批未通过（API筛选用 `status=已拒绝`）

### 查看维修申请详情

```bash
# 查看单个维修申请详情（包含状态、审批意见、维修人员等）
bash scripts/assethub_api.sh request GET "/maintenance/requests/{request_id}"

# 维修工单列表（维修执行层）
bash scripts/assethub_api.sh request GET "/maintenance/workorders?page=1&pageSize=20"

# 维修记录日志（包含维修过程详情）
bash scripts/assethub_api.sh request GET "/maintenance/logs?request_id={request_id}"
```

### 维修状态跟踪决策树

```
报修后查不到记录？
  └─→ 用 request_no 或 asset_code 查询：
      bash scripts/assethub_api.sh request GET "/maintenance/requests?asset_code=000000555"
  └─→ 确认 status 字段值（API筛选请用中文，如 `status=待审批`）：

状态一直停留在"待审批"？
  └─→ 超级管理员直接审批：
      bash scripts/assethub_api.sh request POST "/maintenance/requests/{id}/approve" \
        '{"approved": true, "opinion": "同意维修"}'

状态是"已批准"但没人来修？
  └─→ 查看是否有维修人员被分配：
      GET /maintenance/requests/{id} 检查 repair_person 字段
  └─→ 创建维修工单（派工）：
      POST /maintenance/workorders '{"request_id": 123, "repair_person": "张三"}'

想查某台设备的维修历史？
  └─→ GET /maintenance/logs?asset_code=000000555
  └─→ 或 GET /maintenance/requests?asset_code=000000555
```

### 常用维修操作命令

```bash
# 维修申请列表
bash scripts/assethub_api.sh request GET "/maintenance/requests?page=1&pageSize=20"

# 维修申请列表（按状态，注意状态值必须用中文）
bash scripts/assethub_api.sh request GET "/maintenance/requests?status=待审批&pageSize=20"

# 创建维修申请（AI 安全入口，一次完成，无需二次确认）
# 注意：curl 直接调用时需添加 Idempotency-Key Header
bash scripts/assethub_api.sh request POST "/maintenance/ai/submit-request" '{
  "asset_code": "CT-001",
  "issue_description": "球管打火，报警 E01",
  "fault_description": "球管打火，报警 E01",
  "fault_level": "紧急",
  "priority": "critical",
  "request_department": "放射科",
  "contact_phone": "13800138000",
  "source": "assetclaw",
  "intent": "repair_request"
}'

# 直接 curl 调用（需手动加 Idempotency-Key）
curl -sS -X POST "http://192.168.1.111:5183/api/maintenance/ai/submit-request" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "X-Tenant-ID: <TENANT_ID>" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: op-$(date +%s)-$RANDOM" \
  -d '{"asset_code":"CT-001","fault_description":"球管打火，报警 E01","issue_description":"球管打火，报警 E01","fault_level":"紧急","priority":"critical","request_department":"放射科","contact_phone":"13800138000","source":"assetclaw","intent":"repair_request"}'

# 审批维修申请
bash scripts/assethub_api.sh request POST "/maintenance/requests/123/approve" '{
  "approved": true,
  "opinion": "同意维修"
}'
# 注：curl 直接调用时需添加 Idempotency-Key Header

# 开始执行维修
bash scripts/assethub_api.sh request POST "/maintenance/requests/123/start" '{
  "repair_person": "李四"
}'
# 注：curl 直接调用时需添加 Idempotency-Key Header

# 完成维修
bash scripts/assethub_api.sh request POST "/maintenance/requests/123/complete" '{
  "repair_content": "更换球管，清理内部灰尘，校准参数",
  "repair_cost": 150000,
  "parts_replaced": "CT球管",
  "repair_end_date": "2026-04-03"
}'
# 注：curl 直接调用时需添加 Idempotency-Key Header

# 维修工单列表
bash scripts/assethub_api.sh request GET "/maintenance/workorders?page=1&pageSize=20"

# 创建维修工单
bash scripts/assethub_api.sh request POST "/maintenance/workorders" '{
  "title": "CT 设备故障维修",
  "asset_code": "CT-001",
  "priority": "critical",
  "description": "球管老化，需要更换",
  "estimated_hours": 24
}'

# 分配维修工单
bash scripts/assethub_api.sh request POST "/maintenance/workorders/123/assign" '{
  "assigned_to": "李四",
  "assignee_name": "李四"
}'

# 完成维修工单
bash scripts/assethub_api.sh request POST "/maintenance/workorders/123/complete" '{
  "work_content": "更换球管完成",
  "actual_hours": 20,
  "labor_cost": 2000,
  "outsourcing_cost": 0,
  "materials": [{"name": "球管", "quantity": 1, "cost": 148000}]
}'

# 维修日志列表
bash scripts/assethub_api.sh request GET "/maintenance/logs?page=1&pageSize=20"

# 创建维修日志
bash scripts/assethub_api.sh request POST "/maintenance/logs" '{
  "asset_code": "ZY2020000122",
  "maintenance_type": "故障维修",
  "maintenance_date": "2026-04-01",
  "maintenance_person": "张三",
  "maintenance_content": "更换碳纤维骨科牵引架轴承",
  "maintenance_duration": 2,
  "parts_replaced": "轴承",
  "maintenance_cost": 500
}'

# 维修统计
bash scripts/assethub_api.sh request GET "/maintenance/statistics?start_date=2026-01-01&end_date=2026-04-01"

# 维修效率统计
bash scripts/assethub_api.sh request GET "/maintenance/efficiency/overview"

# 维修费用分析
bash scripts/assethub_api.sh request GET "/maintenance/costs/analysis"
```

## 调配/闲置/报废

```bash
# 调配申请列表
bash scripts/assethub_api.sh request GET "/transfer?page=1&pageSize=20"

# 发起调配申请
bash scripts/assethub_api.sh request POST "/transfer" '{
  "asset_code": "XXX-001",
  "reason": "科室合并，需调拨设备",
  "to_department": "心内科"
}'

# 审批调配
bash scripts/assethub_api.sh request PUT "/transfer/123/approve" '{
  "approved": true,
  "opinion": "同意"
}'

# 执行调配完成
bash scripts/assethub_api.sh request PUT "/transfer/123/complete"

# 闲置资产列表
bash scripts/assethub_api.sh request GET "/idle?page=1&pageSize=20"

# 闲置资产列表（新接口，带更多筛选参数）
bash scripts/assethub_api.sh request GET "/idle/assets?page=1&pageSize=20&status=published"

# 发布闲置
bash scripts/assethub_api.sh request POST "/idle" '{
  "asset_code": "XXX-001",
  "publish_person": "王五"
}'

# 发布闲置资产（新接口）


}'

# 调配闲置资产
bash scripts/assethub_api.sh request PUT "/idle/123/allocate" '{
  "target_department": "放射科",
  "allocate_date": "2026-04-02"
}'

# 取消闲置发布
bash scripts/assethub_api.sh request PUT "/idle/123/cancel"

# 闲置资产统计
bash scripts/assethub_api.sh request GET "/idle/statistics"

# 调配申请列表
bash scripts/assethub_api.sh request GET "/assets/transfer-requests?page=1&pageSize=20"

# 发起调配申请（注意路径是 /transfer，需 transfer_no）
bash scripts/assethub_api.sh request POST "/transfer" '{
  "transfer_no": "SQ20260509001",
  "asset_code": "XXX-001",
  "reason": "科室合并，需调拨设备",
  "to_department": "心内科"
}'

# 审批调配申请
bash scripts/assethub_api.sh request POST "/assets/transfer-requests/123/approve" '{
  "approved": true,
  "opinion": "同意"
}'

# 执行调配完成
bash scripts/assethub_api.sh request PUT "/transfer/123/complete"

# 调配统计
bash scripts/assethub_api.sh request GET "/transfer/statistics"

# 报废申请列表
bash scripts/assethub_api.sh request GET "/scrapping?page=1&pageSize=20"

# 创建报废申请
bash scripts/assethub_api.sh request POST "/scrapping" '{
  "asset_code": "OLD-CT-001",
  "asset_name": "旧 CT 扫描仪",
  "applicant": "张三",
  "scrapping_reason": "设备老旧，无法维修",
  "estimated_value": 5000
}'

# 审批报废
bash scripts/assethub_api.sh request POST "/scrapping/123/approve" '{
  "approved": true,
  "opinion": "同意报废"
}'

# 完成报废
bash scripts/assethub_api.sh request POST "/scrapping/123/complete"
```

## 盘点

```bash
# 盘点计划列表
bash scripts/assethub_api.sh request GET "/inventory-plans?page=1&pageSize=20"

# 创建盘点计划
bash scripts/assethub_api.sh request POST "/inventory-plans" '{
  "plan_name": "2026年上半年度设备盘点",
  "plan_no": "PD-2026-001",
  "start_date": "2026-04-01",
  "end_date": "2026-04-30",
  "remark": "全院资产盘点"
}'

# 激活盘点计划
bash scripts/assethub_api.sh request PUT "/inventory-plans/123/activate"

# 盘点任务列表
bash scripts/assethub_api.sh request GET "/inventory-tasks?page=1&pageSize=20"

# 创建盘点任务
bash scripts/assethub_api.sh request POST "/inventory-tasks" '{
  "inventory_plan_id": 123,
  "task_name": "放射科室盘点任务",
  "assignee": "李四",
  "assignee_name": "李四",
  "location": "放射科",
  "department_code": "DEPT-001"
}'

# 开始盘点
bash scripts/assethub_api.sh request PUT "/inventory-tasks/123/start"

# 完成盘点
bash scripts/assethub_api.sh request PUT "/inventory-tasks/123/complete" '{
  "actual_count": 50,
  "remark": "部分设备位置有调整"
}'

# 盘点差异列表
bash scripts/assethub_api.sh request GET "/inventory-discrepancies?page=1&pageSize=20"

# 处理盘点差异
bash scripts/assethub_api.sh request PUT "/inventory-discrepancies/123/handle" '{
  "handling_status": "已处理",
  "handling_method": "正常",
  "handling_notes": "已确认位置正确"
}'

# 批量处理盘点差异
bash scripts/assethub_api.sh request POST "/inventory-discrepancies/batch-handle" '{
  "ids": [1, 2, 3],
  "handling_status": "已处理",
  "handling_method": "正常"
}'

# 完成盘点计划
bash scripts/assethub_api.sh request PUT "/inventory-plans/123/complete"

# 取消盘点计划
bash scripts/assethub_api.sh request PUT "/inventory-plans/123/cancel"
```

## 采购/质检/验收

```bash
# 采购申请列表
bash scripts/assethub_api.sh request GET "/procurement/requests?page=1&pageSize=20"

# 创建采购申请
bash scripts/assethub_api.sh request POST "/procurement/requests" '{
  "title": "迈瑞监护仪采购",
  "department": "心内科",
  "applicant": "张三",
  "budget": 150000,
  "remark": "科室新增需要"
}'

# 审批采购
bash scripts/assethub_api.sh request PUT "/procurement/requests/123/approve" '{
  "action": "approve",
  "opinion": "同意采购"
}'

# 执行采购
  "completed": true,
  "result": "已完成采购"
}'

# 验收

# 计量记录列表
bash scripts/assethub_api.sh request GET "/quality-control/metrology?page=1&pageSize=20"

# 创建计量记录
bash scripts/assethub_api.sh request POST "/quality-control/metrology" '{
  "asset_code": "XXX-001",
  "metrology_type": "年度计量",
  "metrology_date": "2026-04-01",
  "result": "合格"
}'

# 质量控制记录列表
bash scripts/assethub_api.sh request GET "/quality-control/quality-control?page=1&pageSize=20"

# 创建质量控制记录
bash scripts/assethub_api.sh request POST "/quality-control/quality-control" '{
  "asset_code": "XXX-001",
  "qc_type": "年度质检",
  "qc_date": "2026-04-01",
  "qc_person": "李四",
  "result": "合格",
  "finding": "无异常"
}'

# 质检统计
bash scripts/assethub_api.sh request GET "/quality-control/statistics"
```

## 文档

```bash
# 文档列表
bash scripts/assethub_api.sh request GET "/technical-documents?page=1&pageSize=20&keyword=CT"

# 文档列表（按分类）
bash scripts/assethub_api.sh request GET "/technical-documents?category=技术资料&pageSize=20"

# 上传文档（需要 form-data，curl 示例）
curl -sS -X POST "http://192.168.1.111:5183/api/technical-documents" \
  -H "Authorization: Bearer <TOKEN>" \
  -F "file=@/path/to/file.pdf" \
  -F "title=设备操作手册" \
  -F "category=操作手册" \
  -F "asset_code=XXX-001"

# 审核文档
bash scripts/assethub_api.sh request POST "/technical-documents/123/review" '{
  "status": "approved",
  "comment": "审核通过"
}'

# 创建文档分享
bash scripts/assethub_api.sh request POST "/technical-documents/123/share" '{
  "expires_days": 30,
  "supplier_name": "供应商名称"
}'

# 文档评论
bash scripts/assethub_api.sh request POST "/technical-documents/enhanced/documents/123/comments" '{
  "content": "文档内容有误，请更正"
}'

# 收藏文档
bash scripts/assethub_api.sh request POST "/technical-documents/enhanced/documents/123/favorite"

# AI 问答
bash scripts/assethub_api.sh request POST "/technical-documents/ai/ask" '{
  "question": "这台设备的维护周期是多久？",
  "document_ids": [1, 2, 3]
}'

# AI 搜索
bash scripts/assethub_api.sh request POST "/technical-documents/ai/search" '{
  "query": "CT 球管维护"
}'

# 文档分类列表
bash scripts/assethub_api.sh request GET "/technical-documents/enhanced/categories"

# 文档标签列表
bash scripts/assethub_api.sh request GET "/technical-documents/enhanced/tags"
```

## 预防性维护

```bash
# 维护计划列表
bash scripts/assethub_api.sh request GET "/maintenance/plans?page=1&pageSize=20"

# 创建维护计划
bash scripts/assethub_api.sh request POST "/maintenance/plans" '{
  "plan_name": "CT机年度维护",
  "asset_code": "CT-001",
  "maintenance_type": "预防性维护",
  "cycle_type": "year",
  "cycle_value": 1,
  "trigger_type": "time",
  "responsible_person": "李工程师",
  "next_maintenance_date": "2027-01-01"
}'

# 配置维护提醒
bash scripts/assethub_api.sh request POST "/maintenance/reminders/config" '{
  "plan_id": 123,
  "reminder_days": 7,
  "reminder_types": ["email", "sms"],
  "recipient": "李工程师"
}'

# 发送维护提醒
bash scripts/assethub_api.sh request POST "/maintenance/reminders/send" '{
  "plan_id": 123,
  "reminder_type": "email"
}'

# 检查维护提醒
bash scripts/assethub_api.sh request GET "/maintenance/reminders/check"

# 完成维护计划
bash scripts/assethub_api.sh request POST "/maintenance/plans/123/complete" '{
  "maintenance_date": "2026-04-01",
  "maintenance_person": "李工程师",
  "actual_hours": 4,
  "parts_replaced": "滤网",
  "maintenance_result": "正常",
  "maintenance_cost": 500
}'

# 维护计划历史
bash scripts/assethub_api.sh request GET "/maintenance/plans/123/history"

# 维修模板列表
bash scripts/assethub_api.sh request GET "/maintenance/templates?page=1&pageSize=20"

# 维修日志列表
bash scripts/assethub_api.sh request GET "/maintenance/logs?page=1&pageSize=20"
bash scripts/assethub_api.sh request GET "/maintenance/logs?asset_code=CT-001&pageSize=20"

# 创建维修日志
bash scripts/assethub_api.sh request POST "/maintenance/logs" '{
  "asset_code": "ZY2020000122",
  "maintenance_type": "故障维修",
  "maintenance_date": "2026-04-01",
  "maintenance_person": "张三",
  "maintenance_content": "更换碳纤维骨科牵引架轴承",
  "maintenance_duration": 2,
  "parts_replaced": "轴承",
  "maintenance_cost": 500
}'

# 获取维修模板列表
bash scripts/assethub_api.sh request GET "/maintenance/templates"

# 获取维修效率统计
bash scripts/assethub_api.sh request GET "/maintenance/efficiency/overview"

# ========== 维护计划（预防性维护）==========

# 维护计划列表
bash scripts/assethub_api.sh request GET "/maintenance/plans?page=1&pageSize=20"
bash scripts/assethub_api.sh request GET "/maintenance/plans?status=active&pageSize=20"

# 获取维护计划详情
bash scripts/assethub_api.sh request GET "/maintenance/plans/{id}"

# 创建维护计划
bash scripts/assethub_api.sh request POST "/maintenance/plans" '{
  "plan_name": "CT机年度维护",
  "asset_code": "CT-001",
  "maintenance_type": "预防性维护",
  "cycle_type": "year",
  "cycle_value": 1,
  "trigger_type": "time",
  "responsible_person": "李工程师",
  "next_maintenance_date": "2027-01-01"
}'

# 更新维护计划
bash scripts/assethub_api.sh request PUT "/maintenance/plans/{id}" '{
  "plan_name": "CT机年度维护（更新）",
  "responsible_person": "王工程师"
}'

# 完成维护计划
bash scripts/assethub_api.sh request POST "/maintenance/plans/{id}/complete" '{
  "maintenance_date": "2026-04-01",
  "maintenance_person": "李工程师",
  "actual_hours": 4,
  "parts_replaced": "滤网",
  "maintenance_result": "正常",
  "maintenance_cost": 500
}'

# 删除维护计划
bash scripts/assethub_api.sh request DELETE "/maintenance/plans/{id}"

# 获取维护计划历史
bash scripts/assethub_api.sh request GET "/maintenance/plans/{id}/history"

# ========== 维修提醒 ==========

# 提醒列表
bash scripts/assethub_api.sh request GET "/maintenance/reminders?page=1&pageSize=20"

# 配置维护提醒
bash scripts/assethub_api.sh request POST "/maintenance/reminders/config" '{
  "plan_id": 123,
  "reminder_days": 7,
  "reminder_types": ["email", "sms"],
  "recipient": "李工程师"
}'

# 发送维护提醒
bash scripts/assethub_api.sh request POST "/maintenance/reminders/send" '{
  "plan_id": 123,
  "reminder_type": "email"
}'

# 检查维护提醒（查看即将到期的维护任务）
bash scripts/assethub_api.sh request GET "/maintenance/reminders/check"

# ========== 维修工单 ==========

# 维修工单列表
bash scripts/assethub_api.sh request GET "/maintenance/workorders?page=1&pageSize=20"
bash scripts/assethub_api.sh request GET "/maintenance/workorders?status=pending&pageSize=20"
bash scripts/assethub_api.sh request GET "/maintenance/workorders?asset_code=CT-001"

# 获取维修工单详情
bash scripts/assethub_api.sh request GET "/maintenance/workorders/{id}"

# 创建维修工单
bash scripts/assethub_api.sh request POST "/maintenance/workorders" '{
  "title": "CT 设备故障维修",
  "asset_code": "CT-001",
  "priority": "critical",
  "description": "球管老化，需要更换",
  "estimated_hours": 24
}'

# 分配维修工单
bash scripts/assethub_api.sh request POST "/maintenance/workorders/{id}/assign" '{
  "assigned_to": "李四",
  "assignee_name": "李四"
}'

# 开始执行工单
bash scripts/assethub_api.sh request POST "/maintenance/workorders/{id}/start" '{
  "actual_start_time": "2026-04-01 09:00:00"
}'

# 完成维修工单
bash scripts/assethub_api.sh request POST "/maintenance/workorders/{id}/complete" '{
  "work_content": "更换球管完成",
  "actual_hours": 20,
  "labor_cost": 2000,
  "outsourcing_cost": 0,
  "materials": [{"name": "球管", "quantity": 1, "cost": 148000}]
}'

# 关闭工单
bash scripts/assethub_api.sh request POST "/maintenance/workorders/{id}/close" '{
  "close_reason": "维修完成",
  "remark": "已正常使用"
}'

# 取消工单
bash scripts/assethub_api.sh request POST "/maintenance/workorders/{id}/cancel" '{
  "cancel_reason": "设备已报废"
}'

# 添加工单物料
bash scripts/assethub_api.sh request POST "/maintenance/workorders/{id}/materials" '{
  "materials": [
    {"name": "球管", "quantity": 1, "cost": 148000},
    {"name": "滤网", "quantity": 2, "cost": 500}
  ]
}'

# 维修申请列表
bash scripts/assethub_api.sh request GET "/maintenance/requests?page=1&pageSize=20"
bash scripts/assethub_api.sh request GET "/maintenance/requests?status=待审批&pageSize=20"
bash scripts/assethub_api.sh request GET "/maintenance/requests?asset_code=CT-001"

# 获取维修申请详情
bash scripts/assethub_api.sh request GET "/maintenance/requests/{id}"

# 创建维修申请（AI 安全入口，一次完成，无需二次确认）
bash scripts/assethub_api.sh request POST "/maintenance/ai/submit-request" '{
  "asset_code": "CT-001",
  "issue_description": "球管打火，报警 E01",
  "fault_description": "球管打火，报警 E01",
  "fault_level": "紧急",
  "priority": "critical",
  "request_department": "放射科",
  "contact_phone": "13800138000",
  "source": "assetclaw",
  "intent": "repair_request"
}'

# 审批维修申请
bash scripts/assethub_api.sh request POST "/maintenance/requests/{id}/approve" '{
  "approved": true,
  "opinion": "同意维修"
}'

# 开始执行维修
bash scripts/assethub_api.sh request POST "/maintenance/requests/{id}/start" '{
  "repair_person": "李四"
}'

# 完成维修
bash scripts/assethub_api.sh request POST "/maintenance/requests/{id}/complete" '{
  "repair_content": "更换球管，清理内部灰尘，校准参数",
  "repair_cost": 150000,
  "parts_replaced": "CT球管",
  "repair_end_date": "2026-04-03"
}'
```

## 折旧

```bash
# 折旧列表
bash scripts/assethub_api.sh request GET "/depreciation?page=1&pageSize=20"

# 按部门折旧汇总
bash scripts/assethub_api.sh request GET "/depreciation/summary/by-department"

# 按月折旧趋势
bash scripts/assethub_api.sh request GET "/depreciation/summary/by-month?months=12"

# 按类型折旧汇总
bash scripts/assethub_api.sh request GET "/depreciation/summary/by-type"

# 计算折旧
bash scripts/assethub_api.sh request POST "/depreciation/calculate" '{
  "as_of_date": "2026-04-01"
}'

# 折旧方法列表
bash scripts/assethub_api.sh request GET "/depreciation/methods"

# 导出折旧报表
bash scripts/assethub_api.sh request GET "/depreciation/export"
```

## 部门/用户/角色

```bash
# 部门树
bash scripts/assethub_api.sh request GET "/departments/tree"

# 部门列表
bash scripts/assethub_api.sh request GET "/departments?page=1&pageSize=20"

# 创建部门
bash scripts/assethub_api.sh request POST "/departments" '{
  "department_name": "放射科",
  "parent_code": "ROOT"
}'

# 用户列表
bash scripts/assethub_api.sh request GET "/users?page=1&pageSize=20"

# 创建用户
bash scripts/assethub_api.sh request POST "/users" '{
  "username": "zhangsan",
  "real_name": "张三",
  "password": "Password123",
  "role": "engineer",
  "email": "zhangsan@example.com",
  "phone": "13800138000"
}'

# 获取当前用户信息
bash scripts/assethub_api.sh request GET "/users/me"

# 角色列表
bash scripts/assethub_api.sh request GET "/roles-permissions/roles"

# 获取角色权限
bash scripts/assethub_api.sh request GET "/roles-permissions/roles/engineer/permissions"

# 更新角色权限
bash scripts/assethub_api.sh request PUT "/roles-permissions/roles/engineer/permissions" '{
  "permissions": ["asset.view", "asset.create", "maintenance.request"]
}'

# 获取角色菜单
bash scripts/assethub_api.sh request GET "/roles-permissions/roles/engineer/menus"

# 更新角色菜单
bash scripts/assethub_api.sh request PUT "/roles-permissions/roles/engineer/menus" '{
  "menus": ["assets", "maintenance", "inventory"]
}'

# 当前用户菜单权限
bash scripts/assethub_api.sh request GET "/roles-permissions/user/menus"
```

## IoT/定位

```bash
# IoT 设备列表
bash scripts/assethub_api.sh request GET "/iot/devices?page=1&pageSize=20"

# 注册 IoT 设备
bash scripts/assethub_api.sh request POST "/iot/devices" '{
  "device_name": "温湿度传感器-001",
  "device_type": "environment_sensor",
  "device_id": "ENV-001",
  "asset_code": "ASSET-001",
  "manufacturer": "小米",
  "model": "MHO-A400"
}'

# 上报设备定位数据
bash scripts/assethub_api.sh request POST "/iot/location/assets/ASSET-001/location" '{
  "latitude": 31.2304,
  "longitude": 121.4737,
  "altitude": 10,
  "battery_level": 85
}'

# 批量上报区域定位
bash scripts/assethub_api.sh request POST "/iot/zone-location/ingest/batch" '{
  "events": [
    {
      "device_id": "BEACON-001",
      "asset_code": "ASSET-001",
      "event_time": "2026-04-01T10:00:00Z",
      "location_code": "L001",
      "building_name": "门诊楼",
      "floor_number": 3,
      "area_name": "放射科",
      "rssi": -65,
      "battery_level": 85
    }
  ]
}'

# 查询最新环境监测数据
bash scripts/assethub_api.sh request GET "/iot/environment-monitoring/assets/ASSET-001/latest"

# 查询资产位置历史
bash scripts/assethub_api.sh request GET "/iot/location/assets/ASSET-001/location/history?start_time=2026-04-01&end_time=2026-04-02"

# 资产绑定设备
bash scripts/assethub_api.sh request POST "/asset-location/assets/ASSET-001/bind-device" '{
  "device_id": "BEACON-001"
}'

# 查询区域定位管道健康状态
bash scripts/assethub_api.sh request GET "/iot/zone-location/pipeline/health"

# 查询设备类型列表
bash scripts/assethub_api.sh request GET "/iot/devices/types"
```

## 标签打印

```bash
# 标签模板列表
bash scripts/assethub_api.sh request GET "/asset-labels/templates?page=1&pageSize=20"

# 创建标签模板
bash scripts/assethub_api.sh request POST "/asset-labels/templates" '{
  "name": "标准资产标签",
  "description": "包含资产编号、名称、位置",
  "width": 4,
  "height": 2,
  "dpi": 300,
  "fields": [
    {"field_name": "asset_code", "label": "资产编号", "x": 0, "y": 0},
    {"field_name": "asset_name", "label": "资产名称", "x": 0, "y": 20}
  ]
}'

# 批量生成 ZPL 标签
bash scripts/assethub_api.sh request POST "/asset-labels/generate-zpl-batch" '{
  "template_id": 1,
  "asset_codes": ["ASSET-001", "ASSET-002", "ASSET-003"],
  "quantity_per_asset": 1
}'

# 测试打印机连接
bash scripts/assethub_api.sh request POST "/asset-labels/printer/test-connection" '{
  "printer_ip": "192.168.1.100",
  "printer_port": 9100,
  "timeout_ms": 5000
}'

# 打印标签
bash scripts/assethub_api.sh request POST "/asset-labels/print" '{
  "template_id": 1,
  "asset_code": "ASSET-001",
  "printer_ip": "192.168.1.100",
  "printer_port": 9100,
  "quantity": 1,
  "print_timeout_ms": 10000,
  "retry_count": 3
}'
```

## 告警

```bash
# 智能告警列表
bash scripts/assethub_api.sh request GET "/intelligent-alerts?page=1&pageSize=20"

# 告警概览
bash scripts/assethub_api.sh request GET "/intelligent-alerts/overview"

# 处理告警
bash scripts/assethub_api.sh request POST "/intelligent-alerts/123/handle" '{
  "handle_result": "已确认并处理"
}'

# 标记告警为已读
bash scripts/assethub_api.sh request POST "/intelligent-alerts/123/read"

# 全部标记已读
bash scripts/assethub_api.sh request POST "/intelligent-alerts/read-all"

# 位置告警列表
bash scripts/assethub_api.sh request GET "/location-alerts?page=1&pageSize=20"

# 处理位置告警
bash scripts/assethub_api.sh request PUT "/location-alerts/123/handle" '{
  "handle_result": "已确认资产位置正常"
}'

# 批量处理位置告警
bash scripts/assethub_api.sh request POST "/location-alerts/batch/handle" '{
  "ids": [1, 2, 3],
  "handle_result": "已确认"
}'

# 位置告警统计
bash scripts/assethub_api.sh request GET "/location-alerts/stats"
```

## 审计/备份

```bash
# 审计日志列表
bash scripts/assethub_api.sh request GET "/audit-logs?page=1&pageSize=20"

# 审计日志列表（按操作类型）
bash scripts/assethub_api.sh request GET "/audit-logs?action_type=asset.create&pageSize=20"

# 审计日志统计
bash scripts/assethub_api.sh request GET "/audit-logs/stats?start_date=2026-01-01&end_date=2026-04-01"

# 备份列表
bash scripts/assethub_api.sh request GET "/backup?page=1&pageSize=20"

# 创建备份
bash scripts/assethub_api.sh request POST "/backup" '{
  "description": "定期备份 2026-04-01"
}'

# 恢复备份
bash scripts/assethub_api.sh request POST "/backup/123/restore" '{
  "confirm": true
}'
```

## 仪表盘/统计

```bash
# 仪表盘概览
bash scripts/assethub_api.sh request GET "/dashboard"

# 实时数据
bash scripts/assethub_api.sh request GET "/dashboard/realtime"

# 资产统计概览（含总数、原值、净值）
bash scripts/assethub_api.sh request GET "/assets/statistics/overview"

# 资产价值分布
bash scripts/assethub_api.sh request GET "/analysis/value-distribution"

# 折旧趋势
bash scripts/assethub_api.sh request GET "/analysis/depreciation"

# 风险仪表盘
bash scripts/assethub_api.sh request GET "/risk/dashboard"

# 合规状态
bash scripts/assethub_api.sh request GET "/compliance/status"

# 合规仪表盘统计
bash scripts/assethub_api.sh request GET "/compliance/dashboard-stats"

# 资产分类列表（用于下拉选择）
bash scripts/assethub_api.sh request GET "/assets/categories"

# 调配统计
bash scripts/assethub_api.sh request GET "/transfer/statistics"

# 闲置统计
bash scripts/assethub_api.sh request GET "/idle/statistics"
```

## 模块配置

```bash
# 模块列表
bash scripts/assethub_api.sh request GET "/modules?page=1&pageSize=20"

# 租户模块配置列表
bash scripts/assethub_api.sh request GET "/module-configs/list"

# 启用模块
bash scripts/assethub_api.sh request POST "/module-configs/enable" '{
  "module_id": "assets",
  "config": {}
}'

# 停用模块
bash scripts/assethub_api.sh request POST "/module-configs/disable" '{
  "module_id": "assets"
}'

# 获取单模块配置
bash scripts/assethub_api.sh request GET "/module-configs/assets"

# 更新模块配置
bash scripts/assethub_api.sh request PUT "/module-configs/assets" '{
  "enabled": true,
  "config": {"key": "value"}
}'

# 获取模块菜单权限
bash scripts/assethub_api.sh request GET "/module-configs/assets/menus"

# 批量更新模块菜单
bash scripts/assethub_api.sh request PUT "/module-configs/assets/menus" '{
  "menus": [
    {"menu_key": "assets", "is_visible": true},
    {"menu_key": "maintenance", "is_visible": true}
  ]
}'

# 模块版本历史
bash scripts/assethub_api.sh request GET "/module-configs/assets/versions"

# 创建模块版本备份
bash scripts/assethub_api.sh request POST "/module-configs/assets/versions" '{
  "change_log": "配置更新"
}'

# 回滚模块版本
bash scripts/assethub_api.sh request POST "/module-configs/assets/rollback" '{
  "version_id": 5
}'

# 验证模块配置
bash scripts/assethub_api.sh request GET "/module-configs/assets/validate"
```

## 工作流

```bash
# 获取默认工作流
bash scripts/assethub_api.sh request GET "/workflow/default"

# 获取工作流状态
bash scripts/assethub_api.sh request GET "/workflow/states"

# 获取迁移规则
bash scripts/assethub_api.sh request GET "/workflow/transitions"

# 执行状态迁移
bash scripts/assethub_api.sh request POST "/workflow/transition/123" '{
  "transition_id": 2,
  "reason": "设备报废"
}'

# 获取资产可执行状态迁移
bash scripts/assethub_api.sh request GET "/assets/123/transitions"
```

## AI 分析

```bash
# AI 故障分析
bash scripts/assethub_api.sh request GET "/asset-ai-analysis/analysis-history?page=1&pageSize=20"

# 分析单个资产
bash scripts/assethub_api.sh request POST "/asset-ai-analysis/analyze-asset/CT-001" '{
  "start_date": "2026-01-01",
  "end_date": "2026-04-01"
}'

# 批量分析资产
bash scripts/assethub_api.sh request POST "/asset-ai-analysis/analyze-assets" '{
  "asset_codes": ["CT-001", "CT-002"],
  "analysis_type": "fault_prediction"
}'

# 维修效率分析
bash scripts/assethub_api.sh request GET "/maintenance/efficiency/overview"

# 维修响应时间统计
bash scripts/assethub_api.sh request GET "/maintenance/efficiency/response-time"

# 工程师绩效统计
bash scripts/assethub_api.sh request GET "/maintenance/efficiency/technician"

# 资产使用频率
bash scripts/assethub_api.sh request GET "/maintenance/efficiency/asset-frequency"

# 维修类型分布
bash scripts/assethub_api.sh request GET "/maintenance/analysis/type-distribution"

# 维修费用趋势
bash scripts/assethub_api.sh request GET "/maintenance/analysis/cost-trend"

# 预测性维护
bash scripts/assethub_api.sh request POST "/agent-mesh/intelligence/predictive-maintenance" '{
  "asset_code": "CT-001",
  "days_ahead": 30
}'

# 风险评分
bash scripts/assethub_api.sh request POST "/agent-mesh/intelligence/risk-score" '{
  "asset_code": "CT-001"
}'

# 健康指数
bash scripts/assethub_api.sh request POST "/agent-mesh/intelligence/health-index" '{
  "asset_code": "CT-001"
}'

# 维修 AI 对话初始化
bash scripts/assethub_api.sh request POST "/maintenance/ai/init"

# 维修 AI 发送消息
bash scripts/assethub_api.sh request POST "/maintenance/ai/message" '{
  "conversation_id": "conv-xxx",
  "message": "CT球管打火怎么办"
}'
```

## 库存管理

```bash
# 库存记录列表
bash scripts/assethub_api.sh request GET "/inventory?page=1&pageSize=20"

# 创建库存记录
bash scripts/assethub_api.sh request POST "/inventory" '{
  "item_name": "球管",
  "category": "备件",
  "warehouse": "备件库",
  "location": "A区-01",
  "quantity": 5,
  "unit": "个",
  "remark": "CT备件"
}'

# 调整库存
# 入库:
bash scripts/assethub_api.sh request PUT "/inventory/123" '{
  "adjust_type": "in",
  "quantity": 2,
  "reason": "新购入库"
}'
# 出库:
bash scripts/assethub_api.sh request PUT "/inventory/123" '{
  "adjust_type": "out",
  "quantity": 1,
  "reason": "维修使用"
}'
# 调整:
bash scripts/assethub_api.sh request PUT "/inventory/123" '{
  "adjust_type": "adj",
  "quantity": -1,
  "reason": "盘点调整"
}'
```

## 系统配置

```bash
# 获取数据库配置
bash scripts/assethub_api.sh request GET "/system-config/database"

# 更新数据库配置
bash scripts/assethub_api.sh request PUT "/system-config/database" '{
  "host": "localhost",
  "port": 3306,
  "database": "assethub",
  "user": "root",
  "password": "newpassword"
}'

# 测试数据库连接
bash scripts/assethub_api.sh request POST "/system-config/database/test"

# IoT Token 列表

# 生成 IoT Token
}'

# 验证 IoT Token
}'

# 获取 IoT Token 使用指南
```

---

## 🆕 新增端点说明 (v1.5.8)

本版本补充了此前 SKILL.md 中缺失的重要端点，按模块分类添加。每个模块补充 3~8 个最核心的端点。

### 📋 验收记录（/acceptance）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/acceptance/records` | GET/POST | 验收记录列表/创建 |
| `/acceptance/records/{id}` | GET/PUT | 验收记录详情/更新 |
| `/acceptance/records/{id}/status` | PUT | 更新验收状态 |
| `/acceptance/records/{id}/checklist/stats` | GET | 验收检查项统计 |
| `/acceptance/statistics` | GET | 验收统计 |

```bash
# 验收记录列表
bash scripts/assethub_api.sh request GET "/acceptance/records?page=1&pageSize=20"

# 验收记录详情
bash scripts/assethub_api.sh request GET "/acceptance/records/{id}"

# 更新验收状态
bash scripts/assethub_api.sh request PUT "/acceptance/records/{id}/status" '{
  "status": "approved"
}'

# 验收统计
bash scripts/assethub_api.sh request GET "/acceptance/statistics"
```

### 🚨 不良事件（/adverse-events）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/adverse-events` | GET/POST | 不良事件列表/创建 |
| `/adverse-events/{id}` | GET/PUT | 不良事件详情/更新 |
| `/adverse-events/{id}/approve` | POST | 审批不良事件 |
| `/adverse-events/{id}/close` | POST | 关闭不良事件 |
| `/adverse-events/statistics/overview` | GET | 不良事件统计概览 |
| `/adverse-events/alerts/overdue` | GET | 超期未关闭预警 |

```bash
# 不良事件列表
bash scripts/assethub_api.sh request GET "/adverse-events?page=1&pageSize=20"

# 创建不良事件
bash scripts/assethub_api.sh request POST "/adverse-events" '{
  "asset_code": "XXX-001",
  "event_type": "不良反应",
  "description": "设备异常导致患者不适",
  "severity": "中等"
}'

# 审批不良事件
bash scripts/assethub_api.sh request POST "/adverse-events/{id}/approve" '{
  "opinion": "同意",
  "approved": true
}'

# 不良事件统计
bash scripts/assethub_api.sh request GET "/adverse-events/statistics/overview"
```

### 📊 资产使用（/asset-usage）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/asset-usage/checkout` | POST | 资产借用/使用登记 |
| `/asset-usage/return/{id}` | POST | 归还资产 |
| `/asset-usage/records` | GET | 使用记录列表 |
| `/asset-usage/statistics` | GET | 使用统计 |

```bash
# 借用资产
bash scripts/assethub_api.sh request POST "/asset-usage/checkout" '{
  "asset_code": "XXX-001",
  "user_id": 1,
  "user_name": "张三",
  "expected_return_date": "2026-05-15"
}'

# 归还资产
bash scripts/assethub_api.sh request POST "/asset-usage/return/{id}"

# 使用记录
bash scripts/assethub_api.sh request GET "/asset-usage/records?page=1&pageSize=20"

# 使用统计
bash scripts/assethub_api.sh request GET "/asset-usage/statistics"
```

### 🔧 维修成本与效率分析（/maintenance）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/maintenance/costs` | GET/POST | 维修成本列表/创建 |
| `/maintenance/costs/analysis` | GET | 维修成本分析 |
| `/maintenance/costs/high-cost-assets` | GET | 高成本资产排行 |
| `/maintenance/efficiency/response-time` | GET | 维修响应时间统计 |
| `/maintenance/efficiency/technician` | GET | 工程师绩效统计 |
| `/maintenance/analysis/type-distribution` | GET | 维修类型分布 |
| `/maintenance/analysis/cost-trend` | GET | 维修费用趋势 |
| `/maintenance/templates/recommend` | GET | 推荐维修模板 |

```bash
# 维修成本分析
bash scripts/assethub_api.sh request GET "/maintenance/costs/analysis"

# 高成本资产排行
bash scripts/assethub_api.sh request GET "/maintenance/costs/high-cost-assets"

# 维修响应时间统计
bash scripts/assethub_api.sh request GET "/maintenance/efficiency/response-time"

# 工程师绩效统计
bash scripts/assethub_api.sh request GET "/maintenance/efficiency/technician"

# 维修类型分布
bash scripts/assethub_api.sh request GET "/maintenance/analysis/type-distribution"

# 维修费用趋势
bash scripts/assethub_api.sh request GET "/maintenance/analysis/cost-trend"

# 推荐维修模板
bash scripts/assethub_api.sh request GET "/maintenance/templates/recommend?asset_code=XXX-001"
```

### 📈 仪表盘配置（/dashboard-configs）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/dashboard-configs` | GET/POST | 仪表盘配置列表/创建 |
| `/dashboard-configs/active` | GET | 获取当前激活的仪表盘配置 |
| `/dashboard-configs/{id}` | GET/PUT | 仪表盘配置详情/更新 |
| `/dashboard-configs/{id}/data` | GET | 获取指定仪表盘的数据 |

```bash
# 仪表盘配置列表
bash scripts/assethub_api.sh request GET "/dashboard-configs?page=1&pageSize=20"

# 获取激活的仪表盘
bash scripts/assethub_api.sh request GET "/dashboard-configs/active"

# 获取指定仪表盘数据
bash scripts/assethub_api.sh request GET "/dashboard-configs/{id}/data"
```

### 🏥 合规管理补充（/compliance）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/compliance/health` | GET | 合规健康检查 |
| `/compliance/dashboard-stats` | GET | 合规仪表盘统计 |
| `/special-equipment/statistics/overview` | GET | 特种设备统计概览 |
| `/special-equipment/expiring-inspections` | GET | 特种设备检验到期 |
| `/staff/qualifications/expiring` | GET | 人员资质到期预警 |
| `/staff/training-records` | GET/POST | 培训记录 |

```bash
# 合规健康检查
bash scripts/assethub_api.sh request GET "/compliance/health"

# 合规仪表盘统计
bash scripts/assethub_api.sh request GET "/compliance/dashboard-stats"

# 特种设备统计概览
bash scripts/assethub_api.sh request GET "/special-equipment/statistics/overview"

# 特种设备检验到期列表
bash scripts/assethub_api.sh request GET "/special-equipment/expiring-inspections"

# 人员资质到期预警
bash scripts/assethub_api.sh request GET "/staff/qualifications/expiring"
```

### 👥 用户管理补充（/users）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/users/register` | POST | 用户注册 |
| `/users/pending` | GET | 待审批用户列表 |
| `/users/{id}` | GET/PUT/DELETE | 用户详情/更新/删除 |
| `/users/{id}/change-password` | PUT | 修改密码 |
| `/users/join-enterprise` | POST | 申请加入企业 |
| `/users/role-requests/pending` | GET | 待审批角色申请 |
| `/users/role-requests/{id}/approve` | PUT | 审批角色申请 |

```bash
# 用户注册
bash scripts/assethub_api.sh request POST "/users/register" '{
  "username": "zhangsan",
  "password": "Password123",
  "real_name": "张三",
  "phone": "13800138000"
}'

# 待审批用户
bash scripts/assethub_api.sh request GET "/users/pending?page=1&pageSize=20"

# 审批用户
bash scripts/assethub_api.sh request PUT "/users/{id}/approve" '{
  "approved": true,
  "opinion": "同意"
}'

# 修改密码
bash scripts/assethub_api.sh request PUT "/users/{id}/change-password" '{
  "old_password": "oldpass",
  "new_password": "newpass"
}'

# 加入企业
bash scripts/assethub_api.sh request POST "/users/join-enterprise" '{
  "enterprise_code": "ENT-001",
  "username": "zhangsan"
}'
```

### 📉 折旧补充（/depreciation）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/depreciation/{id}` | GET | 单条折旧详情 |
| `/depreciation/export` | GET | 导出折旧报表 |
| `/depreciation/depreciation/methods` | GET | 折旧方法列表 |
| `/depreciation/depreciation/summary/by-department` | GET | 按部门折旧汇总（嵌套） |

```bash
# 折旧详情
bash scripts/assethub_api.sh request GET "/depreciation/{id}"

# 导出折旧报表
bash scripts/assethub_api.sh request GET "/depreciation/export"

# 折旧方法列表
bash scripts/assethub_api.sh request GET "/depreciation/methods"

# 按部门折旧汇总（嵌套路径）
bash scripts/assethub_api.sh request GET "/depreciation/depreciation/summary/by-department"
```

### 📦 盘点补充（/inventory）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/inventory/self/windows` | GET | 获取当前可用的自助盘点窗口 |
| `/inventory/self/assets` | GET | 自助盘点—获取可盘点资产 |
| `/inventory/self/confirm` | POST | 自助盘点确认 |
| `/inventory/{id}/scan` | POST | 扫码盘点 |
| `/inventory/{id}/scan-logs` | GET | 盘点扫码日志 |
| `/inventory-reports/export/inventory-records` | GET | 导出盘点记录 |
| `/inventory-reports/export/inventory-discrepancies` | GET | 导出盘点差异 |
| `/inventory-discrepancies/generate-from-details` | POST | 从盘点明细自动生成差异 |

```bash
# 获取自助盘点窗口
bash scripts/assethub_api.sh request GET "/inventory/self/windows"

# 自助盘点—可盘点资产
bash scripts/assethub_api.sh request GET "/inventory/self/assets?page=1&pageSize=50"

# 自助盘点确认
bash scripts/assethub_api.sh request POST "/inventory/self/confirm" '{
  "inventory_id": 123,
  "confirmed_assets": ["XXX-001", "XXX-002"]
}'

# 扫码盘点
bash scripts/assethub_api.sh request POST "/inventory/{id}/scan" '{
  "asset_code": "XXX-001",
  "scan_result": "在用",
  "actual_location": "放射科"
}'

# 从盘点明细自动生成差异
bash scripts/assethub_api.sh request POST "/inventory-discrepancies/generate-from-details" '{
  "inventory_id": 123
}'
```

### 📄 文档管理补充（/technical-documents）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/technical-documents/{id}/file` | GET | 下载文档文件 |
| `/technical-documents/assets/{assetIdOrCode}` | GET | 查询某资产关联的文档 |
| `/technical-documents/pending` | GET | 待审核文档列表 |
| `/technical-documents/ai/ocr` | POST | AI 识别文档内容（OCR） |
| `/technical-documents/ai/preview/{id}` | GET | AI 预览文档 |
| `/technical-documents/enhanced/statistics` | GET | 文档增强统计 |

```bash
# 下载文档文件
bash scripts/assethub_api.sh request GET "/technical-documents/{id}/file"

# 查询资产关联文档
bash scripts/assethub_api.sh request GET "/technical-documents/assets/XXX-001"

# 待审核文档
bash scripts/assethub_api.sh request GET "/technical-documents/pending?page=1&pageSize=20"

# AI OCR 识别
bash scripts/assethub_api.sh request POST "/technical-documents/ai/ocr" '{
  "document_id": 123
}'

# AI 预览文档
bash scripts/assethub_api.sh request GET "/technical-documents/ai/preview/{id}"
```

### 🛒 采购补充（/procurement）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/procurement/stats` | GET | 采购统计 |
| `/procurement/{id}/files` | POST | 上传采购相关文件 |

```bash
# 采购统计
bash scripts/assethub_api.sh request GET "/procurement/stats"

# 上传采购文件
bash scripts/assethub_api.sh request POST "/procurement/{id}/files"
```

### 🗄️ 闲置/调配/报废补充

| 端点 | 方法 | 说明 |
|------|------|------|
| `/idle/{id}` | GET/DELETE | 闲置详情/删除闲置 |
| `/transfer/{id}` | GET/DELETE | 调配详情/删除调配 |
| `/scrapping/{id}/appraise` | POST | 报废资产评估 |
| `/scrapping/{id}/dispose` | POST | 报废处置 |
| `/scrapping/statistics/summary` | GET | 报废统计汇总 |

```bash
# 闲置详情
bash scripts/assethub_api.sh request GET "/idle/{id}"

# 调配详情
bash scripts/assethub_api.sh request GET "/transfer/{id}"

# 报废资产评估
bash scripts/assethub_api.sh request POST "/scrapping/{id}/appraise" '{
  "appraised_value": 5000,
  "appraiser": "评估员"
}'

# 报废处置
bash scripts/assethub_api.sh request POST "/scrapping/{id}/dispose" '{
  "dispose_method": "回收",
  "dispose_date": "2026-05-01"
}'

# 报废统计
bash scripts/assethub_api.sh request GET "/scrapping/statistics/summary"
```

### 📍 资产定位补充（/asset-location）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/asset-location/assets/{assetIdOrCode}/location` | GET/POST | 获取/上报资产位置 |
| `/asset-location/assets/{assetIdOrCode}/bind-device` | POST | 绑定定位设备 |
| `/asset-location/assets/{assetIdOrCode}/unbind-device` | POST | 解绑定位设备 |
| `/asset-location/assets/in-area` | POST | 查询某区域内的资产 |

```bash
# 获取资产当前位置
bash scripts/assethub_api.sh request GET "/asset-location/assets/{assetIdOrCode}/location"

# 上报资产位置
bash scripts/assethub_api.sh request POST "/asset-location/assets/{assetIdOrCode}/location" '{
  "latitude": 31.23,
  "longitude": 121.47,
  "location_code": "A-01-01"
}'

# 绑定定位设备
bash scripts/assethub_api.sh request POST "/asset-location/assets/{assetIdOrCode}/bind-device" '{
  "device_id": "BEACON-001"
}'

# 查询区域内的资产
bash scripts/assethub_api.sh request POST "/asset-location/assets/in-area" '{
  "location_code": "A-01",
  "floor": 1
}'
```

### 🏷️ 标签管理补充（/asset-labels）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/asset-labels/templates/{id}` | GET/PUT/DELETE | 标签模板详情/更新/删除 |
| `/asset-labels/print-queue` | GET | 打印队列列表 |
| `/asset-labels/print-queue/{id}/status` | PUT | 更新打印任务状态 |

```bash
# 标签模板详情
bash scripts/assethub_api.sh request GET "/asset-labels/templates/{id}"

# 更新标签模板
bash scripts/assethub_api.sh request PUT "/asset-labels/templates/{id}" '{
  "name": "标准资产标签（更新）",
  "width": 4,
  "height": 2
}'

# 删除标签模板
bash scripts/assethub_api.sh request DELETE "/asset-labels/templates/{id}"

# 打印队列
bash scripts/assethub_api.sh request GET "/asset-labels/print-queue"

# 更新打印状态
bash scripts/assethub_api.sh request PUT "/asset-labels/print-queue/{id}/status" '{
  "status": "completed"
}'
```

### 🔔 智能预警补充（/intelligent-alerts）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/intelligent-alerts/maintenance` | GET | 保养到期预警 |
| `/intelligent-alerts/inspections` | GET | 特种设备检验到期预警 |
| `/intelligent-alerts/qualifications` | GET | 人员资质到期预警 |
| `/intelligent-alerts/safety` | GET | 安全检测到期预警 |
| `/intelligent-alerts/uptime` | GET | 开机率异常预警 |
| `/intelligent-alerts/settings` | GET/POST | 预警设置 |
| `/intelligent-alerts/handle-all` | POST | 批量处理预警 |

```bash
# 保养到期预警
bash scripts/assethub_api.sh request GET "/intelligent-alerts/maintenance"

# 特种设备检验到期预警
bash scripts/assethub_api.sh request GET "/intelligent-alerts/inspections"

# 人员资质到期预警
bash scripts/assethub_api.sh request GET "/intelligent-alerts/qualifications"

# 开机率异常预警
bash scripts/assethub_api.sh request GET "/intelligent-alerts/uptime"

# 预警设置
bash scripts/assethub_api.sh request POST "/intelligent-alerts/settings" '{
  "alert_types": ["maintenance", "inspections"],
  "enabled": true,
  "channels": ["sms"]
}'

# 批量处理预警
bash scripts/assethub_api.sh request POST "/intelligent-alerts/handle-all"
```

### 🏥 IoT 补充（/iot）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/iot/health` | GET | IoT 服务健康检查 |
| `/iot/asset-monitoring/assets/{assetCode}/latest` | GET | 资产最新监测数据 |
| `/iot/asset-monitoring/assets/{assetCode}/series` | GET | 资产监测时序数据 |
| `/iot/patient-volume/assets/{assetCode}/latest` | GET | 设备病患量最新数据 |
| `/iot/patient-volume/assets/{assetCode}/series` | GET | 设备病患量时序数据 |
| `/iot/patient-volume/assets/usage-stats` | GET | 设备使用统计 |

```bash
# IoT 健康检查
bash scripts/assethub_api.sh request GET "/iot/health"

# 资产监测最新数据
bash scripts/assethub_api.sh request GET "/iot/asset-monitoring/assets/{assetCode}/latest"

# 资产监测时序数据
bash scripts/assethub_api.sh request GET "/iot/asset-monitoring/assets/{assetCode}/series?start_time=2026-04-01&end_time=2026-04-30"

# 设备病患量最新
bash scripts/assethub_api.sh request GET "/iot/patient-volume/assets/{assetCode}/latest"

# 设备使用统计
bash scripts/assethub_api.sh request GET "/iot/patient-volume/assets/usage-stats"
```

### 🔑 角色权限补充（/roles-permissions）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/roles-permissions/permissions/list` | GET | 权限列表 |
| `/roles-permissions/permissions/definitions` | GET | 权限定义 |
| `/roles-permissions/menus/list` | GET | 菜单列表 |
| `/roles-permissions/menus/definitions` | GET | 菜单定义 |
| `/roles-permissions/roles` | POST | 创建角色 |
| `/roles-permissions/roles/{role}` | PUT/DELETE | 更新/删除角色 |
| `/roles-permissions/user/check-permission` | POST | 检查用户权限 |
| `/enhanced-permissions/users/{userId}/data-scope` | GET/PUT | 用户数据范围 |

```bash
# 权限列表
bash scripts/assethub_api.sh request GET "/roles-permissions/permissions/list"

# 菜单列表
bash scripts/assethub_api.sh request GET "/roles-permissions/menus/list"

# 创建角色
bash scripts/assethub_api.sh request POST "/roles-permissions/roles" '{
  "role": "technician",
  "name": "维修技师",
  "permissions": ["maintenance.view", "maintenance.create"],
  "menus": ["maintenance", "assets"]
}'

# 更新角色
bash scripts/assethub_api.sh request PUT "/roles-permissions/roles/technician" '{
  "permissions": ["maintenance.view", "maintenance.create", "maintenance.approve"],
  "menus": ["maintenance", "assets", "inventory"]
}'

# 检查用户权限
bash scripts/assethub_api.sh request POST "/roles-permissions/user/check-permission" '{
  "user_id": 1,
  "permission": "maintenance.approve"
}'

# 用户数据范围
bash scripts/assethub_api.sh request GET "/enhanced-permissions/users/{userId}/data-scope"
```

### 🏠 部门管理补充（/departments）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/departments/{id}` | GET/PUT/DELETE | 部门详情/更新/删除 |
| `/departments/health` | GET | 部门健康状态 |

```bash
# 部门详情
bash scripts/assethub_api.sh request GET "/departments/{id}"

# 更新部门
bash scripts/assethub_api.sh request PUT "/departments/{id}" '{
  "department_name": "心内科（更新）",
  "parent_code": "ROOT"
}'

# 删除部门
bash scripts/assethub_api.sh request DELETE "/departments/{id}"

# 部门健康状态
bash scripts/assethub_api.sh request GET "/departments/health"
```

### 🏥 开机率管理（/uptime）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/uptime/statistics` | GET/POST | 开机率统计数据 |
| `/uptime/statistics/overview` | GET | 开机率概览 |
| `/uptime/statistics/dashboard` | GET | 开机率仪表盘 |
| `/uptime/operation-logs` | GET/POST | 开关机操作日志 |
| `/uptime/config` | GET | 开机率配置 |

```bash
# 开机率概览
bash scripts/assethub_api.sh request GET "/uptime/statistics/overview"

# 开机率仪表盘
bash scripts/assethub_api.sh request GET "/uptime/statistics/dashboard"

# 开机率操作日志
bash scripts/assethub_api.sh request GET "/uptime/operation-logs?page=1&pageSize=20"

# 记录开关机操作
bash scripts/assethub_api.sh request POST "/uptime/operation-logs" '{
  "asset_code": "XXX-001",
  "operation": "开机",
  "operator": "张三",
  "operation_time": "2026-05-01 08:00:00"
}'
```

### 📊 资产统计补充

| 端点 | 方法 | 说明 |
|------|------|------|
| `/assets/statistics/by-department` | GET | 按部门统计资产 |
| `/assets/statistics/expiring-warranties` | GET | 即将过保资产 |
| `/assets/duplicate-check` | GET | 检查资产编码是否重复 |

```bash
# 按部门资产统计
bash scripts/assethub_api.sh request GET "/assets/statistics/by-department"

# 即将过保资产
bash scripts/assethub_api.sh request GET "/assets/statistics/expiring-warranties?days=30"

# 检查资产编码重复
bash scripts/assethub_api.sh request GET "/assets/duplicate-check?asset_code=XXX-001"
```

### 💾 备份补充（/backup）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/backup/add-tenant-id` | POST | 为表添加 tenant_id 字段（多租户迁移） |
| `/backup/{id}/download` | GET | 下载备份文件 |

```bash
# 下载备份文件
bash scripts/assethub_api.sh request GET "/backup/{id}/download"

# 添加 tenant_id 字段
bash scripts/assethub_api.sh request POST "/backup/add-tenant-id" '{
  "table_name": "assets"
}'
```

### 🌐 国际化（/i18n）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/i18n/locales` | GET | 获取支持的语言列表 |
| `/i18n/messages/{locale}` | GET | 获取指定语言的翻译文本 |
| `/i18n/translate` | POST | 翻译文本 |

```bash
# 支持的语言
bash scripts/assethub_api.sh request GET "/i18n/locales"

# 获取中文翻译
bash scripts/assethub_api.sh request GET "/i18n/messages/zh-CN"

# 翻译文本
bash scripts/assethub_api.sh request POST "/i18n/translate" '{
  "text": "Hello",
  "target_locale": "zh-CN"
}'
```

### 🔌 系统健康检查补充

| 端点 | 方法 | 说明 |
|------|------|------|
| `/health/ready` | GET | 系统就绪检查 |
| `/health/alive` | GET | 服务存活检查 |
| `/health/metrics` | GET | 监控指标（Prometheus 格式） |
| `/health/circuit-breakers` | GET | 断路器状态 |
| `/health/circuit-breakers/{name}/reset` | POST | 重置断路器 |

```bash
# 就绪检查
bash scripts/assethub_api.sh request GET "/health/ready"

# 存活检查
bash scripts/assethub_api.sh request GET "/health/alive"

# 监控指标
bash scripts/assethub_api.sh request GET "/health/metrics"

# 断路器状态
bash scripts/assethub_api.sh request GET "/health/circuit-breakers"

# 重置断路器
bash scripts/assethub_api.sh request POST "/health/circuit-breakers/{name}/reset"
```

---

# ⚠️ 重要兼容说明

## 维修申请字段

- **必填**: `asset_code` + `fault_description`
- **兼容旧文档**: 可同时传 `issue_description`（与 `fault_description` 相同值）

## 调配申请

- 新版路径: `POST /api/transfer`
- 旧版路径: `POST /api/assets/{id}/transfer-apply`（兼容 `asset_code` 参数）

## 闲置发布

- `publish_person` 必填
- `asset_code` 和 `asset_name` 至少一个

## 报废申请

- 必填: `asset_code`, `asset_name`, `applicant`, `scrapping_reason`

## 盘点计划

- 新版路径: `/inventory-plans`（推荐）
- 旧版路径: `/inventory`

---

# 📤 输出格式规范

**查询结果统一用表格展示**，字段包括：
- 编号/ID、名称/标题、状态
- 关联资产/部门/人员
- 创建时间/更新时间
- 关键数值（价格、数量、费用等）

**统计类查询**应包含合计行和关键洞察。

**操作结果**先展示操作内容，再展示回查确认结果。

---

# 📍 常见设备名称映射

| 用户说 | 系统资产名称 |
|--------|------------|
| 监护仪 | 插件式病人监护仪 |
| 心电/心电图机 | 数字式多道心电图机、12导联心电图机等 |
| 呼吸机 | 呼吸机 |
| 注射泵 | 注射泵 |
| 除颤仪 | 体外除颤监护仪 |
| 血液透析 | 血液透析设备(血液透析滤过机) |
| CT | CT机、16层CT机、64排螺旋CT等 |
| 核磁共振 | 核磁共振成像设备(MRI) |
| 车辆/机动车 | 救护车、轿车、客车、旅行车、核酸检测车、铲车、装载机、电动车（指机动车，非手推车） |

---

# 📝 故障描述规范

报修时的描述应尽量具体：

| 规范 | 示例 |
|------|------|
| ✅ 正确 | "显示屏不亮，无法开机" |
| ✅ 正确 | "心电导联无信号" |
| ✅ 正确 | "CT球管打火，报警E01" |
| ❌ 错误 | "坏了" / "不能用" / "故障" |

---

# 🔢 状态值速查

| 资源 | 状态值 |
|------|--------|
| 资产 | `在用` / `维修` / `闲置` / `调配中` / `报废` |
| 维修申请 | `pending` / `approved` / `in_progress` / `completed` / `cancelled` |
| 调配 | `pending` / `approved` / `rejected` / `completed` |
| 盘点计划 | `draft` / `active` / `completed` / `cancelled` |
| 盘点任务 | `pending` / `in_progress` / `completed` / `cancelled` |
| 采购 | `pending` / `approved` / `rejected` / `executed` / `completed` |
| 报废 | `pending` / `approved` / `rejected` / `completed` |
| 质检结果 | `合格` / `不合格` / `待整改` |
| 文档审核 | `pending` / `approved` / `rejected` |

---

# 📝 经验教训（基于实际操作发现）

## 2026-04-02 关键发现：科室资产多字段分布问题

**问题现象：**
- 查询"检验科资产"时，使用 `department=检验科` 参数只返回 0 条记录
- 全量扫描（遍历所有页 + 所有文本字段）后，发现检验科实际有 **550 件资产**

**根本原因：**
AssetHub 的科室信息分散存储在多个字段：
- `department` — 正式科室字段（很多资产此处为空）
- `location` — 位置字段，包含大量科室信息（如"检验科（崇山）"）
- `use_department` — 使用科室字段
- `department_new` — 新版科室字段

**经验：**
1. 查询科室资产时，**必须**对所有文本字段做关键词匹配，不能依赖单一 department 参数
2. 全量扫描时需遍历**所有页**（总资产 28291 条 × 95 页）
3. 车辆识别需要排除"输液车/处置车/抢救车"等医用小型手推车

## 2026-04-02 发现：API 安全机制与 AI 入口

**问题现象：**
- 直接调用 `/maintenance/requests` POST 无 Idempotency-Key → 返回"需要 Idempotency-Key"
- 带 Idempotency-Key 调用普通端点 → 触发二次确认，返回 confirmToken
- 带 Idempotency-Key 调用 AI 入口 `/maintenance/ai/submit-request` → **直接成功**，无需二次确认

**经验：**
1. 所有写操作必须带 `Idempotency-Key: op-$(date +%s)-$RANDOM`
2. **报修走 AI 安全入口** `POST /maintenance/ai/submit-request`，一次完成，不触发二次确认
3. 普通端点需两段式：第一次拿 confirmToken，第二次带 `X-Risk-Confirm-Token` 重放
