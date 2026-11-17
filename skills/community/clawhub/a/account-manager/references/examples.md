# 示例 - account-manager

> 来源: SKILL.md v1.0 示例章节 + 输入/输出格式

## 示例1: 微信封号换号

### 场景
微信账号因频繁加人被封号,切换新号并继承好友档案和聊天记忆

### 输入
```json
{
  "action": "switch_account",
  "agent_id": "agent_002",
  "platform": "wechat",
  "old_account": "wx_001",
  "new_account": "wx_002",
  "phone_number": "138****0002",
  "banned_reason": "频繁加人",
  "banned_date": "2026-04-15T10:30:00Z"
}
```

### 输出
```json
{
  "success": true,
  "data": {
    "action": "switch_account",
    "agent_id": "agent_002",
    "platform": "wechat",
    "old_account": {
      "account_id": "wx_001",
      "status": "banned",
      "banned_reason": "频繁加人",
      "banned_date": "2026-04-15T10:30:00Z"
    },
    "new_account": {
      "account_id": "wx_002",
      "status": "active",
      "phone_number": "138****0002",
      "login_status": "success"
    },
    "inherited_data": {
      "friends_count": 150,
      "memory_count": 5000,
      "tags_count": 12
    },
    "notification_sent": {
      "high_value": 8,
      "normal": 0,
      "risk": 2
    },
    "switched_at": "2026-04-15T11:00:00Z"
  },
  "error": null,
  "code": null
}
```

## 示例2: 自动检测封号

### 场景
登录失败3次后自动触发封号预警,切换备用账号

### 输入
```json
{
  "action": "switch_account",
  "agent_id": "agent_003",
  "platform": "douyin",
  "old_account": "dy_001",
  "new_account": "dy_002",
  "phone_number": "139****0003",
  "banned_reason": "登录失败3次自动检测",
  "banned_date": "2026-04-15T14:00:00Z"
}
```

### 输出
```json
{
  "success": true,
  "data": {
    "action": "switch_account",
    "agent_id": "agent_003",
    "platform": "douyin",
    "old_account": {
      "account_id": "dy_001",
      "status": "banned",
      "banned_reason": "登录失败3次自动检测"
    },
    "new_account": {
      "account_id": "dy_002",
      "status": "active",
      "login_status": "success"
    },
    "inherited_data": {
      "friends_count": 80,
      "memory_count": 2000,
      "tags_count": 5
    },
    "notification_sent": {
      "high_value": 3,
      "normal": 0,
      "risk": 0
    },
    "switched_at": "2026-04-15T14:15:00Z"
  },
  "error": null,
  "code": null
}
```
