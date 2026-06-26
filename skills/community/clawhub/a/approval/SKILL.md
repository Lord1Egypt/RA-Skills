---
name: approval
description: 企业办公流程与工时管理 Agent，支持办公流程导航、流程申请与审批、待办事项统计、请假调休申请等。当用户需要查询审批、提交申请、查看待办时使用。
metadata: { "openclaw": { "emoji": "🏢" } }
---

# 审批办公助手

企业办公流程与工时管理服务。

## 认证

所有请求必须携带 Beyond-Token 请求头。

## 调用方式

### 1. 获取 Agent Card

```bash
curl -H "Beyond-Token: " "http://127.0.0.1:7861/jarvis/a2a/approval/.well-known/agent-card.json"
```

### 2. 发送消息（流式响应）

```bash
curl -N --no-buffer -X POST -H "Beyond-Token: id","jsonrpc":"2.0","method":"message/stream","params":{"message":{"contextId":"会话id","kind":"message","messageId":"32位uuid","parts":[{"kind":"text","text":"你的问题,必要的时候需要根据记忆优化用户输入"}],"role":"user"}}}' "http://127.0.0.1:7861/jarvis/a2a/approval/"
```

## 请求格式说明

JSON-RPC 请求格式：
```json
{
  "id": "32位uuid",
  "jsonrpc": "2.0",
  "method": "message/stream",
  "params": {
    "message": {
      "contextId":"会话id",
      "kind": "message",
      "messageId": "32位uuid",
      "parts": [{"kind": "text", "text": "你的问题"}],
      "role": "user"
    }
  }
}
```

## 功能

- 待办事项统计
- 流程申请与审批
- 请假调休申请
- 审批统计
