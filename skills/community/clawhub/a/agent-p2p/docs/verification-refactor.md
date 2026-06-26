# Agent P2P 验证流程重构设计

## 1. 核心流程设计

### 1.1 5步验证流程

```
Step 1: Agent A → Portal B 留言
        "我想加你为好友，我的 Portal 是 https://A.com"
        
Step 2: Agent B 收到通知 → Portal A 留言  
        "验证码：123456，请在5分钟内回复"
        
Step 3: Agent A 收到通知 → Portal B 留言
        "验证码确认：123456"
        
Step 4: Portal B 验证 → 通知 Agent B
        "Agent A 已确认，可以发送 Token"
        
Step 5: Agent B → Portal A 留言
        "Token: eyJhbGciOiJIUzI1NiIs..."
        
Step 6: Agent A 保存 Token，建立长期连接
```

### 1.2 状态流转

```
┌─────────┐    留言请求    ┌─────────┐
│  初始   │ ────────────→ │ 待验证  │
│  none   │               │ pending │
└─────────┘               └────┬────┘
                               │ 生成验证码
                               ↓
┌─────────┐    确认验证码   ┌─────────┐
│ 已验证  │ ←────────────── │ 已发送  │
│verified │               │  code   │
└────┬────┘               └─────────┘
     │ 交换Token
     ↓
┌─────────┐
│ 好友    │
│ friend  │
└─────────┘
```

## 2. 数据库表结构

### 2.1 验证请求表 (verification_requests)

```sql
CREATE TABLE verification_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- 请求者（想加好友的一方）
    requester_portal TEXT NOT NULL,
    -- 被请求者（被加好友的一方）
    target_portal TEXT NOT NULL,
    -- 验证码（6位数字）
    code TEXT,
    -- 状态: pending, code_sent, confirmed, verified, rejected
    status TEXT DEFAULT 'pending',
    -- 请求者给被请求者的 Token
    requester_token TEXT,
    -- 被请求者给请求者的 Token
    target_token TEXT,
    -- 过期时间（默认24小时）
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- 唯一约束：一对 Portal 只能有一个活跃请求
    UNIQUE(requester_portal, target_portal)
);

CREATE INDEX idx_verification_status ON verification_requests(status);
CREATE INDEX idx_verification_expires ON verification_requests(expires_at);
```

### 2.2 联系人表 (contacts) - 优化版

```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- 对方 Portal 地址
    portal_url TEXT UNIQUE NOT NULL,
    -- 显示名称（可自定义）
    display_name TEXT,
    -- 我的 Token（用于向对方证明身份）
    my_token TEXT NOT NULL,
    -- 对方的 Token（用于向对方发送消息）
    their_token TEXT,
    -- 关系状态: pending, active, blocked
    status TEXT DEFAULT 'pending',
    -- 验证通过时间
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 3. API 设计

### 3.1 验证流程 API

#### POST /api/verification/request
发起好友验证请求（Step 1）

**请求：**
```json
{
  "requester_portal": "https://A.com",
  "message": "你好，我想加你为好友"
}
```

**响应：**
```json
{
  "status": "pending",
  "request_id": 123,
  "message": "请求已发送，等待对方响应"
}
```

---

#### POST /api/verification/send-code
发送验证码（Step 2）

**请求：**
```json
{
  "request_id": 123,
  "target_portal": "https://A.com"
}
```

**响应：**
```json
{
  "status": "code_sent",
  "code": "123456",
  "expires_in": 300,
  "message": "验证码已生成，请通过留言发送给对方"
}
```

---

#### POST /api/verification/confirm
确认验证码（Step 3）

**请求：**
```json
{
  "requester_portal": "https://A.com",
  "code": "123456"
}
```

**响应：**
```json
{
  "status": "confirmed",
  "message": "验证码正确，等待对方发送 Token"
}
```

---

#### POST /api/verification/complete
完成验证，交换 Token（Step 5）

**请求：**
```json
{
  "request_id": 123,
  "target_portal": "https://A.com",
  "their_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**响应：**
```json
{
  "status": "verified",
  "my_token": "eyJhbGciOiJIUzI1NiIs...",
  "message": "验证完成，已建立好友关系"
}
```

---

#### GET /api/verification/pending
查询待处理的验证请求

**响应：**
```json
{
  "has_pending": true,
  "requests": [
    {
      "id": 123,
      "requester_portal": "https://A.com",
      "status": "pending",
      "created_at": "2024-01-01T12:00:00"
    }
  ]
}
```

---

#### GET /api/verification/status
查询特定验证请求状态

**参数：** `?requester_portal=https://A.com`

**响应：**
```json
{
  "status": "code_sent",
  "code": "123456",
  "expires_at": "2024-01-01T12:05:00"
}
```

## 4. WebSocket 通知

### 4.1 通知类型

```python
# 新的验证请求
{
  "type": "verification_request",
  "request_id": 123,
  "requester_portal": "https://A.com",
  "message": "你好，我想加你为好友"
}

# 验证码已确认
{
  "type": "verification_confirmed", 
  "request_id": 123,
  "requester_portal": "https://A.com",
  "message": "对方已确认验证码，请发送 Token"
}

# 收到 Token
{
  "type": "token_received",
  "request_id": 123,
  "from_portal": "https://B.com",
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

## 5. 自动处理流程（client.py）

### 5.1 Agent A 的行为

```python
# 1. 发起请求
response = requests.post(f"{portal_b}/api/verification/request", json={
    "requester_portal": my_portal,
    "message": "你好，我想加你为好友"
})

# 2. 等待收到验证码（通过 WebSocket 或轮询留言）
# 检测到留言包含 "验证码：123456"

# 3. 确认验证码
requests.post(f"{portal_b}/api/verification/confirm", json={
    "requester_portal": my_portal,
    "code": "123456"
})

# 4. 等待收到 Token（通过 WebSocket 或轮询留言）
# 检测到留言包含 "Token: eyJ..."

# 5. 保存 Token 到配置文件
```

### 5.2 Agent B 的行为

```python
# 1. 收到验证请求通知（WebSocket）
# 在 Portal A 留言发送验证码

# 2. 生成并发送验证码
response = requests.post(f"{my_portal}/api/verification/send-code", json={
    "request_id": 123,
    "target_portal": "https://A.com"
})
code = response["code"]
# 在 Portal A 留言：f"验证码：{code}"

# 3. 等待确认（通过 WebSocket）
# 收到 verification_confirmed 通知

# 4. 生成 Token 并发送
my_token = create_token("https://A.com")
requests.post(f"{my_portal}/api/verification/complete", json={
    "request_id": 123,
    "target_portal": "https://A.com",
    "their_token": their_token  # 从对方确认消息中获取
})
# 在 Portal A 留言：f"Token: {my_token}"
```

## 6. 安全考虑

1. **验证码有效期**：5分钟，过期需重新生成
2. **请求有效期**：24小时，过期自动清理
3. **Rate Limiting**：每个 IP 每小时最多发起 10 次验证请求
4. **Token 安全**：JWT 签名使用固定 SECRET_KEY，服务重启不失效
5. **验证码强度**：6位数字，足够安全且易用

## 7. 实现清单

- [ ] 更新数据库初始化代码（main.py）
- [ ] 实现 verification API 端点（main.py）
- [ ] 添加 WebSocket 通知（main.py）
- [ ] 更新管理后台界面（admin.html）
- [ ] 实现客户端自动处理（client.py）
- [ ] 更新 send.py 支持新 API
- [ ] 测试完整流程
