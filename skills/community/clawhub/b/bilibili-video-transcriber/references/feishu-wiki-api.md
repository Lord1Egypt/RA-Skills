# Feishu Wiki API 参考

## 创建 Wiki 节点

**端点**: `POST /open-apis/wiki/v2/spaces/{space_id}/nodes`

### 成功请求格式

```json
{
  "node_type": "origin",
  "obj_type": "docx",
  "space_id": "7624328764398324948",
  "parent_node_token": ""
}
```

### 关键字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `node_type` | string | ✅ | 固定值 `"origin"` |
| `obj_type` | string | ✅ | 固定值 `"docx"`（不是数字 `2`） |
| `space_id` | string | ✅ | 目标知识库 space_id |
| `parent_node_token` | string | ❌ | 空字符串表示根节点 |

### 常见错误

**错误 `99992402` — field validation failed**
```json
{
  "field_violations": [
    {"field": "obj_type", "description": "... options: [doc,sheet,...]", "value": "2"},
    {"field": "node_type", "description": "node_type is required"}
  ]
}
```
**原因**: `obj_type` 传了数字 `2` 而非字符串 `"docx"`，且缺少 `node_type` 字段。

---

## 写入文档块

**端点**: `POST /open-apis/docx/v1/documents/{obj_token}/blocks/{obj_token}/children`

```json
{
  "children": [...blocks...],
  "index": -1
}
```

- `index: -1` 表示追加到末尾
- 每批最多约 12 个 block（经验值）
- block_type `2` = 文本块

### 文本 block 格式

```json
{
  "block_type": 2,
  "text": {
    "elements": [
      {"text_run": {"content": "内容", "text_element_style": {"bold": true}}}
    ]
  }
}
```

---

## 已知知识库 space_id

| 知识库名称 | space_id |
|-----------|----------|
| AI工具 | `7624328764398324948` |
| 羽毛球AI项目 | `7627078274052558020` |
| 展厅设计知识库 | `7626286573381929940` |
| 具身智能 | `7623664966343609272` |

---

### ⚠️ 文档标题设置

**重要**：`wiki/v2/nodes` API 创建的文档 **无法** 通过 PATCH title 修改标题（lark-cli 返回 `1770001 invalid param`）。

**正确做法**：用 `lark-cli docs +create --title` 一步到位创建带标题的 Wiki 文档，不要事后再改。

---

## lark-cli --data @file 路径限制（重要 Pitfall）

`--data @file` **必须使用相对路径**，绝对路径（如 `/tmp/file.json`）会报错：
```
--file must be a relative path within the current directory, got "/tmp/file.json"
```

**正确做法**：
```bash
cd /root
echo '{"member_type":"openid",...}' > ./collab.json
lark-cli api POST "/open-apis/wiki/v2/spaces/{space_id}/members" --data @./collab.json
```

---

## Wiki 空间成员 API

**端点**: `POST /open-apis/wiki/v2/spaces/{space_id}/members`

**请求体**：
```json
{"member_type": "openid", "member_id": "ou_c657175fd34e7463c9f83947061d0130", "member_role": "member"}
```

**注意事项**：
- `member_type` 必须是 `openid`（全小写），**不是** `open_id`，错误值报 `131002 param err`
- `space_id` 必须是目标知识库的 wiki space_id，不是文档 doc_id
- 如果报错 `131002`，先确认 space_id 是否正确（不同知识库的 space_id 不同）
- Wiki 文档继承知识库权限，创建到知识库后通常无需单独设置文档级权限

---

## lark-cli 参考

```bash
# 创建节点（wiki）
lark-cli api POST "/open-apis/wiki/v2/spaces/{space_id}/nodes" \
  --data '{"node_type":"origin","obj_type":"docx","space_id":"...","parent_node_token":""}'

# 写入文档块
lark-cli api POST \
  "/open-apis/docx/v1/documents/{obj_token}/blocks/{obj_token}/children" \
  --data '{"children":[...],"index":-1}'

# 设置文档标题
lark-cli api PATCH "/open-apis/docx/v1/documents/{obj_token}" \
  --data '{"title":"文档标题"}'
```