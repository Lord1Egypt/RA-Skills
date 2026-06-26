---
name: deli-ocr-file-parser
description: "当用户需要将扫描版 PDF、图片、OFD、票据、合同扫描件、法院文书扫描件或其他 Agent 无法直接读取的文件解析为文本/Markdown 时使用。适用于 OCR 识别、扫描件识别、图片转文字、图片转 Markdown、PDF 转 Markdown、文件解析失败、文档无法读取、提取结果为空、乱码、扫描版文件解析不了、agent 解析不了文件、平台无法解析文件、需要调用得理 OCR 接口等场景。优先使用当前 Agent/平台原生解析能力；只有原生解析失败、结果明显不可用，或用户明确要求使用得理 OCR 时才调用接口。"
metadata:
  version: 1.0.0
---

# 得理 OCR 文件解析

## Instructions

将文件转换为可继续分析的 Markdown 或文本。默认把当前 Agent / 平台的文件解析能力放在第一优先级；得理 OCR 只作为兜底能力。

### 1. 先尝试原生解析

对每个文件先使用当前 Agent 或平台已有能力解析：

- PDF：先尝试平台 PDF 解析、`pdfplumber`、`PyMuPDF` 或同类本地解析。
- 图片或扫描件：先尝试平台视觉模型、多模态识别或内置 OCR 工具。
- Office / 表格：先尝试平台能力或 `python-docx`、`openpyxl`、CSV/JSON 解析。
- 文本、HTML、Markdown：直接读取或转换，不调用 OCR。

满足以下条件时，视为原生解析成功，不要调用得理 OCR：

- 提取文本非空，且不是大量乱码、重复页眉页脚或无意义字符。
- 扫描版 PDF 的关键页已经得到可读文字。
- 用户没有明确要求改用得理 OCR。

### 2. 失败时再调用得理 OCR

只有出现以下情况才使用 `scripts/parse_file.py`：

- 扫描版 PDF、图片、OFD 或票据图片无法被当前 Agent 解析。
- 原生解析结果为空、缺页、乱码、表格/票据关键信息无法识别。
- 用户明确说“用得理 OCR”“调用我们 OCR 接口”“这个文件 agent 解析不了”“扫描版识别一下”。

运行示例：

```bash
python3 scripts/parse_file.py <input_file> --output_dir <output_directory> --save-response
```

常用参数：

- `--lang zh-cn+en`：OCR 语言，默认中文加英文。
- `--task-type file_parsing`：接口任务类型，默认通用文件解析；也可按场景设为 `pdf_to_markdown`、`image_ocr`、`document_ocr`。
- `--save-response`：同时保存接口原始 JSON，便于排查。

输出：

- `<原文件名>.md`：可继续交给其他 skill 或 Agent 分析的 Markdown。
- `<原文件名>.ocr.json`：仅在 `--save-response` 时生成的接口响应。

### 3. 批量文件处理

对目录中的多个文件逐个判断，避免对已经能解析的文件重复调用 OCR。推荐输出到单独目录：

```text
parsed/
├── 01_合同扫描件.md
├── 02_付款回单.md
└── raw_response/
```

后续证据整理、合同审查、法律意见书等任务应直接使用已解析的 Markdown / 文本结果。

## 支持格式

得理接口支持以下上传格式：

| 类型 | 扩展名 |
|------|--------|
| 文档 | `.pdf`、`.docx`、`.doc`、`.docm`、`.dotm`、`.rtf`、`.txt`、`.ofd` |
| 表格 | `.xlsx`、`.xls` |
| 图片 | `.png`、`.jpeg`、`.gif`、`.bmp`、`.img` |
| 网页 | `.html` |

如果文件格式不支持，先提示用户转换格式，不要调用接口。

### 配置步骤

1. 前往 [https://open.delilegal.com/personal/keys](https://open.delilegal.com/personal/keys) 注册/登录
2. 创建应用并获取 API Key
3. 将 API Key 填入技能目录下的 `config.json` 文件：
   ```json
   {
     "apikey": "你的API Key"
   }
   ```

> ⚠️ **未配置 API Key 时**，不得执行检索，必须先提示用户：
> "config.json 中的 apikey 尚未配置。请前往 https://open.delilegal.com/personal/keys 创建 API Key，并填入技能目录下的 config.json 文件中。"

配置说明：

- `apikey`：得理开放平台 API Key。
- `openapiBaseUrl`：可选，用于覆盖默认接口地址；正式环境通常不需要配置。
- 兼容旧环境变量：`EVIDENCE_OCR_API_URL`、`EVIDENCE_OCR_API_TOKEN`、`EVIDENCE_FILE_API_TOKEN`、`AILAWYERS_API_KEY`。

## 使用注意

1. 不要因为 `config.json` 已配置 `apikey` 就自动调用得理 OCR。
2. 不要把大段解析文本通过命令行参数传给其他脚本；先写入 `.md` 或 `.txt` 文件。
3. 始终保留原始文件，不要原地覆盖。
4. OCR 结果必须提醒用户复核，尤其是金额、日期、姓名、案号、发票号码和银行账号。
5. 处理敏感材料时，只输出任务所需的解析结果，不在对话中粘贴完整隐私内容。
