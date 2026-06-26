---
name: feishu-pdf-uploader
description: |
  飞书PDF文件上传器 - 将本地PDF文件上传到飞书云盘。
  使用飞书OpenAPI的upload_prepare → upload_part → upload_finish流程，
  支持大文件分片上传。
  
  Use when uploading PDF or any files to Feishu (Lark) cloud drive.
  Handles multipart/form-data upload without checksum parameter.
license: MIT
metadata:
  version: "1.0.0"
  tags: [feishu, lark, pdf, upload, cloud, drive]
  author: kimi-claw
  openclaw:
    emoji: "📤"
    requires:
      bins: [python3, python3-requests]
      config:
        - channels.feishu.accounts
---

# Feishu PDF Uploader | 飞书PDF上传器

上传本地PDF文件到飞书云盘。支持任意文件类型，不仅限于PDF。

Upload local PDF files (or any files) to Feishu (Lark) cloud drive.

## 快速开始 | Quick Start

```bash
python3 scripts/upload_pdf.py /path/to/file.pdf --folder-token FOLDER_TOKEN
```

## 使用方法 | Usage

### 命令行

```bash
python3 scripts/upload_pdf.py <file_path> [options]

Options:
  --folder-token    目标文件夹token (默认从环境变量读取)
  --app-id          飞书应用ID (默认从config读取)
  --app-secret      飞书应用密钥 (默认从config读取)
```

### Python API

```python
from upload_pdf import upload_file_to_feishu

result = upload_file_to_feishu(
    file_path="/path/to/file.pdf",
    folder_token="VnTdf2MNglfgPtdrhCxcSTdOnZd",
    app_id="cli_xxx",
    app_secret="xxx"
)
# Returns: {"success": True, "file_token": "...", "url": "..."}
```

## 工作原理 | How It Works

1. **Prepare** - 调用 `/drive/v1/files/upload_prepare` 获取 upload_id
2. **Upload** - 调用 `/drive/v1/files/upload_part` 上传文件内容
3. **Finish** - 调用 `/drive/v1/files/upload_finish` 完成上传

### 关键技术点

**⚠️ 重要**：upload_part接口**不需要** `checksum` 参数！

正确参数：
- `upload_id` - 从prepare获取
- `seq` - 分片序号（从0开始）
- `size` - 文件大小（字节）
- `file` - 文件内容（multipart/form-data）

❌ 错误：添加checksum参数 → 返回 `1061002 params error`
✅ 正确：只传upload_id/seq/size/file → 上传成功

## 配置 | Configuration

从OpenClaw配置自动读取：
- `channels.feishu.accounts[].appId`
- `channels.feishu.accounts[].appSecret`

## 错误处理 | Error Handling

| 错误码 | 原因 | 解决 |
|--------|------|------|
| 1061002 | params error | 移除checksum参数 |
| 1062008 | checksum param Invalid | 不要传checksum |
| 1061021 | upload id expire | 重新调用prepare |

## 使用场景 | Use Cases

- 上传投资报告PDF到飞书云盘
- 备份生成的文档到云端
- 批量文件上传自动化

## 安全说明 | Security

凭证仅用于获取tenant access token并上传文件。不会存储或传输到其他地方。
