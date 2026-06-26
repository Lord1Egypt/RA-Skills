# WeChat Automation

🤖 企业微信自动化技能 - 让消息推送更简单

## 快速开始

### 1. 安装

```bash
npx clawhub@latest install wechat-automation
```

### 2. 获取 Webhook Key

1. 打开企业微信管理后台
2. 进入「工作台」→「群机器人」
3. 添加机器人，复制 Webhook Key

### 3. 配置

```bash
clawhub config set wechat.webhook_key YOUR_WEBHOOK_KEY
```

### 4. 使用

```bash
# 发送文本消息
clawhub wechat send --text "Hello World"

# 发送 Markdown 消息
clawhub wechat send --markdown "**标题**\n\n内容"
```

## 功能特性

- ✅ 文本消息推送
- ✅ Markdown 格式支持
- ✅ 群聊消息发送
- ✅ @用户提醒
- ✅ 定时任务支持

## 示例

### 项目上线通知

```bash
clawhub wechat send --markdown "
## 🎉 项目上线成功

**项目**: XXX 系统
**时间**: $(date)
**环境**: 生产环境

所有测试通过，可以开始使用。
"
```

### 每日站会提醒

```bash
clawhub wechat schedule --cron "0 9 * * *" --text "
📅 每日站会提醒

时间：上午 9:00
地点：会议室 A / 线上链接

请准备：
1. 昨天完成的工作
2. 今天的计划
3. 遇到的阻碍
"
```

### 监控告警

```javascript
const wechat = require('wechat-automation');

// 服务器异常告警
async function alertError(error) {
  await wechat.sendMessage({
    text: `
## 🚨 服务器告警

**错误**: ${error.message}
**时间**: ${new Date().toISOString()}
**级别**: 严重

请立即处理！
    `,
    markdown: true,
    mentioned_list: ['@all']
  });
}
```

## API 参考

### sendMessage(options)

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| webhookKey | string | 是 | 企业微信 Webhook Key |
| text | string | 是 | 消息内容 |
| markdown | boolean | 否 | 是否使用 Markdown 格式 |
| chatid | string | 否 | 目标群聊 ID |
| mentioned_list | array | 否 | 需要@的用户列表 |

## 注意事项

1. **频率限制**: 每个 Webhook 最多 20 条/分钟
2. **内容长度**: 消息不超过 2048 字节
3. **权限**: 需要企业微信管理员权限获取 Webhook

## 更新日志

### v0.2.0 (2026-03-30)
- ✅ 完善 API 文档
- ✅ 添加使用示例
- ✅ 支持 Markdown 格式
- ✅ 添加测试脚本

### v0.1.0 (2026-03-29)
- ✅ 初始版本
- ✅ 基础 webhook 支持

## 许可证

MIT License

## 作者

小鸣 🦞 - 持续执行中
