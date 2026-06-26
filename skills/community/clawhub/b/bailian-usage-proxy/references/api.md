# API 文档

## 代理端点

所有端点兼容 OpenAI API 格式。

### Chat Completions

```
POST /v1/chat/completions
```

**请求头：**
```http
Authorization: Bearer {internal_api_key}
Content-Type: application/json
```

**请求体：**
```json
{
  "model": "qwen-turbo",
  "messages": [
    {"role": "user", "content": "你好"}
  ],
  "stream": false
}
```

**响应：**
```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1700000000,
  "model": "qwen-turbo",
  "choices": [...],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

### Embeddings

```
POST /v1/embeddings
```

**请求体：**
```json
{
  "model": "text-embedding-v2",
  "input": "要嵌入的文本"
}
```

## 管理端点

### 用户管理

#### 创建用户
```
POST /admin/users
```

**请求体：**
```json
{
  "user_name": "张三",
  "department": "算法部",
  "daily_limit": 1000000
}
```

**响应：**
```json
{
  "user_key": "bk-xxxx",
  "user_name": "张三",
  "daily_limit": 1000000
}
```

#### 获取用户列表
```
GET /admin/users
```

#### 更新用户
```
PUT /admin/users/{user_key}
```

#### 删除用户
```
DELETE /admin/users/{user_key}
```

### 用量查询

#### 查询用量
```
GET /admin/usage?user_key=xxx&start=2026-03-01&end=2026-03-08&group_by=day
```

**参数：**
- `user_key`: 用户标识（可选）
- `start`: 开始日期
- `end`: 结束日期
- `group_by`: 聚合维度（hour/day/month）

**响应：**
```json
{
  "data": [
    {
      "date": "2026-03-08",
      "user_key": "bk-xxx",
      "model": "qwen-turbo",
      "request_count": 100,
      "total_tokens": 50000
    }
  ]
}
```

#### 实时用量
```
GET /admin/usage/realtime
```

返回今日所有用户的实时用量。

#### 用量排行
```
GET /admin/usage/top?limit=10&period=7d
```

**参数：**
- `limit`: 返回条数
- `period`: 时间范围（1d/7d/30d）

## 错误码

| 状态码 | 说明 |
|--------|------|
| 401 | API Key 无效或已禁用 |
| 429 | 超出日限额或限流 |
| 500 | 服务器内部错误 |
| 502 | 阿里百炼服务不可用 |
