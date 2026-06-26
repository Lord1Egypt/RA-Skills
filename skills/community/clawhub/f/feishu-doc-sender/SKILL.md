---
name: feishu-doc-sender
description: Send Word (.docx) and PDF documents to Feishu/Lark users and groups. Automatically detects document files in workspace and delivers them with proper formatting. Use when the user wants to send documents, reports, eBooks, or any .docx/.pdf files through Feishu.
---

# Feishu Document Sender

飞书文档发送助手 — 轻松发送 Word 和 PDF 文件到飞书对话。

## What This Skill Does

- 📄 **自动检测**工作目录中的 Word (.docx) 和 PDF 文件
- 📤 **一键发送**到飞书私聊或群聊
- 🎯 **智能匹配**根据文件名关键词找到目标文件
- 📋 **批量支持**可同时发送多个文件

## When to Use

- 发送生成的报告、书籍、文档给老板/团队
- 交付工作成果（Word/PDF格式）
- 批量分发文件到飞书群组
- 需要确认文件格式后再发送

## Usage

### 简单用法
```
User: "把AI办公入门发给老板"
→ 自动找到 AI办公入门.docx 和 AI办公入门.pdf
→ 确认后发送
```

### 指定格式
```
User: "发Word版本就行"
→ 只发送 .docx 文件

User: "只要PDF"
→ 只发送 .pdf 文件
```

### 批量发送
```
User: "把昨天的报告都发给我"
→ 查找并列出匹配的文件
→ 确认后批量发送
```

## File Detection Logic

1. **扫描工作目录** (`/workspace/`)
2. **匹配文件名**（模糊匹配，支持关键词）
3. **过滤格式**（.docx / .pdf / .epub 可选）
4. **按时间排序**（最新的优先）
5. **去重处理**（同名文件只保留最新）

## Best Practices

### 文件命名建议
为了让 Skill 更好地找到文件：
- ✅ `AI办公入门_最终版.docx`
- ✅ `2024年度报告.pdf`
- ✅ `项目方案_v2.docx`
- ❌ `新建 Microsoft Word 文档.docx`
- ❌ `final_final_FINAL.pdf`

### 发送前确认
Skill 会列出找到的文件并询问确认，避免发错：
```
找到以下文件：
1. AI办公入门_最终版.docx (31KB)
2. AI办公入门.pdf (59KB)

确认发送吗？
```

## Supported Formats

| 格式 | 扩展名 | 用途 |
|------|--------|------|
| Word 文档 | .docx | 可编辑的办公文档 |
| PDF 文档 | .pdf | 不可篡改的正式文档 |
| EPUB 电子书 | .epub | 电子书阅读器格式（可选）|

## Error Handling

- **文件不存在** → 提示用户检查文件名或重新生成
- **格式不支持** → 建议转换为 .docx 或 .pdf
- **发送失败** → 检查飞书权限和网络连接
- **文件过大** → 提示飞书单文件大小限制（通常 20-100MB）

## Integration with Other Skills

这个 Skill 通常配合以下 Skill 使用：
- `md-to-pdf` — Markdown 转 PDF 后发送
- `kdp-generator` — 生成书籍后发送给作者
- `feishu-doc` — 飞书文档操作后分享成果

## Clawhub Info

- **Version**: 1.0.0
- **Author**: OpenClaw Community
- **Tags**: feishu, lark, document, pdf, word, sender
- **License**: MIT
