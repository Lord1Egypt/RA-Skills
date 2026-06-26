---
name: file-summary
description: |
  Local document summary tool. Activate when user mentions "总结文件", "帮我总结", "总结文档", "分析文档" or provides a local file path (txt/docx/pdf/xlsx/xls).
---

# File Summary Tool

Single tool `file_summary` for local document text extraction and summary.

## Token Extraction

From user input `帮我总结 D:\测试.pdf` → `file_path` = `D:\测试.pdf`

## Actions

### Extract Document Content

{ "action": "extract", "file_path": "D:\\测试.pdf" }

Returns:
- Success: Plain text content of the document (txt/docx/pdf/xlsx/xls)
- Error: Error message starting with ❌ (e.g. ❌ File not found, ❌ Unsupported format)

### Generate Summary

{ "action": "summary", "file_path": "D:\\测试.pdf" }

Returns: Concise summary of the document content (integrated with OpenClaw LLM)

## Workflow

To summarize a local document:
1. Extract content: `{ "action": "extract", "file_path": "your_file_path" }` → returns plain text
2. Generate summary: OpenClaw LLM summarizes the extracted text automatically

## Configuration

channels:
  local:
    tools:
      file_summary: true # default: true
      python: true # required - need Python environment

## Dependency

### Required Environment
1. Python 3.8+ (added to system environment variables)
2. Required Python packages (auto-installed by script):
   - python-docx (for docx)
   - pypdf (for pdf)
   - openpyxl (for xlsx)
   - xlrd==1.2.0 (for xls)

### Tool Path Configuration
1. Place the tool files in OpenClaw's skill folder:
   OpenClaw/skills/file-summary/
   ├─ SKILL.md (this file)
   ├─ file2sum.py
2. Set the execution command in OpenClaw:
   ${skill_path}\\file2sum.py

## Permissions

Required:
- Local file read permission (user needs to grant file access)
- Python execute permission (no special system permissions required)

## Usage

### Local Deployment
1. Put the `file-summary` folder into OpenClaw's `skills` directory
2. Restart OpenClaw
3. User input example:
   - "帮我总结 D:\测试.pdf"
   - "总结文件 D:\数据\销售表.xlsx"

### Public Deployment
1. Upload the `file-summary` folder (include md/py) to a public platform (e.g. GitHub/Gitee, ClawHub)
2. Share the download link
3. Users import via OpenClaw "Skill Market → Import from URL"