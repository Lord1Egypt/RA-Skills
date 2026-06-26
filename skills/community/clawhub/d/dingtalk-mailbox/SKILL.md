---
name: dingtalk-mailbox
description: 钉钉邮箱访问skill，使用mcporter调用钉钉邮箱MCP服务。支持查询可用邮箱列表、搜索邮件（类KQL表达式）、获取邮件详情、发送邮件。适用于需要通过AI助手管理钉钉邮箱的场景，如查询邮件、自动回复、邮件归档等。
version: 1.0.0
author: Claude Code
tags:
  - email
  - dingtalk
  - mcp
  - mail
  - mailbox
---

# 钉钉邮箱 Skill

通过 mcporter 调用钉钉邮箱 MCP 服务，实现邮箱查询、邮件搜索、邮件查看和发送功能。

## 前置要求

1. **安装 mcporter**
   ```bash
   npm install -g mcporter
   ```

2. **钉钉企业邮箱账号**

## 配置步骤

### 1. 获取钉钉邮箱 MCP Token

1. 登录钉钉企业邮箱网页版
2. 进入 **设置** → **MCP服务**
3. 点击 **生成Token**
4. 复制生成的 **JSON配置** 中的 `url` 字段值（StreamableHttp URL）

### 2. 添加 mcporter 配置

使用以下命令添加钉钉邮箱的 MCP Server：

```bash
mcporter config add dingtalk-mailbox --url "<StreamableHttp URL>" --config ~/.mcporter/mcporter.json
```

将 `<StreamableHttp URL>` 替换为从钉钉邮箱获取的实际 URL。

### 3. 验证配置

```bash
mcporter list
```

应该能看到 `dingtalk-mailbox` 服务器及其提供的工具列表。

## 可用功能

### 1. 查询可用邮箱列表 (list_user_mailboxes)

查询当前钉钉用户可以使用的邮箱地址列表。

**参数：** 无

**示例：**
```bash
mcporter call dingtalk-mailbox.list_user_mailboxes
```

**返回示例：**
```json
{
  "emailAccounts": [
    {
      "orgName": "示例公司",
      "type": "ORG",
      "email": "user@example.com"
    }
  ],
  "success": "true"
}
```

### 2. 搜索邮件 (search_emails)

使用类似 KQL 的查询表达式搜索邮件。支持分页、排序和字段选择。

**参数：**
- `email` (string, 必需): 搜索目标邮箱地址
- `query` (string, 必需): KQL 查询表达式
- `size` (string, 必需): 每次返回的最大结果数量（1-100）
- `cursor` (string, 可选): 分页游标

**示例：**
```bash
# 搜索收件箱邮件
mcporter call "dingtalk-mailbox.search_emails(email:\"user@example.com\", query:\"folderId:2\", size:\"5\")"

# 搜索未读邮件
mcporter call "dingtalk-mailbox.search_emails(email:\"user@example.com\", query:\"isRead:false\", size:\"10\")"

# 搜索来自特定发件人的邮件
mcporter call "dingtalk-mailbox.search_emails(email:\"user@example.com\", query:\"from:sender@example.com\", size:\"5\")"
```

**支持的查询字段：**
| 字段 | 说明 | 示例 |
|------|------|------|
| `date` | 日期 | `date>2025-01-01T00:00:00Z` |
| `folderId` | 文件夹ID | `folderId:2` (收件箱), `folderId:1` (已发送) |
| `isRead` | 是否已读 | `isRead:true`, `isRead:false` |
| `hasAttachments` | 是否有附件 | `hasAttachments:true` |
| `subject` | 主题 | `subject:\"紧急\"` |
| `from` | 发件人 | `from:\"alice\"` |
| `to` | 收件人 | `to:\"bob@example.com\"` |

**文件夹ID对照：**
- `1` - 已发送
- `2` - 收件箱
- `3` - 垃圾邮件
- `5` - 草稿
- `6` - 已删除

### 3. 获取邮件详情 (get_email_by_message_id)

根据邮件ID获取完整的邮件内容，包括正文。

**参数：**
- `email` (string, 必需): 邮件所属的邮箱地址
- `messageId` (string, 必需): 邮件ID（通过搜索获得）

**示例：**
```bash
mcporter call "dingtalk-mailbox.get_email_by_message_id(email:\"user@example.com\", messageId:\"<邮件ID>\")"
```

### 4. 发送邮件 (send_email)

使用指定的邮箱地址作为发件人发送邮件。

**参数：**
- `from` (string, 必需): 发信邮箱地址
- `toRecipients` (string[], 必需): 收件人邮箱地址列表
- `subject` (string, 必需): 邮件主题
- `body` (string, 必需): Markdown 格式的邮件正文
- `ccRecipients` (string[], 可选): 抄送人邮箱地址列表

**示例：**
```bash
# 发送简单邮件
mcporter call "dingtalk-mailbox.send_email(from:\"user@example.com\", toRecipients:[\"to@example.com\"], subject:\"会议通知\", body:\"明天下午开会\")"

# 发送带抄送的邮件
mcporter call "dingtalk-mailbox.send_email(from:\"user@example.com\", toRecipients:[\"to@example.com\"], ccRecipients:[\"cc@example.com\"], subject:\"会议通知\", body:\"## 会议通知\n\n明天下午2点在301会议室开会。\")"
```

## 常见使用场景

### 1. 查看今天的邮件
```bash
mcporter call "dingtalk-mailbox.search_emails(email:\"user@example.com\", query:\"date>2025-03-27T00:00:00Z AND folderId:2\", size:\"20\")"
```

### 2. 查找未读邮件
```bash
mcporter call "dingtalk-mailbox.search_emails(email:\"user@example.com\", query:\"isRead:false AND folderId:2\", size:\"10\")"
```

### 3. 查找特定主题的邮件
```bash
mcporter call "dingtalk-mailbox.search_emails(email:\"user@example.com\", query:\\\"subject:\\\"项目通知\\\"\\\", size:\\\"10\\\")"
```

### 4. 批量发送邮件
```bash
mcporter call "dingtalk-mailbox.send_email(from:\"user@example.com\", toRecipients:[\"a@example.com\", \"b@example.com\"], subject:\"通知\", body:\"各位同事：\n\n请注意查收附件。\n\n谢谢！\")"
```

## 常见问题

### 无法连接到 MCP 服务器

请确认：
1. Token 是否有效
2. URL 是否正确复制
3. 网络连接是否正常

### 查看完整工具 schema

```bash
mcporter list dingtalk-mailbox --schema
```

## 测试结果

| 功能 | 状态 | 说明 |
|------|------|------|
| list_user_mailboxes | ✅ 已测试 | 成功获取邮箱列表 |
| search_emails | ✅ 已测试 | 成功搜索收件箱邮件 |
| get_email_by_message_id | ✅ 已测试 | 成功获取邮件详情 |
| send_email | ✅ 已测试 | 成功发送测试邮件 |

## 参考资料

- [钉钉邮箱 MCP 服务说明](https://help.aliyun.com/document_detail/2925708.html)
- [Agent Skills 规范](https://agentskills.io/specification)
- [mcporter 文档](https://mcpmarket.com/zh/tools/skills/mcporter)

## License

MIT
