# e-office 即时通讯（IM）完整 API 文档

## 概述

e-office IM 是一个基于 **NestJS + Socket.IO** 的 WebSocket 即时通讯服务，支持私聊、群聊、消息已读未读等功能。

## 技术架构

| 组件 | 技术 |
|------|------|
| WebSocket | Socket.IO |
| 后端框架 | NestJS |
| 消息缓存 | Redis |
| 消息加密 | AES (crypto-js) |

## 连接信息

| 项目 | 值 |
|------|-----|
| 默认端口 | 3000 |
| WebSocket 路径 | `/` |
| CORS | 支持跨域 |

## 认证流程

### 1. 获取 Token

IM 服务使用 OA 系统的 token，连接时通过 `handshake.auth.token` 传递。

### 2. 连接参数

```javascript
const socket = io('http://localhost:3000', {
  auth: {
    token: 'OA_TOKEN'
  },
  query: {
    connectType: 'web',       // web | mobile | client
    loginUserId: 'user_id'   // 当前登录用户ID
  }
});
```

## Socket.IO 事件列表

### 客户端 → 服务器事件

| 事件名 | 说明 | 典型用途 |
|--------|------|----------|
| `hello` | 测试连接 | 心跳测试 |
| `login` | 用户登录 | - |
| `get offline info` | 获取离线消息 | 用户上线时拉取 |
| `user onlineUsers` | 获取在线用户列表 | 查看哪些人在线 |
| `create group` | 创建群组 | 新建群聊 |
| `group delete user` | 删除群成员 | 移除群成员 |
| `delete group` | 解散群组 | 删除群聊 |
| `user add group` | 添加群成员 | 邀请加入群聊 |
| `user readed` | 私聊已读 | 标记私聊消息已读 |
| `group readed` | 群聊已读 | 标记群聊消息已读 |
| `withdraw msg` | 撤回消息 | 撤回发送的消息 |
| `delete msg` | 删除消息 | 删除消息 |
| `sync chat list` | 同步聊天列表 | 多端消息同步 |
| `system message read sync` | 系统消息已读同步 | 多端已读同步 |
| `set message muted sync` | 免打扰同步 | 多端免打扰同步 |
| `change work status` | 修改工作状态 | 修改在线状态 |
| `page communication` | 页面通信 | 跨页面通信 |
| `send message` | 发送消息 | 发送私聊/群聊消息 |
| `quick build push` | 快速表单推送 | 表单推送提醒 |
| `handle edit form push` | 表单编辑推送 | 审批表单推送 |
| `handle autouser push` | 办理人设置推送 | 流程推送 |
| `remove-export-center-item` | 导出项删除同步 | 导出中心同步 |

### 服务器 → 客户端事件

| 事件名 | 说明 | 触发时机 |
|--------|------|----------|
| `refresh page` | 刷新页面 | 账号被踢下线 |
| `online user change` | 在线用户变化 | 用户上线下线 |
| `export channel` | 导出通道 | 导出进度 |
| `queue monitor` | 队列监控 | 后台任务进度 |
| `import channel` | 导入通道 | 导入完成 |
| `system message read sync` | 系统消息已读 | 已读同步 |
| `eoffice.system-message-channel` | 系统消息 | 收到系统消息 |
| `user offline info` | 私聊离线消息 | 用户上线时推送 |
| `group offline info` | 群聊离线消息 | 用户上线时推送 |
| `private message` | 私聊消息 | 收到私聊 |
| `group message` | 群聊消息 | 收到群聊 |
| `message have read` | 消息已读 | 对方已读消息 |
| `withdraw msg` | 撤回消息 | 消息被撤回 |
| `delete msg` | 删除消息 | 消息被删除 |
| `sync chat list` | 同步聊天列表 | 列表更新 |
| `set message muted sync` | 免打扰同步 | 设置变更 |
| `change work status` | 工作状态变化 | 他人状态变更 |
| `page communication` | 页面通信 | 跨端通信 |
| `quick build pull` | 快速表单拉取 | 表单推送响应 |
| `handle edit form pull` | 表单编辑拉取 | 表单响应 |
| `handle autouser pull` | 办理人拉取 | 流程响应 |
| `remove export item` | 删除导出项 | 导出项删除 |

## 详细 API 规范

### 连接与认证

#### 建立连接

```javascript
import { io } from 'socket.io-client';

const socket = io('http://localhost:3000', {
  auth: {
    token: 'YOUR_OA_TOKEN'
  },
  query: {
    connectType: 'web',
    loginUserId: 'admin'
  },
  transports: ['websocket']
});

socket.on('connect', () => {
  console.log('IM 服务已连接');
});

socket.on('disconnect', (reason) => {
  console.log('连接断开:', reason);
});
```

