---
name: encrypted-file-writer
description: 写入内容到本地加密/受保护的文件，支持企业安全策略环境。支持文本文件、Word 文档 (.docx)、Excel 表格 (.xlsx) 等 80+ 种格式，通过正确的编码处理避免乱码问题。
---

# Encrypted File Writer - 加密文件写入器

> 写入内容到本地加密/受保护的文件，支持企业安全策略环境

## 功能特性

- **多格式支持**: 80+ 种文件类型（文本、代码、配置、Office 文档）
- **编码安全**: 自动使用 UTF-8 编码，避免乱码问题
- **企业兼容**: 支持企业安全策略环境下的授权文件写入
- **灵活模式**: 支持覆盖写入和追加模式
- **标准输入**: 支持从管道或标准输入读取内容
- **目录自动创建**: 目标目录不存在时自动创建
- **Office 支持**: 直接创建/编辑 .docx 和 .xlsx（无需安装 Office）

---

## 激活条件

当用户提到以下关键词时激活：
- "写入文件"
- "保存文件"
- "创建文件"
- "写入加密文件"
- "保存受保护的文件"
- "写入内容到文件"
- "避免乱码写入"
- "企业安全策略写入"
- "写入 docx/xlsx 文件"

---

## 使用方法

### 通过 exec 工具调用

```bash
# 覆盖写入
python D:\ai\workspace\skills\encrypted-file-writer\write_file.py "文件路径" "内容"

# 追加写入
python D:\ai\workspace\skills\encrypted-file-writer\write_file.py "文件路径" "内容" --append

# 从标准输入读取
echo "内容" | python D:\ai\workspace\skills\encrypted-file-writer\write_file.py "文件路径" --stdin

# 指定编码
python D:\ai\workspace\skills\encrypted-file-writer\write_file.py "文件路径" "内容" --encoding gbk
```

### 示例

```bash
# 写入文本文件
python D:\ai\workspace\skills\encrypted-file-writer\write_file.py "E:\data\test.txt" "Hello World"

# 写入日志（追加模式）
python D:\ai\workspace\skills\encrypted-file-writer\write_file.py "E:\logs\app.log" "2026-03-08 10:00:00 - 系统启动" --append

# 写入代码文件
python D:\ai\workspace\skills\encrypted-file-writer\write_file.py "D:\project\main.py" "print('Hello')"

# 写入配置文件
python D:\ai\workspace\skills\encrypted-file-writer\write_file.py "D:\config\app.json" "{\"name\": \"test\"}"

# 写入 Word 文档
python D:\ai\workspace\skills\encrypted-file-writer\write_file.py "E:\docs\report.docx" "第一行内容"

# 追加到 Word 文档
python D:\ai\workspace\skills\encrypted-file-writer\write_file.py "E:\docs\report.docx" "追加内容" --append

# 写入 Excel 文件（CSV 格式）
python D:\ai\workspace\skills\encrypted-file-writer\write_file.py "E:\data\data.xlsx" "姓名，年龄，城市
张三，25，北京
李四，30，上海"

# 从管道写入
echo "多行内容" | python D:\ai\workspace\skills\encrypted-file-writer\write_file.py "E:\data\input.txt" --stdin
```

### 在 OpenClaw 中使用

```yaml
# 写入文件并获取结果
exec:
  command: python D:\ai\workspace\skills\encrypted-file-writer\write_file.py "文件路径" "内容"
```

---

## 支持的文件格式

| 类型 | 扩展名 | 写入方式 |
|------|--------|----------|
| **文本类** | .txt, .md, .markdown, .rst, .log, .csv, .tsv | UTF-8 文本写入 |
| **代码类** | .java, .py, .js, .ts, .jsx, .tsx, .c, .cpp, .h, .cs, .go, .rs, .rb, .php, .vue | UTF-8 文本写入 |
| **配置类** | .json, .xml, .yaml, .yml, .toml, .ini, .cfg, .properties, .gradle, .config, .env | UTF-8 文本写入 |
| **样式类** | .html, .htm, .css, .scss, .sass, .less | UTF-8 文本写入 |
| **脚本类** | .sh, .bash, .bat, .cmd, .ps1, .sql | UTF-8 文本写入 |
| **Office** | .docx (Word), .xlsx (Excel) | OpenXML ZIP 格式写入 |

---

## 写入模式

| 模式 | 参数 | 说明 |
|------|------|------|
| **覆盖写入** | (默认) | 如果文件存在则覆盖，不存在则创建 |
| **追加写入** | `--append` 或 `-a` | 在文件末尾追加内容 |

### 追加模式行为

