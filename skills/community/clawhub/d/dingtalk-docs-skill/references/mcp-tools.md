# 钉钉文档 MCP 工具速查

MCP 名称：`dingtalk-doc`（注册方式见 SKILL.md 初始化流程）

---

## 文档内容操作

### create_document
创建文字类型（adoc）钉钉文档，支持带初始 markdown 内容。

- 关键参数：`title`（标题）、`content`（markdown 正文）、`parentNodeId`（父节点 ID，指定放置位置）
- 返回：新文档的 `dentryUuid`、文档链接
- 注意：只能创建 adoc 类型，不能创建表格/演示等

### update_document
更新文字类型（adoc）文档的内容，支持两种模式：

- `overwrite`：覆盖全部内容（常用于推送本地文件）
- `append`：追加到文档末尾
- 关键参数：`dentryUuid`、`content`（markdown）、`updateMode`（overwrite/append）
- 限制：**仅支持 adoc 类型文档**，其他类型会报错

### get_document_content（高敏感）
获取文档的 markdown 正文内容。

- 关键参数：`dentryUuid`
- 用途：读取文档内容、做差异对比后再更新

---

## 块级精确编辑

适用于需要在文档特定位置插入/修改/删除段落、标题、表格等场景。

### list_document_blocks
列出文档的一级块元素（段落、标题、表格等）。

- 关键参数：`dentryUuid`，支持按起始/终止位置和块类型过滤
- 返回：blockId 列表，供后续插入/更新/删除使用

### insert_document_block
在文档指定位置插入新块元素。

- 关键参数：`dentryUuid`、`blockType`（块类型）、块内容属性对象
- 支持类型：段落、标题、表格、高亮块、列表等

### update_document_block
更新指定块元素的内容或样式。

- 关键参数：`dentryUuid`、`blockId`、新内容（含 `blockType` 和属性对象）

### delete_document_block
删除指定块元素。

- 关键参数：`dentryUuid`、`blockId`
- 需有编辑权限

---

## 文档/节点查找

### search_documents
按关键词搜索当前用户有权限访问的文档。

- 关键参数：`keyword`（匹配标题和内容）、可选过滤条件（类型、时间范围等）
- 用途：在不知道 dentryUuid 时定位目标文档

### list_nodes
列出指定文件夹或知识库下的直接子节点（文件夹/文档/文件）。

- 关键参数：`parentNodeId`（知识库 ID 或文件夹节点 ID），支持分页
- 注意：**只返回直接子节点，不递归**；需要更深层列表时多次调用

### get_document_info
获取节点的元信息（标题、类型、创建者、创建时间等）。

- 关键参数：`nodeId`（支持文档 URL 或 dentryUuid）
- 返回的 `contentType` 字段可判断文档类型（adoc/sheet/ppt 等）

---

## 文件夹与节点管理

### create_folder
在指定位置创建文件夹，返回新文件夹的节点 ID。

- 关键参数：`name`（文件夹名）、`parentNodeId`（父节点）

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

### submit_export_job
提交导出任务，返回 `jobId`。

- 关键参数：`dentryUuid`、`exportType`（`pdf` / `docx` 等）
- 返回：`jobId`，供轮询使用

### query_export_job
查询导出任务状态，直到完成为止。

- 关键参数：`jobId`
- 返回：任务状态；完成时包含下载链接
- 注意：需轮询直至状态为成功，建议间隔 1-2 秒

---

## 附件操作

### get_doc_attachment_upload_info
获取向指定文档上传附件所需的 OSS 凭证（文档内嵌附件，非知识库文件）。

### download_doc_attachment
获取文档内指定附件的临时下载 URL。

- 关键参数：`nodeId`（文档标识）、`resourceId`（附件资源标识）

### download_file
获取钉盘文件的下载凭证，供 Claude 发起 HTTP GET 下载。
