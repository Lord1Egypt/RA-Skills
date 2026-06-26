# 还活着么监测服务

独居人群每日签到监测服务，关爱独居安全。

## 功能介绍

### 核心功能

**每日签到**
- 用户每天签到证明"还活着"
- 可添加心情、状态描述
- 支持语音、文字、图片签到

**紧急联系人**
- 设置多个紧急联系人
- 分级通知机制
- 支持Telegram、Discord、Email、短信

**自动监测**
- 每6小时检查用户状态
- 超过24小时未签到自动告警
- 48小时高危状态通知所有联系人

**签到历史**
- 查看签到记录
- 统计分析
- 导出报告

## API 端点

### POST /register
注册用户并设置紧急联系人

**请求示例：**
```json
{
  "userId": "user123",
  "name": "张三",
  "phone": "13800138000",
  "emergencyContacts": [
    {
      "name": "李四",
      "relation": "朋友",
      "phone": "13900139000",
      "telegram": "123456789",
      "priority": 1
    }
  ]
}
```

### POST /checkin
用户每日签到

**请求示例：**
```json
{
  "userId": "user123",
  "message": "今天状态不错！",
  "mood": "😊",
  "location": "在家"
}
```

### GET /status/:userId
查询用户签到状态

**响应示例：**
```json
{
  "userId": "user123",
  "name": "张三",
  "lastCheckin": "2026-03-06T10:30:00Z",
  "hoursSinceLastCheckin": 5,
  "status": "正常",
  "consecutiveDays": 15
}
```

### GET /history/:userId
查看签到历史

**查询参数：**
- `days`: 查询天数（默认7天）
- `limit`: 返回记录数

## 配置说明

必需配置：
- `SKILLPAY_API_KEY`: SkillPay API密钥

可选配置：
- `TELEGRAM_BOT_TOKEN`: Telegram通知
- `DISCORD_WEBHOOK_URL`: Discord通知
- `EMAIL_USER/EMAIL_PASS`: 邮件通知
- `SMS_API_KEY`: 短信通知

## 告警流程

1. **12小时未签到** → 温馨提醒用户
2. **24小时未签到** → 通知第一紧急联系人
3. **48小时未签到** → 通知所有紧急联系人，标记高危

## 使用场景

- 独居老人安全监测
- 独居年轻人互相关心
- 抑郁症患者安全保障
- 慢性病患者日常监测
- 独自旅行安全确认

## 定价

- 0.001 USDT/天
- 自动通过 SkillPay.me 结算

## 安装

```bash
npm install
npm start
```

## 许可证

MIT
