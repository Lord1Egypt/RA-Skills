# 用户 ID 映射表模板

> 复制此文件，填入你的实际 ID

## 群聊信息

| 项目 | 值 |
|------|-----|
| 群聊 ID | `oc_xxx` |

## Bot 配置

| Bot 名称 | accountId | appId |
|----------|-----------|-------|
| 主Bot | `default` | `cli_xxx` |
| 码农Bot | `coder` | `cli_xxx` |
| 审核Bot | `reviewer` | `cli_xxx` |

## 用户 ID 映射

### 用户A

| Bot | accountId | open_id |
|-----|-----------|---------|
| 主Bot | `default` | `ou_xxx` |
| 码农Bot | `coder` | `ou_xxx` |
| 审核Bot | `reviewer` | `ou_xxx` |

### 用户B

| Bot | accountId | open_id |
|-----|-----------|---------|
| 主Bot | `default` | `ou_xxx` |
| 码农Bot | `coder` | `ou_xxx` |
| 审核Bot | `reviewer` | `ou_xxx` |

---

## 如何获取 open_id

### 方法1：用户发送消息时获取

当用户给 Bot 发消息时，从消息事件中获取：

```json
{
  "sender": {
    "sender_id": {
      "open_id": "ou_xxx"  // 这就是用户的 open_id
    }
  }
}
```

### 方法2：通过飞书 API 获取

调用飞书 API 获取用户信息。

---

## 使用示例

### 码农Bot 给用户A发私聊

```bash
# 1. 查表：码农Bot 看到用户A的 open_id
# 2. 发送

message action=send \
  channel=feishu \
  accountId="coder" \
  target="ou_码农Bot看到的用户A的open_id" \
  message="消息内容"
```

### 主Bot 在群聊 @用户A

```bash
# 1. 查表：主Bot 看到用户A的 open_id
# 2. 发送

message action=send \
  channel=feishu \
  accountId="default" \
  target="oc_群聊ID" \
  message="<at user_id=\"ou_主Bot看到的用户A的open_id\">用户A</at> 消息内容"
```
