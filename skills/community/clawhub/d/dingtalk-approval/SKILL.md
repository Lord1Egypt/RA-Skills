---
name: dingtalk-approval
description: |
  钉钉 OA 审批处理插件，支持查询待办、查看审批详情、执行同意/拒绝，以及查询假期余额。

  **当以下情况时使用此 Skill**：
  (1) 用户需要查询钉钉 OA 审批待办任务列表
  (2) 用户需要执行审批操作（同意或拒绝）
  (3) 用户提到"钉钉审批"、"OA 审批"、"待办任务"、"审批单据"
  (4) 用户要求处理钉钉工作通知或审批流程
  (5) 需要批量处理审批任务或查看审批详情
---

# DingTalk Approval (钉钉 OA 审批) SKILL

## 🚨 执行前必读

- ✅ **查询待办**：调用 `get_pending_tasks` 获取任务列表，返回包含 task_id
- ✅ **执行审批**：调用 `execute_approval_task` 时必须传入从 `get_pending_tasks` 获取的 task_id
- ⚠️ **配置要求**：需要在 openclaw.json 中配置 dingtalkUserId、appKey 和 appSecret
- ⚠️ **权限要求**：钉钉应用需要开通 OA 审批权限（process 相关 API 权限）

---

## 📋 快速索引：意图 → 工具 → 必填参数

| 用户意图 | 工具 | 必填参数 | 常用可选 |
|---------|------|---------|---------|
| 查询我的待办审批 | get_pending_tasks | 无 | - |
| 查看审批单详情 | get_task_details | task_id | - |
| 同意某个审批 | execute_approval_task | task_id, action="AGREE" | remark（审批意见） |
| 拒绝某个审批 | execute_approval_task | task_id, action="REFUSE" | remark（拒绝原因） |
| 查询我的假期余额 | get_vacation_balance | 无 | - |

---

## 🎯 核心工作流程

### 1. 查询待办任务

**调用时机**：用户询问"有什么待办"、"我的审批任务"等

**工具**：`get_pending_tasks`

**参数**：无

**返回示例**：
```
1. 请假申请 - 张三 (任务 ID: task_12345)
2. 报销审批 - 李四 (任务 ID: task_67890)
3. 合同审批 - 王五 (任务 ID: task_abcde)
```

### 2. 查看审批单详情

**调用时机**：用户想要了解审批单的详细信息（申请人、申请内容、审批流程等）

**工具**：`get_task_details`

**参数**：
- `task_id`：从 `get_pending_tasks` 返回中获取的任务 ID

**返回示例**：
```
📋 **审批单详情**

**单据标题**: 请假申请 - 张三
**申请人**: 张三
**申请时间**: 2026-03-11 10:30:00
**当前状态**: 审批中
**审批类型**: 请假申请

📝 **申请内容**:
- 请假类型：年假
- 请假天数：3 天
- 开始时间：2026-03-15
- 结束时间：2026-03-17
- 请假事由：家庭事务

🔄 **审批流程**:
- ✅ 同意 | 李四（部门经理）| 2026-03-11 11:00:00
- ⏳ 待审批 | 王五（HR）| 
```

### 3. 执行审批操作

**调用时机**：用户明确要求同意或拒绝某个审批

**工具**：`execute_approval_task`

**必填参数**：
- `task_id`：从 `get_pending_tasks` 返回中获取的任务 ID
- `action`：`"AGREE"`（同意）或 `"REFUSE"`（拒绝）

**可选参数**：
- `remark`：审批意见或备注（建议填写，特别是拒绝时）

**返回示例**：
```
审批成功：已同意任务 task_12345
```

---

## ⚙️ 配置说明

在 openclaw.json 中添加以下配置：

```json
{
  "plugins": {
    "entries": {
      "dingtalk-approval": {
        "config": {
          "dingtalkUserId": "your-dingtalk-user-id",
          "appKey": "your-app-key",
          "appSecret": "your-app-secret"
        }
      }
    }
  }
}
```

**配置项说明**：
- `dingtalkUserId`：钉钉用户 ID（用于执行审批操作）
- `appKey`：钉钉开放平台应用的 AppKey
- `appSecret`：钉钉开放平台应用的 AppSecret

**获取方式**：
1. 登录 [钉钉开放平台](https://open.dingtalk.com/)
2. 创建或选择已有应用
3. 在"凭证与基础信息"中获取 AppKey 和 AppSecret
4. 确保应用开通了"OA 审批"相关权限

---

## 🔧 工具详细参数

### get_pending_tasks

查询当前用户的 OA 审批待办任务列表。

**Parameters**: 无

**Returns**: 任务列表字符串，每行包含任务标题和 task_id

**错误处理**：
- 无待办任务：返回"当前没有待办单据"
- API 异常：返回具体错误信息

---

### execute_approval_task

执行 OA 审批的同意或拒绝操作。

**Parameters**:
- `task_id` (string, required): 待办任务的唯一 ID（从 get_pending_tasks 获取）
- `action` (string, required): 审批动作，枚举值 ["AGREE", "REFUSE"]
- `remark` (string, optional): 审批意见/备注

**Returns**: 成功或失败消息

**错误处理**：
- task_id 无效：返回 API 错误信息
- 权限不足：返回权限错误
- 网络异常：返回连接错误

---

## 📝 使用示例

### 示例 1：查询待办并审批

```
用户：我有什么待办审批吗？
助手：调用 get_pending_tasks → 返回 3 个待办
助手：您有 3 个待办：
      1. 请假申请 - 张三 (task_12345)
      2. 报销审批 - 李四 (task_67890)
      3. 合同审批 - 王五 (task_abcde)

用户：同意第一个请假申请
助手：调用 execute_approval_task(task_id="task_12345", action="AGREE", remark="同意")
助手：✅ 已同意张三的请假申请
```

### 示例 2：拒绝审批并备注

```
用户：拒绝李四的报销，发票不齐全
助手：调用 execute_approval_task(task_id="task_67890", action="REFUSE", remark="发票不齐全，请补充后重新提交")
助手：❌ 已拒绝李四的报销审批，备注：发票不齐全，请补充后重新提交
```

### 示例 3：查询假期余额

```
用户：帮我查一下还有多少年假
助手：调用 get_vacation_balance
助手：年假: 5天 (总10天, 已用5天)
```

---

## ⚠️ 常见问题

### 1. 配置加载失败

**错误**：`[dingtalk-approval] 配置不完整！`

**解决**：检查 openclaw.json 配置路径是否正确，确保在 `plugins.entries.dingtalk-approval.config` 下

### 2. 获取 token 失败

**错误**：`invalid appkey or appsecret`

**解决**：检查 appKey 和 appSecret 是否正确，确认应用状态正常

### 3. 无权限访问

**错误**：`permission denied`

**解决**：在钉钉开放平台为应用添加 OA 审批相关 API 权限

### 4. task_id 无效

**错误**：`invalid task id`

**解决**：确保 task_id 是从 `get_pending_tasks` 返回的最新数据，任务可能已被处理

### 5. 假期权限不足

**错误**：`应用尚未开通假期查询权限（qyapi_holiday_readonly）`

**解决**：在钉钉开放平台为当前应用申请 `qyapi_holiday_readonly` 权限后重试

---

## 🔗 相关资源

- [钉钉开放平台](https://open.dingtalk.com/)
- [OA 审批 API 文档](https://open.dingtalk.com/document/orgapp-server/query-the-tasks-to-be-processed-by-the-user)
- [钉钉用户 ID 获取方式](https://open.dingtalk.com/document/orgapp-server/obtain-the-userid-of-a-member)

---

## Author

Yang

## License

MIT
