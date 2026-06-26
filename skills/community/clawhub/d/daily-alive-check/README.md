# 还活着么监测服务

独居人群每日签到监测服务，长时间未签到自动通知紧急联系人。

## 功能特点

- 📱 **每日签到**: 用户每天签到证明"还活着"
- 👥 **紧急联系人**: 设置多个紧急联系人
- ⏰ **自动监测**: 超过24小时未签到自动告警
- 🔔 **多渠道通知**: Telegram、Discord、Email、短信
- 📊 **签到历史**: 查看签到记录和统计
- 💝 **关怀提醒**: 定时提醒用户签到
- 🆘 **紧急求助**: 一键发送求助信息

## 使用场景

### 独居老人
- 子女可以实时了解父母安全状况
- 长时间未签到自动通知家人
- 避免意外发生无人知晓

### 独居年轻人
- 朋友互相关心生活状态
- 抑郁症患者的安全监测
- 独自旅行时的安全保障

### 特殊人群
- 慢性病患者的日常监测
- 独自工作的高危职业人员
- 需要定期确认安全的任何人

## API 使用

### 注册用户

```bash
curl -X POST http://localhost:3000/register \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user123",
    "name": "张三",
    "phone": "13800138000",
    "emergencyContacts": [
      {
        "name": "李四",
        "relation": "朋友",
        "phone": "13900139000",
        "telegram": "123456789"
      }
    ]
  }'
```

### 每日签到

```bash
curl -X POST http://localhost:3000/checkin \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user123",
    "message": "今天状态不错！",
    "mood": "😊"
  }'
```

### 查询状态

```bash
curl http://localhost:3000/status/user123
```

### 查看签到历史

```bash
curl http://localhost:3000/history/user123?days=7
```

## 配置说明

创建 `.env` 文件：

```env
# SkillPay API Key（必需）
SKILLPAY_API_KEY=sk_e390b52cb259fc4f4aa1489547a48375d72876acdee75de57101d9e0e833fcb7

# 服务器端口
PORT=3000

# Telegram Bot（可选）
TELEGRAM_BOT_TOKEN=

# Discord Webhook（可选）
DISCORD_WEBHOOK_URL=

# 邮件SMTP（可选）
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=
EMAIL_PASS=

# 短信服务（可选）
SMS_API_KEY=
SMS_API_SECRET=

# 监测配置
ALERT_THRESHOLD_HOURS=24
CHECK_INTERVAL=6
```

## 工作流程

1. **用户注册** → 设置个人信息和紧急联系人
2. **每日签到** → 用户主动签到或自动提醒
3. **状态监测** → 系统每6小时检查一次
4. **超时告警** → 超过24小时未签到触发告警
5. **通知联系人** → 自动通知所有紧急联系人
6. **持续跟进** → 直到用户签到或联系人确认

## 告警机制

### 第一阶段（12小时）
- 发送温馨提醒给用户
- "好久没见到你了，记得签到哦"

### 第二阶段（24小时）
- 通知第一紧急联系人
- "XXX已经24小时未签到，请确认安全"

### 第三阶段（48小时）
- 通知所有紧急联系人
- 标记为高危状态
- 建议联系人上门查看

## 隐私保护

- 所有数据加密存储
- 仅紧急情况下通知联系人
- 用户可随时删除数据
- 不会泄露用户位置信息

## 定价

- 基础服务：0.001 USDT/天
- 通过 SkillPay.me 自动结算
- 紧急联系人通知免费

## 安装运行

```bash
npm install
npm start
```

## 测试

```bash
npm test
```

## 许可证

MIT

---

**Sources:**
- [「死了麼」被評為「痛點99分、功能1分」，為什麼中國年輕人狂下載？](https://www.bnext.com.tw/article/89759/alive-check-app)
- ["死了么"App为何能火？一个产品经理的冷拆解](https://www.woshipm.com/share/6323812.html)
- [估值9000万？独家对话"死了么"APP创始人](https://m.36kr.com/p/3638430937910658)
