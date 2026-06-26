# Feishu Auto-Report Skill - 飞书自主汇报技能

---
name: Feishu Auto-Report - 飞书自主汇报
description: 专为多 Agent 协作设计。Agent 完成任务后自主调用本技能向用户汇报结果，显示独立机器人身份。零配置，Agent 启动时自动扫描使用，无需手动配置飞书凭证。
descriptionEn: Designed for multi-agent collaboration scenarios. After completing tasks, agents independently call this skill to report results to users with independent robot identity. Zero configuration, agents automatically scan and use it without manual Feishu credential configuration.
version: 5.0.0
author: pikaqiuyaya
license: MIT
tags:
  - feishu
  - auto-report
  - multi-agent
  - notification
  - zh-CN
  - 飞书
  - 自主汇报
  - 多 Agent
  - 零配置
language: zh-CN
---

# Feishu Auto-Report Skill - 飞书自主汇报技能

## 设计目标

在多 Agent 协作架构中，执行 Agent（Agent-B/C）完成任务后需要向用户汇报结果。本技能提供零配置的消息发送能力，让每个 Agent 以自己的身份独立发送通知，无需 Agent-A 转发。

## 技术实现

通过飞书开放平台的 Internal App 凭证获取 tenant_access_token，调用飞书消息 API 发送文本消息。支持 open_id（私聊）和 chat_id（群聊）两种接收者类型，确保消息精准触达。

## 配置依赖

技能自动从以下配置文件读取飞书凭证（无需手动配置）：
- `~/.openclaw/openclaw-{agentId}.json`

Agent 启动时会自动扫描该路径下的配置文件，读取 `channels.feishu.appId` 和 `channels.feishu.appSecret` 字段完成鉴权。

## API 调用流程

```bash
# 1. 获取租户级访问令牌
POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/
Headers: Content-Type: application/json
Body: {"app_id": "xxx", "app_secret": "xxx"}

# 2. 发送文本消息
POST https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={idType}
Headers: 
  Authorization: Bearer {tenant_access_token}
  Content-Type: application/json
Body: {
  "receive_id": "{targetId}",
  "msg_type": "text",
  "content": "{\"text\":\"{messageContent}\"}"
}
```

## 脚本参数

| 参数 | 说明 | 示例 |
|------|------|------|
| agentId | Agent 标识 | agent-b |
| targetId | 接收者 ID | ou_xxx 或 oc_xxx |
| idType | ID 类型 | open_id / chat_id |
| content | 消息内容 | 任务已完成 |

## 与 setup-multi-gateway 配合

1. Agent-A 接收用户指令
2. Agent-A 通过 sessions_send 派发任务
3. Agent-B/C 执行任务
4. Agent-B/C 自主调用本技能汇报
5. 用户收到对应 Agent 的通知

## 注意事项

- open_id 是应用隔离的，每个 Agent 使用自己的 open_id
- chat_id 是通用的，跨 Agent 共享
- content 必须是转义的 JSON 字符串
