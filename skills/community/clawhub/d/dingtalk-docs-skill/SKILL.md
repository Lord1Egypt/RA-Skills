---
name: dingtalk-docs-skill
description: 当用户想要操作钉钉文档时使用本 Skill。支持：推送本地 markdown 到钉钉知识库、拉取云端文档到本地、覆盖/追加更新文档内容、块级精确编辑、搜索与列出知识库文档、下载文件与附件、导出文档为 PDF/Word、管理节点权限、创建/重命名/移动/复制/删除文档与文件夹、初始化钉钉文档 MCP 配置。当用户想操作飞书、语雀、Notion 等其他平台、只修改本地文件、管理钉钉 IM 消息或群组时，不要使用本 Skill。
license: MIT
compatibility: Requires dingtalk-doc MCP server (StreamableHttp transport). Compatible with any MCP-capable agent (Claude Code, Cursor, VS Code, Roo Code, Gemini CLI, Codex, etc.). Auto-detects Claude Code; falls back to writing config files or manual setup for other agents.
---

# 钉钉文档

通过钉钉文档官方 MCP Server 全面操作云端文档。

## 语言规则

**始终使用用户输入的语言进行回复。** 如果用户用英文提问，则全程用英文回复；如果用户用中文，则全程用中文回复。无法判断时默认使用中文。

## 能力范围

**读**
- 拉取云端文档正文为 markdown（保存到本地）
- 列出知识库/文件夹下的文档节点
- 按关键词搜索文档
- 获取文档元信息（标题、类型、创建时间等）
- 下载钉盘文件或文档内嵌附件

**写**
- 将本地 markdown 推送为钉钉文档（adoc 类型）
- 覆盖或追加内容到已有文档
- 按块精确编辑（插入/更新/删除段落、标题、表格等）
- 上传本地文件（PDF、图片、Word 等）到知识库

**管理**
- 创建文件夹
- 重命名/移动/复制/删除文档和文件夹
- 导出文档为 PDF 或 Word 格式
- 查看/添加/修改知识库节点的成员权限

**不负责：**
- 飞书、语雀、Notion 等其他平台
- 只修改本地文件（无云端操作）
- 钉钉 IM 消息、企业成员管理

## 前置条件

钉钉文档 MCP Server 必须已配置到当前 Agent 的 MCP 设置中，服务名称为 `dingtalk-doc`。

如果 MCP 工具不可用，先走**初始化流程**，再执行任何文档操作。

## 初始化流程（首次使用或 MCP 不可用时）

1. 告知用户访问帮助手册页面并完成开通：
   > 请打开以下链接，使用钉钉账号登录后，点击页面上的【开通服务】按钮：
   > https://aihub.dingtalk.com/#/detail?mcpId=9629&detailType=marketMcpDetail

2. 开通后复制页面右侧 **StreamableHttp URL**（不是 JSON Config）

3. 请用户将 URL 粘贴给你

