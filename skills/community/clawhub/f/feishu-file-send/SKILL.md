---
name: feishu-file-send
description: 发送文件到飞书。支持图片、音频、文档等任意文件类型。
emoji: 📎
---

# Feishu File Send Skill

通过飞书发送文件（图片、音频、文档等）。

## 发送方法

### 使用 message 工具（推荐）

```python
# 发送图片
message(action="send", channel="feishu", media="/absolute/path/to/image.png", caption="图片描述")

# 发送文件（HTML、PDF、音频等）
message(action="send", channel="feishu", media="/absolute/path/to/file.pdf", caption="文件描述")

# 发送音频录音
message(action="send", channel="feishu", media="~/.openclaw/workspace/recording_latest.wav", caption="录音已降噪处理")
```

### 关键参数

- `action`: 必须为 `"send"`
- `channel`: 必须为 `"feishu"`
- `media`: 文件绝对路径（推荐）
- `file_path`: 文件路径（别名）
- `path`: 文件路径（别名）
- `caption`: 文件描述（可选）

### ⚠️ 重要规则

1. **文件必须在 workspace 目录**（安全策略 CVE-2026-26321）
   - 不要用 `/tmp/` 路径发送
   - 先复制到 workspace 再发送

2. **不要用 `message` 参数发送文件**
   - 用户将无法收到！
   - 使用 `media`、`file_path` 或 `path` 参数

3. **使用绝对路径**
   - 推荐：`~/.openclaw/workspace/filename`
   - 或：`/Users/wangbotao/.openclaw/workspace/filename`

## 工作目录

- 建议将文件复制到工作目录 `~/.openclaw/workspace/` 后发送
- 使用绝对路径

## 示例

### 发送录音

```python
# RecordMic.app 已自动复制到 workspace
message(action="send", channel="feishu", media="~/.openclaw/workspace/recording_latest.wav", caption="录音已降噪处理")
```

### 发送图片

```python
message(action="send", channel="feishu", media="~/.openclaw/workspace/screenshot.png", caption="屏幕截图")
```

### 发送文档

```python
message(action="send", channel="feishu", media="~/.openclaw/workspace/report.pdf", caption="报告")
```

### 创建并发送 PDF（完整流程）

```python
# 1. 创建 PDF 文件（内容：12345）
# 使用 Python 创建最小 PDF
import subprocess
subprocess.run(['python3', '-c', '''
pdf_content = """%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT /F1 24 Tf 100 700 Td (12345) Tj ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000266 00000 n 
0000000358 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
433
%%EOF"""
with open('/Users/wangbotao/.openclaw/workspace/test.pdf', 'w') as f:
    f.write(pdf_content)
print('Created test.pdf')
'''], cwd='/Users/wangbotao/.openclaw/workspace')

# 2. 发送 PDF
message(action="send", channel="feishu", media="/Users/wangbotao/.openclaw/workspace/test.pdf", caption="test.pdf - 内容：12345")
```

**测试结果（2026-03-10）：** 成功创建并发送 test.pdf，文件大小 580 字节，messageId: om_x100b55c3299cd8a0c2c3dc260402e23

## 故障排除

### 发送失败

- 检查文件是否在 workspace 目录
- 不要用 /tmp/ 路径
- 文件大小是否合理（> 1KB）
- 检查飞书权限（im:message, drive:file）

### 用户收不到

- 确认使用了 `media`、`file_path` 或 `path` 参数
- 不要用 `message` 参数发送文件
- 检查 channel 是否为 "feishu"

## 更新日志

- 2026-03-10: 创建 skill，文档化飞书文件发送方法