#### 连接参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| token | string | OA 系统获取的访问令牌 |
| connectType | string | 连接类型：`web`、`mobile`、`client` |
| loginUserId | string | 当前登录用户的 ID |

### 消息发送

#### 发送私聊消息

```javascript
socket.emit('send message', {
  type: 'user',
  message_id: Date.now().toString(),
  message_content: encrypt('你好，这是加密内容'),  // AES 加密
  text_message_content: '你好，这是原文',
  message_type: 1,  // 1=text, 2=image, 3=file
  sender: 'current_user_id',
  chat_object_id: 'room_id',  // 两个 user_id 组成的固定 ID
  to: 'receiver_user_id',
  sender_name: '发送者姓名'
});
```

**响应处理**：

```javascript
socket.on('private message', (msg) => {
  // 消息推送格式同发送
  console.log('收到私聊:', msg);
});
```

#### 发送群聊消息

```javascript
socket.emit('send message', {
  type: 'personal_group',  // 或 'public_group'
  message_id: Date.now().toString(),
  message_content: encrypt('群消息内容'),
  text_message_content: '群消息内容',
  message_type: 1,
  sender: 'current_user_id',
  room_id: 'room_id',
  members: ['user1', 'user2', 'user3'],
  group_name: '群名称',
  sender_name: '发送者姓名',
  at_list: [
    { user_id: 'mentioned_user_id', user_name: '被@用户名' }
  ]
});
```

**响应处理**：

```javascript
socket.on('group message', (msg) => {
  console.log('收到群聊:', msg);
});
```

### 消息已读

#### 私聊已读

```javascript
socket.emit('user readed', {
  chat_id: 'chat_object_id',
  toUserId: '对方用户ID'
});
```

**对方收到通知**：

```javascript
socket.on('message have read', (data) => {
  // data = { type: 'user', chat_id: 'xxx', read_time: 1234567890, user_id: 'xxx' }
});
```

#### 群聊已读

```javascript
socket.emit('group readed', {
  chat_id: 'room_id',
  toUserId: 'room_id'
});
```

**群成员收到通知**：

```javascript
socket.on('message have read', (data) => {
  // data = { type: 'group', chat_id: 'xxx', read_time: 1234567890, user_id: 'xxx' }
});
```

### 消息撤回与删除

#### 撤回消息

```javascript
socket.emit('withdraw msg', {
  chat_id: 'room_id',
  message_id: 'message_id',
  type: 'user',  // 'user' 或 'group'
  toUserId: 'receiver_id',
  at_list: []
});
```

**接收撤回通知**：

```javascript
socket.on('withdraw msg', (data) => {
  // { chat_id, message_id, type, toUserId, at_list }
});
```

#### 删除消息

```javascript
socket.emit('delete msg', {
  chat_id: 'room_id',
  message_id: 'message_id'
});
```

### 群组管理

#### 创建群组

```javascript
socket.emit('create group', {
  room_id: 'unique_room_id',
  members: ['user1', 'user2', 'user3']  // 不包含创建者
});
```

#### 添加群成员

```javascript
socket.emit('user add group', {
  room_id: 'room_id',
  members: ['user4', 'user5']
});
```

**接收通知**：

```javascript
socket.on('user add group', (data) => {
  // data = { room_id: 'xxx', members: ['user4', 'user5'] }
});
```

#### 删除群成员

```javascript
socket.emit('group delete user', {
  room_id: 'room_id',
  members: ['user_to_remove']
});
```

**接收通知**：

```javascript
socket.on('group delete user', (data) => {
  // data = { room_id: 'xxx', members: ['user_to_remove'] }
});
```

#### 解散群组

```javascript
socket.emit('delete group', {
  room_id: 'room_id',
  members: ['all_member_ids']
});
```

**接收通知**：

```javascript
socket.on('delete group', (data) => {
  // data = { room_id: 'xxx' }
});
```

### 在线状态

#### 获取在线用户

```javascript
socket.emit('user onlineUsers', {}, (response) => {
  console.log(response);
  // {
  //   onlineUsers: ['user1', 'user2'],
  //   webUsers: ['user1'],
  //   mobileUsers: [],
  //   clientUsers: ['user2']
  // }
});
```

#### 监听在线状态变化

```javascript
socket.on('online user change', (data) => {
  console.log('上线:', data.online);
  console.log('离线:', data.offline);
  // {
  //   online: { webUsers: [...], mobileUsers: [...], clientUsers: [...] },
  //   offline: { webUsers: [...], mobileUsers: [...], clientUsers: [...] }
  // }
});
```

