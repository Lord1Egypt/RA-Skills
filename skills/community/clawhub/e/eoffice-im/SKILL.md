---
name: eoffice-im
description: 泛微 e-office 即时通讯（IM）WebSocket API - 私聊、群聊等
version: 1.0.0
homepage: https://github.com/yourname/eoffice-im-skill
metadata:
  emoji: "💬"
  requires:
    env:
      - EOFFICE_IM_BASE_URL
      - EOFFICE_IM_TOKEN
  primaryEnv: EOFFICE_IM_TOKEN
---

# e-office 即时通讯（IM）Skill

当用户提到以下场景时使用此 skill：
- 发送即时消息给用户或群组
- 查询聊天记录
- 管理群组成员
- 获取用户在线状态
- 任何涉及即时通讯的操作

## 连接方式

### WebSocket 连接

```
WebSocket URL: ws://{EOFFICE_IM_BASE_URL}/
```

### 连接参数

连接时需要在 handshake 中传递：

| 参数 | 说明 |
|------|------|
| token | 访问令牌 |
| connectType | 连接类型：`web`、`mobile`、`client` |
| loginUserId | 登录用户 ID |

### 连接示例（JavaScript）

```javascript
import { io } from 'socket.io-client';

const socket = io('http://localhost:3000', {
  auth: {
    token: 'your-token-here'
  },
  query: {
    connectType: 'web',
    loginUserId: 'admin'
  }
});

socket.on('connect', () => {
  console.log('Connected to IM server');
});

socket.on('private message', (msg) => {
  console.log('Received message:', msg);
});
```

## 环境配置

| 变量 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `EOFFICE_IM_BASE_URL` | 是 | IM 服务地址 | `http://localhost:3000` |
| `EOFFICE_IM_TOKEN` | 是 | 访问令牌 | 从 OA 登录获取 |

## 发送消息

### 发送私聊消息

```javascript
socket.emit('send message', {
  type: 'user',
  message_id: Date.now(),
  message_content: '消息内容（AES加密）',
  text_message_content: '消息内容（原文）',
  message_type: 1,  // 1=text, 2=image, 3=file
  sender: 'user_id',
  chat_object_id: 'room_id',
  to: 'receiver_user_id',
  sender_name: '发送者姓名'
});
```

**响应**：服务器返回相同的消息对象（包含 `send_time`）

### 发送群聊消息

```javascript
socket.emit('send message', {
  type: 'personal_group',  // 或 'public_group'
  message_id: Date.now(),
  message_content: '消息内容（AES加密）',
  text_message_content: '消息内容（原文）',
  message_type: 1,
  sender: 'user_id',
  room_id: 'room_id',
  members: ['user1', 'user2'],
  group_name: '群名称',
  sender_name: '发送者姓名',
  at_list: [{user_id: 'xxx', user_name: 'xxx'}]  // @人员
});
```

**响应**：服务器推送到 `group message` 事件

## 消息类型

| type 值 | 说明 |
|---------|------|
| `user` | 私聊消息 |
| `personal_group` | 私人群聊 |
| `public_group` | 公共群 |

| message_type 值 | 说明 |
|-----------------|------|
| 1 | 文本消息 |
| 2 | 图片消息 |
| 3 | 文件消息 |

## 接收消息

### 监听私聊消息

```javascript
socket.on('private message', (msg) => {
  console.log('私聊消息:', msg);
});
```

### 监听群聊消息

```javascript
socket.on('group message', (msg) => {
  console.log('群聊消息:', msg);
});
```

## 消息操作

### 消息已读 - 私聊

```javascript
socket.emit('user readed', {
  chat_id: 'chat_object_id',
  toUserId: 'sender_user_id'
});
```

**接收已读通知**：

```javascript
socket.on('message have read', (data) => {
  // { type: 'user', chat_id: 'xxx', read_time: timestamp, user_id: 'xxx' }
});
```

### 消息已读 - 群聊

```javascript
socket.emit('group readed', {
  chat_id: 'room_id',
  toUserId: '群ID'
});
```

### 撤回消息

```javascript
socket.emit('withdraw msg', {
  chat_id: 'room_id',
  message_id: 'message_id',
  type: 'user',  // 或 'group'
  toUserId: 'user_id',
  at_list: []
});
```

### 删除消息

```javascript
socket.emit('delete msg', {
  chat_id: 'room_id',
  message_id: 'message_id'
});
```

