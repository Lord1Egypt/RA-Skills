---
name: doc_xls2docx_xlsx
description: >
  Skill for batch converting legacy Office files (.doc, .xls) to modern formats (.docx, .xlsx).
  Use when user asks to convert .doc/.xls files, migrate Office documents, or modernize document format.
  Requires Windows with Microsoft Word installed for .doc conversion; uses Python libraries for .xls conversion.
description_zh: "批量将旧版 Office 文件（.doc、.xls）转换为新版格式（.docx、.xlsx）的技能"
description_en: "Batch convert legacy Office files (.doc, .xls) to modern formats (.docx, .xlsx)"
license: MIT
metadata:
  version: "1.0.0"  # semver format: MAJOR.MINOR.PATCH
  category: document-processing
  author: User
  platform: Windows
  requirements:
    - Windows OS with Microsoft Word (for .doc conversion)
    - Python with packages: xlrd, openpyxl, pywin32, python-docx
triggers:
  - convert .doc to .docx
  - convert .xls to .xlsx
  - Office format migration
  - .doc 转换为 .docx
  - .xls 转换为 .xlsx
  - 文档格式转换
---

# doc_xls2docx_xlsx

## 技能说明 / Skill Description

### 概述 / Overview

This skill converts legacy Microsoft Office files to modern formats:
- **.doc → .docx** using Word COM automation (Windows only, requires Word)
- **.xls → .xlsx** using Python (xlrd + openpyxl, cross-platform)

本技能用于将旧版 Microsoft Office 文件转换为现代格式：
- **.doc → .docx**：使用 Word COM 自动化（仅 Windows，需要安装 Word）
- **.xls → .xlsx**：使用 Python 库（xlrd + openpyxl，跨平台）

---

## 前置依赖 / Prerequisites

### .doc → .docx 转换需要 / For .doc Conversion

**Windows 系统 + Microsoft Word 已安装**

使用 pywin32 通过 Word COM 接口进行转换，无需 LibreOffice。

Requires Windows OS and Microsoft Word installed. Uses pywin32 Word COM interface.

### .xls → .xlsx 转换需要 / For .xls Conversion

**Python 包依赖 / Python Dependencies:**

```bash
pip install xlrd openpyxl
```

---

## 使用方法 / Usage

### 1. 转换单个文件 / Convert Single File

#### .doc → .docx

```powershell
python <skill_dir>/scripts/doc_to_docx_com.py input.doc [output.docx]
```

#### .xls → .xlsx

```powershell
python <skill_dir>/scripts/xls_to_xlsx.py input.xls [output.xlsx]
```

### 2. 批量转换目录 / Batch Convert Directory

#### .doc → .docx

```powershell
python <skill_dir>/scripts/doc_to_docx_com.py "C:\path\to\directory"
```

#### .xls → .xlsx

```powershell
python <skill_dir>/scripts/xls_to_xlsx.py --batch "C:\path\to\directory"
```

---

## 转换脚本说明 / Conversion Scripts

### doc_to_docx_com.py

- **平台**: Windows only (requires Word COM)
- **功能**: 将 .doc 文件转换为 .docx 格式
- **特点**: 保留原文档格式、样式、图片等所有内容
- **原理**: 使用 pywin32 调用 Word COM 接口，以只读方式打开并另存为 .docx

### xls_to_xlsx.py

- **平台**: Cross-platform (Windows/macOS/Linux)
- **功能**: 将 .xls 文件转换为 .xlsx 格式
- **特点**: 支持多 Sheet、日期格式、字体样式、单元格对齐等
- **原理**: 使用 xlrd 读取 .xls，使用 openpyxl 创建 .xlsx

---

## 示例 / Examples

### 示例 1: 批量转换当前目录所有旧格式文件

**Example 1: Batch convert all legacy files in current directory**

```powershell
# 转换所有 .doc 文件
python doc_to_docx_com.py "C:\Users\Documents"

# 转换所有 .xls 文件
python xls_to_xlsx.py --batch "C:\Users\Documents"
```

### 示例 2: 转换单个文件并指定输出位置

**Example 2: Convert single file with output path**

```powershell
# .doc 转换
python doc_to_docx_com.py "input.doc" "output.docx"

# .xls 转换
python xls_to_xlsx.py "input.xls" "output.xlsx"
```

---

## 注意事项 / Important Notes

1. **文件覆盖**: 如果输出文件已存在，会被自动覆盖
2. **临时文件**: Word COM 转换会在同一目录生成临时文件，转换完成后自动清理
3. **大文件**: 超大 .xls 文件（>10MB）可能转换较慢
4. **编码问题**: 某些特殊字符可能出现编码问题，脚本已做处理

1. **File Overwrite**: Existing output files will be overwritten
2. **Temp Files**: Word COM creates temp files in same directory, auto-cleaned after conversion
3. **Large Files**: Very large .xls files (>10MB) may convert slowly
4. **Encoding**: Special characters are handled by the scripts

---

## 错误处理 / Error Handling

| 错误类型 | 解决方法 |
|----------|----------|
| "pywin32 not found" | 运行: `pip install pywin32` |
| "Word COM failed" | 确保 Word 已安装且可正常打开 |
| "xlrd import error" | 运行: `pip install xlrd openpyxl` |
| "Permission denied" | 关闭正在使用的源文件 |

| Error | Solution |
|--------|----------|
| "pywin32 not found" | Run: `pip install pywin32` |
| "Word COM failed" | Ensure Word is installed and can open files |
| "xlrd import error" | Run: `pip install xlrd openpyxl` |
| "Permission denied" | Close the source file if it's open |

---

## 脚本执行流程 / Script Execution Flow

### doc_to_docx_com.py 流程

1. 初始化 Python COM
2. 创建 Word Application 对象（不可见）
3. 以只读方式打开 .doc 文件
4. 另存为 .docx 格式 (FileFormat=16)
5. 关闭文档，退出 Word
6. 输出转换结果

### xls_to_xlsx.py 流程

1. 使用 xlrd 打开 .xls 文件
2. 创建新的 openpyxl 工作簿
3. 遍历每个 Sheet，复制数据
4. 处理日期、布尔值、错误类型等特殊格式
5. 保存为 .xlsx 文件
6. 输出转换结果
