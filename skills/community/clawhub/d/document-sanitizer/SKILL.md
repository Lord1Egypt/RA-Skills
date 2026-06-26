---
name: document-sanitizer
description: >
  Batch desensitize docx/xlsx files via keyword and regex rules, with one-click reversible restoration.
  Replace sensitive terms (company names, personal info, phone numbers, IDs, emails) with safe placeholders,
  then restore originals anytime using the unified mapping record.
description_zh: "批量对 docx/xlsx 文件执行关键字和正则脱敏替换，支持一键反向恢复"
description_en: "Batch desensitize docx/xlsx files via keyword and regex rules, with one-click reversible restoration"
license: MIT
metadata:
  version: "1.5.1"
  category: document-processing
  author: longjf25
  platform: Cross-platform
  requirements:
    - Python 3.8+
    - python-docx
    - openpyxl
    - (Optional) pywin32 + Microsoft Word for .doc auto-conversion on Windows
    - (Optional) xlrd for .xls auto-conversion
triggers:
  - desensitize documents
  - sanitize docx xlsx
  - 文档脱敏
  - 批量脱敏
  - 敏感词替换
  - 脱敏恢复
  - document sanitization
  - redact sensitive data
---

# document-sanitizer

## 技能说明 / Skill Description

### 概述 / Overview

本技能用于批量对 Word (.docx) 和 Excel (.xlsx) 文件执行脱敏处理，支持关键字精确替换和正则表达式动态替换，并提供一键恢复功能。

This skill batch-desensitizes Word (.docx) and Excel (.xlsx) files using keyword exact-match and regex dynamic replacement, with one-click reversible restoration.

### 核心特性 / Key Features

| 特性 | 说明 / Description |
|------|-------------------|
| 关键字精确替换 / Exact Match | 配置关键字对，替换为带 `[]` 标记的占位符（如"白云"→`[黑水]`）|
| 正则动态替换 / Regex Dynamic | 匹配手机号、身份证号、邮箱等，自动生成占位符如 `[RED_手机号_1]` |
| 文件名脱敏 / Filename Sanitization | 默认开启，输出文件自动使用脱敏后的文件名 |
| 统一脱敏记录 / Unified Record | 所有映射累积到 `_sanitize_record.json`，无论文档如何修改都能恢复 |
| 一键恢复 / One-Click Restore | 读取记录反向替换，还原文件名和内容，校验残留占位符 |
| 旧格式自动转换 / Legacy Format Conversion | 检测到 .doc/.xls 时提示自动转换为 .docx/.xlsx |

---

## 前置依赖 / Prerequisites

### Python 包依赖 / Python Dependencies

```bash
pip install python-docx openpyxl
```

### 可选依赖（旧格式转换）/ Optional (Legacy Format Conversion)

```bash
pip install xlrd pywin32
```

- `.doc → .docx` 转换需要 Windows + Microsoft Word（使用 Word COM 自动化）
- `.xls → .xlsx` 转换使用 xlrd + openpyxl（跨平台）

---

## 使用方法 / Usage

### 1. 准备配置文件 / Prepare Config File

在工作目录下创建 `_sanitize_config.json`：

Create `_sanitize_config.json` in your workspace:

```json
{
  "exact_rules": [
    {"pattern": "白云", "replacement": "黑水"},
    {"pattern": "南方", "replacement": "北风"},
    {"pattern": "广州", "replacement": "镇北"}
  ],
  "regex_rules": [
    {"pattern": "1[3-9]\\d{9}", "label": "手机号"},
    {"pattern": "\\d{6}(?:19|20)\\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\\d|3[01])\\d{3}[\\dXx]", "label": "身份证号"},
    {"pattern": "[a-zA-Z0-9._%+\\-]+@[a-zA-Z0-9.\\-]+\\.[a-zA-Z]{2,}", "label": "邮箱"}
  ]
}
```

### 2. 执行脱敏 / Run Sanitization

```bash
# 基本脱敏（默认脱敏文件名）
python <skill_dir>/scripts/sanitize.py sanitize <工作目录>

# 不脱敏文件名
python <skill_dir>/scripts/sanitize.py sanitize <工作目录> --no-rename

# 自动转换 .doc/.xls 旧格式文件
python <skill_dir>/scripts/sanitize.py sanitize <工作目录> --auto-convert
```

### 3. 恢复文档 / Restore Documents

```bash
python <skill_dir>/scripts/sanitize.py restore <工作目录>
```