- **文本文件**: 直接在文件末尾追加字节
- **.docx 文件**: 在文档末尾添加新段落
- **.xlsx 文件**: 在表格末尾添加新行

---

## 编码选项

| 编码 | 参数 | 适用场景 |
|------|------|----------|
| **UTF-8** | (默认) | 推荐，国际通用编码 |
| **GBK** | `--encoding gbk` | 中文 Windows 系统兼容 |
| **GB2312** | `--encoding gb2312` | 简体中文旧文件 |
| **Latin-1** | `--encoding latin1` | 西欧语言文件 |

---

## 技术原理

| 文件类型 | 处理方式 |
|----------|----------|
| **文本文件** | 内容先编码为 UTF-8 字节，再以二进制模式写入，避免编码转换问题 |
| **Word (.docx)** | 使用 zipfile 创建/修改 OpenXML 格式，在 document.xml 中添加段落 |
| **Excel (.xlsx)** | 使用 zipfile 创建/修改 OpenXML 格式，生成 sharedStrings 和 worksheet |

### .docx 写入细节

1. **创建新文件**: 生成最小 OpenXML 结构（[Content_Types].xml, _rels/, word/document.xml）
2. **追加内容**: 解压读取 document.xml，在 `</w:body>` 前插入新段落，重新打包

### .xlsx 写入细节

1. **创建新文件**: 生成最小 OpenXML 结构（workbook.xml, worksheets/, sharedStrings.xml）
2. **数据格式**: 支持 CSV 格式输入（逗号或制表符分隔）
3. **字符串处理**: 自动去重并构建共享字符串表

---

## 依赖要求

- Python 3.x（仅需标准库：sys, os, argparse, zipfile, shutil, tempfile, datetime, re, io, json）
- **无需安装额外依赖**

---

## 输出格式

**成功输出**:
```
[OK] 成功写入 XXX 字节到：文件路径
FILE_PATH=文件路径
BYTES_WRITTEN=字节数
```

**失败输出**:
```
[ERROR] 错误信息
```

---

## 使用场景

### 1. 日志记录
```bash
python write_file.py "E:\logs\app.log" "[INFO] 操作完成" --append
```

### 2. 配置文件更新
```bash
python write_file.py "D:\config\settings.json" "{\"debug\": true}"
```

### 3. 代码生成
```bash
python write_file.py "D:\project\output.py" "def main():\n    print('Hello')"
```

### 4. Word 文档创建/编辑
```bash
# 创建新文档
python write_file.py "E:\docs\report.docx" "报告标题
报告内容第一行
报告内容第二行"

# 追加到现有文档
python write_file.py "E:\docs\report.docx" "新增段落" --append
```

### 5. Excel 数据导出
```bash
python write_file.py "E:\exports\data.xlsx" "姓名，年龄，城市
张三，25，北京
李四，30，上海"
```

### 6. 临时文件创建
```bash
python write_file.py "C:\temp\task_123.txt" "任务数据..."
```

---

## 注意事项

⚠️ **重要说明**:
- 本工具仅写入用户有权限访问的本地文件
- 不支持绕过合法的文件访问控制
- 适用于企业环境中授权的文件写入场景
- 默认使用 UTF-8 编码，如需其他编码请指定 `--encoding` 参数
- 写入前会自动创建不存在的目录
- .docx/.xlsx 使用 OpenXML 标准格式，兼容 Microsoft Office 和 LibreOffice

⚠️ **Office 文件限制**:
- .docx 追加模式会在文档末尾添加新段落，不保留原有格式
- .xlsx 追加模式会重新构建整个文件，适合小数据量场景
- 复杂格式（样式、公式、图表）需要专用库（python-docx/openpyxl）

---

## 与 encrypted-file-reader 配合使用

```bash
# 读取 Word 文档
python D:\ai\workspace\skills\encrypted-file-reader\read_file.py "E:\docs\report.docx"

# 修改内容后写回
python D:\ai\workspace\skills\encrypted-file-writer\write_file.py "E:\docs\report.docx" "新内容" --append
```

---

## 法律说明

- 本工具仅用于向用户有合法访问权限的本地文件写入内容
- 不支持绕过任何合法的文件访问控制或权限管理
- 用户应确保使用本工具符合所在组织的政策和法律法规
- 本工具通过标准的文件写入 API 操作，不涉及任何安全绕过

---

## 版本

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-08 | 初始版本，支持文本/代码/配置文件写入，UTF-8 编码保护 |
| 1.1.0 | 2026-03-09 | 新增 .docx 和 .xlsx 写入支持，与 encrypted-file-reader 格式保持一致 |
