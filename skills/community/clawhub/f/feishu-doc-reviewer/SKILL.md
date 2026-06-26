---
name: "feishu-doc-reviewer"
description: "为智能体提供飞书文档读写能力：导出全文、读取评论与段落、写回修改并回复评论。"
---

# 飞书文档 AI 自动审阅与修改

本技能为 Claude Code / OpenClaw 等智能体提供飞书文档的读写工具，便于在对话中基于全文上下文与批注要求完成修改并写回。

## 核心能力

- **获取评论**: 自动提取文档中未解决的评论，支持按关键词筛选。
- **读取原文**: 获取评论对应段落内容，或导出全文 Markdown 供理解上下文。
- **写回修改**: 直接通过 API 更新文档段落内容。
- **删除段落**: 
  - `delete_block`: 清空整个块内容
  - `delete_text_from_block`: **只删除选中的文本**（保留块中其他内容）⭐
- **结果反馈**: 在评论区回复修改结果，并标记为 [AI-DONE]。
- **智能识别**: 自动从评论 quote 中识别对应的块 ID。

## 使用方法

### MCP 协议 (Claude / OpenClaw)

在对话中，您可以直接下达指令，例如：

> "请审阅文档 `doxcnABC123`，只处理包含'格式错误'的评论，并将修改后的语气调整为正式商务风格。"

#### 推荐用法：让 Claude Code 自己推理（无需外部 LLM 配置）

在 Claude Code / OpenClaw 的对话过程中，通常希望由宿主模型完成"怎么改"的推理，本技能只负责"读/写飞书"。

可用的原子工具：
- `get_comments(document_token)`: 获取评论列表
- `get_block(document_id, block_id)`: 获取指定块的文本内容
- `update_block(document_id, block_id, new_text)`: 更新块内容
- `delete_block(document_id, block_id)`: 清空整个块内容
- `delete_text_from_block(document_id, block_id, text_to_delete)`: **只删除块中选中的文本**⭐
- `reply_comment(file_token, comment_id, content)`: 回复评论
- `resolve_comment(file_token, comment_id)`: 标记评论为已解决

### CLI 工具

技能提供命令行工具，可直接处理评论：

```bash
cd /path/to/.openclaw/workspace/skills/feishu-doc-reviewer

# ⭐ 推荐：只删除批注选中的内容（保留块中其他内容）
python3 process_comment.py <document_token> <comment_id> --action delete_selected

# 删除整个段落（清空块）
python3 process_comment.py <document_token> <comment_id> --action delete

# 修改段落内容
python3 process_comment.py <document_token> <comment_id> --action modify --new-content "新内容"

# 仅回复评论（自定义处理）
python3 process_comment.py <document_token> <comment_id> --action custom

# 指定块 ID（不传则自动识别）
python3 process_comment.py <document_token> <comment_id> --block-id doxcnXXX
```

## 源代码结构

核心代码位于 `src/` 目录下：

- `src/feishu_api.py`: **飞书接口层**，封装了认证、获取评论、读取/更新/删除文档块等 API 调用。
- `src/config.py`: **配置管理**，读取环境变量。
- `process_comment.py`: **评论处理工具**，实现评论处理的完整流程（获取评论→处理块→回复→标记解决）。

## 配置要求

请确保项目根目录下的 `.env` 文件包含以下配置：

```bash
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
```

## 依赖安装

使用 pip 安装所需依赖：

```bash
pip install -r requirements.txt
```

## API 说明

### delete_block vs delete_text_from_block

| 方法 | 功能 | 使用场景 |
|------|------|----------|
| `delete_block` | 清空整个块内容 | 整个段落都需要删除 |
| `delete_text_from_block` | 只删除块中选中的文本 | 只删除批注选中的部分，保留块中其他内容 ⭐ |

**delete_text_from_block 实现说明：**

1. 首先获取块的当前内容
2. 从评论的 `quote` 字段获取要删除的文本
3. 从块内容中移除该文本
4. 用 `PATCH` 更新块

```python
# 只删除选中的文本
result = api.delete_text_from_block(document_id, block_id, text_to_delete)
if result.get("ok"):
    print(f"删除后内容：{result.get('new_content')}")
```

### resolve_comment 注意事项

必须使用 `PATCH` 方法，使用 `PUT` 会返回 404。

```python
# 正确 ✅
response = requests.patch(url, headers=headers, json={"is_solved": True})

# 错误 ❌
response = requests.put(url, headers=headers, json={"is_solved": True})  # 返回 404
```

## 常见问题

### Q: 为什么删除块返回 403 或 404？

**A:** 可能的原因：
1. 应用缺少 `docx:document:write` 权限 → 在飞书开放平台添加权限
2. 使用了错误的 API 路径 → 使用 `PATCH` 而非 `DELETE`
3. Token 过期 → 重新获取 tenant_access_token

### Q: 如何识别评论对应的块 ID？

**A:** `process_comment.py` 工具已实现自动识别逻辑：
1. 从评论的 `quote` 字段获取选中的文本
2. 遍历文档块，匹配内容
3. 返回匹配的块 ID

如果自动识别失败，可以手动指定 `--block-id`。

### Q: delete_selected 和 delete 有什么区别？

**A:** 
- `delete_selected`（推荐）：只删除批注选中的文本，保留块中其他内容
- `delete`：清空整个块内容

例如，如果一个块包含 A+B+C 三段内容，批注只选中了 B：
- `delete_selected` → 删除 B，保留 A+C
- `delete` → 删除 A+B+C（整个块清空）
