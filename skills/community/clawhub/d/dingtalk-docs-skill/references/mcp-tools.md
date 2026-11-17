# 钉钉文档 MCP 工具速查

MCP 名称：`dingtalk-doc`（注册方式见 SKILL.md 初始化流程）

---

## 文档内容操作

### create_document
创建文字类型（adoc）钉钉文档，支持带初始 markdown 内容。

- 关键参数：`name`（文档标题，必填）、`markdown`（初始正文）、`folderId`（目标文件夹节点）、`workspaceId`（知识库 ID）
- 放置位置优先级：`folderId` > `workspaceId` > 两者都不传时建在「我的文档」根目录
- 返回：新文档的 `dentryUuid`、文档链接
- **`markdown` 换行必须用真实换行符（U+000A）**，不能是字面量 `\n`，否则标题/段落/表格会全部渲染在同一行
- 上限 **10000 字符**，超出改用 `update_document` 分批 append
- 注意：只能创建 adoc 类型；表格/演示等其他类型用 `create_file`

### update_document
更新文字类型（adoc）文档的内容，支持两种模式：

- `overwrite`（默认）：清空全文后重写，**会丢失原有图片/评论**，谨慎使用
- `append`：追加内容，可配合 `index` 精确插入到指定块之前
- 关键参数：`nodeId`（文档 URL 或 dentryUuid）、`markdown`（正文）、`mode`（overwrite/append）、`index`（仅 append 生效）、`format`（markdown/jsonml，默认 markdown）
- **`index` 语义**：从 0 开始，表示插入到文档第 index 个块**之前**；不传则追加到末尾。index 由 `list_document_blocks` 获取
- **index 位移规则**：插入成功后，该位置及其后所有块的 index 依次 **+1**；批量插/删须按此重算，或采用「先加后删配对完成」避免连锁位移
- **`markdown` 换行必须用真实换行符（U+000A）**，不能是字面量 `\n`
- 上限 **10000 字符**，超出分批 append
- 限制：**仅支持 adoc 类型文档**，其他类型会报错

### get_document_content（高敏感）
获取文档的 markdown 正文内容。

> ⚠️ **敏感读取边界**：本操作把云端文档正文**拉进当前对话上下文**。遵循最小化——只读当前任务确需的文档、不批量拉全文；请求模糊或命中多目标时**先确认具体是哪一篇**再读；读取内容仅用于当前任务，不外传、不写入无关文件。

- 关键参数：`nodeId`（文档 URL 或 dentryUuid）
- 用途：读取文档内容、做差异对比后再更新、核对图片是否内联成功（返回 markdown 中可见 `![](...)`）
- **仅适用于 `adoc` 文字文档**。调用前通过 `get_document_info` 或结果中的 `contentType` 确认类型
- `axls`（钉钉表格）、`dlink`（快捷方式）及其他非 `adoc` 节点会报错或不提供正文，禁止将报错视为可重试错误
- 对 `axls`，仅在当前会话确实提供表格读取工具时使用该工具；工具不可用时请用户粘贴所需内容或提供导出文件
- 对 `dlink`，先解析其指向的原始 nodeId，再对原节点执行后续查询。检索结果按原始 nodeId 去重，优先保留原节点

---

## 块级精确编辑

适用于需要在文档特定位置插入/修改/删除段落、标题、表格等场景。

### list_document_blocks
列出文档的一级块元素（段落、标题、表格等）。

- 关键参数：`nodeId`（文档 URL 或 dentryUuid）、`startIndex`/`endIndex`（范围）、`blockType`（过滤）、`format`（element/jsonml，默认 element）
- 返回：各块的 `blockId` 与 `index`，供 `update_document(index)` / insert / update / delete_document_block 定位使用
- **图片块识别坑**：element 格式下，内联图片块表现为**空文本 paragraph**，与真空段落无法区分；核对图片请用 markdown 视图（`get_document_content`）或导出，不要依赖 element 列表

### insert_document_block
在文档指定位置插入新块元素。

- 关键参数：`nodeId`、`element`（含 `blockType` 及对应属性对象）、定位用 `referenceBlockId`（优先）或 `index`、`where`（before/after，默认 after）、`format`（element/jsonml）
- 支持类型：paragraph/heading/blockquote/callout/columns/orderedList/unorderedList/table/attachment 等
- **行内 image 不可用**：`element.children` 的 `properties.src`（图片 Url）虽在 schema 中声明，但实测插入行内 image 会报 **"Undefined block element"**。**不要用本工具插图**，改走 markdown 导入链路（见「本地图片内联到文档正文」）
- **attachment 的 `size` 必须省略**：`size`（number）经 MCP 桥接层会被序列化成字符串，报 **"expected number, but got string"**；插入 attachment 块时省略 size
- **attachment 块 ≠ 内联图**：attachment 块导出为 `[文件名](链接)` 的附件卡片，不是内联图片；仅在图片内联链路中作为临时上传媒介，转存成功后即删除

### update_document_block
更新指定块元素的内容或样式。

- 关键参数：`nodeId`、`blockId`、`element`（含 `blockType` 和属性对象）

