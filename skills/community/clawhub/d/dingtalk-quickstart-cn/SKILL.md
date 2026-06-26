---
name: dingtalk-quickstart-cn
version: 1.0.0
description: |
  钉钉快速集成配置 - 5分钟连接 OpenClaw 与钉钉，解锁机器人消息、审批流程、智能办公。适合：企业用户、钉钉生态、国内企业。
metadata:
  openclaw:
    emoji: "钉"
    version: 1.0.0
    requires:
      bins: ["curl"]
---

# 钉钉快速集成配置

**目标**：5 分钟内完成 OpenClaw + 钉钉集成，开始自动化办公。

---

## 🚀 快速开始（3 步）

### 第一步：创建钉钉机器人

1. 打开钉钉群 → 群设置 → 智能群助手 → 添加机器人
2. 选择「自定义」机器人
3. 填写信息：
   - **机器人名称**：OpenClaw Assistant
   - **机器人头像**：自定义或默认
4. 安全设置（三选一）：
   - **推荐**：加签（Secret）— 最安全
   - IP 地址（白名单）
   - 自定义关键词
5. 创建后记录：
   - `Webhook URL`
   - `Secret`（如果选择了加签）

### 第二步：配置 OpenClaw

在 OpenClaw 配置文件 `~/.openclaw/config.yml` 添加：

```yaml
channels:
  dingtalk:
    enabled: true
    webhook: "https://oapi.dingtalk.com/robot/send?access_token=xxx"
    secret: "SECxxx"  # 可选，加签时需要
```

然后重启 OpenClaw：
```bash
openclaw gateway restart
```

### 第三步：测试发送

在 OpenClaw 对话中测试：

```
发送钉钉消息：测试成功，OpenClaw 已连接！
```

如果钉钉群收到消息，集成完成！

---

## 📋 常见使用场景

### 场景 1：自动发送每日简报

**指令**：
```
每天 8:00 发送钉钉消息：今日待办事项：[事项列表]
```

**OpenClaw 会自动**：
1. 读取待办事项
2. 生成简报
3. 定时发送到钉钉群

### 场景 2：监控告警通知

**指令**：
```
当服务器 CPU > 80% 时，发送钉钉告警消息
```

**OpenClaw 会自动**：
1. 监控服务器指标
2. 触发阈值时发送钉钉消息
3. 包含详细告警信息

### 场景 3：审批流程自动化

**指令**：
```
读取钉钉审批单 [单号]，自动处理并回复结果
```

**OpenClaw 会自动**：
1. 调用钉钉审批 API
2. 分析审批内容
3. 执行相应操作

---

## 🔧 高级配置

### 多机器人支持

如果需要管理多个钉钉群：

```yaml
channels:
  dingtalk:
    enabled: true
    bots:
      - name: "开发群"
        webhook: "https://oapi.dingtalk.com/robot/send?access_token=xxx1"
        secret: "SECxxx1"
      - name: "运维群"
        webhook: "https://oapi.dingtalk.com/robot/send?access_token=xxx2"
        secret: "SECxxx2"
```

### 消息模板配置

创建自定义消息模板：

```yaml
channels:
  dingtalk:
    templates:
      alert: |
        ### 🚨 告警通知
        **类型**：{type}
        **级别**：{level}
        **详情**：{detail}
        **时间**：{timestamp}
      daily: |
        ### 📅 每日简报
        **日期**：{date}
        **待办**：{todos}
        **提醒**：{reminders}
```

---

## 🐛 故障排查

### 问题 1：消息发送失败

**错误**：`invalid webhook url`

**解决**：
1. 检查 Webhook URL 格式
2. 确认机器人未被删除
3. 测试 URL 可达性：
   ```bash
   curl -X POST "YOUR_WEBHOOK_URL" \
     -H "Content-Type: application/json" \
     -d '{"msgtype":"text","text":{"content":"测试"}}'
   ```

### 问题 2：签名验证失败

**错误**：`sign not match`

**解决**：
1. 确认使用加签方式
2. 检查 Secret 是否正确
3. 确认时间戳在 1 小时内

### 问题 3：IP 白名单限制

**错误**：`ip not in whitelist`

**解决**：
1. 检查机器人 IP 白名单设置
2. 添加 OpenClaw 服务器 IP
3. 或改用加签方式（无需 IP 白名单）

---

## 📚 钉钉 API 参考

### 消息类型

**文本消息**：
```json
{
  "msgtype": "text",
  "text": {
    "content": "这是一条文本消息"
  }
}
```

**Markdown 消息**：
```json
{
  "msgtype": "markdown",
  "markdown": {
    "title": "Markdown 标题",
    "text": "### 标题\n**粗体**\n- 列表项"
  }
}
```

**链接消息**：
```json
{
  "msgtype": "link",
  "link": {
    "title": "链接标题",
    "text": "链接描述",
    "messageUrl": "https://example.com",
    "picUrl": "https://example.com/icon.png"
  }
}
```

---

## 💰 定价参考

- **基础集成**：¥99（机器人创建 + 消息发送）
- **企业定制**：¥299（多机器人 + 模板 + 定时任务）
- **全托管服务**：¥999/月（OpenClaw 托管 + 钉钉集成 + 技术支持）

---

## 🆘 获取帮助

- **钉钉开发文档**：https://open.dingtalk.com/document
- **OpenClaw 文档**：https://docs.openclaw.ai
- **OpenClaw 社区**：https://discord.com/invite/clawd

---

**创建时间**：2026-03-21
**作者**：OpenClaw 中文生态
**版本**：1.0.0