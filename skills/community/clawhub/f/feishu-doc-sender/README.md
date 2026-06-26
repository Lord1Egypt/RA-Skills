# Feishu Document Sender

飞书文档发送助手 — 轻松发送 Word 和 PDF 文件。

## Installation

```bash
# Install from Clawhub
openclaw skill install feishu-doc-sender

# Or install from local zip
openclaw skill install ./feishu-doc-sender-v1.0.0.zip
```

## Usage Examples

### 发送文档给老板
```
"把AI办公入门发给老板"
→ 自动找到 AI办公入门.docx 和 AI办公入门.pdf
→ 确认后发送
```

### 只发送特定格式
```
"只要Word版本"
"发PDF给我"
```

### 使用脚本查找文件
```bash
# 查找所有文档
python3 scripts/find_docs.py

# 查找包含特定关键词的文档
python3 scripts/find_docs.py -k "报告" "2024"

# JSON 格式输出
python3 scripts/find_docs.py -k "AI" -f json
```

## Features

- ✅ 自动检测工作目录中的 .docx 和 .pdf 文件
- ✅ 支持关键词模糊匹配
- ✅ 按修改时间排序（最新优先）
- ✅ 批量发送支持
- ✅ 发送前确认机制

## File Naming Best Practices

- ✅ `项目方案_v2.docx`
- ✅ `2024年度报告.pdf`
- ✅ `AI办公入门_最终版.docx`
- ❌ `新建文档1.docx`（太通用，难匹配）

## Troubleshooting

**找不到文件？**
- 检查文件是否在工作目录
- 使用更通用的关键词
- 确认文件扩展名是 .docx 或 .pdf

**发送失败？**
- 检查飞书权限配置
- 确认接收方是飞书联系人/群组
- 检查文件大小是否超限

## License

MIT
