---
name: dingtalk-notify
description: >
  通过钉钉工作通知发送消息给指定用户。统一的消息推送渠道。
  Use when: 需要发送钉钉工作通知、测试钉钉连通性、重试失败的钉钉消息、
  发送文件到钉钉、切换钉钉机器人模型。Triggers: "钉钉通知", "钉钉推送",
  "发送钉钉", "dingtalk notify", "钉钉连通性", "钉钉测试", "工作通知"。
---

# DingTalk Notify

统一钉钉工作通知推送。

## 发送文本通知

```bash
~/.openclaw/workspace/scripts/dingtalk-work-notify.sh '[消息内容]' '106648074224033227'
```

**userId**: `106648074224033227`（飞）

## 发送文件

```bash
# 增强版（支持多种文件类型）
~/.openclaw/workspace/scripts/dingtalk-send-file-enhanced.sh [文件路径] '106648074224033227'

# 简易版
~/.openclaw/workspace/scripts/dingtalk-send-file-simple.sh [文件路径] '106648074224033227'
```

## 连通性测试

```bash
~/.openclaw/workspace/scripts/dingtalk-work-notify.sh '🔔 连通性测试' '106648074224033227'
```

## 失败重试

```bash
# 自动重试未送达的消息
~/.openclaw/workspace/scripts/dingtalk-retry-send.sh
```

## 状态检查

```bash
# 检查钉钉服务状态
~/.openclaw/workspace/scripts/dingtalk-status.sh
```

## 认证方式

OAuth2 自动刷新，脚本自动处理 Token。

**记录保存**：所有发送记录保存在 `~/.openclaw/backups/notifications/send-record-YYYY-MM-DD.jsonl`
