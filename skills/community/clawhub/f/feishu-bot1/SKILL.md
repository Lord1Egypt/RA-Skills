---
name: feishu-ops
description: |
  飞书（Feishu/Lark）文档与消息操作技能。When to use: 用户要求创建、删除、修改飞书文档；查询或更新文档中指定行/列的数据；向飞书联系人或群聊发送消息。Triggers: "创建飞书文档"、"删除文档"、"修改文档内容"、"更新第X行第Y列"、"查询文档"、"发送飞书消息"、"发消息给群"。
---

# 飞书操作技能 (feishu-ops)

支持飞书文档的完整 CRUD 以及单元格精细操作，同时支持发送消息给个人和群聊。

## 凭证配置

所有操作需要 `app_id` 和 `app_secret`，位于技能目录的 `scripts/config.json`：

```json
{
  "app_id": "cli_xxxxx",
  "app_secret": "xxxxx"
}
```

若无配置文件，脚本会报错并提示创建。

## 文档操作

### 创建文档

```python
python scripts/feishu_doc.py create "文档标题"
```

成功返回：`{"doc_token": "xxx", "doc_url": "https://feishu.cn/doc/xxx"}`

### 删除文档

```python
python scripts/feishu_doc.py delete <doc_token>
```

### 写入/追加文档内容

```python
# 全量写入（覆盖）
python scripts/feishu_doc.py write <doc_token> "## 标题\n这是内容"

# 追加段落
python scripts/feishu_doc.py append <doc_token> "新追加的段落"
```

### 读取文档

```python
python scripts/feishu_doc.py read <doc_token>
```

### 精细操作：单元格读写

飞书文档的 blocks API 支持按 block_id 精确操作。使用前需先 `read` 文档获取 block 树结构。

```python
# 查询指定 block 内容
python scripts/feishu_doc.py query-block <doc_token> <block_id>

# 更新指定 block 的文本内容
python scripts/feishu_doc.py update-block <doc_token> <block_id> "新的文本内容"

# 在文档末尾追加一个段落 block
python scripts/feishu_doc.py append-block <doc_token> "段落文本"
```

> **表格操作**：表格为复合 block。先用 `read` 获取表格 block_id，再遍历表格内部 cell blocks 进行读写。

## 消息操作

### 发送文本消息给用户

需要目标用户的 `open_id`（可用 `search_user.py` 查询）。

```python
python scripts/feishu_msg.py send-user <open_id> "消息内容"
```

### 发送文本消息到群

需要目标群的 `chat_id`（可用 `search_chat.py` 查询）。

```python
python scripts/feishu_msg.py send-chat <chat_id> "消息内容"
```

### 查询群聊消息

```python
python scripts/feishu_msg.py get-messages <chat_id> [page_size]
```

返回群内消息列表，自动正确显示中文内容。

### 发送文件到群

需要先安装 SDK：
```bash
pip install lark-oapi
```

发送本地文件到群：
```python
python scripts/feishu_msg.py send-file <chat_id> <本地文件路径>
```

例如发送到龙虾测试群：
```python
python scripts/feishu_msg.py send-file oc_2c6df8f6e06e88d34729baacc124b89e "C:\\Users\\10430\\Desktop\\采购数据.xlsx"
```

### 查询用户 open_id

```python
python scripts/feishu_msg.py search-user <姓名关键词>
```

### 查询群聊 chat_id

```python
python scripts/feishu_msg.py search-chat <群名关键词>
```

## 常用工作流

**创建文档并写入内容：**
1. `create` 获取 doc_token
2. `write` 或 `append-block` 写入内容
3. `read` 确认内容

**更新表格中第R行第C列：**
1. `read` 获取文档 block 树
2. 找到目标表格的 block_id
3. 遍历表格 rows/cells，用 `update-block` 更新目标单元格

**发消息给同事：**
1. `search-user` 查找 open_id
2. `send-user` 发送消息

## 脚本索引

| 脚本 | 功能 |
|------|------|
| `scripts/feishu_doc.py` | 文档 CRUD + block 精细操作 |
| `scripts/feishu_msg.py` | 消息发送 + 用户/群查询 + 获取消息 + 文件发送（需 lark-oapi SDK） |
| `scripts/config.json` | 凭证配置 |
| `references/api_ref.md` | 完整 API 参数说明 |
