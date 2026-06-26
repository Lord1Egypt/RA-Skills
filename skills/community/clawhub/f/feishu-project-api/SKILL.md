---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: aaa188b6ae8741f41867870539adec8b
    PropagateID: aaa188b6ae8741f41867870539adec8b
    ReservedCode1: 304402200590abf7b187929d774ccdd09ef8ff1ff1bebf094dce28beb065f0073af80c7c02204fc588b6761f419388e5e73db119bf7c6c3aa5da8737cc4fc47842c50b222f0e
    ReservedCode2: 3046022100b3d47fbaa3082764dc2479abf9a0e1d42bf02bf1d3a4500def42b95042495661022100836d7db760316653e802081033b3c39efa3473a3d723eeef9cfae2981f01b7ca
description: 飞书项目Open API技能，查询/创建/更新/删除工作项，管理流程模板、节点配置、自定义字段、视图和角色权限，批量分析商机进度与风险。触发：查商机、分析进度、管理工作项模板、批量更新任务、流程配置。
name: feishu-project-api
---

# 飞书项目 Open API 技能

> 适用场景：工作项全生命周期管理、流程模板配置、自定义字段管理、视图管理、商机进度与风险分析、批量任务操作。
> 核心价值：无需手动操作，自动化完成项目管理工作，输出结构化分析报告。

---

## ⚡ 能力总览

| 能力分类 | 支持操作 |
|---------|---------|
| **工作项管理** | 查询、创建、更新、删除、终止/恢复 |
| **流程与节点** | 流转节点、更新节点负责人、获取工作流详情 |
| **子任务** | 创建、更新、完成、删除子任务 |
| **模板管理** | 获取/新增/更新/删除流程模板，配置节点规则 |
| **自定义字段** | 创建、更新、删除字段，管理字段选项 |
| **工作项类型** | 获取类型配置、更新类型基础信息 |
| **视图管理** | 创建/更新/删除固定视图、条件视图、全景视图 |
| **角色配置** | 获取流程角色与人员配置 |
| **评论管理** | 添加/查询/更新/删除工作项评论 |
| **工时管理** | 登记/更新/删除工时记录 |
| **进度分析** | 批量查询工作项，分析停滞风险，生成报告 |

---

## 🔑 快速开始

### 工具调用格式

```
feishu_project_api({
  method: "POST",
  path: "/work_item/{type_key}/filter",
  body: { work_item_type_keys: ["xxx"], page_size: 50 }
})
```

### 必知概念

- **`{project_key}`** — 项目唯一标识，从 URL 中提取（如 `wrza2p`）
- **`{work_item_type_key}`** — 工作项类型 ID（如商机 `67da250a6f31f4ecc390a619`）
- **`{work_item_id}`** — 具体工作项实例 ID（如 `5982710249`）
- **`{template_id}`** — 流程模板 ID

---

## 📋 工作项管理

### 查询单个工作项详情
```
POST /open_api/{project_key}/work_item/{work_item_type_key}/query
body: { work_item_ids: [工作项ID] }
```

### 批量筛选工作项
```
POST /open_api/{project_key}/work_item/filter
body: {
  work_item_type_keys: ["type_key1", "type_key2"],
  page_size: 50
}
```

### 创建工作项
```
POST /open_api/{project_key}/work_item/create
body: {
  work_item_type: "type_key",
  fields: { title: "工作项标题", assignee: { user_key: "负责人user_key" } }
}
```

### 更新工作项
```
PUT /open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}
body: { fields: { 字段key: 新值 } }
```

### 删除工作项
```
DELETE /open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}
```

### 终止/恢复工作项
```
PUT /open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/abort
```

---

## 🔧 流程模板管理（重点能力）

### 获取工作项下的所有流程模板
```
GET /open_api/{project_key}/template_list/{work_item_type_key}
```

### 获取单个流程模板的详细配置
```
GET /open_api/{project_key}/template_detail/{template_id}
```
> 返回节点信息配置、节点流转配置（角色负责人、节点条件等）

### 新增流程模板
```
POST /open_api/template/v2/create_template
body: {
  project_key: "wrza2p",
  work_item_type_key: "67da250a6f31f4ecc390a619",
  name: "新流程模板名称",
  description: "模板描述",
  // 其他模板配置字段
}
```

### 更新流程模板
```
PUT /open_api/template/v2/update_template
body: {
  template_id: "template_id",
  name: "更新后的模板名称",
  // 需要更新的字段
}
```

### 删除流程模板
```
DELETE /open_api/template/v2/delete_template/{project_key}/{template_id}
```

---

## 🗂️ 自定义字段管理（重点能力）

### 获取空间或工作项类型下的所有字段
```
POST /open_api/{project_key}/field/all
body: { work_item_type_key: "type_key" }
```

### 在工作项类型下创建自定义字段
```
POST /open_api/{project_key}/field/{work_item_type_key}/create
body: {
  field_name: "字段名称",
  field_type: "text",  // text/number/date/user/select 等
  required: false,
  description: "字段说明"
}
```

### 更新自定义字段配置
```
PUT /open_api/{project_key}/field/{work_item_type_key}
body: {
  field_id: "字段ID",
  field_name: "更新后名称",
  // 其他可更新配置
}
```

