# chat-bus 接口协议文档

## 通用参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `chat_dir` | 共享目录路径 | `.chat-bus/`（当前目录下） |
| `user` / `username` | 当前用户名 | 必填（发消息/接收时） |

---

## register.py — 用户管理

### 注册
```json
{"action": "register", "user": "alice", "display_name": "Alice", "bio": "开发者"}
```

### 更新信息
```json
{"action": "update", "user": "alice", "display_name": "新名字"}
```

### 查看用户
```json
{"action": "info", "username": "alice"}
```

### 列出所有用户
```json
{"action": "list"}
```

### 注销
```json
{"action": "unregister", "user": "alice"}
```

---

## send.py — 发送消息

### 单聊
```json
{"user": "alice", "type": "direct", "to": "bob", "content": "你好!"}
```

### 群聊
```json
{"user": "alice", "type": "room", "room": "general", "content": "大家好!"}
```

### 广播（给所有注册用户）
```json
{"user": "alice", "type": "broadcast", "content": "公告通知"}
```

---

## receive.py — 接收消息

### 接收私聊
```json
{"user": "bob", "source": "inbox", "limit": 20, "mark_read": true}
```

### 接收房间消息
```json
{"user": "bob", "source": "room", "room": "general", "since": "2026-04-13T22:00:00"}
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `source` | "inbox" 或 "room" | "inbox" |
| `since` | 只取此时间之后的消息 | 无（取全部） |
| `limit` | 最大消息数 | 50 |
| `mark_read` | 自动标记已读 | true |
| `unread_only` | 只取未读消息 | false |

---

## history.py — 消息历史

### 查询私聊历史
```json
{"source": "inbox", "user": "bob", "limit": 50, "offset": 0}
```

### 查询房间历史（带搜索）
```json
{"source": "room", "room": "general", "search": "关键词", "sender": "alice", "date": "2026-04-13"}
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `search` | 内容关键词搜索 | 无 |
| `sender` | 按发送者过滤 | 无 |
| `date` | 按日期过滤 (YYYY-MM-DD) | 无 |
| `limit` | 最大返回数 | 100 |
| `offset` | 跳过前 N 条 | 0 |

---

## rooms.py — 房间管理

### 创建房间
```json
{"action": "create", "user": "alice", "room": "general", "topic": "公共讨论"}
```

### 加入房间
```json
{"action": "join", "user": "bob", "room": "general"}
```

### 离开房间
```json
{"action": "leave", "user": "bob", "room": "general"}
```

### 查看房间信息
```json
{"action": "info", "room": "general"}
```

### 列出所有房间
```json
{"action": "list"}
```

### 删除房间（仅创建者）
```json
{"action": "delete", "user": "alice", "room": "general"}
```

---

## 消息文件格式

每条消息是一个 JSON 文件：

```json
{
  "id": "abc123def456",
  "sender": "alice",
  "sender_display": "Alice",
  "recipient": "bob",
  "content": "你好!",
  "timestamp": "2026-04-13T22:05:00",
  "type": "direct"
}
```

文件名格式：`2026-04-13_220500_alice_abc123def456.json`
- 已读消息重命名为 `.json.read`
