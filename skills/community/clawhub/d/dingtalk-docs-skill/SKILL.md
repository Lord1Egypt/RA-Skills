---
name: dingtalk-docs-skill
description: 当用户想要操作钉钉文档或向钉钉知识库推送本地文件时使用本 Skill。支持：将 Markdown/纯文本推送为可编辑钉钉文档、原格式上传 HTML/图片/PDF/Office 等文件、拉取云端文档到本地、覆盖/追加更新文档内容、块级精确编辑、搜索与列出知识库文档、下载文件与附件、导出文档为 PDF/Word、管理节点权限、创建/重命名/移动/复制/删除文档与文件夹、初始化钉钉文档 MCP 配置。当用户想操作飞书、语雀、Notion 等其他平台、只修改本地文件、管理钉钉 IM 消息或群组时，不要使用本 Skill。
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
- 按内容类型将本地内容推送到知识库：创建可编辑的 adoc 文档，或保留原格式上传文件
- 覆盖或追加内容到已有文档
- 按块精确编辑（插入/更新/删除段落、标题、表格等）
- 上传本地文件（PDF、图片、Word 等）到知识库
- 将本地图片**内联**嵌入文档正文（自动上传转存为内联图，非占位符人工粘贴）

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

4. 收到 URL 后，**先做两项安全校验，再注册**：

   **① URL 域名白名单**：只接受钉钉官方域名——`aihub.dingtalk.com`、`alidocs.dingtalk.com` 及其它 `*.dingtalk.com` 子域。若 URL 域名不在白名单内，**停止注册**并提示用户「该 URL 非钉钉官方域名，可能填错或有风险，请核对」，用户确认后再继续。此举防止把 MCP 流量（含个人 API Key）导向恶意/错误 endpoint。

   **② 写前确认（不静默改用户环境）**：写任何配置文件前，先向用户展示**目标文件完整路径 + 将写入的确切 JSON 内容**，用户显式同意后再写；只追加 `dingtalk-doc` 新条目，绝不覆盖或改动文件里已有的其它配置。

   两项校验通过后，按以下顺序尝试注册 MCP 服务（`dingtalk-doc` 为服务名，必须为 ASCII）：

   **方案 A — Claude Code**（优先尝试；默认项目级 scope，运行前把命令展示给用户）：
   ```bash
   claude mcp add --transport http --scope local dingtalk-doc "<用户提供的 URL>"
   ```
   - `--scope local`：仅当前项目生效（项目级，影响面最小）。用户明确希望所有项目通用时，才改 `--scope user`（全局），改前先确认。
   - 成功则跳到步骤 5。

   **方案 B — 写入配置文件**（通用方案，大多数 Agent 均可用）：

   **优先项目级、全局需确认**：优先写 workspace 内的**项目级**配置（影响面最小、随项目走、不碰用户全局环境）；仅当该 Agent 没有项目级配置项（如 Gemini CLI、OpenAI Codex 只有全局），或用户明确同意写全局时，才写**全局用户级**配置，且写前必须按步骤 4 ② 展示路径 + 内容确认。

   检测当前环境存在哪些配置文件，找到第一个匹配项写入：

   | Agent | 配置文件（项目级，优先写这个） | 配置文件（全局，仅无项目级或用户确认后写） | `mcpServers` 键名 |
   |-------|----------------|----------------|-----------------|
   | Cursor | `.cursor/mcp.json` | `~/.cursor/mcp.json`（写前确认） | `mcpServers` |
   | VS Code Copilot | `.vscode/mcp.json` | `~/Library/Application Support/Code/User/mcp.json`（Mac）<br>`%APPDATA%\Code\User\mcp.json`（Win）（写前确认） | `servers` |
   | Roo Code | `.roo/mcp.json` | —（无全局需求） | `mcpServers` |
   | Gemini CLI | —（无项目级） | `~/.gemini/settings.json`（仅全局，写前确认） | `mcpServers` |
   | OpenAI Codex | —（无项目级） | `~/.codex/config.json`（仅全局，写前确认） | `mcpServers` |

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
- 获得 URL 后，调用 `get_document_info` 传入该 URL 解析出 nodeId，再以该 nodeId 作为 `list_nodes` / `create_folder` 的 `folderId`（知识库根则用 `workspaceId`）

### 更改默认知识库

当用户说"更换默认知识库"、"修改知识库地址"等时：

