# doc-extract-filter

## 元数据

### 基本信息
- **name**: doc-extract-filter
- **description**: 文件处理技能，支持多种文件格式的文本提取、关键词/正则表达式筛选、排除筛选和批量文件处理
- **version**: 1.1.1
- **author**: file-agent team
- **license**: MIT-0

### OpenClaw 配置
```json
{
  "name": "doc-extract-filter",
  "description": "文件处理技能，支持多种文件格式的文本提取、关键词/正则表达式筛选、排除筛选和批量文件处理",
  "version": "1.1.1",
  "author": "file-agent team",
  "license": "MIT-0",
  "type": "tool",
  "entry_point": "scripts/doc-extract-filter.py",
  "parameters": {
    "file_path": {
      "type": "string",
      "description": "文件路径",
      "required": false
    },
    "action": {
      "type": "string",
      "description": "操作类型：extract 或 filter",
      "required": true
    },
    "keywords": {
      "type": "array",
      "description": "关键词列表（仅 filter 操作需要）",
      "required": false
    },
    "regex": {
      "type": "string",
      "description": "正则表达式模式（仅 filter 操作需要）",
      "required": false
    },
    "enable_ocr": {
      "type": "boolean",
      "description": "启用 OCR 支持（用于扫描件 PDF）",
      "required": false
    },
    "exclude_keywords": {
      "type": "array",
      "description": "排除关键词列表（仅 filter 操作需要）",
      "required": false
    },
    "exclude_regex": {
      "type": "string",
      "description": "排除正则表达式模式（仅 filter 操作需要）",
      "required": false
    },
    "context_length": {
      "type": "integer",
      "description": "上下文长度（默认50字符）",
      "required": false
    },
    "filter_level": {
      "type": "string",
      "description": "筛选级别：line（按行）或 paragraph（按段落）",
      "required": false
    },
    "batch": {
      "type": "boolean",
      "description": "开启批量处理模式",
      "required": false
    },
    "input_dir": {
      "type": "string",
      "description": "批量处理的输入文件夹路径",
      "required": false
    },
    "file_paths": {
      "type": "array",
      "description": "批量处理的文件列表",
      "required": false
    },
    "output_dir": {
      "type": "string",
      "description": "批量结果输出目录",
      "required": false
    },
    "merge_results": {
      "type": "boolean",
      "description": "是否合并所有文件结果为一个 JSON 文件",
      "required": false
    }
  }
}
```

### CoPaw 配置
```yaml
name: doc-extract-filter
description: 文件处理技能，支持多种文件格式的文本提取、关键词/正则表达式筛选、排除筛选和批量文件处理
version: 1.1.1
author: file-agent team
license: MIT-0
type: tool
entry_point: scripts/doc-extract-filter.py
parameters:
  file_path:
    type: string
    description: 文件路径
    required: false
  action:
    type: string
    description: 操作类型：extract 或 filter
    required: true
  keywords:
    type: array
    description: 关键词列表（仅 filter 操作需要）
    required: false
  regex:
    type: string
    description: 正则表达式模式（仅 filter 操作需要）
    required: false
  enable_ocr:
    type: boolean
    description: 启用 OCR 支持（用于扫描件 PDF）
    required: false
  exclude_keywords:
    type: array
    description: 排除关键词列表（仅 filter 操作需要）
    required: false
  exclude_regex:
    type: string
    description: 排除正则表达式模式（仅 filter 操作需要）
    required: false
  context_length:
    type: integer
    description: 上下文长度（默认50字符）
    required: false
  filter_level:
    type: string
    description: 筛选级别：line（按行）或 paragraph（按段落）
    required: false
  batch:
    type: boolean
    description: 开启批量处理模式
    required: false
  input_dir:
    type: string
    description: 批量处理的输入文件夹路径
    required: false
  file_paths:
    type: array
    description: 批量处理的文件列表
    required: false
  output_dir:
    type: string
    description: 批量结果输出目录
    required: false
  merge_results:
    type: boolean
    description: 是否合并所有文件结果为一个 JSON 文件
    required: false
```

## 更新说明
- **版本 1.1.1**: 新增格式扩展+兼容性优化和筛选功能增强
  - 新增支持 CSV、Markdown（.md）、WPS（.wps/.et）文件提取
  - 修复 Excel 合并单元格、PDF 扫描件、Word 图文混排的提取问题
  - 新增 --enable-ocr 参数（可选），支持扫描件 PDF 轻量 OCR 提取
  - 新增智能格式检测逻辑，自动识别文件类型，无需用户指定
  - 新增 --exclude-keywords/--exclude-regex 参数，支持排除指定内容
  - 新增 --context-length N 参数，返回筛选结果的上下文（默认 50 字符）
  - 新增 --filter-level（line/paragraph）参数，支持按行/段落筛选
  - 批量处理模式下，筛选增强逻辑自动适配，结果按文件维度保留筛选细节
  - 依赖新增 tesseract（可选）、python-markdown，写入 requirements.txt 并标注可选
