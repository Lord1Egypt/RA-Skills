# PDF 表格提取指南

本文档说明从 PDF 文件中提取表格数据的注意事项、常见问题和处理策略。

---

## 概述

`merge_reports.py` 使用 `pdfplumber` 库提取 PDF 中的表格。pdfplumber 基于线条检测算法，对**有明确边框线**的表格识别效果最佳。

---

## 安装依赖

```bash
pip install pdfplumber
```

---

## 提取命令

### 基本提取（提取所有页面的所有表格）

```bash
python merge_reports.py extract-pdf \
  --input report.pdf \
  --output extracted.xlsx
```

### 指定页码范围

```bash
python merge_reports.py extract-pdf \
  --input report.pdf \
  --output extracted.xlsx \
  --pages "0-5"
```

页码从 0 开始。支持范围（`"0-5"`）和列表（`"0,2,4"`）格式。

### 仅提取指定表格

```bash
python merge_reports.py extract-pdf \
  --input report.pdf \
  --output extracted.xlsx \
  --pages "3" \
  --table-index 0
```

如果一页中有多个表格，`--table-index` 指定提取第几个（从 0 开始）。

---

## 常见问题与处理策略

### 1. 表格无法识别

**现象**：`No tables found in report.pdf` 警告，输出为空。

**原因**：
- PDF 中的表格没有边框线（无边框表格）
- 表格使用空格对齐而非线条
- PDF 是扫描件（图片），非文本型 PDF

**处理策略**：
- 如果是扫描件：需要先用 OCR 工具（如 Tesseract、PaddleOCR）转换为文本
- 如果是无边框表格：尝试调整 pdfplumber 的提取策略，或在 WorkBuddy 中直接读取 PDF（Read 工具支持 PDF 内容提取）
- 备选方案：让用户将 PDF 另存为 Excel，或手动复制表格数据到 Excel

### 2. 表头识别错误

**现象**：提取的表头行不是预期的表头，可能是标题行或空行。

**原因**：PDF 表格的第一行可能包含合并单元格或标题文字。

**处理策略**：
- 使用 `--header-row` 参数跳过前面的行（在 merge 命令中可用）
- 提取后手动检查并调整表头行
- 在 WorkBuddy 中读取提取后的 Excel，用 Edit 工具修正表头

### 3. 数据错位

**现象**：某些列的数据不在正确的位置，或出现空列。

**原因**：
- PDF 表格中有合并单元格，pdfplumber 会将合并单元格拆分为多个单元格
- 表格中有跨行或跨列的合并区域

**处理策略**：
- 提取后检查数据，手动修正错位
- 对于合并单元格的数据，提取后需要向前填充（forward fill）
- 可以在 WorkBuddy 中用 Python 脚本进行数据清洗

### 4. 数字格式异常

**现象**：数字被提取为字符串，或包含逗号、括号等格式字符。

**原因**：PDF 中的数字可能使用千分位逗号（`1,234,567`）或括号表示负数（`(1,234)`）。

**处理策略**：
- `merge_reports.py` 的 `_to_numeric()` 函数会自动去除逗号
- 括号负数需要在提取后手动处理
- 建议在合并前先检查提取结果的数据类型

### 5. 多页表格拼接

**现象**：一个表格跨多页，每页都有表头行，导致提取结果中有重复表头。

**处理策略**：
- 提取后去除重复的表头行
- 在 merge 命令中使用 concat 模式时，脚本会自动跳过空行，但不会去除中间的表头行
- 建议先提取到 Excel，检查并清理后再进行合并

---

## 最佳实践

1. **先提取后检查**：始终先单独提取 PDF 表格到 Excel，检查数据完整性和准确性后，再进行合并操作。

2. **页码范围**：如果知道表格在哪几页，使用 `--pages` 参数指定，避免提取无关页面的内容。

3. **多表格处理**：如果 PDF 中有多个不同的表格，使用 `--table-index` 分别提取，避免混淆。

4. **Excel 优先**：如果同时有 Excel 和 PDF 版本的报表，优先使用 Excel 版本，数据更可靠。

5. **批量提取**：如果需要处理多个 PDF 文件，可以在 merge 命令中同时传入 Excel 和 PDF 文件，脚本会自动处理混合输入。

---

## pdfplumber 提取策略参考

pdfplumber 默认使用 `"lines"` 策略检测表格。如果效果不好，可以在脚本中尝试以下策略：

```python
# 策略1: 基于线条（默认）
tables = page.extract_tables(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines"})

# 策略2: 基于文本对齐
tables = page.extract_tables(table_settings={"vertical_strategy": "text", "horizontal_strategy": "text"})

# 策略3: 混合策略
tables = page.extract_tables(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "text"})
```

如果默认提取效果不佳，可以修改 `scripts/merge_reports.py` 中的 `extract_pdf_tables()` 函数，调整 `table_settings` 参数。
