---
name: feishu-share-link
description: 飞书专属分享链接生成规范。当生成文档、多维表格、知识库等链接时，必须同时提供专属企业域名的链接和通用飞书根域名的链接，确保稳妥访问。支持多租户动态读取。
---

# 飞书专属分享链接生成规范 (Feishu Share Link)

## 📌 核心规则
在向用户发送飞书文件（文档、多维表格、知识库、电子表格等）的分享链接时，**必须同时发送两条链接**：
1. **专属链接**：使用当前企业/租户的专属域名前缀（例如 `https://czpn2fds56.feishu.cn`）。
2. **通用链接**：使用默认的飞书根域名（`https://feishu.cn`）作为备用，确保无论在何种客户端或网络环境下都能获得最稳妥的访问体验。

## 🔍 获取专属域名的方法
作为大模型，当你准备生成链接时，请执行以下步骤获取当前用户的专属域名：
1. 读取 `~/.openclaw/workspace/TOOLS.md`，查找是否有类似 `Feishu Custom Domain: xxx.feishu.cn` 的记录。
2. 如果没有，优先询问用户其飞书企业专属域名前缀是什么，或者提示用户将前缀写入 `TOOLS.md`。如果用户未提供，专属链接暂缺，仅发送通用链接。

## 🔗 各类型链接拼接格式
假设获取到的专属域名为 `{CUSTOM_DOMAIN}`（例如 `czpn2fds56.feishu.cn`），根域名为 `feishu.cn`。
回复用户时，请采用如下双链接排版格式：

### 1. 多维表格 (Bitable)
- 🏢 **专属链接**: `https://{CUSTOM_DOMAIN}/base/{APP_TOKEN}?from=from_copylink`
- 🌐 **通用链接**: `https://feishu.cn/base/{APP_TOKEN}?from=from_copylink`

### 2. 新版云文档 (Docx)
- 🏢 **专属链接**: `https://{CUSTOM_DOMAIN}/docx/{DOC_TOKEN}`
- 🌐 **通用链接**: `https://feishu.cn/docx/{DOC_TOKEN}`

### 3. 知识库 (Wiki)
- 🏢 **专属链接**: `https://{CUSTOM_DOMAIN}/wiki/{WIKI_TOKEN}`
- 🌐 **通用链接**: `https://feishu.cn/wiki/{WIKI_TOKEN}`

### 4. 电子表格 (Sheet)
- 🏢 **专属链接**: `https://{CUSTOM_DOMAIN}/sheets/{SPREADSHEET_TOKEN}`
- 🌐 **通用链接**: `https://feishu.cn/sheets/{SPREADSHEET_TOKEN}`
