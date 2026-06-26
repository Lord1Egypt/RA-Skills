---
name: cym-zentao
description: 禅道项目管理 CLI 工具 - 支持任务创建、执行查询等功能
metadata:
  {"openclaw": {"emoji": "📋", "requires": {"bins": ["node"]}, "always": true}}
---

# cym-zentao - 禅道项目管理 CLI

## 命令

### login
测试登录：
```bash
cym-zentao login
```

### list-executions
列出执行（项目迭代）：
```bash
cym-zentao list-executions [keyword]
```

### create-task
创建任务：
```bash
cym-zentao create-task <executionId|executionName> <name> <assignedTo> [options]
```

**参数说明：**
- `executionId|executionName`: 执行ID（数字）或执行名称（支持模糊匹配）
- `name`: 任务名称
- `assignedTo`: 指派给（用户名）
- `options`: JSON 字符串，可选参数

**options 格式：** JSON 字符串
- `pri`: 优先级 (1-4)
- `estimate`: 预计工时
- `type`: 任务类型
- `estStarted`: 开始日期 (YYYY-MM-DD)
- `deadline`: 截止日期 (YYYY-MM-DD)
- `desc`: 描述

**示例：**
```bash
# 使用执行ID
cym-zentao create-task 6159 "测试功能" "陈跃美"

# 使用执行名称（支持模糊匹配）
cym-zentao create-task "日常事务-郑太相" "测试功能" "陈跃美"

# 带选项
cym-zentao create-task 6159 "测试功能" "陈跃美" '{"pri":2,"estimate":8,"type":"test"}'
```

### create-tasks-batch
批量创建任务（从 JSON 文件）：
```bash
cym-zentao create-tasks-batch <executionId|executionName> <tasksFile>
```

**tasksFile 格式：** JSON 数组，每个元素包含：
- `name`: 任务名称（必填）
- `assignedTo`: 指派给（必填）
- `estimate`: 预计工时
- `estStarted`: 开始日期 (YYYY-MM-DD)
- `deadline`: 截止日期 (YYYY-MM-DD)
- `type`: 任务类型，默认 "test"
- `pri`: 优先级，默认 3
- `desc`: 描述

**示例文件 tasks.json：**
```json
[
  {"name": "调研功能", "assignedTo": "1010753", "estimate": 6, "estStarted": "2026-03-25", "deadline": "2026-03-25"},
  {"name": "编写代码", "assignedTo": "1010753", "estimate": 6, "estStarted": "2026-03-26", "deadline": "2026-03-26"},
  {"name": "测试功能", "assignedTo": "1010753", "estimate": 6, "estStarted": "2026-03-27", "deadline": "2026-03-27"},
  {"name": "验收功能", "assignedTo": "004936", "estimate": 1, "estStarted": "2026-03-27", "deadline": "2026-03-27"}
]
```

**使用示例：**
```bash
cym-zentao create-tasks-batch "日常事务-郑太相" tasks.json
```

### list-tasks
列出任务：
```bash
cym-zentao list-tasks <executionId|executionName> [status]
```

**示例：**
```bash
# 使用执行ID
cym-zentao list-tasks 6159

# 使用执行名称
cym-zentao list-tasks "日常事务-郑太相"

# 按状态筛选
cym-zentao list-tasks 6159 "doing"
```

## 自然语言创建任务

你也可以用自然语言描述来创建任务，AI 会自动解析：

### 单任务创建
```
给陈跃美在日常事务-郑太相下面创建明天的任务，任务名称为"测试功能"，任务预计耗时6小时
```

AI 会解析出：
- 执行名称：日常事务-郑太相
- 任务名称：测试功能
- 指派给：陈跃美
- 开始日期：明天
- 预计工时：6小时

### 批量任务创建
```
在禅道"日常事务-郑太相"下面创建任务：
时间2026-3-25，任务调研skills实现，预计耗时6小时，指派给陈跃美
时间2026-3-26，任务编写skills代码，预计耗时6小时，指派给陈跃美
时间2026-3-27，任务测试skills功能，预计耗时6小时，指派给陈跃美
时间2026-3-27，任务验收skills功能，预计耗时1小时，指派给郑太相
```

AI 会：
1. 首先查找执行"日常事务-郑太相"的ID
2. 批量创建4个任务，分别设置正确的日期、工时和指派给
3. 返回创建结果汇总
