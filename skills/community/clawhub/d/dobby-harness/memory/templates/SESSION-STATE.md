# Session State Template - 会话状态模板

> 用于保存和恢复会话状态的标准化模板

---

## 📋 基本信息

```json
{
  "sessionId": "{{SESSION_ID}}",
  "startTime": "{{START_TIME}}",
  "lastActivity": "{{LAST_ACTIVITY}}",
  "status": "active|paused|completed|failed",
  "model": "{{MODEL}}",
  "channel": "{{CHANNEL}}"
}
```

---

## 🎯 当前任务

```json
{
  "taskId": "{{TASK_ID}}",
  "description": "{{TASK_DESCRIPTION}}",
  "status": "pending|running|completed|failed",
  "progress": 0-100,
  "startedAt": "{{STARTED_AT}}",
  "completedAt": "{{COMPLETED_AT}}",
  "error": null
}
```

---

## 🧠 上下文快照

### 关键信息
- **用户**: {{USER_NAME}}
- **项目**: {{PROJECT_NAME}}
- **工作区**: {{WORKSPACE_PATH}}
- **当前目录**: {{CWD}}

### 相关文件
```
- file1.js (modified)
- file2.md (created)
- ...
```

### 环境变量
```
NODE_ENV=development
PORT=3000
...
```

---

## 📝 执行历史

| 时间 | 操作 | 结果 | 耗时 |
|------|------|------|------|
| {{TIME}} | {{ACTION}} | {{RESULT}} | {{DURATION}} |
| ... | ... | ... | ... |

---

## 🔧 工具使用统计

| 工具 | 调用次数 | 成功 | 失败 | 平均耗时 |
|------|---------|------|------|---------|
| read | 0 | 0 | 0 | 0ms |
| write | 0 | 0 | 0 | 0ms |
| exec | 0 | 0 | 0 | 0ms |
| ... | ... | ... | ... | ... |

---

## 💭 思考过程

### 关键决策
1. **决策点**: {{DECISION}}
   - **选项**: [选项 A, 选项 B]
   - **选择**: [已选选项]
   - **理由**: [选择理由]

### 遇到的问题
- **问题**: {{PROBLEM}}
  - **解决方案**: {{SOLUTION}}
  - **结果**: {{OUTCOME}}

---

## 📦 中间结果

```json
{
  "artifact1": {
    "type": "file",
    "path": "./path/to/file",
    "status": "created",
    "checksum": "abc123"
  },
  "artifact2": {
    "type": "data",
    "value": {...},
    "status": "computed"
  }
}
```

---

## 🔄 待恢复状态

### 未完成的任务
- [ ] {{PENDING_TASK_1}}
- [ ] {{PENDING_TASK_2}}
- [ ] ...

### 需要重试的操作
- [ ] {{RETRY_ACTION_1}} (失败原因：{{REASON}})
- [ ] ...

### 等待的外部事件
- [ ] {{WAITING_FOR}} (超时：{{TIMEOUT}})

---

## 📊 性能指标

```json
{
  "totalTokens": 0,
  "totalCost": 0.00,
  "avgResponseTime": 0,
  "cacheHitRate": 0,
  "errorRate": 0
}
```

---

## 🔖 标签和分类

- **项目**: {{PROJECT_TAG}}
- **类型**: {{TYPE_TAG}}
- **优先级**: {{PRIORITY_TAG}}
- **状态**: {{STATUS_TAG}}

---

## 📌 备注

> 任何需要特别说明的信息

---

*模板版本：1.0 | 最后更新：2026-04-18*
