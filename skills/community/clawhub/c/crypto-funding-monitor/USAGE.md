# Crypto Funding Monitor - 使用示例

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 配置环境变量

复制 `.env.example` 到 `.env` 并填写配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
SKILLPAY_API_KEY=sk_e390b52cb259fc4f4aa1489547a48375d72876acdee75de57101d9e0e833fcb7
TELEGRAM_BOT_TOKEN=your_bot_token_here
DISCORD_WEBHOOK_URL=your_webhook_url_here
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```

### 3. 启动服务

```bash
npm start
```

## API 使用示例

### 触发一次监测

```bash
curl -X POST http://localhost:3000/monitor \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user123",
    "transactionId": "tx456",
    "channels": {
      "telegram": {
        "chatId": "123456789"
      },
      "discord": true,
      "email": {
        "to": "user@example.com"
      }
    }
  }'
```

### 订阅定时推送

```bash
curl -X POST http://localhost:3000/subscribe \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user123",
    "channels": {
      "telegram": {
        "chatId": "123456789"
      },
      "email": {
        "to": "user@example.com"
      }
    },
    "schedule": ["0 9 * * *", "0 18 * * *"]
  }'
```

### 查询订阅状态

```bash
curl http://localhost:3000/subscription/user123
```

### 取消订阅

```bash
curl -X POST http://localhost:3000/unsubscribe \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user123"
  }'
```

## Telegram Bot 使用

### 1. 创建 Telegram Bot

1. 在 Telegram 中找到 @BotFather
2. 发送 `/newbot` 创建新 bot
3. 按提示设置 bot 名称
4. 获取 Bot Token 并配置到 `.env`

### 2. 获取 Chat ID

1. 启动你的 bot
2. 发送任意消息给 bot
3. 访问: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. 在返回的 JSON 中找到 `chat.id`

### 3. Bot 命令

- `/start` - 开始使用
- `/subscribe` - 订阅推送
- `/unsubscribe` - 取消订阅

## Discord Webhook 设置

1. 进入 Discord 服务器设置
2. 选择 "集成" > "Webhook"
3. 创建新 Webhook
4. 复制 Webhook URL 到 `.env`

## Email 配置

### Gmail 示例

1. 启用两步验证
2. 生成应用专用密码
3. 配置到 `.env`:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```

## 定时任务配置

默认推送时间：
- 早上 9:00
- 晚上 18:00

修改 `.env` 自定义时间：

```env
SCHEDULE_MORNING=0 9 * * *
SCHEDULE_EVENING=0 18 * * *
```

Cron 表达式格式：
```
* * * * *
│ │ │ │ │
│ │ │ │ └─ 星期 (0-7)
│ │ │ └─── 月份 (1-12)
│ │ └───── 日期 (1-31)
│ └─────── 小时 (0-23)
└───────── 分钟 (0-59)
```

## 测试

运行测试脚本：

```bash
node test.js
```

## 数据源

- **RootData**: 加密项目融资数据
- **Twitter**: 实时融资动态
- 更多数据源可通过扩展 `src/scrapers/` 添加

## 收益模式

- 每次调用: 0.001 USDT
- 通过 SkillPay.me 自动结算
- 用户订阅后按调用次数计费

## 故障排查

### 数据抓取失败

检查网络连接和 API 配置：

```bash
# 测试 RootData 连接
curl https://www.rootdata.com/Fundraising

# 测试 Twitter API
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.twitter.com/2/tweets/search/recent?query=crypto
```

### 通知推送失败

检查配置和权限：

```bash
# 测试 Telegram Bot
curl https://api.telegram.org/botYOUR_TOKEN/getMe

# 测试 Discord Webhook
curl -X POST YOUR_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{"content": "Test message"}'
```

## 进阶功能

### 自定义数据源

在 `src/scrapers/` 添加新的抓取器：

```javascript
class CustomScraper {
  async getData() {
    // 实现数据抓取逻辑
  }
}
```

### 自定义通知渠道

在 `src/notifiers/` 添加新的推送器：

```javascript
class CustomNotifier {
  async send(data) {
    // 实现推送逻辑
  }
}
```

## 许可证

MIT
