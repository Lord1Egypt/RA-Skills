# WeChat Automation v0.2

企业微信自动化技能，支持 webhook 消息发送和自动化流程。

## 功能

- ✅ 企业微信 webhook 消息发送
- ✅ 群消息推送
- ✅ 定时任务支持
- ✅ 消息模板

## 安装

```bash
npx clawhub@latest install wechat-automation
```

## 配置

```bash
# 设置企业微信 Webhook Key
clawhub config set wechat.webhook_key YOUR_WEBHOOK_KEY
```

## 使用

### 发送消息

```bash
# 发送文本消息
clawhub wechat send --text "Hello World"

# 发送 Markdown 消息
clawhub wechat send --markdown "**重要通知**\n\n项目进度更新..."

# 发送到指定群
clawhub wechat send --text "消息内容" --chatid "CHAT_ID"
```

### 自动化示例

```bash
# 定时发送日报
clawhub wechat schedule --cron "0 18 * * *" --text "日报提醒"
```

## API

### sendMessage(text, options)

发送消息到企业微信群。

**参数:**
- `text` (string): 消息内容
- `options` (object): 可选配置
  - `markdown` (boolean): 是否使用 Markdown 格式
  - `chatid` (string): 目标群聊 ID
  - `mentioned_list` (array): 需要@的用户列表

**返回:**
```json
{
  "errcode": 0,
  "errmsg": "ok",
  "msgid": "msg_xxxxx"
}
```

## 示例

```javascript
const wechat = require('wechat-automation');

// 发送通知
await wechat.sendMessage({
  text: '🎉 项目上线成功！',
  markdown: true
});

// 发送日报
await wechat.sendMessage({
  text: `
## 日报 2026-03-30

### 完成情况
- ✅ 功能 A
- ✅ 功能 B

### 明日计划
- [ ] 功能 C
  `,
  markdown: true
});
```

## 注意事项

1. 需要企业微信管理员权限获取 Webhook Key
2. 每个 Webhook 有发送频率限制（通常 20 条/分钟）
3. 消息内容不能超过 2048 字节

## 更新日志

### v0.2 (2026-03-30)
- ✅ 完善 API 文档
- ✅ 添加使用示例
- ✅ 支持 Markdown 格式

### v0.1 (2026-03-29)
- ✅ 初始版本
- ✅ 基础 webhook 支持
