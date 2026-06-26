# Crypto Funding Monitor

实时监测加密货币项目融资和TEG信息的智能skill，支持多平台推送。

## 功能特性

- 🔍 **多平台监测**: RootData、X (Twitter) 等平台
- 📊 **融资信息**: 最新融资轮次、金额、投资方
- 🚀 **TEG项目**: Token Generation Event 项目追踪
- 📱 **多渠道推送**: Telegram、Discord、Email
- 💰 **付费调用**: 通过 SkillPay.me 集成，每次调用 0.001 USDT
- ⏰ **定时推送**: 每日定时简报

## 使用方法

### API 端点

#### POST /monitor
触发一次监测并推送简报

**请求参数**:
```json
{
  "userId": "user123",
  "transactionId": "tx456",
  "channels": {
    "telegram": { "chatId": "123456789" },
    "discord": true,
    "email": { "to": "user@example.com" }
  }
}
```

#### POST /subscribe
订阅定时推送服务

**请求参数**:
```json
{
  "userId": "user123",
  "channels": {
    "telegram": { "chatId": "123456789" },
    "email": { "to": "user@example.com" }
  },
  "schedule": ["0 9 * * *", "0 18 * * *"]
}
```

#### POST /unsubscribe
取消订阅

**请求参数**:
```json
{
  "userId": "user123"
}
```

## 配置

需要配置以下环境变量：

- `SKILLPAY_API_KEY`: SkillPay API密钥（必需）
- `TELEGRAM_BOT_TOKEN`: Telegram Bot令牌（可选）
- `DISCORD_WEBHOOK_URL`: Discord Webhook URL（可选）
- `EMAIL_USER/EMAIL_PASS`: SMTP邮箱配置（可选）
- `TWITTER_BEARER_TOKEN`: Twitter API令牌（可选）

## 定价

- 每次调用: 0.001 USDT
- 通过 SkillPay.me 自动结算

## 数据源

- **RootData**: 加密项目融资数据库
- **Twitter/X**: 实时融资动态
- 支持扩展更多数据源

## 推送渠道

- **Telegram**: Bot推送到个人或群组
- **Discord**: Webhook推送到频道
- **Email**: SMTP邮件推送

## 定时任务

默认推送时间：
- 早上 9:00
- 晚上 18:00

可通过环境变量自定义。

## 技术栈

- Node.js + Express
- SkillPay.me 支付集成
- RootData + Twitter 数据源
- Telegram + Discord + Email 推送
- node-cron 定时任务

## 许可证

MIT
