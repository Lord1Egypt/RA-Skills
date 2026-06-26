---
name: claude-anywhere
description: "不是聊天机器人，是你口袋里的AI员工。Claude Anywhere 让你通过 Telegram、企业微信、QQ 随时随地读写文件、执行命令、分析图片、管理代码。Not a chatbot — your AI engineer in your pocket. Claude Anywhere lets you read/write files, execute commands, analyze images, manage code — from Telegram, WeChat Work, or QQ, anywhere."
version: 1.6.1
metadata:
  openclaw:
    requires:
      bins: [node, claude]
      env: [TELEGRAM_BOT_TOKEN]
    primaryEnv: TELEGRAM_BOT_TOKEN
    emoji: "📱"
    homepage: https://claudeanywhere.com/buy.html
---

# Claude Anywhere

**🦞 龙虾与Claude Code的完美结合 / OpenClaw meets Claude Code, anywhere.**

不是聊天机器人。是你口袋里的 AI 员工。
Not a chatbot. Your AI engineer, in your pocket.

Claude Anywhere 让你通过 Telegram、企业微信、QQ 随时随地：
- 📂 读写文件 / Read/write files
- ⚡ 执行命令 / Execute commands
- 📷 分析图片 / Analyze images
- 📄 文件分析 / Analyze files (PDF, Excel, CSV, code)
- 🔄 会话恢复 / Resume sessions across devices
- ⏰ 定时任务 / Schedule cron tasks

**Pro 版 ¥39.99/月 → [立即升级](https://claudeanywhere.com/buy.html)**

## 3步上手 / 3 Steps to Start

### Telegram
1. 在 Telegram 搜索 @BotFather，发 /newbot，复制 Token
2. `git clone https://github.com/yizhao1978/claude-anywhere.git && cd claude-anywhere && npm install && cp .env.example .env`
3. 填入 Token → `npm run telegram` → 完成

### 企业微信 WeChat Work
1. 登录 work.weixin.qq.com → 应用管理 → AI助手 → 创建机器人，记录 Bot ID 和 Secret
2. `git clone https://github.com/yizhao1978/claude-anywhere.git && cd claude-anywhere && npm install && cp .env.example .env`
3. 填入 Bot ID + Secret → `npm run wecom` → 完成

### QQ
1. 打开 https://q.qq.com/qqbot/openclaw/index.html → 扫码 → 创建机器人 → 获取 AppID + AppSecret
2. `git clone https://github.com/yizhao1978/claude-anywhere.git && cd claude-anywhere && npm install && cp .env.example .env`
3. 填入 AppID + AppSecret → `npm run qq` → 完成

### 三平台一键启动
配好所有 Token → `npm start` → 自动启动已配置的平台

## Free Tier (no LICENSE_KEY)
- 5 messages/day
- 7-day trial period
- Single-turn conversations
- Text only
- Upgrade prompts on every reply

## Pro (¥39.99/月 | ¥399.9/年) → https://claudeanywhere.com/buy.html
- Unlimited messages
- Multi-turn conversations with /resume
- Image and file analysis
- WeChat Work full support
- **付款后自动开通，无需填写 License Key / Auto-activated after payment**

## License Activation

扫码付款后 Pro 自动开通，无需任何操作。
After WeChat Pay, Pro is activated instantly and automatically.








