# 🚀 Crypto Funding Monitor Skill

## 快速开始

### 方式一：使用快速启动脚本（推荐）

```bash
chmod +x quickstart.sh
./quickstart.sh
```

### 方式二：手动启动

```bash
# 1. 安装依赖
npm install

# 2. 配置环境变量（可选）
# 编辑 .env 文件，添加 Telegram、Discord、Email 配置

# 3. 启动服务
npm start

# 4. 测试功能
node test.js
```

## 核心功能

✅ **已配置 SkillPay API Key** - 可直接使用付费功能
✅ **RootData 融资监测** - 自动抓取最新融资项目
✅ **Twitter 动态追踪** - 搜索加密货币融资推文
✅ **TEG 项目监测** - 追踪即将 Token Generation 的项目
✅ **多渠道推送** - 支持 Telegram、Discord、Email
✅ **定时简报** - 每日自动推送（9:00, 18:00）
✅ **按次付费** - 每次调用 0.001 USDT

## 项目结构

```
├── src/
│   ├── index.js              # 主服务器
│   ├── payment.js            # SkillPay 集成 ✅
│   ├── scheduler.js          # 定时任务
│   ├── scrapers/             # 数据抓取
│   │   ├── rootdata.js       # RootData
│   │   └── twitter.js        # Twitter
│   └── notifiers/            # 通知推送
│       ├── telegram.js       # Telegram
│       ├── discord.js        # Discord
│       └── email.js          # Email
├── package.json              # 依赖配置
├── skill.json                # Clawhub 配置 ✅
├── .env                      # 环境变量 ✅
└── test.js                   # 测试脚本
```

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/monitor` | POST | 触发监测（需支付） |
| `/subscribe` | POST | 订阅服务 |
| `/unsubscribe` | POST | 取消订阅 |
| `/subscription/:userId` | GET | 查询订阅 |

## 使用示例

### 触发一次监测

```bash
curl -X POST http://localhost:3000/monitor \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user123",
    "transactionId": "tx456",
    "channels": {
      "telegram": { "chatId": "123456789" }
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
      "telegram": { "chatId": "123456789" },
      "email": { "to": "user@example.com" }
    }
  }'
```

## 部署到 Clawhub

```bash
# 1. 安装 Clawhub CLI
npm install -g @clawhub/cli

# 2. 登录
clawhub login

# 3. 发布
clawhub publish

# 4. 查看状态
clawhub status your-skill-id
```

详细部署指南请查看 [DEPLOY.md](DEPLOY.md)

## 配置说明

### 必需配置（已完成）
- ✅ `SKILLPAY_API_KEY`: sk_e390b52cb259fc4f4aa1489547a48375d72876acdee75de57101d9e0e833fcb7

### 可选配置（增强功能）
- `TELEGRAM_BOT_TOKEN`: Telegram Bot 令牌
- `DISCORD_WEBHOOK_URL`: Discord Webhook URL
- `EMAIL_USER/EMAIL_PASS`: SMTP 邮箱配置
- `TWITTER_BEARER_TOKEN`: Twitter API 令牌

## 收益模式

💰 **按次付费**: 每次调用 0.001 USDT
💰 **订阅模式**: 用户订阅后定时推送
💰 **自动结算**: SkillPay.me 自动处理支付

## 文档

- 📖 [使用指南](USAGE.md) - 详细使用说明
- 🚀 [部署指南](DEPLOY.md) - Clawhub 部署步骤
- 📋 [发布检查清单](CHECKLIST.md) - 发布前检查
- 🏗️ [项目结构](PROJECT_STRUCTURE.md) - 代码结构说明

## 测试

```bash
# 运行测试脚本
node test.js

# 启动服务器
npm start

# 访问健康检查
curl http://localhost:3000/health
```

## 技术栈

- Node.js + Express
- SkillPay.me 支付集成
- RootData + Twitter 数据源
- Telegram + Discord + Email 推送
- node-cron 定时任务

## 支持

- GitHub Issues: [提交问题](https://github.com/your-repo/issues)
- Clawhub 文档: https://docs.clawhub.com
- SkillPay 支持: https://skillpay.me/support

## 许可证

MIT

---

**准备好开始赚钱了吗？** 🚀

1. `npm install` - 安装依赖
2. `npm start` - 启动服务
3. `clawhub publish` - 发布到 Clawhub
4. 💰 开始赚取 USDT！
