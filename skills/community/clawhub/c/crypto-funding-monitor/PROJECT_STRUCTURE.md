# 项目结构

```
crypto-funding-monitor-skill/
├── src/
│   ├── index.js              # 主入口文件，Express服务器
│   ├── payment.js            # SkillPay支付集成
│   ├── scheduler.js          # 定时任务调度器
│   ├── scrapers/             # 数据抓取模块
│   │   ├── rootdata.js       # RootData平台抓取
│   │   └── twitter.js        # Twitter/X平台抓取
│   └── notifiers/            # 通知推送模块
│       ├── telegram.js       # Telegram推送
│       ├── discord.js        # Discord推送
│       └── email.js          # Email推送
├── package.json              # 项目依赖配置
├── skill.json                # Clawhub skill配置
├── .env                      # 环境变量（已配置SkillPay API Key）
├── .env.example              # 环境变量示例
├── .gitignore                # Git忽略文件
├── README.md                 # 项目说明
├── USAGE.md                  # 使用指南
├── DEPLOY.md                 # 部署指南
└── test.js                   # 测试脚本
```

## 核心模块说明

### 1. src/index.js
主应用入口，包含：
- Express API服务器
- 路由配置（/monitor, /subscribe, /unsubscribe等）
- 数据收集和通知分发逻辑
- 定时任务设置

### 2. src/payment.js
SkillPay支付集成：
- 支付验证
- 创建支付请求
- 使用记录

### 3. src/scrapers/
数据抓取器：
- **rootdata.js**: 从RootData抓取融资和TEG项目
- **twitter.js**: 从Twitter搜索相关推文

### 4. src/notifiers/
通知推送器：
- **telegram.js**: Telegram Bot推送
- **discord.js**: Discord Webhook推送
- **email.js**: SMTP邮件推送

### 5. src/scheduler.js
基于node-cron的定时任务管理器

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| /health | GET | 健康检查 |
| /monitor | POST | 触发一次监测并推送 |
| /subscribe | POST | 订阅定时推送服务 |
| /unsubscribe | POST | 取消订阅 |
| /subscription/:userId | GET | 查询订阅状态 |
| /payment/callback | POST | 支付回调 |

## 技术栈

- **Node.js**: 运行环境
- **Express**: Web框架
- **axios**: HTTP客户端
- **cheerio**: HTML解析（网页抓取）
- **node-cron**: 定时任务
- **telegraf**: Telegram Bot框架
- **discord.js**: Discord集成
- **nodemailer**: 邮件发送
- **dotenv**: 环境变量管理

## 配置说明

### 必需配置
- `SKILLPAY_API_KEY`: SkillPay API密钥（已配置）

### 可选配置
- `TELEGRAM_BOT_TOKEN`: Telegram Bot令牌
- `DISCORD_WEBHOOK_URL`: Discord Webhook URL
- `EMAIL_USER/EMAIL_PASS`: SMTP邮箱配置
- `TWITTER_BEARER_TOKEN`: Twitter API令牌
- `ROOTDATA_API_KEY`: RootData API密钥

## 工作流程

1. **用户订阅**
   - 用户调用 `/subscribe` 端点
   - 系统创建支付请求
   - 用户完成支付
   - 订阅激活

2. **定时监测**
   - 每日定时（9:00, 18:00）触发
   - 从RootData、Twitter抓取数据
   - 格式化为简报
   - 推送到用户配置的渠道

3. **手动触发**
   - 用户调用 `/monitor` 端点
   - 验证支付（0.001 USDT）
   - 立即执行监测和推送

## 收益模式

- **按次付费**: 每次调用 0.001 USDT
- **订阅模式**: 用户订阅后定时推送
- **自动结算**: 通过SkillPay.me自动处理支付

## 下一步

1. 安装依赖: `npm install`
2. 配置环境变量: 编辑 `.env` 文件
3. 启动服务: `npm start`
4. 测试功能: `node test.js`
5. 部署到Clawhub: 参考 `DEPLOY.md`
