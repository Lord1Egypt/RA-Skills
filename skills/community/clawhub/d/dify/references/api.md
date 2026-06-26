# Dify API 完整参考

## 基础URL

- 云端: `https://api.dify.ai/v1`
- 自托管: `http://your-server/v1`

## 认证

所有请求需要Bearer Token认证:

```http
Authorization: Bearer {your_api_key}
```

API Key获取: 应用详情页 → Access Info → API Key

---

## Chat App API

### 发送聊天消息

```http
POST /chat-messages
```

**请求体:**
```json
{
  "query": "用户消息内容",
  "inputs": {},                    // 应用变量
  "response_mode": "streaming",    // streaming | blocking
  "user": "unique-user-id",        // 用户标识
  "conversation_id": "",           // 会话ID(首次空，后续传返回值)
  "files": [                       // 可选，文件附件
    {
      "type": "image",
      "transfer_method": "remote_url",
      "url": "https://example.com/image.jpg"
    }
  ],
  "auto_generate_name": true       // 自动生成会话标题
}
```

**响应 (blocking模式):**
```json
{
  "event": "message",
  "task_id": "uuid",
  "message_id": "uuid",
  "conversation_id": "uuid",
  "answer": "AI回复内容",
  "metadata": {
    "usage": {
      "total_tokens": 100,
      "latency": 0.5
    }
  }
}
```

### 停止响应

```http
POST /chat-messages/{task_id}/stop
```

### 获取会话历史

```http
GET /messages?conversation_id={id}&user={user_id}
```

### 会话列表

```http
GET /conversations?user={user_id}
```

### 重命名会话

```http
PATCH /conversations/{id}
{
  "name": "新名称",
  "auto_generate": false
}
```

### 删除会话

```http
DELETE /conversations/{id}
```

---

## Workflow API

### 执行工作流

```http
POST /workflows/run
```

**请求体:**
```json
{
  "inputs": {
    "variable_name": "value"
  },
  "response_mode": "blocking",
  "user": "user-123",
  "files": [                       // 可选，文件输入
    {
      "type": "document",
      "transfer_method": "local_file",
      "upload_file_id": "file-id"
    }
  ]
}
```

**响应:**
```json
{
  "workflow_run_id": "uuid",
  "task_id": "uuid",
  "data": {
    "id": "uuid",
    "status": "succeeded",         // running | succeeded | failed | stopped
    "outputs": {
      "result": "输出内容"
    },
    "total_tokens": 100,
    "total_steps": 5,
    "created_at": 1705407629,
    "finished_at": 1705407630
  }
}
```

---

## 文件上传

### 上传文件

```http
POST /files/upload
Content-Type: multipart/form-data

file: (binary)
user: user-123
```

**响应:**
```json
{
  "id": "file-uuid",
  "name": "document.pdf",
  "size": 10240,
  "type": "document"
}
```

---

## 反馈API

### 提交反馈

```http
POST /messages/{message_id}/feedbacks
{
  "rating": "like",        // like | dislike | null
  "user": "user-123"
}
```

### 获取反馈

```http
GET /messages/{message_id}/feedbacks?user={user_id}
```

---

## 文本转语音

### TTS

```http
POST /text-to-audio
{
  "text": "要转换的文本",
  "user": "user-123",
  "message_id": "optional-message-id"
}
```

---

## 错误响应

```json
{
  "status": 400,
  "code": "invalid_param",
  "message": "参数错误描述"
}
```

**常见错误码:**
- `invalid_param` - 参数错误
- `app_unavailable` - 应用不可用
- `provider_not_initialize` - 模型未配置
- `provider_quota_exceeded` - 配额超限
- `model_currently_not_support` - 模型不支持
- `completion_request_error` - 生成失败