### delete_document_block
删除指定块元素。

- 关键参数：`nodeId`、`blockId`（支持逗号分隔批量删除，一次最多 50 个；未命中的列入返回的 `notFoundBlockIds`）
- 需有编辑权限
- **删后必须复核**：并行/连续删除曾出现「返回成功但未删或误删邻块」，删除后务必用 `list_document_blocks` 复核结果

---

## 文档/节点查找

### search_documents
按关键词搜索当前用户有权限访问的文档。

- 关键参数：`keyword`（匹配标题和内容）、可选过滤条件（类型、时间范围等）
- 用途：在不知道 dentryUuid 时定位目标文档

### list_nodes
列出指定文件夹或知识库下的直接子节点（文件夹/文档/文件）。

- 关键参数：`folderId`（文件夹节点）或 `workspaceId`（知识库 ID）；分页用 `pageSize`（默认/最大 50）+ `pageToken`（首次不传）
- 注意：**只返回直接子节点，不递归**；需要更深层列表时多次调用

### get_document_info
获取节点的元信息（标题、类型、创建者、创建时间等）。

- 关键参数：`nodeId`（支持文档 URL 或 dentryUuid）
- 返回的 `contentType` 字段可判断文档类型（adoc/sheet/ppt 等）

---

## 文件夹与节点管理

### create_folder
在指定位置创建文件夹，返回新文件夹的节点 ID。

- 关键参数：`name`（文件夹名，必填）、`folderId`（父文件夹节点）或 `workspaceId`（知识库 ID；同时传 folderId 时以 folderId 为准，都不传建在"我的文档"根目录）

### create_file
创建各类型节点（文档、表格、演示、白板、脑图、多维表、文件夹）。

- 支持三种创建位置（优先级顺序）：指定 folderId、指定 workspaceId、默认位置
- 与 `create_document` 的区别：`create_file` 可创建所有类型，但不支持带初始内容

### delete_document
将节点移入回收站（30 天内可恢复，超过 30 天永久删除）。

- 支持：知识库下的文档节点、文件夹节点、钉盘文件
- **执行前需告知用户这是移入回收站，获得确认后再调用**

### rename_document
重命名节点（知识库下的文档/文件夹节点）。

### move_document
将节点移动到目标文件夹。

- 支持：知识库节点、钉盘文件/文件夹
- `nodeId` 支持文档 URL 或 dentryUuid

### copy_document
将节点复制到目标文件夹。

- 与 `move_document` 参数相同，区别是原节点保留

---

## 文件上传（非 adoc 文件）

上传本地文件（PDF、图片、Word 等）到钉钉文档/知识库，分三步：

1. **get_file_upload_info** — 获取 OSS 上传凭证（第一步）
2. **HTTP PUT** — 使用凭证将文件直传 OSS（Claude 代理发起 HTTP 请求）
3. **commit_uploaded_file** — 提交完成文件入库（第三步）

> ⚠️ **数据离开本地**：第 2 步 HTTP PUT 把**本地文件的原始字节直传到钉钉 OSS 云端存储**，不是纯本地操作。执行前须在确认摘要中明示「本地文件 `<名称>` 原始字节将上传到钉钉云端」，用户同意后再传；上传 URL 由钉钉官方接口签发，不接受手填任意 endpoint。

### get_file_upload_info
- 关键参数：`fileName`、`fileSize`、目标位置（folderId 或 workspaceId）

### commit_uploaded_file
- 关键参数：上传凭证中的 `uploadKey`

---

## 权限管理

### add_permission
为知识库节点添加企业用户成员（指定角色）。

### update_permission
修改企业用户在节点上的角色。

### list_permission
查询节点当前的成员权限列表。

---

## 导出

将文档异步导出为 PDF 或 Word 等格式，分两步：

> ⚠️ **数据扩散**：导出产生文档的**可移植副本**（PDF/Word/markdown），完成后的下载链接在时效内**任何持有者可访问**。提示用户副本的存储/分享/传播责任与风险自负，链接有时效、勿长期外发。

### submit_export_job
提交导出任务，返回 `jobId`。

- 关键参数：`nodeId`（文档 URL 或 dentryUuid）、`exportFormat`（`docx` / `markdown` / `pdf`）
- 返回：`jobId`，供轮询使用

### query_export_job
查询导出任务状态，直到完成为止。

- 关键参数：`jobId`
- 返回：任务状态；完成时包含下载链接
- 注意：需轮询直至状态为成功，建议间隔 1-2 秒

---

## 附件操作

### get_doc_attachment_upload_info
获取向指定文档上传「文档内嵌附件」的 OSS 上传凭证。注意区别于 `get_file_upload_info`（后者是往知识库/钉盘放独立文件）：本工具绑定到某个文档 `nodeId`，是「本地图片内联」链路的第一步。

- 关键参数：`nodeId`（文档 URL 或 dentryUuid）、`fileName`（含扩展名）、`fileSize`（字节，须与实际一致）、`mimeType`（如 `image/png`）
- 返回：`uploadUrl`（OSS PUT 目标，有时效，尽快使用）+ `resourceId`
- 随后对 `uploadUrl` 执行 HTTP PUT 上传**原始字节**，Header 带 `Content-Type: <mimeType>`、`Content-Length: <fileSize>`，须返回 **200**