4. 收到 URL 后，按以下顺序尝试注册 MCP 服务（`dingtalk-doc` 为服务名，必须为 ASCII）：

   **方案 A — Claude Code**（优先尝试，运行命令看是否成功）：
   ```bash
   claude mcp add --transport http --scope user dingtalk-doc "<用户提供的 URL>"
   ```
   成功则跳到步骤 5。

   **方案 B — 写入配置文件**（通用方案，大多数 Agent 均可用）：

   检测当前环境存在哪些配置文件，找到第一个匹配项写入：

   | Agent | 配置文件（全局） | 配置文件（项目级） | `mcpServers` 键名 |
   |-------|---------------|----------------|-----------------|
   | Cursor | `~/.cursor/mcp.json` | `.cursor/mcp.json` | `mcpServers` |
   | VS Code Copilot | `~/Library/Application Support/Code/User/mcp.json`（Mac）<br>`%APPDATA%\Code\User\mcp.json`（Win） | `.vscode/mcp.json` | `servers` |
   | Roo Code | — | `.roo/mcp.json` | `mcpServers` |
   | Gemini CLI | `~/.gemini/settings.json` | — | `mcpServers` |
   | OpenAI Codex | `~/.codex/config.json` | — | `mcpServers` |

   向目标文件追加（若文件已有 `mcpServers`/`servers`，只添加新条目，不覆盖原有内容）：

   ```json
   {
     "mcpServers": {
       "dingtalk-doc": {
         "type": "http",
         "url": "<用户提供的 URL>"
       }
     }
   }
   ```
   > VS Code Copilot 的 `.vscode/mcp.json` 使用 `"servers"` 而非 `"mcpServers"`，写入时注意区分。

   成功写入则跳到步骤 5。

   **方案 C — 手动兜底**（方案 A/B 均不适用时）：

   向用户展示以下信息，请其参照所用 Agent 的文档手动添加 MCP 服务，完成后回来继续：
   ```
   传输类型：StreamableHttp（HTTP）
   服务名称：dingtalk-doc
   URL：<用户提供的 URL>
   ```
   用户手动配置完成后，本 Skill 只需确认 MCP 工具可用即可继续。

   > URL 中含有个人 API Key，写入配置后不要在回复中重复显示完整 URL。

5. 询问用户的默认知识库地址：
   > 请在浏览器中打开你常用的钉钉知识库，把地址栏的 URL 粘贴给我（格式类似 `https://alidocs.dingtalk.com/i/spaces/xxxxx/overview`）。
   > 如果暂时不设默认知识库，可以跳过，后续每次操作时再指定。

6. 收到知识库 URL 后，写入 `references/dingtalk.config`：
   ```
   DINGTALK_DEFAULT_WORKSPACE_URL=<用户提供的知识库 URL>
   ```
   此文件已被 `.gitignore` 排除，不会进入版本控制。无需重启，下次操作时直接读取生效。

7. MCP 配置写入后，提示用户重启 Agent 客户端以使 MCP 生效，重启后回来继续操作即可。

### 使用默认知识库

- 当用户说"列出我的知识库文档"、"推送到知识库"等未指明位置的操作时，优先使用默认知识库 URL
- **读取顺序**：① 读取 `references/dingtalk.config` 中的 `DINGTALK_DEFAULT_WORKSPACE_URL`；② 若文件不存在或值为空，检查环境变量 `$DINGTALK_DEFAULT_WORKSPACE_URL`（兼容已有 Claude Code 配置）；③ 两者均无则询问用户
- 获得 URL 后，调用 `get_document_info` 传入该 URL 解析出 nodeId，再用 nodeId 调用 `list_nodes` 或作为 `parentNodeId`

### 更改默认知识库

当用户说"更换默认知识库"、"修改知识库地址"等时：

1. 请用户在浏览器打开目标钉钉知识库，复制地址栏 URL
2. 收到新 URL 后，覆盖写入 `references/dingtalk.config`：
   ```
   DINGTALK_DEFAULT_WORKSPACE_URL=<新的知识库 URL>
   ```
3. 无需重启，下次操作时读取新值即生效

### 安全规则

- MCP 服务 URL 含有个人 API Key，**不得出现在任何版本控制文件中**；写入配置后不要在回复中重复显示完整 URL
- `references/dingtalk.config` 保存知识库 URL，已被 `.gitignore` 排除，不会提交到版本控制
- 如果用户将 URL 粘贴到聊天中，立即写入配置后不再引用

## 默认路径

1. 确认 MCP 工具可用（若不可用，进入初始化流程）
2. 理解用户意图，映射到对应 MCP 工具（见工具映射表）
3. 如需要 dentryUuid/nodeId 但用户未提供：优先读取 `references/dingtalk.config`（或环境变量 `$DINGTALK_DEFAULT_WORKSPACE_URL`）获取默认知识库 URL，调用 `get_document_info` 解析出 nodeId；否则调用 `search_documents` 或 `list_nodes` 定位目标，让用户确认后再操作
4. **执行前确认**（只读操作除外，见下方说明）：向用户展示操作摘要，收到明确同意后再调用 MCP 工具
5. 执行操作
6. 报告结果：操作类型、文档标题、文档链接（如有）

