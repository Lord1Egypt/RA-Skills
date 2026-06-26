# Crypto Funding Monitor Skill

实时监测加密货币项目融资和TEG信息的智能skill，支持多平台推送。

## 功能特性

- 🔍 **多平台监测**: RootData、X (Twitter) 等平台
- 📊 **融资信息**: 最新融资轮次、金额、投资方
- 🚀 **TEG项目**: Token Generation Event 项目追踪
- 📱 **多渠道推送**: Telegram、Discord、Email
- 💰 **付费调用**: 通过 SkillPay.me 集成，每次调用 0.001 USDT
- ⏰ **定时推送**: 每日定时简报

## 安装

```bash
npm install
```

## 配置

创建 `.env` 文件：

```env
# SkillPay API Key
SKILLPAY_API_KEY=sk_e390b52cb259fc4f4aa1489547a48375d72876acdee75de57101d9e0e833fcb7

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Discord Webhook
DISCORD_WEBHOOK_URL=your_discord_webhook_url

# Email (SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_email_password

# Twitter API (Optional)
TWITTER_BEARER_TOKEN=your_twitter_bearer_token

# RootData API (if available)
ROOTDATA_API_KEY=your_rootdata_api_key
```

## 使用

```bash
npm start
```

## API 端点

### POST /monitor
触发一次监测并推送简报

### POST /subscribe
订阅定时推送服务

### POST /unsubscribe
取消订阅

## 上传到 Clawhub

1. 确保 `skill.json` 配置正确
2. 使用 Clawhub CLI 上传：
   ```bash
   clawhub publish
   ```

## 收益模式

- 每次调用收费: 0.001 USDT
- 通过 SkillPay.me 自动结算
- 用户订阅后定时推送

## License

MIT