### download_doc_attachment
获取文档内指定资源（`resourceId`）的临时**签名下载 URL**（OSS 公开可取）。

- 关键参数：`nodeId`（文档 URL 或 dentryUuid）、`resourceId`（资源标识）
- 返回：签名 `downloadUrl`
- **实测补注（与官方 schema 前置说明不同）**：官方 schema 写「需先 `list_document_blocks` 找到 attachment 块再提取 resourceId」，但实测**任意经 `get_doc_attachment_upload_info` 上传过的 resourceId 都能直接取到签名 URL，无需 attachment 块存在**。「本地图片内联」链路正是利用这一点：上传 → 取签名 URL → 写进 markdown 让钉钉抓取转存，全程不落地 attachment 块

### download_file
获取钉盘文件的下载凭证，供 Claude 发起 HTTP GET 下载。

> ⚠️ **数据扩散**：`download_doc_attachment` 的签名 URL 与 `download_file` 的下载凭证都会把云端内容取到本地或生成**临时可访问链接**，时效内任何持有者可访问；提示用户扩散风险与存储/分享责任自负。

---

## 本地图片内联到文档正文（推荐链路）

把本地图片作为**内联图**嵌入 adoc 文档正文，区别于「作为独立文件上传到知识库/钉盘」（`get_file_upload_info` 三步流程）。适用场景：markdown 引用了本地相对路径图片、需要图片随文档一起在线渲染/评论/协作。

**原理**：钉钉在 `create_document` / `update_document` 导入 markdown 时，会**自动抓取外部 https 图片 URL 的真字节并转存为文档自托管内联图**。因此只要能拿到一个钉钉 OSS 可公开访问的签名 URL，写入 `![alt](url)` 即可让图片内联。

**链路（所有写操作严格串行）**：

1. `get_doc_attachment_upload_info`(nodeId, fileName, fileSize, mimeType) → 拿 `uploadUrl` + `resourceId`
2. HTTP PUT 图片**原始字节**到 `uploadUrl`，Header `Content-Type: <mimeType>`、`Content-Length: <fileSize>`，须返回 200
3. `download_doc_attachment`(nodeId, resourceId) → 拿**签名下载 URL**（OSS 公开可取）
4. `update_document`(mode=append, index=<目标位置>) 或 `create_document`，markdown 写入 `![alt](签名下载URL)` → 钉钉导入器抓取真字节并转存为内联图
5. **替换旧图（净零位移）**：先 append 新图到旧图所在 index，再按旧块 `blockId` 删除旧块——先加后删配对完成，避免连锁重算 index

**不要依赖 `resourceUrl` 当图源（行为不稳定）**：`get_doc_attachment_upload_info` 返回的 `resourceUrl`（形如 `/core/api/resources/img/…`）实测行为取决于资源可达性——指向本文档刚上传、导入器可达的资源时可被正确解析为内联图（实测字节级一致）；但指向无权访问/跨文档/不可达的资源时，导入器抓取失败会存成「暂无权限访问」占位插画（≈42210 字节 PNG）。为消除这种不确定性，**统一只用 `download_doc_attachment` 返回的签名下载 URL**（实测 100% 转存成功）。

**字节级验收（必做）**：
1. 导出文档（`submit_export_job`）或用 `get_document_content` 取 markdown
2. 下载新图的签名 URL
3. 比对字节数是否等于原图 —— 相等即健康；若为 ≈42210 字节的占位图，说明误用了 `resourceUrl`
4. 抽查 2-3 张即可，不必全量

---

## 已知陷阱速查（图片 / 块编辑）

| 陷阱 | 现象 | 正确做法 |
|---|---|---|
| 用 `resourceUrl`（`/core/api/resources/img/…`）当 markdown 图源 | 行为不稳定：资源可达时能解析，无权/跨文档/不可达时抓取失败存成「暂无权限访问」占位插画（≈42210 字节 PNG） | 统一用 `download_doc_attachment` 的签名下载 URL（最可靠） |
| `insert_document_block` 的行内 image（`children.src`） | 报 "Undefined block element"（schema 声明但实际不可用） | 不要尝试，走 markdown 导入链路 |
| attachment 块传 `size` | 被 MCP 桥接层序列化为字符串，报 "expected number, but got string" | 省略 `size` |
| 把 attachment 块当图片用 | 导出为 `[文件名](链接)`，是附件卡片不是内联图 | 仅作上传媒介，图片转存后即删 |
| 并行写同一文档 | 报 "unable to write to document concurrently"；并行 delete 曾出现「返回成功但未删/误删邻块」 | 所有写操作严格串行；删后必须 `list_document_blocks` 复核 |
| element 视图找图片块 | 图片块表现为空文本 paragraph，与真空段无法区分 | 用 markdown 视图（`get_document_content`）或导出核对 |
| markdown 传字面量 `\n` | 全文渲染在同一行，格式错乱 | 用真实换行符（U+000A） |
