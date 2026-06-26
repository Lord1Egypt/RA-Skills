# Healthchecks.io 配置指南

## 注册与创建 Check

1. 访问 https://healthchecks.io/ 注册免费账号
2. 创建新项目（如 "My Devices"）
3. 添加 Check：
   - Name: 设备名称（如 "Home MacBook"）
   - Period: 3 minutes（与心跳间隔匹配）
   - Grace: 5 minutes（宽限期，超过才告警）
4. 获取 Ping URL（格式：`https://hc-ping.com/UUID`）

## 安全注意事项

- Ping URL 等同于密码，不要在聊天/公开场合分享完整链接
- 聊天平台（飞书、Slack 等）会自动抓取消息中的 URL 做链接预览
- 只传递 UUID 部分，由脚本拼接完整 URL

## 获取 API Key（用于远程查询）

1. 进入项目 Settings → API Access
2. 创建 Read-Only API Key
3. 保存 key 用于 check.sh 查询

## 免费版限额

- 20 个 Checks
- 支持 Email / Webhook / Slack / Telegram 通知
- 日志保留 100 条

## 推荐配置

| 参数 | 推荐值 | 说明 |
|---|---|---|
| Period | 3 min | 心跳间隔 |
| Grace | 5 min | 宽限期 |
| Tags | device, mac | 方便分类 |

断网后最慢 **8 分钟**（Period + Grace）触发告警。
想更快可以缩短 Grace 到 2-3 分钟。

## 通知集成

### 邮件
默认已开启，无需配置。

### 飞书 Webhook
1. 在飞书群创建自定义机器人，获取 Webhook URL
2. 在 healthchecks.io → Integrations → Webhook
3. 配置 Down URL 和 Up URL 为飞书 Webhook
4. Request Body (Down):
```json
{"msg_type":"text","content":{"text":"⚠️ 设备离线：$NAME（最后心跳：$LAST_PING）"}}
```
5. Request Body (Up):
```json
{"msg_type":"text","content":{"text":"✅ 设备恢复：$NAME 已重新上线"}}
```

### 其他
healthchecks.io 还支持 Slack、Telegram、Discord、PagerDuty 等 20+ 集成。
