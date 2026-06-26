# Clawhub 部署指南

## 前置要求

1. 安装 Clawhub CLI
```bash
npm install -g @clawhub/cli
```

2. 登录 Clawhub
```bash
clawhub login
```

## 部署步骤

### 1. 配置环境变量

确保 `.env` 文件已正确配置所有必需的环境变量。

### 2. 测试本地运行

```bash
npm install
npm start
```

访问 `http://localhost:3000/health` 确认服务正常运行。

### 3. 验证 skill.json

确保 `skill.json` 包含正确的配置：
- SkillPay API Key
- 定价信息
- 端点描述

### 4. 发布到 Clawhub

```bash
clawhub publish
```

按照提示完成发布流程。

### 5. 验证部署

发布成功后，Clawhub 会提供一个 skill URL。使用以下命令测试：

```bash
curl -X POST https://clawhub.com/api/skills/your-skill-id/monitor \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "test-user",
    "transactionId": "test-tx",
    "channels": {
      "telegram": { "chatId": "your-chat-id" }
    }
  }'
```

## 更新 Skill

修改代码后，重新发布：

```bash
# 更新版本号
npm version patch

# 重新发布
clawhub publish
```

## 监控和日志

查看 skill 运行日志：

```bash
clawhub logs your-skill-id
```

查看使用统计：

```bash
clawhub stats your-skill-id
```

## 收益提现

1. 登录 Clawhub 控制台
2. 进入 "Earnings" 页面
3. 连接钱包并提现 USDT

## 故障排查

### 支付验证失败
- 检查 SkillPay API Key 是否正确
- 确认用户已完成支付

### 数据抓取失败
- 检查 RootData/Twitter API 配置
- 验证网络连接

### 通知推送失败
- 检查 Telegram Bot Token
- 验证 Discord Webhook URL
- 确认 Email SMTP 配置

## 技术支持

如遇问题，请联系：
- Clawhub 支持: support@clawhub.com
- GitHub Issues: https://github.com/your-repo/issues
