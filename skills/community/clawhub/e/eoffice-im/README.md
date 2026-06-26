# eoffice-im

泛微 e-office 即时通讯（IM）WebSocket 服务 Skill。

让 AI Agent 能够通过自然语言发送即时消息、管理群组、查询用户在线状态等。

## 功能特性

- **私聊消息** - 发送和接收点对点消息
- **群聊消息** - 创建群组、管理群成员、群组消息
- **消息管理** - 消息已读、撤回、删除
- **在线状态** - 查询用户在线状态、监听上下线变化
- **离线消息** - 用户上线后自动拉取离线消息

## 安装

### 前置要求

- OpenClaw / Clawdbot 已安装
- e-office IM 服务已部署并运行

### 安装步骤

1. **通过 ClawHub 安装**（推荐）

```bash
openclaw skill install eoffice-im
```

2. **手动安装**

```bash
# 克隆或下载此仓库
git clone https://github.com/yourname/eoffice-im-skill.git

# 进入目录
cd eoffice-im-skill

# 链接到 OpenClaw
openclaw skill link ./eoffice-im-skill
```

## 配置

### 1. 配置环境变量

在 OpenClaw 的 `openclaw.json` 或 `.env` 中配置：

```json
{
  "skills": {
    "entries": {
      "eoffice-im": {
        "env": {
          "EOFFICE_IM_BASE_URL": "http://localhost:3000",
          "EOFFICE_IM_TOKEN": "your-oa-token-here"
        }
      }
    }
  }
}
```

### 2. 环境变量说明

| 变量 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `EOFFICE_IM_BASE_URL` | 是 | IM 服务地址 | `http://localhost:3000` |
| `EOFFICE_IM_TOKEN` | 是 | OA 系统访问令牌 | 从 OA 登录获取 |

> **Token 获取**：IM 服务使用 OA 系统的 token，连接时通过 `handshake.auth.token` 传递。

## 使用示例

### 发送私聊消息

```
用户: 给张三发送一条消息，内容是"明天开会"

Agent: 我来帮你发送消息...

socket.emit('send message', {
  type: 'user',
  message_content: encrypt('明天开会', key, iv),
  text_message_content: '明天开会',
  message_type: 1,
  sender: 'current_user_id',
  chat_object_id: 'user1_user2',  // 两个 user_id 排序后用下划线连接
  to: 'zhangsan_user_id',
  sender_name: '发送者姓名'
});

消息发送成功！
```

### 创建群组

```
用户: 创建一个群组，成员有张三、李四、王五

Agent: 好的，我来创建群组...

socket.emit('create group', {
  room_id: 'unique_room_id',
  members: ['zhangsan_id', 'lisi_id', 'wangwu_id']
});

群组创建成功！
```

### 查询在线用户

```
用户: 哪些人在线？

Agent: 我来查询在线用户...

socket.emit('user onlineUsers', {}, (response) => {
  console.log(response.onlineUsers);
});

当前在线用户：张三、李四
```

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

## Socket.IO 事件

### 客户端 → 服务器

| 事件名 | 说明 |
|--------|------|
| `hello` | 心跳测试 |
| `login` | 用户登录 |
| `get offline info` | 获取离线消息 |
| `user onlineUsers` | 获取在线用户列表 |
| `create group` | 创建群组 |
| `user add group` | 添加群成员 |
| `group delete user` | 删除群成员 |
| `delete group` | 解散群组 |
| `send message` | 发送消息 |
| `user readed` | 私聊已读 |
| `group readed` | 群聊已读 |
| `withdraw msg` | 撤回消息 |
| `delete msg` | 删除消息 |
| `change work status` | 修改工作状态 |

### 服务器 → 客户端

| 事件名 | 说明 |
|--------|------|
| `private message` | 私聊消息 |
| `group message` | 群聊消息 |
| `message have read` | 消息已读通知 |
| `withdraw msg` | 撤回通知 |
| `delete msg` | 删除通知 |
| `online user change` | 在线状态变化 |
| `user offline info` | 离线私聊消息 |
| `group offline info` | 离线群聊消息 |
| `sync chat list` | 聊天列表同步 |

## 完整 API 文档

详见 `references/im-api.md`

## 文件结构

```
eoffice-im/
├── SKILL.md                    # Skill 主文件
├── README.md                   # 本文件
└── references/
    └── im-api.md              # 完整 IM API 文档
```

## 许可证

MIT License