### 工作项类型基础信息更新
```
PUT /open_api/{project_key}/work_item/type/{work_item_type_key}
body: { name: "类型新名称", description: "类型描述" }
```

---

## 📊 视图管理（重点能力）

### 获取视图列表
```
POST /open_api/{project_key}/view_conf/list
body: { page_size: 20 }
```

### 创建固定视图
```
POST /open_api/{project_key}/{work_item_type_key}/fix_view
body: { name: "视图名称", filters: [...] }
```

### 创建条件视图
```
POST /open_api/view/v1/create_condition_view
body: {
  project_key: "wrza2p",
  work_item_type_key: "type_key",
  name: "条件视图名称",
  conditions: [{ field_key: "status", operator: "is", value: ["open"] }]
}
```

### 更新条件视图
```
POST /open_api/view/v1/update_condition_view
body: { view_id: "视图ID", conditions: [...], collaborators: [...] }
```

### 删除视图
```
DELETE /open_api/{project_key}/fix_view/{view_id}
```

---

## 🔁 节点与流转管理

### 获取工作项工作流详情（含节点信息）
```
GET /open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/workflow/query
```

### 获取 WBS 工作流详情
```
GET /open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/wbs_view
```

### 更新节点（负责人、排期、表单）
```
PUT /open_api/{project_key}/workflow/{work_item_type_key}/{work_item_id}/node/{node_id}
body: {
  assignee: { user_key: "user_key" },
  due: "2026-04-30",
  fields: { 字段key: 新值 }
}
```

### 节点完成/回滚
```
POST /open_api/{project_key}/workflow/{work_item_type_key}/{work_item_id}/node/{node_id}/operate
body: { action: "complete" }  // 或 "rollback"
```

### 状态流转
```
POST /open_api/{project_key}/workflow/{work_item_type_key}/{work_item_id}/node/state_change
body: { target_state: "done", fields: {...} }
```

---

## 🧒 子任务管理

### 创建子任务
```
POST /open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/workflow/task
body: { node_id: "节点ID", title: "子任务标题", assignee: {...} }
```

### 更新子任务
```
POST /open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/workflow/{node_id}/task/{task_id}
body: { title: "更新标题", status: "done" }
```

### 子任务完成/回滚
```
POST /open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/subtask/modify
body: { task_id: "task_id", action: "complete" }
```

---

## 💬 评论管理

### 添加评论
```
POST /open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/comment/create
body: { content: "评论内容" }
```

### 查询评论
```
GET /open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/comments
```

---

## ⏱️ 工时管理

### 添加工时记录
```
POST /open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/work_hour_record
body: { hours: 4, date: "2026-04-04", user_key: "user_key" }
```

### 查询工时记录
```
POST /open_api/work_item/man_hour/records
body: { work_item_ids: ["id1", "id2"] }
```

---

## 🔍 进度与风险分析（标准分析流程）

### 第1步：获取全量工作项
```
POST /open_api/{project_key}/work_item/filter
body: { work_item_type_keys: ["type_key"], page_size: 100 }
```

### 第2步：提取关键字段
```
返回数据中提取：
- id / name / sub_stage / state_name / progress
- current_owners / fields（字典格式）
```

### 第3步：进度分组统计
```
按 state_name 分组 → 计算各状态占比
识别停滞节点（>30天无更新 → 黄色预警）
```

### 第4步：风险识别
```
单负责人 >5个子项 → 负载风险
停滞 >60天 → 红色预警
100%停滞在同一节点 → 系统性瓶颈
```

### 第5步：生成分析报告
```
输出结构：执行摘要 → 现状 → 风险 → 建议
```

---

## 🔗 工作项关联关系管理

### 获取空间下所有关联关系
```
GET /open_api/{project_key}/work_item/relation
```

### 新增关联关系
```
POST /open_api/work_item/relation/create
body: { name: "关系名称", source_type: "type1", target_type: "type2" }
```

### 绑定/解绑关联工作项
```
POST /open_api/{project_key}/relation/{work_item_type_key}/{work_item_id}/batch_bind
DELETE /open_api/{project_key}/relation/{work_item_type_key}/{work_item_id}
```

---

## 🚨 常见错误处理

| 错误码 | 含义 | 解决 |
|--------|------|------|
| 20039 | 缺少 X-USER-KEY | 确认 user_key 正确配置 |
| 230001 | 项目不存在 | 检查 project_key |
| 230002 | 参数错误 | 检查请求 body 格式 |
| 230003 | 类型不存在 | 检查 work_item_type_key |
| has_more=true | 还有数据 | 用 next_cursor 翻页 |

---

## 📁 已知项目配置

| 项目 | project_key | 商机type_key | 备注 |
|------|-----------|------------|------|
| LSOP（小鹏P7+） | `wrza2p` | `67da250a6f31f4ecc390a619` | 商机工作项 |

---

## 📝 分析报告模板

```markdown
# {项目名} 进度与风险分析报告

## 执行摘要
## 工作项概览
## 进度分析（按状态节点）
## 风险识别
## 负责人负载分析
## 行动建议
```