### 执行前确认规则

**需要确认的操作**（所有会写入或修改云端数据的操作）：
`create_document`、`update_document`、`create_folder`、`create_file`、`delete_document`、`rename_document`、`move_document`、`copy_document`、`insert_document_block`、`update_document_block`、`delete_document_block`、文件上传（`get_file_upload_info` + `commit_uploaded_file`）、`submit_export_job`、`add_permission`、`update_permission`

**无需确认的操作**（只读）：
`search_documents`、`list_nodes`、`get_document_info`、`get_document_content`、`list_document_blocks`、`list_permission`、`query_export_job`、`download_file`、`download_doc_attachment`

**确认摘要格式**（根据操作类型调整）：

```
即将执行以下操作，请确认：

操作：<创建 / 更新（覆盖）/ 更新（追加）/ 删除 / 重命名 / 移动 / 复制 / 创建文件夹>
目标：<文档标题或文件夹名>
位置：<知识库名或文件夹路径>
说明：<一句话描述本次变更，例如"将以本地文件 xxx.md 的内容覆盖云端文档全文">

确认请回复「是」或「确认」，取消请回复「否」或「取消」。
```

收到取消时：停止操作，不重试，告知用户已取消。

## MCP 工具映射

详见 `references/mcp-tools.md`。常用映射如下：

| 用户意图 | MCP 工具 |
|---------|---------|
| 推送/创建文档（含 markdown 内容） | `create_document` |
| 拉取云端文档内容到本地 | `get_document_content` |
| 覆盖或追加文档内容 | `update_document` |
| 精确块级编辑（段落/标题/表格等） | `list_document_blocks` → `insert/update/delete_document_block` |
| 列出知识库/文件夹下的文档 | `list_nodes` |
| 按关键词搜索文档 | `search_documents` |
| 获取文档元信息（标题、类型等） | `get_document_info` |
| 下载钉盘文件 | `download_file` |
| 下载文档内嵌附件 | `download_doc_attachment` |
| 导出文档为 PDF/Word | `submit_export_job` → `query_export_job`（轮询至完成）|
| 创建文件夹 | `create_folder` |
| 删除文档节点 | `delete_document` |
| 重命名节点 | `rename_document` |
| 移动节点到其他文件夹 | `move_document` |
| 复制节点到其他文件夹 | `copy_document` |
| 查看节点成员权限 | `list_permission` |
| 添加/修改节点成员权限 | `add_permission` / `update_permission` |

## 失败处理

- **MCP 工具不可用**：停止，进入初始化流程，不要猜测或尝试其他方式调用
- **未提供目标文档**：先用 `search_documents` 或 `list_nodes` 找到目标，让用户确认后再操作
- **update_document 报错**：确认目标是否为 adoc（文字类型）文档，非 adoc 文档不支持此操作
- **delete_document 前**：确认摘要中必须注明"将移入回收站，30 天内可恢复"，收到确认后再执行
- **API 报错（权限/鉴权类）**：当 API 返回权限不足、无权限、鉴权失败、Forbidden、Unauthorized 等错误时，除了展示原文错误信息外，提示用户可能尚未开通所在组织的钉钉开发者权限，引导用户参考以下链接完成开通：
  > 请访问钉钉开发者入门文档，确认你已在所在组织中开通了开发者权限：
  > https://open.dingtalk.com/document/dingstart/dingtalk-developer
  >
  > 开通步骤简述：登录钉钉开放平台 → 选择对应组织 → 完成开发者认证/开通。完成后重新尝试操作。
- **其他 API 报错**：原文展示错误信息，不猜测原因，不自动重试

## 关键约束

