---
name: feishu-openclaw-integration
version: 1.0.0
slug: feishu-openclaw-integration
tags: ["latest", "chinese", "enterprise"]
description: 飞书 + OpenClaw 无缝集成 - 5 分钟搭建企业 AI 助手。支持群聊机器人、智能客服、自动化工作流。
metadata:
  openclaw:
    emoji: "🚀"
    requires:
      bins: ["node", "npm"]
      env: ["FEISHU_APP_ID", "FEISHU_APP_SECRET"]
---

# 飞书 + OpenClaw 集成 Skill

5 分钟搭建企业 AI 助手 - 零代码，即插即用。

## 核心价值

- ✅ **零代码** - 配置即用，无需编程
- ✅ **企业级** - 飞书官方 API，稳定可靠
- ✅ **智能回复** - 接入 OpenClaw 大模型
- ✅ **自动化** - 定时推送、事件触发
- ✅ **私有化** - 数据不离开企业

## 快速开始

### 方式 1：OpenClaw 内置（推荐，5 分钟）

1. **配置飞书频道**（OpenClaw 已内置支持）

```bash
# 编辑 ~/.openclaw/config/channels.json
{
  "feishu": {
    "enabled": true,
    "appId": "YOUR_APP_ID",
    "appSecret": "YOUR_APP_SECRET",
    "encryptKey": "YOUR_ENCRYPT_KEY",
    "verificationToken": "YOUR_VERIFICATION_TOKEN"
  }
}
```

2. **创建飞书应用**（3 分钟）

   - 访问 https://open.feishu.cn
   - 创建「企业自建应用」
   - 启用「机器人」权限
   - 配置事件回调（OpenClaw 自动处理）

3. **测试**

   ```
   # 在飞书群@机器人
   @Jarvis 帮我写一份周报
   ```

### 方式 2：Node.js SDK（10 分钟）

```bash
# 安装依赖
npm install @larksuiteoapi/node-sdk axios

# 创建集成脚本
cat > feishu-bot.js << 'EOF'
const lark = require('@larksuiteoapi/node-sdk');
const axios = require('axios');

const client = new lark.Client({
  appId: process.env.FEISHU_APP_ID,
  appSecret: process.env.FEISHU_APP_SECRET,
});

const OPENCLAW_URL = process.env.OPENCLAW_URL || 'http://localhost:3000';

// 处理飞书消息
client.im.message.subscribe({
  on: async (event) => {
    const { message } = event;
    const content = JSON.parse(message.content);

    // 发送到 OpenClaw
    const response = await axios.post(`${OPENCLAW_URL}/api/chat`, {
      message: content.text,
      userId: message.sender_id,
      channel: 'feishu',
    });

    // 回复消息
    await client.im.message.create({
      receive_id_type: 'chat_id',
      params: { receive_id: message.chat_id },
      data: {
        msg_type: 'text',
        content: JSON.stringify({ text: response.data.reply })
      }
    });
  }
});
EOF

# 运行
FEISHU_APP_ID=xxx FEISHU_APP_SECRET=xxx node feishu-bot.js
```

## 实用场景

### 1. 群聊 AI 助手

```yaml
# config/group-assistant.yaml
prompts:
  tech_group:
    system: "你是技术群的 AI 助手，专业、简洁、直接。"
    temperature: 0.3

  product_group:
    system: "你是产品群的 AI 助手，关注用户体验、需求分析。"
    temperature: 0.7
```

### 2. 智能客服

```python
# 自动回复规则
AUTO_REPLY = {
    '价格': '基础版 ¥99，高级版 ¥299',
    '售后': '请联系售后微信：xxx',
    '发票': '提供增值税普通发票，开票请联系财务',
}

def handle_keyword(text):
    for keyword, reply in AUTO_REPLY.items():
        if keyword in text:
            return reply
    return None  # 转到 OpenClaw 处理
```

### 3. 定时通知

```javascript
// 每天早上 9 点发送日报提醒
const schedule = require('node-schedule');

schedule.scheduleJob('0 9 * * *', async () => {
  await client.im.message.create({
    receive_id_type: 'chat_id',
    params: { receive_id: 'WORK_GROUP_ID' },
    data: {
      msg_type: 'interactive',
      content: JSON.stringify({
        config: {
          wide_screen_mode: true
        },
        elements: [{
          tag: 'div',
          text: {
            tag: 'lark_md',
            content: '📊 **日报提醒**\n\n请大家在今天 18:00 前提交日报'
          }
        }]
      })
    }
  });
});
```

### 4. 数据分析

```javascript
// 分析群聊数据，生成报告
async function generateReport(chatId) {
  const messages = await client.im.message.list({
    params: {
      container_id_type: 'chat_id',
      container_id: chatId,
      page_size: 100
    }
  });

  // 发送给 OpenClaw 分析
  const analysis = await axios.post(`${OPENCLAW_URL}/api/analyze`, {
    data: messages,
    task: '总结今天的讨论要点'
  });

  return analysis.data;
}
```

## 高级功能

