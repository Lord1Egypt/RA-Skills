# 飞书 API 参考

## 认证

```
POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal
Body: {"app_id": "...", "app_secret": "..."}
返回: {"code": 0, "tenant_access_token": "..."}
```

## 文档 API

### 创建文档
```
POST https://open.feishu.cn/open-apis/docx/v1/documents
Headers: Authorization: Bearer <token>
Body: {"title": "文档标题"}
返回: {"code": 0, "data": {"document": {"document_id": "xxx"}}}
```

### 读取文档 blocks
```
GET https://open.feishu.cn/open-apis/docx/v1/documents/<doc_token>/blocks?page_size=500
返回: {"code": 0, "data": {"items": [block, ...]}}
```

### 查询单个 block
```
GET https://open.feishu.cn/open-apis/docx/v1/documents/<doc_token>/blocks/<block_id>
```

### 追加 blocks（到父 block）
```
POST https://open.feishu.cn/open-apis/docx/v1/documents/<doc_token>/blocks/<parent_block_id>/children
Body: {"children": [block, ...], "index": 0}
```

### 更新 block 文本
```
PATCH https://open.feishu.cn/open-apis/docx/v1/documents/<doc_token>/blocks/<block_id>
Body: {"update_text_elements": {"elements": [...]}}
```

### 删除 block
```
DELETE https://open.feishu.cn/open-apis/docx/v1/documents/<doc_token>/blocks/<block_id>
```

## 消息 API

### 发送消息
```
POST https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=<type>
Headers: Authorization: Bearer <token>
Body: {
  "receive_id": "<id>",
  "msg_type": "text",
  "content": "{\"text\": \"消息内容\"}",
  "uuid": "<uuid>"
}
```
- `receive_id_type`: `open_id`（用户）或 `chat_id`（群）

### 搜索用户
```
GET https://open.feishu.cn/open-apis/contact/v3/users/search?query=<关键词>&page_size=20
```

### 搜索群聊
```
GET https://open.feishu.cn/open-apis/im/v1/chats?search_key=<关键词>&page_size=20
```

## Block 类型参考

| block_type | 类型 | 键名 |
|-----------|------|------|
| 1 | Page | `page` |
| 2 | Text | `text` |
| 3 | Heading 1 | `heading1` |
| 4 | Heading 2 | `heading2` |
| 5 | Heading 3 | `heading3` |
| 6-11 | Heading 4-9 | `heading4`...`heading9` |
| 12 | Bullet List | `bullet` |
| 13 | Ordered List | `ordered` |
| 14 | Code | `code` |
| 15 | Quote | `quote` |
| 17 | Todo | `todo` |
| 31 | Table | `table` |
| 32 | Table Cell | `table_cell` |

## 表格 block 内部结构

表格 block (type=11) 包含 `table_rows`，每个 row 包含 `cells`。

查询表格内容需要：
1. `GET /blocks` 获取文档 blocks
2. 找到 `block_type == 11` 的表格 block
3. `GET /blocks/<table_block_id>` 获取表格详情（含 rows/cells）
4. 每个 cell 是独立的 block，可用 `update_text_elements` 更新

## 错误码

| code | 含义 |
|------|------|
| 0 | 成功 |
| 99991661 | 无权限 |
| 230001 | 文档不存在 |
| 230002 | block 不存在 |
