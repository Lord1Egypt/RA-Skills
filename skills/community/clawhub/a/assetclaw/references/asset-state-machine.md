# AssetHub 资产状态机

> 资产状态机是资产管理系统的核心。所有跨模块操作（维修、调配、闲置、报废）最终都会落到状态流转上。本文件给出完整状态定义、流转图、流转入口和客户端应对方式。

---

## 1. 状态枚举

| 中文值 | 英文值 | 含义 |
|--------|--------|------|
| `在用` | `in_use` | 正常在用状态（默认） |
| `闲置` | `idle` | 闲置中，未被任何科室使用 |
| `维修` | `maintenance` | 正在维修（含工单执行中） |
| `报废` | `scrapped` | 已审批报废，下线 |
| `调配中` | `transferring` | 正在转移部门（流程未完成） |

---

## 2. 状态流转图

```
              ┌─────────┐
              │  闲置   │ ◄────── 闲置发布取消
              │  idle   │
              └────┬────┘
                   │ 调配再利用
                   ▼
┌─────────┐  维修完成   ┌─────────┐
│  在用   │ ◄────────── │  维修   │
│ in_use  │             │ maintenance │
└────┬────┘             └────┬────┘
     │                       │
     │ 维修开始               │ 报废审批通过
     ▼                       ▼
┌─────────┐             ┌─────────┐
│  维修   │ ──────────► │  报废   │
│ maintenance│           │ scrapped│
└─────────┘             └─────────┘

     ▲
     │ 调配中
     │
┌─────────┐
│ 调配中  │ ──────► 在用（新部门）
│transferring│
└─────────┘
```

**简化图**：

```
在用 ──► 闲置 ──► 在用（再利用）
 │
 ├──► 维修 ──► 在用 / 报废
 │   ──► 报废
 ├──► 调配中 ──► 在用（新部门）
 └──► 报废
```

---

## 3. 流转入口（按目标状态分组）

### 3.1 在用 → 闲置

- 入口：`POST /api/idle`（`/api/idle/assets`）
- 触发：发布闲置
- Body：`asset_code`、`publish_person`、`publish_reason`
- 回查：`GET /api/idle/assets?status=published`

### 3.2 闲置 → 在用

- 入口：`PUT /api/idle/:id/allocate`
- 触发：调配闲置资产到目标科室
- Body：`target_department`、`allocate_date`

### 3.3 闲置 → 在用（取消）

- 入口：`PUT /api/idle/:id/cancel`
- 触发：取消闲置发布，资产回到「在用」

### 3.4 在用 → 维修

- 入口：`POST /api/maintenance/ai/submit-request`（推荐，AI 安全入口）
- 备选：`POST /api/maintenance-management/requests`（普通端点，触发二次确认）
- Body 必填：`asset_code`、`fault_description`

### 3.5 维修 → 在用

- 入口：`POST /api/maintenance/requests/:id/complete`
- 触发：维修完成
- Body：`repair_content`、`repair_cost`、`parts_replaced`

### 3.6 维修 → 报废（维修中报废）

- 入口：先 `POST /api/scrapping` 创建报废申请，再 `POST /api/scrapping/:id/approve`
- 触发：维修判定无修复价值

### 3.7 在用 → 报废（直接报废）

- 入口：`POST /api/scrapping`
- Body：`asset_code`、`asset_name`、`applicant`、`scrapping_reason`、`estimated_value`
- 后续：`/approve` → `/complete`

### 3.8 在用 → 调配中 → 在用（新部门）

- 入口 1（提交申请）：
  - 新：`POST /api/assets/transfer-requests`
  - 旧：`POST /api/assets/:id/transfer-apply`
- 入口 2（审批）：`POST /api/assets/transfer-requests/:request_id/approve`
- 入口 3（执行）：`PUT /api/transfer/:id/complete`

---

## 4. 状态机非法流转示例

| 非法操作 | 响应 |
|----------|------|
| 报废状态 → 维修 | `422 UNPROCESSABLE_ENTITY` 状态机非法 |
| 闲置状态 → 维修 | `422` 闲置资产需先「再利用」到在用 |
| 维修状态 → 调配中 | `422` 维修完成后再调配 |
| 调配中 → 报废 | 视实现（通常需先 `complete` 调配，再发起报废） |

---

## 5. 流转历史查询

### 5.1 资产级历史

```
GET /api/assets/:id/transitions
```

返回该资产的所有状态流转记录（`from_status`、`to_status`、`reason`、`operator`、`created_at`）。

### 5.2 资产变更日志

```
GET /api/assets/:id/change-logs
```

返回字段变更历史（`field`、`old_value`、`new_value`、`changed_by`、`changed_at`）。

---

## 6. 客户端处理建议

### 6.1 查询前先看状态

```python
asset = GET /api/assets/{id}
if asset['status'] != '在用':
    raise CannotRepairError(f"资产当前状态：{asset['status']}，无法报修")
```

### 6.2 写后立即回查

```python
POST /api/maintenance/ai/submit-request  # 维修申请
↓
GET /api/maintenance/requests/{id}  # 回查
↓
GET /api/assets/{id}  # 看资产状态是否变更为「维修」
```

### 6.3 高危操作二次确认

如果目标流转触发 428（如直接报废审批），按 `api-conventions.md` 第 6 节处理。

### 6.4 失败重试策略

- 状态机非法流转（422）：**不要**重试，需修改请求或纠正前置状态
- 高危网关 428：见 `api-conventions.md` 第 6 节
- 限流 429：退避后重试

---

## 7. 工作流引擎

- 路径：`/api/workflow`
- 端点：
  - `GET /api/workflow/default` —— 默认工作流
  - `GET /api/workflow/states` —— 状态定义
  - `GET /api/workflow/transitions` —— 迁移规则
  - `POST /api/workflow/transition/:asset_id` —— 执行状态迁移
  - `GET /api/assets/:id/transitions` —— 资产可执行的迁移列表

工作流引擎是**配置化**的状态机：租户管理员可自定义状态与流转规则；OpenClaw skill 默认按上述标准状态流转处理，自定义情况需查询 `/workflow/transitions` 动态适配。

---

## 8. 状态值在数据库中的对应

- 字段名：`status`（字符串，中文值）
- 索引：通常在 `assets.status` 上有索引
- 查询示例：`GET /api/assets?status=在用&pageSize=20`

### 8.1 部分端点使用英文值

维修相关端点（`/maintenance/requests`）状态字段：

| 中文值 | 英文值（部分端点） |
|--------|------------------|
| 待审批 | `pending` |
| 已批准 | `approved` |
| 维修中 | `in_progress` |
| 已完成 | `completed` |
| 已拒绝 | `rejected` |
| 已取消 | `cancelled` |

**客户端处理**：查询时优先用**中文值**；如返回为空，尝试英文值。

---

## 9. 参考来源

- `backend/services/asset-state-machine.js`（状态机实现）
- `backend/routes/workflow.js`（工作流配置）
- `backend/services/scrapping/`（报废流转）
- `backend/services/transfer/`（调配流转）
- `backend/services/maintenance/`（维修流转）
- `backend/modules/asset-management/`（资产状态字段）