1. 请用户在浏览器打开目标钉钉知识库，复制地址栏 URL
2. 收到新 URL 后，覆盖写入 `references/dingtalk.config`：
   ```
   DINGTALK_DEFAULT_WORKSPACE_URL=<新的知识库 URL>
   ```
3. 无需重启，下次操作时读取新值即生效

### 安全规则

- **URL 域名白名单**：注册的 MCP URL 只接受钉钉官方域名（`*.dingtalk.com`）；非白名单域名先停下让用户核对，防止把含 API Key 的流量导向恶意/错误 endpoint
- **写前确认 + 优先项目级**：写任何 Agent 配置文件前展示目标路径 + 确切内容供用户确认；优先项目级配置，全局用户级配置仅在无项目级选项或用户明确同意时写，且只追加不覆盖
- MCP 服务 URL 含有个人 API Key，**不得出现在任何版本控制文件中**；写入配置后不要在回复中重复显示完整 URL
- `references/dingtalk.config` 保存知识库 URL，已被 `.gitignore` 排除，不会提交到版本控制
- 如果用户将 URL 粘贴到聊天中，立即写入配置后不再引用

## 默认路径

1. 确认 MCP 工具可用（若不可用，进入初始化流程）
2. 理解用户意图，映射到对应 MCP 工具（见工具映射表）
3. 如需要 dentryUuid/nodeId 但用户未提供：优先读取 `references/dingtalk.config`（或环境变量 `$DINGTALK_DEFAULT_WORKSPACE_URL`）获取默认知识库 URL，调用 `get_document_info` 解析出 nodeId；否则调用 `search_documents` 或 `list_nodes` 定位目标，让用户确认后再操作
4. 对推送请求确定推送方案；若格式、是否保留原格式、是否需要在线编辑或用户意图不足以唯一确定方案，先让用户选择方案，**不得开始创建或上传**
5. **执行前确认**（只读操作除外，见下方说明）：方案确定后，向用户展示操作摘要，收到明确同意后再调用 MCP 工具
6. 执行操作
7. 报告结果：操作类型、文档标题、文档链接（如有）

### 执行前确认规则

**需要确认的操作**（所有会写入或修改云端数据的操作）：
`create_document`、`update_document`、`create_folder`、`create_file`、`delete_document`、`rename_document`、`move_document`、`copy_document`、`insert_document_block`、`update_document_block`、`delete_document_block`、文件上传（`get_file_upload_info` + `commit_uploaded_file`）、`submit_export_job`、`add_permission`、`update_permission`

**无需确认的操作**（只读）：
`search_documents`、`list_nodes`、`get_document_info`、`get_document_content`、`list_document_blocks`、`list_permission`、`query_export_job`、`download_file`、`download_doc_attachment`

> **只读 ≠ 无边界**（敏感读取护栏）：`get_document_content` / `download_*` 会把云端正文或文件字节拉进本地上下文。遵循**最小化**——只读当前任务确需的文档、不批量拉全文；请求模糊或命中多目标时**先确认具体是哪一篇**再读；读取内容仅用于当前任务，不外传、不沉淀到无关文件。

**确认摘要格式**（根据操作类型调整）：

```
即将执行以下操作，请确认：

操作：<创建 / 更新（覆盖）/ 更新（追加）/ 删除 / 重命名 / 移动 / 复制 / 创建文件夹 / 图片内联 / 批量修复>
目标：<文档标题或文件夹名>
位置：<知识库名或文件夹路径>
说明：<一句话描述本次变更，例如"将以本地文件 xxx.md 的内容覆盖云端文档全文"；批量修复须注明"将删除 N 个块并重插 N 张图">

确认请回复「是」或「确认」，取消请回复「否」或「取消」。
```

收到取消时：停止操作，不重试，告知用户已取消。

## 数据安全与边界

本 Skill 在本地与钉钉云端之间**双向搬运数据**。以下三类跨边界操作，除「执行前确认」外，还须在回复中明示数据去向与风险（对齐 clawhub 上架安全要求）：

### 1. 数据离开本地（上传 / HTTP PUT）

- **文件上传**（`get_file_upload_info` → HTTP PUT → `commit_uploaded_file`）与**图片内联**（`get_doc_attachment_upload_info` → HTTP PUT）会把**本地文件的原始字节经 HTTP PUT 直传钉钉 OSS 云端**，再入库/转存——这不是纯本地操作。
- 确认摘要须写明：「本地文件 `<名称>` 的原始字节将上传到钉钉云端存储」，用户同意后再传。
- 上传目标 URL 由钉钉官方接口签发（OSS 凭证），**不接受用户手填的任意 endpoint**。

