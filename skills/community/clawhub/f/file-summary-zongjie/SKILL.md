---
name: file-summary
description: |
  local document summary & analysis tool. 
  triggers: 
  帮我总结, 总结文件, 分析文档, 分析总结, 总结一下, 分析一下
  summarize for me, analyze for me, summarize the file, analyze the document, file summary, document analysis
  Supported formats: txt, docx, pdf, xlsx, xls
  ⚠️ Privacy Note: Extracted content will be sent to OpenClaw LLM for summary/analysis — DO NOT use with sensitive/confidential files.
---

# File Summary & Analysis Tool (文件总结与分析工具)

A universal tool for extracting text from local documents and generating summaries/analysis, supporting both Chinese and English trigger words.

## Token Extraction (参数提取)

### Chinese Input Example (中文示例)
From user input `帮我总结 D:\测试.pdf` → `file_path` = `D:\测试.pdf`

### English Input Example (英文示例)
From user input `summarize for me C:\test.pdf` → `file_path` = `C:\test.pdf`

## Actions (操作指令)

### Extract Document Content (提取文档内容)
{ "action": "extract", "file_path": "D:\\测试.pdf" }
{ "action": "extract", "file_path": "C:\\test.pdf" }

Returns (返回结果):
- Success: Plain text content of the document (txt/docx/pdf/xlsx/xls)
- Error: Error message starting with ❌ (e.g. ❌ File not found, ❌ Unsupported format)

### Generate Summary/Analysis (生成总结/分析)
{ "action": "summary", "file_path": "D:\\测试.pdf" }
{ "action": "analysis", "file_path": "C:\\test.pdf" }

Returns (返回结果):
- Summary: Concise key-point summary of the document content (integrated with OpenClaw LLM)
- Analysis: In-depth analysis of the document content (integrated with OpenClaw LLM)

## Workflow (工作流程)

To summarize/analyze a local document:
1. Extract content: `{ "action": "extract/analysis", "file_path": "your_file_path" }` → returns plain text
2. Generate result: OpenClaw LLM summarizes/analyzes the extracted text automatically

## Configuration (配置项)

channels:
  local:
    tools:
      file_summary: true # default: true
      python: true # required - need Python environment

## Dependency (依赖环境)

### Required Environment (必备环境)
1. Python 3.8+ (added to system environment variables)
2. Required Python packages (auto-installed by script):
   - python-docx (for docx)
   - pypdf (for pdf)
   - openpyxl (for xlsx)
   - xlrd==1.2.0 (for xls)

### Tool Path Configuration (工具路径配置)
1. Place the tool files in OpenClaw's skill folder:
   OpenClaw/skills/file-summary/
   ├─ SKILL.md (this file)
   ├─ file2sum.py
2. Set the execution command in OpenClaw:
   ${skill_path}\\file2sum.py

## Permissions (权限要求)

Required (必备):
- Local file read permission (user needs to grant file access)
- Python execute permission (no special system permissions required)

## Usage (使用方法)

### Local Deployment (本地部署)
1. Put the `file-summary` folder into OpenClaw's `skills` directory
2. Restart OpenClaw
3. Input Examples (输入示例):
   - Chinese (中文): "帮我总结 D:\测试.pdf", "分析文档 C:\数据\销售表.xlsx"
   - English (英文): "summarize for me C:\test.pdf", "analyze the document D:\data\sales.xlsx"

### Public Deployment (公开发布)
1. Upload the `file-summary` folder (include md/py) to a public platform (e.g. GitHub/Gitee, ClawHub)
2. Share the download link
3. Users import via OpenClaw "Skill Market → Import from URL"