- **版本 1.1.0**: 添加了批量文件处理功能
- **版本 1.0.3**: 添加了正则表达式筛选功能
- **版本 1.0.2**: 移除了未使用的依赖，优化了项目结构

## 使用说明

### 功能
- **extract**: 提取文件中的文本内容，支持多种文件格式
- **filter**: 提取文件中的文本并筛选包含指定关键词或匹配正则表达式的内容，支持排除筛选
- **batch**: 批量处理多个文件，支持文件夹遍历和多文件列表

### 调用方式

#### CLI 调用
```bash
# 单个文件处理
python scripts/doc-extract-filter.py --file_path "path/to/file.pdf" --action "extract"
python scripts/doc-extract-filter.py --file_path "path/to/file.pdf" --action "filter" --keywords "关键词1,关键词2"
python scripts/doc-extract-filter.py --file_path "path/to/file.pdf" --action "filter" --regex "\d{4}-\d{2}-\d{2}"

# 提取 PDF 扫描件（启用 OCR）
python scripts/doc-extract-filter.py --file_path "path/to/scanned.pdf" --action "extract" --enable-ocr

# 筛选并排除指定内容
python scripts/doc-extract-filter.py --file_path "path/to/file.pdf" --action "filter" --keywords "关键词" --exclude-keywords "排除词"

# 设置上下文长度和筛选级别
python scripts/doc-extract-filter.py --file_path "path/to/file.pdf" --action "filter" --keywords "关键词" --context-length 100 --filter-level "paragraph"

# 批量处理 - 文件夹路径
python scripts/doc-extract-filter.py --batch --input-dir "path/to/folder" --action "extract" --output-dir "batch-results"

# 批量处理 - 文件列表
python scripts/doc-extract-filter.py --batch --file-paths "path/to/file1.pdf,path/to/file2.docx" --action "extract" --output-dir "batch-results"

# 批量处理并合并结果
python scripts/doc-extract-filter.py --batch --input-dir "path/to/folder" --action "extract" --output-dir "batch-results" --merge-results

# 批量筛选
python scripts/doc-extract-filter.py --batch --input-dir "path/to/folder" --action "filter" --keywords "关键词" --output-dir "batch-results"
```

#### Python 函数调用
```python
from scripts.doc_extract_filter import DocExtractFilter

# 提取文本
result = DocExtractFilter.process("path/to/file.pdf", "extract")

# 提取 PDF 扫描件（启用 OCR）
result = DocExtractFilter.process("path/to/scanned.pdf", "extract", enable_ocr=True)

# 筛选关键词
result = DocExtractFilter.process("path/to/file.pdf", "filter", ["关键词1", "关键词2"])

# 筛选并排除指定内容
result = DocExtractFilter.process("path/to/file.pdf", "filter", ["关键词"], exclude_keywords=["排除词"])

# 设置上下文长度和筛选级别
result = DocExtractFilter.process("path/to/file.pdf", "filter", ["关键词"], context_length=100, filter_level="paragraph")

# 使用正则表达式筛选
result = DocExtractFilter.process("path/to/file.pdf", "filter", regex_pattern="\d{4}-\d{2}-\d{2}")

# 批量处理 - 文件夹路径
result = DocExtractFilter.batch_process(
    input_dir="path/to/folder",
    action="extract",
    output_dir="batch-results"
)

# 批量处理 - 文件列表
result = DocExtractFilter.batch_process(
    file_paths=["path/to/file1.pdf", "path/to/file2.docx"],
    action="extract",
    output_dir="batch-results"
)

# 批量处理并合并结果
result = DocExtractFilter.batch_process(
    input_dir="path/to/folder",
    action="extract",
    output_dir="batch-results",
    merge_results=True
)
```

### 返回格式
```json
{
  "success": true,
  "data": {
    "text": "提取的文本内容",
    "filtered_text": "筛选后的文本内容" // 仅 filter 操作返回
  },
  "error": ""
}
```

### 错误处理
- 文件不存在：返回错误信息
- 不支持的文件类型：返回错误信息
- 操作失败：返回错误信息

## 安装与测试

### 安装
1. 将 `doc-extract-filter` 目录复制到 OpenClaw/CoPaw 的 skills 目录
2. 运行 `pip install -r requirements.txt` 安装依赖

### 测试
使用 `docs/test.pdf` 文件测试功能：
```bash
# 测试提取文本
python scripts/doc-extract-filter.py --file_path "docs/test.pdf" --action "extract"

# 测试关键词筛选
python scripts/doc-extract-filter.py --file_path "docs/test.pdf" --action "filter" --keywords "单价,小计,总金额"

# 测试排除筛选
python scripts/doc-extract-filter.py --file_path "docs/test.pdf" --action "filter" --keywords "单价" --exclude-keywords "小计"
```

### 独立运行
doc-extract-filter 现在包含了所有必要的核心代码，可以独立运行，不依赖于外部的 src 目录。