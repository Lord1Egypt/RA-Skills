# Feishu Doc Reviewer - OpenClaw 集成指南

## ✅ 安装状态

- ✅ 源代码已复制到 `/path/to/.openclaw/workspace/skills/feishu-doc-reviewer/`
- ✅ 依赖已安装（requests, python-dotenv）
- ✅ 飞书 API 测试通过（Token 获取成功）
- ✅ 工具调用脚本已创建

## 🔧 使用方法

### 方式一：直接调用工具脚本

```bash
cd /path/to/.openclaw/workspace/skills/feishu-doc-reviewer

# 获取评论列表
./run-tool.sh list_comments <document_token>

# 获取指定块内容
./run-tool.sh get_block <document_token> <block_id>

# 更新块内容
./run-tool.sh update_block <document_token> <block_id> "<new_text>"

# 回复评论
./run-tool.sh reply_comment <document_token> <comment_id> "<content>"
```

### 方式二：在 OpenClaw 对话中使用

直接在对话中告诉我你的需求，例如：

> "帮我处理飞书文档 doxcnABC123 的评论，把所有包含'格式错误'的评论都修复"

我会自动调用相应的工具来完成。

### 方式三：MCP 协议（高级）

如果你使用支持 MCP 的客户端（如 Claude Desktop），可以配置：

```json
{
  "mcpServers": {
    "feishu-reviewer": {
      "command": "python3",
      "args": ["/path/to/.openclaw/workspace/skills/feishu-doc-reviewer/src/mcp_server.py"],
      "env": {
        "FEISHU_APP_ID": "cli_xxxxxxxx",
        "FEISHU_APP_SECRET": "xxxxxxxx"
      }
    }
  }
}
```

## 📋 可用工具

| 工具名 | 功能 | 参数 |
|--------|------|------|
| `list_doc_comments` | 获取评论列表 | document_token, keyword(可选) |
| `get_block_text` | 获取段落内容 | document_token, block_id |
| `update_block_text` | 更新段落内容 | document_token, block_id, new_text |
| `export_document_markdown` | 导出全文 Markdown | document_token |
| `prepare_document_baseline` | 生成编辑基线 | document_token |

## 🔐 配置信息

- **飞书 App ID:** `cli_xxxxxxxx`
- **配置文件:** `/path/to/.openclaw/workspace/skills/feishu-doc-reviewer/.env`
- **权限要求:** 文档读写、评论读写

## ⚠️ 注意事项

1. **文档授权**：确保飞书应用已添加到目标文档（文档右上角"分享"→"添加文档应用"）
2. **Python 版本**：MCP Server 需要 Python 3.10+（当前系统为 3.9，基础功能可用）
3. **Block ID 格式**：飞书文档的块 ID 通常是 `block_id_xxx` 格式

## 🧪 测试

测试获取文档评论：
```bash
cd /path/to/.openclaw/workspace/skills/feishu-doc-reviewer
./run-tool.sh list_comments <你的文档 token>
```