#### 修改工作状态

```javascript
socket.emit('change work status', {
  userId: 'current_user_id',
  workStatus: 1  // 0=离线, 1=在线, 2=忙碌等
});
```

**接收通知**：

```javascript
socket.on('change work status', (data) => {
  // { userId: 'xxx', workStatus: 1 }
});
```

### 离线消息

#### 获取离线消息

```javascript
socket.emit('get offline info');
```

**接收离线私聊**：

```javascript
socket.on('user offline info', (messages, callback) => {
  console.log('离线私聊消息:', messages);
  callback('success');  // 确认收到
});
```

**接收离线群聊**：

```javascript
socket.on('group offline info', (messages, callback) => {
  console.log('离线群聊消息:', messages);
  callback('success');
});
```

### 多端同步

#### 同步聊天列表

```javascript
socket.emit('sync chat list');
```

**接收同步**：

```javascript
socket.on('sync chat list', () => {
  // 刷新聊天列表 UI
});
```

#### 页面通信

```javascript
// 发送端
socket.emit('page communication', { key: 'value', data: {} });

// 接收端
socket.on('page communication', (data) => {
  console.log('收到页面通信:', data);
});
```

## 消息加密

### AES 加密示例（JavaScript）

```javascript
import CryptoJS from 'crypto-js';

function encrypt(message, key, iv) {
  const encrypted = CryptoJS.AES.encrypt(message, CryptoJS.enc.Latin1.parse(key), {
    iv: CryptoJS.enc.Latin1.parse(iv),
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
  });
  return encrypted.toString();
}

function decrypt(ciphertext, key, iv) {
  const decrypted = CryptoJS.AES.decrypt(ciphertext, CryptoJS.enc.Latin1.parse(key), {
    iv: CryptoJS.enc.Latin1.parse(iv),
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
  });
  return decrypted.toString(CryptoJS.enc.Utf8);
}
```

## Redis 数据结构

IM 服务使用 Redis 存储以下数据：

| Key 模式 | 类型 | 说明 |
|----------|------|------|
| `EOFFICE:IM:clients` | Hash | 用户连接信息 |
| `EOFFICE:IM:user:{userId}:{type}` | Set | 用户设备 socket 集合 |
| `EOFFICE:IM:socket:{socketId}` | String | socket 与用户映射 |
| `EOFFICE:IM:PERSONAL_MESSAGE:{chatId}` | List | 私聊消息历史 |
| `EOFFICE:IM:GROUP_MESSAGE:{roomId}` | List | 群聊消息历史 |
| `EOFFICE:IM:PERSONAL_OFFLINE_INFO_{userId}` | Set | 用户离线私聊房间 |
| `EOFFICE:IM:GROUP_OFFLINE_INFO_{userId}` | Set | 用户离线群聊房间 |
| `EOFFICE:IM:USER_ROOMS:{userId}` | Set | 用户加入的群 |

## 完整示例

### 完整私聊流程

```javascript
import { io } from 'socket.io-client';
import CryptoJS from 'crypto-js';

// 连接
const socket = io('http://localhost:3000', {
  auth: { token: 'OA_TOKEN' },
  query: { connectType: 'web', loginUserId: 'current_user' }
});

// 连接成功
socket.on('connect', () => {
  console.log('已连接 IM');

  // 获取离线消息
  socket.emit('get offline info');
});

// 接收私聊
socket.on('private message', (msg) => {
  console.log('收到私聊:', msg.text_message_content);

  // 标记已读
  socket.emit('user readed', {
    chat_id: msg.chat_object_id,
    toUserId: msg.sender
  });
});

// 接收已读通知
socket.on('message have read', (data) => {
  console.log('对方已读');
});

// 发送私聊
function sendPrivateMessage(to, content) {
  socket.emit('send message', {
    type: 'user',
    message_id: Date.now().toString(),
    message_content: encrypt(content, key, iv),
    text_message_content: content,
    message_type: 1,
    sender: 'current_user',
    chat_object_id: generateChatId('current_user', to),
    to: to,
    sender_name: '当前用户'
  });
}

// 生成聊天房间 ID
function generateChatId(user1, user2) {
  return [user1, user2].sort().join('_');
}
```

## 注意事项

1. **Token 有效期**：注意处理 token 过期，断线重连
2. **消息加密**：生产环境务必加密消息内容
3. **离线消息**：用户上线后自动推送离线消息
4. **多端登录**：同一账号支持多端同时在线
5. **心跳检测**：建议定期发送 `hello` 事件保持连接
