---
name: feishu-file-delivery
homepage: https://github.com/wd041216-bit/openclaw-feishu-file-delivery
description: Deliver locally generated office files back into Feishu chats as real attachments. Use when a task creates a .pptx, .pdf, .docx, .xlsx, .csv, .zip, .txt, or .md file for a Feishu user.
---

# Feishu File Delivery Skill

飞书文件交付技能 — 将本地生成的办公文件自动作为真实附件上传到飞书会话。

## Goal 目标

确保飞书收到真实的文件附件，而不仅仅是文本说明。

## Delivery Contract 交付协议

### 1. Save the artifact locally 保存文件到本地
First, generate and save the file to a real local path with an absolute path.
首先，生成文件并保存到本地绝对路径。

### 2. Write a short caption 编写简短说明
In the final Feishu reply, write a brief caption or summary (1-2 sentences).
在最终的飞书回复中，编写简短的说明或摘要（1-2 句话）。

### 3. List absolute paths on separate lines 每行一个绝对路径
Place each artifact's absolute local path on its own line with:
- No bullets (不要使用项目符号)
- No markdown link wrappers (不要使用 Markdown 链接包装)
- One path per line (每行一个路径)

### Example 示例

```text
已完成，已附上文件：
/absolute/path/to/weekly-review.pptx
/absolute/path/to/weekly-review.pdf
```

## Streaming Response Mode 流式回复模式

When working in Feishu channels, enable streaming responses for better UX:
在飞书通道工作时，启用流式回复以获得更好的用户体验：

1. Send initial acknowledgment immediately (立即发送确认)
2. Stream progress updates every 3 minutes for long tasks (长任务每 3 分钟发送进度更新)
3. Final reply includes file paths for auto-upload (最终回复包含文件路径以便自动上传)

## Supported File Types 支持的文件类型

| Extension | Type | Description |
|-----------|------|-------------|
| `.pptx` / `.ppt` | PowerPoint | 演示文稿 |
| `.pdf` | PDF | PDF 文档 |
| `.docx` / `.doc` | Word | Word 文档 |
| `.xlsx` / `.xls` | Excel | Excel 表格 |
| `.csv` | CSV | 数据表格 |
| `.zip` | Archive | 压缩包 |
| `.txt` / `.md` | Text | 文本文件 |

## Rules 规则

- ✅ Prefer absolute paths over relative paths (使用绝对路径而非相对路径)
- ✅ Do not say only "文件已生成" without the path (不要只说"文件已生成"而不提供路径)
- ✅ When the artifact is the main deliverable, always include the path (当文件是主要交付物时，始终包含路径)
- ✅ Keep the caption short so file paths stay easy to detect (保持说明简短以便路径检测)
- ✅ One path per line, no formatting (每行一个路径，无格式)

## Channel Integration 通道集成

OpenClaw's Feishu outbound adapter automatically detects and uploads files when:
OpenClaw 的飞书出站适配器会在以下情况下自动检测并上传文件：

1. Absolute file paths appear in the reply text (绝对文件路径出现在回复文本中)
2. Paths are on separate lines (路径在单独的行上)
3. Files exist at those paths (文件在这些路径上存在)

## Integration with Other Skills 与其他技能集成

This skill works seamlessly with:
- `pptx-design-director` — PPT design and creation
- `pdf-generator` — PDF generation
- `word-docx` — Word document operations
- `powerpoint-pptx` — PowerPoint manipulation
- `openclaw-slides` — HTML slide generation
- `feishu-doc` — Feishu document operations
- `feishu-sheets` — Feishu spreadsheet operations

## Usage Pattern 使用模式

```
1. Generate file locally (本地生成文件)
   → /path/to/output.pptx

2. Compose brief caption (编写简短说明)
   → "已完成演示文稿："

3. List absolute paths (列出绝对路径)
   → /path/to/output.pptx

4. Send to Feishu (发送到飞书)
   → Adapter auto-uploads attachment (适配器自动上传附件)
```

## Troubleshooting 故障排除

If files don't upload automatically:
如果文件没有自动上传：

1. Verify the file exists at the path (验证文件在路径上存在)
2. Check the path is absolute, not relative (检查路径是绝对路径而非相对路径)
3. Ensure path is on its own line (确保路径在单独的行上)
4. Remove any markdown formatting (移除任何 Markdown 格式)
5. Check Feishu adapter logs (检查飞书适配器日志)
