# 错误码定义 - content-calibrator

> 来源: skills/content-calibrator/SKILL.md 异常处理表

## 错误码列表

| 错误码 | 描述 | 处理方案 |
|:-------|:-----|:---------|
| ENV_MISSING | SENSENOVA_API_KEY 未配置 | 返回 error 提示,提示用户配置环境变量 |
| LLM_TIMEOUT | LLM 调用超时 (>30s) | 返回 error + 降级建议 |
| LLM_PARSE_FAILED | LLM 返回非 JSON | 尝试解析失败后返回 error |
| EMPTY_CONTENT | 空内容输入 | 返回 error |
| INVALID_PLATFORM | 无效平台名 | 返回 error |
| (降级,非错误) | rubric 文件不存在 | 使用默认 rubric + v1 |

## 错误处理说明

### ENV_MISSING

- 触发条件: `.env` 中 `SENSENOVA_API_KEY` 未设置
- 处理: 返回 `{"success": false, "error": "SENSENOVA_API_KEY未配置", "code": "ENV_MISSING"}`
- 降级: 无降级,LLM 评分依赖此 API Key

### LLM_TIMEOUT

- 触发条件: LLM 调用超过 30 秒未返回
- 处理: 返回 error,建议稍后重试或检查网络
- 降级: 无自动降级

### LLM_PARSE_FAILED

- 触发条件: LLM 返回内容无法解析为 JSON
- 处理: 尝试提取 JSON 片段,失败后返回 error

### EMPTY_CONTENT

- 触发条件: content 参数为空
- 处理: 返回 `{"success": false, "error": "内容不能为空", "code": "EMPTY_CONTENT"}`

### INVALID_PLATFORM

- 触发条件: platform 参数不在支持列表中
- 处理: 返回 error,提示有效平台列表

### Rubric 降级 (非错误)

- 触发条件: `data/content-calibrator/rubrics/{platform}.json` 不存在
- 处理: 使用默认 rubric (v1) 继续评分,不返回错误
