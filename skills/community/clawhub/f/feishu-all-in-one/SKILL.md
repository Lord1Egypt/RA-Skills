---
name: feishu-all-in-one
version: 1.0.1
description: |
  飞书 All-in-One 技能包 - 开箱即用的飞书消息收发解决方案。
  集成：文字消息、图片/文件发送、语音转文字、互动卡片、主动消息。
  经过完整验证，所有功能均可直接使用。
metadata:
  tags: [feishu, message, interactive-card, voice-to-text, file, image, audio]
  author: ADIA (文哥团队)
  openclaw:
    emoji: "📱"
    requires:
      bins: [python3, node]
      config:
        - ~/.openclaw/openclaw.json
env:
  - name: FEISHU_APP_ID
    required: true
    description: 飞书应用 App ID
  - name: FEISHU_APP_SECRET
    required: true
    description: 飞书应用 App Secret
---

# 飞书 All-in-One 技能包

> 📦 开箱即用 | 经过完整验证 | 2026-03-04

本技能包整合了飞书消息收发的所有核心能力，经过实际测试验证，确保能够正常工作。

---

## 功能一览

| 功能 | 状态 | 说明 |
|------|------|------|
| 文字消息收发 | ✅ | 接收用户消息、主动推送文字 |
| 图片/文件发送 | ✅ | 支持本地文件、网络图片 |
| 语音转文字 | ✅ | 使用 faster-whisper |
| 互动卡片 | ✅ | 带按钮的交互卡片 |
| 卡片回调处理 | ✅ | 点击按钮自动处理 |

---

## 第一部分：飞书开放平台配置

### 1.1 创建应用

1. 打开 [飞书开放平台](https://open.feishu.cn/)
2. 点击「创建应用」→「企业自建应用」
3. 填写应用名称（如 OpenClaw Bot）
4. 获取 `App ID` 和 `App Secret`

### 1.2 配置应用凭证

在应用详情页获取：
- **App ID**: 如 `cli_xxxxxxxx`
- **App Secret**: 如 `xxxxxxxx`

### 1.3 配置权限

进入「权限管理」，添加以下权限：

| 权限名称 | 权限码 | 说明 |
|---------|--------|------|
| 获取应用基本信息 | app:app.base:readonly | 读取应用基本信息 |
| 发送消息 | im:message:send_as_bot | 以机器人身份发送消息 |
| 接收消息 | im:message:receive | 接收用户消息 |
| 上传图片和文件 | im:file:upload | 上传图片/文件 |
| 下载图片和文件 | im:file:download | 下载图片/文件 |
| 获取用户信息 | contact:user.base:readonly | 读取用户基本信息 |

### 1.4 配置事件与回调（关键！）

1. 进入「事件与回调」
2. **订阅方式**：选择「使用长连接接收事件/回调」
3. **订阅事件**：

| 事件名称 | 事件码 | 说明 |
|---------|--------|------|
| 接收消息 | im.message.receive_v1 | 接收用户发送的消息 |
| 卡片动作触发 | im.card.action.trigger | 互动卡片按钮点击 |

4. **接收地址**：使用长连接模式无需配置公网地址

### 1.5 发布应用

1. 在「版本管理与发布」中创建版本
2. 提交审核
3. 发布后，用户即可与机器人对话

---

## 第二部分：OpenClaw 配置

### 2.1 配置 openclaw.json

编辑 `~/.openclaw/openclaw.json`，添加飞书配置：

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "你的App_ID",
      "appSecret": "你的App_Secret",
      "domain": "feishu"
    }
  }
}
```

### 2.2 配置 accounts（互动卡片必需）

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxxxxxxx",
      "appSecret": "xxxxxxxx",
      "domain": "feishu",
      "accounts": {
        "main": {
          "appId": "cli_xxxxxxxx",
          "appSecret": "xxxxxxxx"
        }
      }
    }
  }
}
```

### 2.3 环境变量

在运行回调服务器前需要设置：

```bash
export FEISHU_APP_ID="cli_xxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxx"
```

---

## 第三部分：技能使用

### 3.1 文字消息

使用 OpenClaw 内置的 `message` 工具：

```javascript
// 发送文字消息
await message({
  action: "send",
  channel: "feishu",
  message: "你好，这是主动推送的消息",
  target: "ou_xxxxxxxx"  // 用户 open_id
});
```

### 3.2 发送图片/文件

```javascript
// 发送本地图片
await message({
  action: "send",
  channel: "feishu",
  message: "这是一张图片",
  filePath: "/path/to/image.png",
  target: "ou_xxxxxxxx"
});

// 发送网络图片
await message({
  action: "send",
  channel: "feishu",
  message: "网络图片",
  media: "https://example.com/image.png",
  target: "ou_xxxxxxxx"
});
```

### 3.3 发送互动卡片

运行修改后的脚本：

```bash
# 进入脚本目录
cd /path/to/skills/feishu-all-in-one/scripts

# 发送确认卡片（发给个人用户）
node send-card.js confirmation "消息内容" \
  --chat-id ou_xxxxxxxx \
  --receive-id-type open_id

# 发送投票卡片
node send-card.js poll "你喜欢哪个？" \
  --options "A,B,C" \
  --chat-id ou_xxxxxxxx \
  --receive-id-type open_id

# 发送自定义卡片
node send-card.js custom \
  --template examples/custom-card.json \
  --chat-id ou_xxxxxxxx \
  --receive-id-type open_id
```

