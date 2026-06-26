# 企业微信 API 研究笔记

**研究时间**: 2026-03-29 18:30  
**来源**: 企业微信开发者中心

---

## 🔑 核心 API

### 1. 消息推送 (Webhook)

**URL 格式**:
```
https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=KEY
```

**请求示例**:
```bash
curl -X POST "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "msgtype": "text",
    "text": {
      "content": "你好，这是测试消息"
    }
  }'
```

**消息类型**:
- `text` - 文本消息
- `markdown` - Markdown 消息
- `news` - 图文消息
- `file` - 文件消息

---

### 2. 接收消息 (Webhook)

**配置流程**:
1. 企业微信管理后台 → 应用管理 → 机器人
2. 创建机器人，获取 Webhook URL
3. 配置接收消息服务器

**接收格式**:
```json
{
  "msgtype": "text",
  "text": {
    "content": "收到消息内容"
  },
  "fromuser": "用户 ID",
  "time": 1234567890
}
```

---

### 3. 群聊管理

**创建群聊**:
```bash
curl -X POST "https://qyapi.weixin.qq.com/cgi-bin/appchat/create?access_token=ACCESS_TOKEN" \
  -d '{
    "name": "群名称",
    "owner": "创建者 ID",
    "userids": ["成员 1", "成员 2"]
  }'
```

---

## 🔐 认证方式

### Access Token 获取
```bash
curl "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=CORPID&corpsecret=CORPSECRET"
```

**有效期**: 2 小时  
**建议**: 缓存 Token，避免频繁请求

---

## 📋 开发准备

### 必需信息
- [ ] 企业 ID (corpid)
- [ ] 应用 Secret (corpsecret)
- [ ] 机器人 Webhook Key
- [ ] Agent ID (应用 ID)

### 注册流程
1. 访问 https://work.weixin.qq.com
2. 注册企业微信账号
3. 创建企业
4. 创建自建应用
5. 获取认证信息

---

## 💡 MVP 实现方案

### 阶段 1: 消息发送 (v0.1)
```bash
# 简单 curl 命令封装
send_message() {
  local key="$1"
  local content="$2"
  curl -X POST "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$key" \
    -H "Content-Type: application/json" \
    -d "{\"msgtype\":\"text\",\"text\":{\"content\":\"$content\"}}"
}
```

### 阶段 2: 自动回复 (v0.2)
```bash
# 监听 Webhook + 条件回复
# 需要服务器接收 POST 请求
```

### 阶段 3: 群管理 (v0.3)
```bash
# 需要完整 API 认证
# 使用 Access Token
```

---

## ⚠️ 注意事项

1. **频率限制**: 每个机器人每分钟最多 20 条消息
2. **内容审核**: 消息内容需符合规范
3. **Token 安全**: 不要泄露 Secret
4. **错误处理**: 检查 API 返回码

---

## 📚 参考文档

- 企业微信开发者中心：https://developer.work.weixin.qq.com
- 机器人 API: https://developer.work.weixin.qq.com/document/path/91770
- 消息推送：https://developer.work.weixin.qq.com/document/path/90236

---

**状态**: 研究完成，准备注册账号  
**下一步**: 企业微信开发者账号注册
