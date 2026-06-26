---
name: document_parse_ocr
description: 支持文档智能识别（异步），适用于大批量文档处理场景。提交公网可访问的文件 URL，自动识别文档中的文本、表格、标题等结构信息，返回结构化的 JSON 结果文件下载地址。
version: 1.0.0
author: SCNet
license: MIT
tags:
  - OCR
  - 文档解析
  - 异步处理
required_env_vars:
  - SCNET_API_KEY
optional_env_vars:
  - SCNET_API_BASE
primary_credential: SCNET_API_KEY
dependencies:
  - python3
  - requests
input:
  - ocrType: 识别类型（可选，目前仅支持 DOC_PARSING）
  - fileUrl: 公网可访问的文件下载地址（URL）
output: 结构化的 JSON 数据，包含文档解析结果（文本、表格、图表、印章、Markdown 内容等），具体字段定义见 fields-summary.md。
---

# Sugon-Scnet 文档智能 OCR 技能

本技能封装了 Scnet OCR 文档智能服务的异步 API，支持提交公网可访问的文件 URL，自动进行文档解析（文本、表格、标题等），并通过轮询获取识别结果。

## 功能特性

- **异步处理**：适用于大批量文档，无需长时间等待同步响应
- **结构化解析**：自动识别文档中的段落、标题、表格、图表、公式、页眉页脚、脚注、印章等元素
- **结果下载**：任务成功后返回结果文件的临时下载地址（有效期为 12 小时）
- **Markdown 输出**：自动生成整页的 Markdown 内容，并映射图片/印章路径

## 前置配置

> **⚠️ 重要**：使用前需要申请 Scnet API Token
### 申请 API Token

1. 访问 [Scnet 官网](https://www.scnet.cn) 注册/登录
2. 在控制台申请 API 密钥（格式：`sc-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）
3. 复制密钥备用

### 配置 Token

**手动配置（推荐）**
1. 在技能目录下创建 `config/.env` 文件，内容如下：
```ini
# =====  Sugon-Scnet OCR API 配置 =====
# 申请地址：https://www.scnet.cn
SCNET_API_KEY=your_scnet_api_key_here

# API 基础地址（一般无需修改）
SCNET_API_BASE=https://api.scnet.cn/api/llm/v1
```
2.添加：SCNET_API_KEY=你的密钥

3.设置文件权限为 600（仅所有者可读写）
**⚠️ 安全警告**：切勿将 API Key 直接粘贴到聊天对话中，否则可能被记录或泄露。

### Token 更新

Token 过期后调用会返回 401 或 403 错误。更新方法：重新申请 Token 并替换 config/.env 中的 SCNET_API_KEY。

### 依赖安装

本技能需要 Python 3.6+ 和 requests 库。请运行以下命令：

```bash
   pip install requests
```
---
### 使用方法

### 参数说明

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|----|------|
| ocrType | string | 否  | 识别类别，目前仅支持：<br>• DOC_PARSING（默认值）|
| fileUrl | string | 是  | 待处理文件的公网可访问下载地址（支持 HTTP/HTTPS） |

### 命令行调用示例

```bash
   python .claude/skills/document_parse_ocr/scripts/main.py DOC_PARSING "https://example.com/document.pdf"
```
如果省略 ocrType，可只传 fileUrl：
```bash
   python scripts/main.py "https://example.com/document.pdf"
```

### 在 AI 对话中使用

用户可以说：

- “帮我解析这个文档：https://example.com/report.pdf”
- “对这份合同进行 OCR 识别，文件地址是 https://...”

AI 会根据 description 中的关键词自动触发本技能。

### AI 调用建议
由于任务异步处理，技能内部会自动轮询（最长等待 10 分钟，可配置）。建议在调用时设置较长的 timeout（如 600 秒），避免因轮询超时导致命令中断.

### 配置选项

编辑 `config/.env` 文件：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| SCNET_API_KEY | 必需 | Scnet API 密钥 |
| SCNET_API_BASE | https://api.scnet.cn/api/llm/v1 | API 基础地址（一般无需修改） |

### 输出

- 标准输出：识别结果的 JSON 格式。若任务成功，输出解析后的文档内容（即结果文件中的 JSON 对象）；若失败，输出错误信息。
- 错误信息：以 错误: 开头的友好提示。

### 注意事项

- 文件 URL 必须是公网可访问的下载链接（不支持本地文件路径）。如需识别本地文件，请先上传至对象存储或临时文件服务。
- 结果文件下载地址有效期为 12 小时，请及时获取。
- 异步任务最长处理时间取决于文档大小和复杂度，轮询超时默认 600 秒（10 分钟），可通过修改 POLL_TIMEOUT 变量调整。
- 技能内部会处理限流（429）重试，最多重试 3 次。

### 故障排除

| 问题 | 解决方案 |
|------|----------|
| 配置文件不存在 | 创建 config/.env 并填入 Token（参考前置配置） |
| API Key 无效/过期 | 重新申请 Token 并更新 `.env` 文件 |
| 文件 URL 无法访问 | 确保 URL 是公网可下载的，且无防火墙限制 |
| 网络连接失败 | 检查网络连接或防火墙设置 |
| 任务长时间 running | 检查文档大小是否超过限制（联系服务商） |
| 401/403/Unauthorized | Token 无效或过期，重新申请并配置 |
| 429 Too Many Requests | 请求过于频繁，技能会自动等待并重试（最多 3 次） |
| 任务失败 (failed) | 检查 error_code 和 error_message，常见原因：文件格式不支持、内容违规等 |