---

## 命令行参数 / CLI Arguments

| 参数 / Argument | 说明 / Description |
|----------------|-------------------|
| `sanitize <workspace>` | 执行脱敏 / Run sanitization |
| `restore <workspace>` | 恢复文档 / Restore documents |
| `--no-rename` | 不对文件名脱敏 / Skip filename sanitization |
| `--auto-convert` | 自动转换 .doc/.xls，无需确认 / Auto-convert legacy formats |

---

## 输出目录 / Output Directories

| 目录 / Directory | 说明 / Description |
|-----------------|-------------------|
| `_sanitized_output/` | 脱敏后的文件 / Sanitized files |
| `_restored_output/` | 恢复后的文件 / Restored files |
| `_sanitize_record.json` | 统一脱敏记录（映射累积）/ Unified record (accumulative mapping) |
| `_sanitize_config.json` | 脱敏规则配置 / Sanitization rules config |

---

## 脱敏记录结构 / Record Structure

```json
{
  "version": 2,
  "created_at": "2026-04-08 16:02:07",
  "last_updated": "2026-04-08 16:02:07",
  "mapping": {
    "黑水": "白云",
    "[RED_手机号_1]": "13828417396"
  },
  "filename_mapping": {
    "黑水物流文档.docx": "白云物流文档.docx"
  },
  "runs": [
    {"timestamp": "...", "files_processed": ["..."]}
  ]
}
```

**核心原理 / Core Principle**：只要 `mapping`（脱敏值→原始值）完整，无论文档经过多少修改，都可以用它来反向替换恢复。

As long as the `mapping` (sanitized value → original value) is complete, documents can be restored regardless of modifications.

---

## 示例 / Examples

### 示例 1：基本脱敏流程 / Example 1: Basic Sanitization

```bash
# 1. 创建配置文件 _sanitize_config.json
# 2. 执行脱敏
python sanitize.py sanitize ./my-docs

# 输出:
# [RENAME] 白云物流文档.docx → 黑水物流文档.docx
# [1/1] 白云物流文档.docx [OK]
# 脱敏输出目录: ./my-docs/_sanitized_output
```

### 示例 2：脱敏后恢复 / Example 2: Sanitize then Restore

```bash
# 脱敏
python sanitize.py sanitize ./my-docs

# 恢复（可多次执行，对修改后的文档也有效）
python sanitize.py restore ./my-docs

# 输出:
# [RENAME] 黑水物流文档.docx → 白云物流文档.docx
# [OK] 无残留占位符
```

### 示例 3：处理包含旧格式文件的目录 / Example 3: Directory with Legacy Files

```bash
# 自动转换 .doc/.xls 并脱敏
python sanitize.py sanitize ./my-docs --auto-convert
```

---

## 技术要点 / Technical Notes

1. **Word run 拆分 / Run Splitting**: Word 会将文本拆分到多个 `<w:r>` 元素中，脚本先合并所有 `w:t` 文本再替换再写回，确保跨 run 的关键字也能正确匹配

   Word splits text across multiple `<w:r>` elements. The script merges all `w:t` text first, applies replacements, then writes back — ensuring cross-run keywords are correctly matched.

2. **反向替换顺序 / Reverse Order**: 恢复时按 key 长度降序替换，避免短 key 误匹配长 key 的子串

   Restoration sorts keys by length descending to prevent short keys from partially matching longer keys.

3. **脱敏范围 / Scope**: 仅支持 .docx/.xlsx 格式。.doc/.xls 旧格式需先转换（可自动完成）

   Only .docx/.xlsx are supported. Legacy .doc/.xls must be converted first (auto-conversion available).

4. **原始文件安全 / Original Safety**: 原始文件不会被修改，所有操作在输出目录中进行

   Original files are never modified — all operations happen in output directories.

---

## 错误处理 / Error Handling

| 错误 / Error | 解决方法 / Solution |
|-------------|-------------------|
| "未找到配置文件" / Config not found | 在工作目录创建 `_sanitize_config.json` |
| "python-docx import error" | 运行 / Run: `pip install python-docx` |
| "openpyxl import error" | 运行 / Run: `pip install openpyxl` |
| ".doc 转换失败" / .doc conversion failed | 确保 Windows + Word 已安装 / Ensure Word is installed |
| "残留占位符" / Residual placeholders | 检查脱敏记录是否完整 / Check record completeness |