**关键参数**：
- `--chat-id`: 目标用户/群聊 ID
- `--receive-id-type`: 
  - `open_id` - 发给个人用户
  - `chat_id` - 发给群聊
  - `user_id` - 飞书用户 ID

### 3.4 启动卡片回调服务器

```bash
cd /path/to/feishu-all-in-one/scripts

# 安装依赖（只需一次）
npm install

# 设置环境变量
export FEISHU_APP_ID="cli_xxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxx"

# 启动回调服务器
node card-callback-server.js &
```

回调服务器会：
1. 长连接方式监听卡片点击事件
2. 自动处理按钮回调
3. 可选：向 Gateway 发送回调通知

### 3.5 语音转文字

安装 faster-whisper：

```bash
python3.11 -m pip install faster-whisper
```

转写音频：

```python
from faster_whisper import WhisperModel

model = WhisperModel('base', device='cpu', compute_type='int8')
segments, info = model.transcribe('/path/to/audio.ogg')

print(f"语言: {info.language}")
for segment in segments:
    print(segment.text)
```

---

## 第四部分：脚本说明

### 4.1 send-card.js（已修复）

**修复内容**：
- 支持 `--receive-id-type open_id` 参数
- 可以发给个人用户而不仅是群聊

**完整用法**：

```bash
# 确认卡片
node send-card.js confirmation "确认删除吗？" \
  --chat-id ou_xxxxxxxx \
  --receive-id-type open_id

# 待办卡片
node send-card.js todo \
  --chat-id ou_xxxxxxxx \
  --receive-id-type open_id

# 投票卡片
node send-card.js poll "周末活动" \
  --options "爬山,吃饭,看电影" \
  --chat-id ou_xxxxxxxx \
  --receive-id-type open_id

# 自定义卡片
node send-card.js custom \
  --template /path/to/card.json \
  --chat-id ou_xxxxxxxx \
  --receive-id-type open_id
```

### 4.2 feishu_file_sender.py

发送本地文件到飞书：

```bash
python3 scripts/feishu_file_sender.py \
  --file /path/to/file.png \
  --receive-id ou_xxxxxxxx \
  --receive-id-type open_id
```

### 4.3 feishu_proactive_messenger.py

主动发送文字消息：

```bash
python3 scripts/feishu_proactive_messenger.py \
  --agent main \
  --text "这是主动推送的消息" \
  --receive-id ou_xxxxxxxx \
  --receive-id-type open_id
```

---

## 第五部分：常见问题

### Q1: 互动卡片发不出去，报错 "invalid receive_id"

**原因**：使用了 `chat_id` 类型发给个人用户  
**解决**：添加 `--receive-id-type open_id` 参数

### Q2: 点击卡片按钮没有反应

**原因**：回调服务器未启动  
**解决**：
```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
node card-callback-server.js &
```

### Q3: 主动消息发送失败

**原因**：用户未与机器人对话过（24小时限制）  
**解决**：让用户先在飞书中给机器人发一条消息

### Q4: 文件上传失败

**原因**：未配置应用凭证  
**解决**：确保 `openclaw.json` 中配置了完整的 `accounts.main`

---

## 第六部分：验证清单

完成配置后，按以下步骤验证：

- [ ] 飞书应用已发布
- [ ] OpenClaw 配置已更新
- [ ] 用户已与机器人对话
- [ ] 能收到用户消息
- [ ] 能发送文字消息
- [ ] 能发送图片
- [ ] 能发送互动卡片
- [ ] 点击卡片按钮有回调
- [ ] 语音消息能收到

---

## 文件结构

```
feishu-all-in-one/
├── SKILL.md                 # 本文档
├── README.md                # 快速开始
├── _meta.json               # 元数据
├── scripts/
│   ├── send-card.js         # 互动卡片发送（支持 open_id）
│   ├── card-callback-server.js  # 回调服务器（含 confirm 处理）
│   ├── card-templates.js    # 卡片模板
│   ├── feishu_file_sender.py    # 文件发送
│   ├── feishu_proactive_messenger.py  # 主动消息
│   └── package.json         # Node 依赖（axios, @larksuiteoapi/node-sdk）
└── references/
    ├── confirmation-card.json   # 确认卡片模板
    ├── todo-card.json             # 待办卡片模板
    ├── poll-card.json             # 投票卡片模板
    └── custom-card.json          # 自定义卡片模板
```

---

## 更新日志

### v1.0.2 (2026-03-04)
- 修复 `feishu_file_sender.py` agent_id 解析失败问题
- 兼容 `agents.defaults` 配置格式
- 支持从 `channels.feishu.accounts` 直接读取凭证（无需 bindings）

### v1.0.1 (2026-03-04)
- 回调服务器添加 `confirm` 按钮处理
- 添加 `@larksuiteoapi/node-sdk` 依赖说明
- 更新安装步骤（npm install）

### v1.0.0 (2026-03-04)
- 初始版本
- 整合 4 个核心能力
- 修复互动卡片 open_id 发送问题
- 添加完整的飞书平台配置指南
