# Feishu Doc 技能

## 概述

飞书文档操作技能，用于在飞书中创建、读取、追加和更新文档。

## 工具

使用 `feishu_doc` 工具，参数：
- `action`: 操作类型
- `doc_token`: 文档 token（从飞书文档 URL 中提取，如 `/docx/XXX` 中的 XXX）
- `content`: 文档内容（markdown 格式）
- `title`: 文档标题（仅 create 时使用）
- `folder_token`: 文件夹 token（可选）

## 操作类型

| action | 说明 | 必需参数 |
|--------|------|----------|
| create | 创建新空白文档 | title |
| read | 读取文档内容 | doc_token |
| append | 向文档追加内容 | doc_token, content |
| write | 覆盖写入整个文档 | doc_token, content |
| list_blocks | 列出文档所有块 | doc_token |
| get_block | 获取单个块 | doc_token, block_id |
| update_block | 更新单个块 | doc_token, block_id, content |
| delete_block | 删除单个块 | doc_token, block_id |

## 创建文档的正确方式

### 坑：create + content 可能不生效

直接用 `create` action 并传入大量 content 可能导致文档创建成功但内容为空：

```json
{
  "action": "create",
  "title": "文档标题",
  "content": "大量内容..."
}
```

### 正确做法：先 create 空文档，再 append

1. 先用 `create` 创建空白文档（只传 title）
2. 再用 `append` 逐次追加内容

```json
// 步骤1：创建空白文档
{
  "action": "create",
  "title": "文档标题"
}

// 返回 doc_token，如 "HYhbdqE2Goy9NLxle9XcomtPnVc"

// 步骤2：追加内容
{
  "action": "append",
  "doc_token": "HYhbdqE2Goy9NLxle9XcomtPnVc",
  "content": "# 标题\n\n内容..."
}
```

## 文档 URL 解析

飞书文档 URL 格式：
- `https://feishu.cn/docx/{token}`
- `https://feishu.cn/wiki/{token}`

从 URL 中提取 token：
- `/docx/` 后面的部分就是 token
- `/wiki/` 后面的部分也是 token

## 使用示例

### 创建技术文档

```json
{
  "action": "create",
  "title": "OpenClaw 使用指南"
}
```

返回：
```json
{
  "document_id": "JZyJdrVVTok9mfxVHqJc91Dhn3g",
  "title": "OpenClaw 使用指南",
  "url": "https://feishu.cn/docx/JZyJdrVVTok9mfxVHqJc91Dhn3g"
}
```

### 读取文档

```json
{
  "action": "read",
  "doc_token": "JZyJdrVVTok9mfxVHqJc91Dhn3g"
}
```

### 追加内容

```json
{
  "action": "append",
  "doc_token": "JZyJdrVVTok9mfxVHqJc91Dhn3g",
  "content": "## 新章节\n\n这里是新增加的内容。"
}
```

### 覆盖写入

```json
{
  "action": "write",
  "doc_token": "JZyJdrVVTok9mfxVHqJc91Dhn3g",
  "content": "# 完全覆盖的标题\n\n全部内容都被替换了。"
}
```

## 内容格式

- 使用 Markdown 格式
- 飞书会自动渲染标题、列表、代码块等
- 建议每段内容不要太长，分多次 append

## 常见问题

### Q: create 后内容是空的
A: 使用 create + append 的两步写法，不要一次性 create + content

### Q: 追加内容格式混乱
A: 每次 append 建议包含完整的 Markdown 结构，飞书会按块处理

### Q: 如何知道 doc_token
A: 从 URL 提取，或 create 后的返回值获取

---

## 相关工具

- `feishu_wiki`: 知识库操作
- `feishu_bitable`: 多维表格操作
- `feishu_drive`: 云盘操作