## 群组管理

### 创建群组

```javascript
socket.emit('create group', {
  room_id: 'room_id',
  members: ['user1', 'user2']  // 不包含创建者
});
```

### 添加群成员

```javascript
socket.emit('user add group', {
  room_id: 'room_id',
  members: ['user3', 'user4']
});
```

**接收通知**：

```javascript
socket.on('user add group', (data) => {
  // { room_id: 'xxx', members: ['user3', 'user4'] }
});
```

### 删除群成员

```javascript
socket.emit('group delete user', {
  room_id: 'room_id',
  members: ['user_id']
});
```

### 解散群组

```javascript
socket.emit('delete group', {
  room_id: 'room_id',
  members: ['user1', 'user2']
});
```

## 在线状态

### 获取在线用户

```javascript
socket.emit('user onlineUsers', {}, (res) => {
  console.log(res);
  // {
  //   onlineUsers: ['user1', 'user2'],
  //   webUsers: [...],
  //   mobileUsers: [...],
  //   clientUsers: [...]
  // }
});
```

### 监听在线状态变化

```javascript
socket.on('online user change', (data) => {
  // {
  //   online: { webUsers: [...], mobileUsers: [...], clientUsers: [...] },
  //   offline: { webUsers: [...], mobileUsers: [...], clientUsers: [...] }
  // }
});
```

### 修改工作状态

```javascript
socket.emit('change work status', {
  userId: 'user_id',
  workStatus: 1  // 0=离线, 1=在线, 2=忙碌等
});
```

## 离线消息

### 获取离线消息

```javascript
socket.emit('get offline info');
```

**接收响应**：

```javascript
// 私聊离线消息
socket.on('user offline info', (messages, callback) => {
  console.log('离线私聊消息:', messages);
  callback('success');  // 确认已接收
});

// 群聊离线消息
socket.on('group offline info', (messages, callback) => {
  console.log('离线群聊消息:', messages);
  callback('success');
});
```

## 消息格式

### PersonalMessage 结构

```typescript
{
  message_id: string | number;    // 消息ID
  reply_message_id?: string;        // 回复消息ID
  message_content: string;          // 加密后的消息内容
  text_message_content: string;    // 原文消息内容
  message_type: number;           // 消息类型
  sender: string;                  // 发送者ID
  send_time: number;               // 发送时间
  chat_object_id: string;         // 私聊房间ID
  withdraw: number;               // 是否撤回
  delete_user_id?: string;        // 删除消息的用户ID
  type: string;                    // 'user'
  sendType?: string;               // 发送状态
  to: string;                      // 接收者ID
  sender_name?: string;            // 发送者姓名
  reply?: any;                     // 回复内容
}
```

### GroupMessage 结构

```typescript
{
  message_id: string | number;    // 消息ID
  reply_message_id?: string;      // 回复消息ID
  message_content: string;        // 加密后的消息内容
  text_message_content: string;   // 原文消息内容
  message_type: number;          // 消息类型
  sender: string;                 // 发送者ID
  send_time: number;             // 发送时间
  withdraw: number;              // 是否撤回
  type: string;                  // 'personal_group' | 'public_group'
  sendType?: string;
  room_id?: string;              // 群房间ID
  members?: string[];            // 群成员列表
  sender_name?: string;          // 发送者姓名
  group_name?: string;           // 群名称
  at_list?: Array<{              // @人员列表
    user_id: string;
    user_name: string;
  }>;
}
```

## 连接管理

### 同步聊天列表

```javascript
socket.emit('sync chat list');
```

### 页面通信（跨端同步）

```javascript
socket.emit('page communication', {
  key: 'value'  // 任意数据
});
```

## 错误处理

监听错误事件：

```javascript
socket.on('error', (error) => {
  console.error('Socket error:', error);
});

socket.on('connect_error', (error) => {
  console.error('Connection error:', error.message);
});
```

## 注意事项

1. **消息加密**：发送的消息内容需要使用 AES 加密（使用连接时提供的 crypto key）
2. **离线消息**：用户离线时，消息会存储在 Redis 中，用户上线后自动推送
3. **多端同步**：同一账号可以在 web、mobile、client 多端同时登录
4. **Token 有效期**：注意处理 token 过期的情况

## 完整 API 文档

详见 `references/im-api.md`
