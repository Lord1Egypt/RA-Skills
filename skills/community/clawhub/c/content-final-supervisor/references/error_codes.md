# 错误码定义 - content-final-supervisor

> 来源: skills/content-final-supervisor/SKILL.md 异常处理表

## 错误码列表

| 错误码 | 描述 | 处理方案 |
|:-------|:-----|:---------|
| SUPERVISION_SERVICE_DOWN | quality-supervisor-mcp 不可用 | 返回 SERVICE_UNAVAILABLE 错误,建议稍后重试 |
| EPISODE_NOT_FOUND | episode_id 不存在 | 返回 NOT_FOUND 错误 |
| CONTENT_EMPTY | 内容为空 | 返回 VALIDATION_ERROR |
| SUPERVISION_TIMEOUT | 终检超时 (>120秒) | 返回 TIMEOUT,建议分阶段终检 |
| REDO_LIMIT_EXCEEDED | 返工次数超限 (>3次) | 触发 final_arbitration 终审 |
| SUPERVISION_OK | 终检通过 | verdict=pass, can_publish=true |
| SUPERVISION_FAIL | 终检失败 | verdict=fail,需返工或终审 |
| SUPERVISION_REDO | 需返工 | verdict=redo,进入返工流程 |

## 错误处理说明

### SUPERVISION_SERVICE_DOWN

- 触发条件: quality-supervisor-mcp 服务未启动或不可达
- 处理: 返回 SERVICE_UNAVAILABLE,建议稍后重试
- 降级: 无降级,终检依赖 MCP 服务

### EPISODE_NOT_FOUND

- 触发条件: episode_id 在数据库中不存在
- 处理: 返回 NOT_FOUND 错误

### CONTENT_EMPTY

- 触发条件: 待检内容 (script_content/storyboard_content/video_url) 为空
- 处理: 返回 VALIDATION_ERROR

### SUPERVISION_TIMEOUT

- 触发条件: 终检执行超过 120 秒
- 处理: 返回 TIMEOUT,建议分阶段终检 (stage=script/storyboard/video 分开执行)

### REDO_LIMIT_EXCEEDED

- 触发条件: 同一阶段返工次数超过 3 次
- 处理: 自动触发 final_arbitration 终审,终审结果为最终结论,不可再返工

### 返工流程

1. verdict=fail 且可修复 → auto_redo → 返工后重新进入对应阶段终检
2. 返工次数 > 3 → final_arbitration 终审
3. verdict=fail 且需人工介入 → final_arbitration 终审
