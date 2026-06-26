# 工具推荐与执行 API 规范

## 1. 推荐工具接口

### 端点
```
POST /agent-api/v1/tool/recommend
```

### 鉴权
**必须**在请求头中包含 API Key 信息：
- `X-Api-Key: <AGENT_EARTH_API_KEY>`

### 请求参数
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | ✅ | 用户输入的自然语言，用于匹配工具 | 
| task_context | string | ❌ | 可选，任务上下文信息 | 

### 响应格式
```json
{
  "tools": [
    {
      "tool_name": "weather_forecast_tool",
      "description": "提供实时天气查询和预报功能",
      "input_schema": {
        "city": {"type": "string", "required": true},
        "date": {"type": "string", "required": false}
      },
      "estimated_points": 1.0
    }
  ]
}
```

---

## 2. 执行工具接口

### 端点
```
POST /agent-api/v1/tool/execute
```

### 鉴权
**必须**在请求头中包含 API Key 信息：
- `X-Api-Key: <AGENT_EARTH_API_KEY>`

### 请求参数
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| tool_name | string | ✅ | 工具名称，需与 recommend 返回的 tool_name 一致 |
| arguments | object | ❌ | 工具参数，默认 {} |
| session_id | string | ❌ | 可选，会话 ID |

### 响应格式

#### 成功响应
```json
{
  "result": { /* 工具执行的具体结果 */ },
  "status": "success"
}
```

#### 失败响应
```json
{
  "status": "error",
  "message": "参数 city 不能为空"
}
```

### 错误码说明
| 错误码 | 说明 | 建议处理方式 |
|--------|------|--------------|
| 401 | 未授权 | 检查 AGENT_EARTH_API_KEY 是否正确配置 |
| 400 | 参数错误 | 检查 arguments 是否符合 input_schema |
| 404 | 工具不存在 | 跳过此工具，尝试下一个候选 |
| 500 | 服务器内部错误 | 降级重试或返回友好提示 |
| 429 | 请求过于频繁 | 短暂延迟后重试 |

---

## 3. 使用注意事项

1. **推荐调用前**：确保 query 足够具体以提高匹配精度
2. **执行前校验**：先检查 arguments 是否满足 input_schema 的 required 字段
3. **超时处理**：单个工具执行建议设置 30 秒超时
4. **重试策略**：对于 5xx 错误可立即重试，4xx 错误不要盲目重试