- `update_document` 和 `create_document` 仅支持 **adoc（文字类型）** 文档，不支持表格、演示、脑图等
- `create_document` 和 `update_document` 的 `markdown` 参数上限均为 **10,000 字符**；超出会报 `invalidRequest.inputArgs.invalid` 错误。推送前应先估算内容字符数，超过 **9,500 字符**（留余量）时走大文档推送策略（见下文）
- `delete_document` 是移入回收站，不是永久删除，30 天内可从回收站恢复
- `list_nodes` 只返回直接子节点，不递归。需要深层列表时需要多次调用
- **导出为异步操作**：`submit_export_job` 返回 jobId 后需轮询 `query_export_job` 直到状态完成，再将下载链接告知用户；轮询间隔建议 1-2 秒
- **Mermaid 文本绘图**：通过 `create_document` 推送的 ` ```mermaid ` 代码块会被解析为普通代码块，而非钉钉原生文本绘图块。钉钉的文本绘图是私有块类型，API 层未暴露，无法通过 MCP 创建或转换。推送前告知用户此限制，建议推送后在钉钉编辑器中手动将代码块转换为文本绘图
- 操作完成后，从返回值中提取文档链接告知用户，方便直接点击查看

## 对话中上传文件的处理

用户可能在对话中直接上传 markdown 文件并要求推送到钉钉。

### 已知限制

- 对话上传的文件内容是**临时的**，不会持久保存到磁盘，上下文压缩或会话结束后内容即丢失
- **非 ASCII 文件（如中文 markdown）通过对话上传时，0x80-0x9F 范围的字节会被文本处理层丢弃，导致不可逆乱码**。这是客户端文本传输的固有限制，编码修复无法还原丢失的字节

### 处理规则

1. **优先使用本地文件路径**：当用户要推送含非 ASCII 内容（中文、日文等）的文件时，请用户提供本地磁盘路径，直接读取文件内容，避免编码问题
2. **对话上传的文件先检查编码**：如果用户直接在对话中上传了文件，先检查内容是否出现乱码。如果存在乱码，立即告知用户并请其提供本地文件路径
3. **纯 ASCII 内容可直接处理**：如果上传的文件内容全是 ASCII（英文、代码等），可以直接处理，在同一轮回复中完成：读取内容 -> 确认摘要 -> （用户确认后）调用 `create_document`
4. **文档命名**：默认使用上传文件名（去掉扩展名）作为钉钉文档标题。如果用户要求修改名字，按用户指定的名字创建
5. **仅支持 markdown / 纯文本**：对话上传的二进制文件（PDF、图片、Word 等）当前不支持直接推送，需要用户提供本地磁盘路径后走文件上传三步流程

## 大文档推送策略

当需要将本地 markdown 文件推送为钉钉在线文档（adoc）时，**推送前先估算内容字符数**。超过 **9,500 字符** 时，单次 `create_document` 必然失败，需主动告知用户并让其选择方案：

### 方案 A — 分段推送（生成可在线编辑的 adoc）

1. 按 `## ` / `### ` 标题边界将内容切分为若干段，每段 ≤ 9,500 字符，避免在表格中间切断
2. 用 `create_document` 写入第 1 段（含标题）
3. 依次用 `update_document`（`append` 模式）追加后续各段，每段单独一次调用
4. 全部追加完成后报告文档链接

**适合场景**：用户需要在钉钉在线编辑、评论、协作，或希望文档格式被渲染

### 方案 B — 上传原始 .md 文件（存入钉盘）

走三步文件上传流程：`get_file_upload_info` → HTTP PUT → `commit_uploaded_file`

**适合场景**：只需存档或分享下载，不需要在线编辑；操作更简单，文件完整保留原格式

### 推荐选择

向用户说明两个方案后，推荐如下：

> 如果你需要在钉钉里直接编辑或与同事协作，推荐方案 A（分段推送）；如果只是存档或分享，推荐方案 B（上传文件）。

收到用户选择后再执行，不要擅自决定。

---

## 资源导航

- `references/mcp-tools.md` — 全部 MCP 工具详细说明，按场景分组