### 2. 数据扩散（导出 / 下载 / 临时签名 URL）

- **导出**（`submit_export_job`）产生文档的**可移植副本**（PDF/Word/markdown）；**下载**（`download_file` / `download_doc_attachment`）与签名 URL 把云端内容取到本地或生成**临时可访问链接**。
- 提示用户：导出/下载产生的是**可扩散副本**，签名 URL 在时效内**任何持有者可访问**；后续存储、分享、传播的责任与风险由用户承担，链接有时效、勿长期外发。

### 3. 敏感读取（拉正文进上下文）

- `get_document_content` 等只读操作把云端正文拉进当前对话上下文。遵循**最小化**：只读确需文档、不批量拉全文、模糊请求先确认具体文档、内容仅用于当前任务（详见「执行前确认规则」下的敏感读取护栏）。

## MCP 工具映射

详见 `references/mcp-tools.md`。常用映射如下：

| 用户意图 | MCP 工具 |
|---------|---------|
| 推送 Markdown / 纯文本为可编辑钉钉文档 | `create_document` |
| 推送 HTML、图片或其他本地文件并保留原格式 | `get_file_upload_info` → HTTP PUT → `commit_uploaded_file` |
| 拉取 adoc 文字文档内容到本地 | `get_document_content` |
| 覆盖或追加文档内容 | `update_document` |
| 精确块级编辑（段落/标题/表格等） | `list_document_blocks` → `insert/update/delete_document_block` |
| 将本地图片内联嵌入文档正文 | `get_doc_attachment_upload_info` → HTTP PUT → `download_doc_attachment`（取签名 URL）→ `update_document`(append, `![](签名URL)`) |
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
- **读取非 adoc 节点**：先调用 `get_document_info` 或使用列表/搜索结果中的类型字段确认 `contentType`。只有 `adoc` 可调用 `get_document_content`；不要对其他类型反复重试该工具
- **读取 axls（钉钉表格）**：`get_document_content` 不支持 `axls`。仅当当前会话实际提供可用的表格 MCP 工具时，才使用该工具读取所需单元格或区域；不得根据报错臆造或调用未安装的工具。若表格工具不可用，明确说明当前无法读取该表格，并请用户直接粘贴需要处理的表格内容，或提供导出的文件/目标数据
- **读取 dlink（快捷方式）**：`dlink` 不是正文载体，不能直接调用 `get_document_content`。从其元信息中取得指向目标的原始 nodeId，使用原始 nodeId 继续查询类型和读取；搜索或列出结果同时含有原节点与指向该节点的 `dlink` 时，按原始 nodeId 去重，优先保留原节点。无法解析原始 nodeId 时，向用户说明该快捷方式无法直接读取，不要重试正文读取
- **读取其他非 adoc 节点**：演示、脑图、白板、文件等非 `adoc` 节点不适用 `get_document_content`。仅在当前会话存在匹配的专用读取工具时使用；否则说明限制，并请用户粘贴所需内容、提供导出文件，或改为下载/导出后处理
- **update_document 报错**：确认目标是否为 adoc（文字类型）文档，非 adoc 文档不支持此操作
- **delete_document 前**：确认摘要中必须注明"将移入回收站，30 天内可恢复"，收到确认后再执行
- **API 报错（权限/鉴权类）**：当 API 返回权限不足、无权限、鉴权失败、Forbidden、Unauthorized 等错误时，除了展示原文错误信息外，提示用户可能尚未开通所在组织的钉钉开发者权限，引导用户参考以下链接完成开通：
  > 请访问钉钉开发者入门文档，确认你已在所在组织中开通了开发者权限：
  > https://open.dingtalk.com/document/dingstart/dingtalk-developer
  >
  > 开通步骤简述：登录钉钉开放平台 → 选择对应组织 → 完成开发者认证/开通。完成后重新尝试操作。
- **并发写冲突**：报 `unable to write to document concurrently` 时，说明有多个写操作同时进行。所有写操作（create/update/insert/delete block）必须**严格串行**，一个完成后再执行下一个；不要并行提交
- **图片内联后显示"暂无权限访问"/占位插画**：说明用了 `resourceUrl`（`/core/api/resources/img/…`）当图源且该资源对导入器不可达，抓到的是占位图（≈42210 字节 PNG）。改用 `download_doc_attachment` 返回的**签名下载 URL** 重新内联，并按字节级验收复核
- **删块结果异常**：删除后若发现块未删或误删邻块，用 `list_document_blocks` 复核实际结果再决定下一步，不要盲目重试删除
- **其他 API 报错**：原文展示错误信息，不猜测原因，不自动重试

