---
name: pdf-tool
description: PDF文字提取工具 — 支持从PDF文件中提取文字内容，用于解析简历。by Barry
author: Barry
version: "1.0.0"
---

# PDF Tool — 简历 PDF 文字提取

**by Barry**

## 触发词

- "这是PDF简历"
- "上传了简历PDF"
- "PDF简历"
- "帮我提取简历内容"
- "PDF转文字"

## 使用方法

### 方式1：pdftotext（推荐，Linux/macOS/Windows）

```bash
pdftotext /path/to/resume.pdf - 2>/dev/null
```

参数说明：
- `-` 表示输出到 stdout
- 忽略 stderr 错误（如加密PDF）

### 方式2：tesseract OCR（扫描件/图片型PDF）

```bash
tesseract /path/to/resume.pdf stdout -l chi_sim+eng 2>/dev/null
```

参数说明：
- `-l chi_sim+eng`：中文简体+英文混合识别
- 可选语言包：chi_sim（简体中文）、eng（英文）、chi_tra（繁体）

### 方式3：完整PDF信息查看

```bash
# 获取PDF元信息（页数、大小、加密状态）
pdfinfo /path/to/resume.pdf 2>/dev/null

# 提取第一页文字
pdftotext -f 1 -l 1 /path/to/resume.pdf -
```

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| pdftotext: No text available | 扫描件无文字层，用 tesseract OCR |
| 加密PDF无法读取 | 告知用户需要未加密的 PDF |
| tesseract 乱码 | 检查语言包是否正确（chi_sim） |
| PDF 文件不存在 | 检查文件路径是否正确 |

## 安全提示

- PDF 处理在用户本地完成，不上传文件
- 简历可能含 PII，处理时注意脱敏
- 不使用任何外部云服务处理 PDF