### 消息卡片（富文本）

```javascript
// 发送精美卡片
await client.im.message.create({
  receive_id_type: 'chat_id',
  params: { receive_id: chatId },
  data: {
    msg_type: 'interactive',
    content: JSON.stringify({
      config: { wide_screen_mode: true },
      header: {
        title: {
          tag: 'plain_text',
          content: '🚀 AI 分析报告'
        }
      },
      elements: [{
        tag: 'div',
        text: {
          tag: 'lark_md',
          content: '**关键结论**\n- 用户增长 20%\n- 留存率 85%'
        }
      }]
    })
  }
});
```

### 文件处理

```javascript
// 处理上传的文件
if (message.msg_type === 'file') {
  const fileKey = JSON.parse(message.content).file_key;

  // 下载文件
  const file = await client.im.file.download({
    params: { type: 'file', file_key: fileKey }
  });

  // 发送给 OpenClaw 分析
  const result = await axios.post(`${OPENCLAW_URL}/api/analyze-file`, {
    file: file.data,
    task: '总结这份文档的关键信息'
  });
}
```

### 多 Agent 协作

```javascript
// 不同群用不同 Agent
const AGENTS = {
  'TECH_GROUP_ID': 'jarvis',      // 技术群
  'PRODUCT_GROUP_ID': 'assistant', // 产品群
  'SALES_GROUP_ID': 'sales-bot',  // 销售群
};

async function routeMessage(chatId, text) {
  const agent = AGENTS[chatId] || 'default';

  return await axios.post(`${OPENCLAW_URL}/api/chat`, {
    message: text,
    agent: agent
  });
}
```

## 配置文件模板

### ~/.openclaw/feishu-config.yaml

```yaml
# 飞书应用配置
app:
  id: "cli_xxxxxxxxx"
  secret: "xxxxxxxxxxxxxxxx"
  encrypt_key: "xxxxxxxxxxxxxxxx"
  verification_token: "xxxxxxxxxxxxxxxx"

# 机器人配置
bot:
  name: "Jarvis"
  avatar: "https://example.com/avatar.png"
  welcome_message: "你好！我是 AI 助手 Jarvis，有什么可以帮你的？"

# 自动回复
auto_reply:
  enabled: true
  rules:
    - keywords: ["价格", "多少钱"]
      reply: "基础版 ¥99，高级版 ¥299，企业定制请联系客服"
    - keywords: ["发票", "开票"]
      reply: "提供增值税普通发票，请联系财务"
    - keywords: ["售后", "客服"]
      reply: "售后微信：xxx"

# AI 配置
ai:
  model: "gpt-4"
  temperature: 0.7
  max_tokens: 2000
  system_prompt: "你是企业 AI 助手，专业、高效、简洁。"

# 群配置
groups:
  - chat_id: "oc_xxxxxxxxx"
    name: "技术群"
    agent: "jarvis-tech"
    enabled_commands: ["/code", "/review", "/help"]
  - chat_id: "oc_xxxxxxxxx"
    name: "产品群"
    agent: "jarvis-product"
    enabled_commands: ["/pr", "/analyze", "/summary"]

# 定时任务
schedule:
  - cron: "0 9 * * *"
    message: "📊 日报提醒：请在 18:00 前提交日报"
    target_groups: ["ALL"]
  - cron: "0 18 * * *"
    command: "/summary"
    target_groups: ["技术群", "产品群"]
```

## 常见问题

### Q: 如何获取飞书应用凭证？

1. 登录 https://open.feishu.cn
2. 点击「创建应用」
3. 选择「企业自建应用」
4. 在应用详情页获取 App ID 和 App Secret

### Q: 如何配置权限？

在飞书开放平台，应用需要开通以下权限：
- `im:message`（发送消息）
- `im:message:group_at_msg`（群@消息）
- `contact:user.base:readonly`（读取用户信息）

### Q: 支持哪些消息类型？

- 文本消息
- 图片消息
- 文件消息
- 富文本消息（卡片）
- 互动消息（按钮）

### Q: 如何处理高并发？

```javascript
// 使用消息队列
const queue = require('bull');
const messageQueue = new queue('feishu-messages');

// 生产者
client.im.message.subscribe({
  on: (event) => {
    messageQueue.add(event);
  }
});

// 消费者（可横向扩展）
messageQueue.process(async (job) => {
  await handleFeishuMessage(job.data);
});
```

## 部署建议

### 开发环境
```bash
# 本地运行
npm install
npm start
```

### 生产环境（推荐）
```bash
# 使用 Docker
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
CMD ["node", "server.js"]
```

### 云部署（免运维）
- **Vercel** - 自动扩缩容
- **Railway** - 数据库 + 应用一键部署
- **Render** - 免费套餐

## 技术支持

- 文档：https://docs.openclaw.ai
- 飞书开放平台：https://open.feishu.cn
- 社区：https://discord.gg/clawd

---

**版本**：1.0.0
**更新**：2026-03-17
**作者**：OpenClaw Community
**许可**：MIT