## 关键约束

- `update_document` 和 `create_document` 仅支持 **adoc（文字类型）** 文档，不支持表格、演示、脑图等
- `create_document` 和 `update_document` 的 `markdown` 参数上限均为 **10,000 字符**；超出会报 `invalidRequest.inputArgs.invalid` 错误。推送前应先估算内容字符数，超过 **9,500 字符**（留余量）时走大文档推送策略（见下文）
- `delete_document` 是移入回收站，不是永久删除，30 天内可从回收站恢复
- `list_nodes` 只返回直接子节点，不递归。需要深层列表时需要多次调用
- **所有写操作严格串行**：`create_document`、`update_document`、`insert/update/delete_document_block` 不能并行作用于同一文档，否则报 `unable to write to document concurrently`；删块后必须 `list_document_blocks` 复核
- **含图推送时 index 按块算**：图片不计入 10000 字符上限，但每张内联图占用一个块位；用 `update_document`(append, index) 定位时，index 以 `list_document_blocks` 的块序号为准，插入后其后所有块 index +1
- **导出为异步操作**：`submit_export_job` 返回 jobId 后需轮询 `query_export_job` 直到状态完成，再将下载链接告知用户；轮询间隔建议 1-2 秒
- **Mermaid 文本绘图**：通过 `create_document` 推送的 ` ```mermaid ` 代码块会被解析为普通代码块，而非钉钉原生文本绘图块。钉钉的文本绘图是私有块类型，API 层未暴露，无法通过 MCP 创建或转换。推送前告知用户此限制，建议推送后在钉钉编辑器中手动将代码块转换为文本绘图
- 操作完成后，从返回值中提取文档链接告知用户，方便直接点击查看

## 对话中上传文件的处理

用户可能在对话中直接上传文件并要求推送到钉钉。先识别文件扩展名、MIME 类型或实际内容，再按下列规则选择推送方案；**保留用户提供的原始格式，不要为了使用 `create_document` 擅自转码或转换格式**。

### 推送方案选择

| 输入内容 | 默认推送方案 | 原因与限制 |
|---|---|---|
| Markdown / 纯文本（`.md`、`.markdown`、`.txt`）或用户直接提供的文字内容 | `create_document` 创建 `adoc` | 适合在线编辑、评论和协作；受单次 10,000 字符限制 |
| HTML（`.html`、`.htm`） | 文件上传三步流程 | 以 HTML 文件原样存入知识库，不转换为 Markdown / adoc |
| 图片（如 `.png`、`.jpg`、`.jpeg`、`.gif`、`.webp`、`.svg`） | 文件上传三步流程 | 以图片文件原样上传 |
| PDF、Office 文件、表格、压缩包、音视频及其他二进制文件 | 文件上传三步流程 | 以原始文件上传；不能使用 `create_document` 或 `update_document` 写入 |
| 无扩展名或类型无法判断的文件 | 先询问用户希望“在线可编辑文档”还是“原文件上传” | 不擅自猜测或转换；只有用户确认文本内容且希望在线编辑时才创建 adoc |

用户明确要求改变默认方案时，以用户要求为准。例如，用户要求将 HTML 转为可编辑文字文档时，先说明转换后可能丢失样式或交互，再经确认后转换为 Markdown / 纯文本并使用 `create_document`。

### MD 优先与方案确认

- **原始 Markdown 文件优先创建 adoc**：对于 `.md` / `.markdown` 文件，用户未指定其他目标时，先估算 Markdown 正文的**字符数**。不以文件字节大小或行数代替此判断；估算不超过 9,500 字符时，默认方案为创建可编辑的 adoc
- **超出 adoc 单次上限时必须选择**：Markdown 正文超过 9,500 字符时，不得自动拆分或直接上传。先向用户说明 adoc 单次 `create_document` / `update_document` 上限为 10,000 字符，并提供两个选项：方案 A 为分段创建并追加 adoc，方案 B 为原样上传 `.md` 文件。推荐需要在线编辑、评论或协作时选择方案 A；只需存档或下载分享时选择方案 B。收到用户选择后才进入写入确认
- **推送方案不明确时必须先确认**：只要文件类型、是否保留原格式、是否转换为可编辑 adoc，或用户期望的交付形态存在歧义，就先展示可选方案并等待用户明确选择。此时可进行只读的文件类型或元信息识别，但不得调用 `create_document`、`get_file_upload_info`、HTTP PUT 或 `commit_uploaded_file`
- **方案确认不替代写入确认**：用户选定方案后，仍须按“执行前确认规则”展示目标位置、文件/文档名称和操作摘要；收到明确同意后才执行云端写入

### 文件上传流程

对于应原样保留的文件，确认目标位置与文件名后，执行：

1. 调用 `get_file_upload_info`，传入原始 `fileName`、实际 `fileSize` 和目标 `folderId` 或 `workspaceId`
2. 使用返回的凭证对文件原始字节执行 HTTP PUT；不得将图片、HTML 或其他文件内容改写为 Markdown
3. 调用 `commit_uploaded_file`，使用返回的 `uploadKey` 提交入库
4. 返回上传文件的名称、节点标识和访问链接（如返回）

### 已知限制

- 对话上传的文件内容是**临时的**，不会持久保存到磁盘，上下文压缩或会话结束后内容即丢失
- **非 ASCII 文件（如中文 markdown）通过对话上传时，0x80-0x9F 范围的字节会被文本处理层丢弃，导致不可逆乱码**。这是客户端文本传输的固有限制，编码修复无法还原丢失的字节

### 处理规则

1. **优先使用本地文件路径**：当用户要推送含非 ASCII 内容（中文、日文等）的文本文件，或任何需要原样上传的二进制/HTML 文件时，请用户提供本地磁盘路径，直接读取文件内容或原始字节，避免编码问题
2. **对话上传的文件先检查编码**：如果用户直接在对话中上传了文件，先检查内容是否出现乱码。如果存在乱码，立即告知用户并请其提供本地文件路径
3. **文本按类型路由**：可正确读取的 Markdown / 纯文本按上表创建 adoc；HTML 即使能读取文本，也默认按原 HTML 文件上传
4. **二进制或原格式上传须读取本地文件**：图片、PDF、Office 文件等需要读取原始字节；如果对话附件无法提供可靠的本地文件内容，请用户提供本地磁盘路径后走文件上传三步流程
5. **命名规则**：创建 adoc 时默认使用文件名去掉扩展名作为文档标题；上传原文件时默认保留原始文件名。用户要求修改名字时，以用户指定的名字为准

## 大文档推送策略

当原始 Markdown 文件的正文超过 **9,500 字符** 时，单次 `create_document` / `update_document` 会超过 10,000 字符上限。此时先让用户在以下两种方案中选择，**不要自动执行任一方案**：

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

## 本地图片内联到文档正文

当用户要把本地图片作为**文档正文的一部分**（内联图，随文档在线渲染/评论），而非作为独立文件存入知识库时，走自动内联链路，**不要用占位符 + 人工粘贴**。完整步骤与陷阱见 `references/mcp-tools.md`「本地图片内联到文档正文」，要点：

1. **区分两种图片意图**：图片作为独立文件存档 → `get_file_upload_info` 三步上传（见「对话中上传文件的处理」）；图片内联进正文 → 本节链路
2. **链路**：`get_doc_attachment_upload_info` 上传拿 `resourceId` → HTTP PUT 原始字节 → `download_doc_attachment` 取**签名下载 URL** → `update_document`(append) 或 `create_document` 写入 `![alt](签名URL)`，钉钉自动抓取转存为内联图
3. **统一用签名下载 URL**：`resourceUrl`（`/core/api/resources/img/…`）行为不稳定——资源可达时能解析，不可达时会变「暂无权限访问」占位插画；为可靠起见一律用 `download_doc_attachment` 的签名下载 URL
4. **替换旧图净零位移**：先 append 新图到旧图 index，再按 `blockId` 删旧块，先加后删配对完成
5. **字节级验收**：推送后导出或取 markdown，下载新图签名 URL 比对字节数等于原图；抽查 2-3 张。修复类批量操作（删坏块 + 重插图）在执行前确认摘要中注明「将删除 N 个块并重插 N 张图」

---

## 资源导航

- `references/mcp-tools.md` — 全部 MCP 工具详细说明，按场景分组（含「本地图片内联到文档正文」完整链路与「已知陷阱速查」）
