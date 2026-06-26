# DataHub API 详细规范

## 认证方式

所有API请求需要提供API Key，支持两种传递方式：

1. **请求体**（POST请求）: `{ "key": "your-api-key" }`
2. **请求头**: `X-API-Key: your-api-key`
3. **查询参数**（GET请求）: `?key=your-api-key`

## 接口1：提交查询

### 请求
- **方法**: POST
- **URL**: `https://datahub.codes/api/datahub/execute/v0`
- **Content-Type**: `application/json`
- **认证**: 通过请求体或Header传递API Key

### 请求体
```json
{
  "query": "自然语言查询内容",
  "sessionId": "可选，会话标识符",
  "key": "your-api-key-here"
}
