# Agent 飞书文档操作详解

## 前置条件

### 1. 飞书机器人配置

在 `~/.openclaw/openclaw.json` 的 `channels.feishu.accounts` 中配置：

```json
"channels": {
  "feishu": {
    "accounts": {
      "{agent名}": { "appId": "cli_xxx", "appSecret": "..." }
    }
  }
}
```

### 2. 开启跨 Agent 通信

在 `tools` 部分添加：

```json
"tools": {
  "sessions": {
    "visibility": "all"
  }
}
```

重启生效：`openclaw gateway restart`

---

## 读取飞书文档

### 方法一：通过文档链接（推荐）
让 agent 直接访问文档链接：
```
请查看这个飞书文档：https://feishu.cn/docx/xxxxx
```
Agent 使用 `web_fetch` 工具读取。

### 方法二：通过文档 ID
提供文档 ID，让 agent 调用飞书 API：

```bash
GET /drive/v1/documents/{document_id}
GET /drive/v1/documents/{document_id}/nodes
```

---

## 创建并编辑文档

### Step 1: 创建文档
```bash
POST /drive/v1/documents
Body: { "title": "文档标题" }
```

### Step 2: 添加内容块
```bash
POST /drive/v1/documents/{document_id}/blocks/{block_id}/children
Body: {
  "children": [
    {
      "block_type": 2,  // 2=text, 3=h1, 4=h2
      "text": {
        "elements": [{
          "text_run": { "content": "内容" }
        }]
      }
    }
  ]
}
```

**Block Type 参考：**
- `2` = 普通文本
- `3` = 一级标题
- `4` = 二级标题
- `5` = 三级标题
- `7` = bullet list（⚠️ 可能报 invalid param，可用文本模拟）

### Step 3: 设置公开权限
```bash
PATCH /drive/v1/permissions/{doc_id}/public?type=docx
Body: {
  "link_share_entity": "anyone_editable",
  "external_access_entity": "anyone_can_edit",
  "security_entity": "anyone_can_edit",
  "comment_entity": "anyone_can_edit",
  "share_entity": "anyone"
}
```

---

## 权限问题汇总

### 问题1：文档在机器人租户下，他人无法访问
**解决**：创建后立即设置公开权限

### 问题2：Agent 无法读取/写入某个文档
**可能原因**：
1. Agent 的飞书应用没有被添加到文档协作者
2. 文档没有设置公开权限
3. Agent 没有该文档所在云空间的管理权限

**解决**：
1. 在飞书中手动将 Agent 的 app 添加为文档协作者
2. 或者将文档所在文件夹设为"共享"

### 问题3：跨 Agent 通信被拒绝
**错误**：`tools.sessions.visibility=all needs to be enabled`
**解决**：在 openclaw.json 中添加 `tools.sessions.visibility: all`，然后重启

---

## 示例工作流

1. **Jimmy** → 让 taizi 创建文档："帮我生成今天的报告到飞书文档"
2. **taizi** → 调用 `POST /drive/v1/documents` 创建文档
3. **taizi** → 调用 block API 写入内容
4. **taizi** → 调用 `PATCH .../public` 设置公开编辑权限
5. **taizi** → 发送文档链接给 Jimmy
6. **Jimmy** → 分享链接给 gezi 或其他 agent
7. **gezi** → 通过链接或 API 读取并编辑文档

---

## 获取 Tenant Access Token

```bash
curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d '{"app_id": "cli_xxx", "app_secret": "xxx"}'
```

返回：`{"tenant_access_token": "xxx", "expire": 7200}`

Token 有效期 2 小时，调用 API 时：
```bash
-H "Authorization: Bearer {tenant_access_token}"
```
