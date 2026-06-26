---
name: diff-tool
version: 1.0.0
description: 文本差异比较工具。比较两个文本、文件或字符串的差异，高亮显示新增、删除和修改的行。适合代码审查、文档对比、版本比对等场景。
author: OpenClaw
triggers:
  - "比较差异"
  - "文本对比"
  - "diff"
  - "找不同"
---

# Diff Tool 🧐

文本差异比较工具，快速比较两个文本或文件的差异。

## 功能

- 📝 比较两个文本字符串的差异
- 📄 比较两个文件的差异
- 🔍 高亮显示新增（绿色）、删除（红色）、修改（黄色）内容
- 📊 显示统计信息（新增/删除/修改行数）
- 🎨 支持多种输出格式（标准/简洁/JSON）

## 使用方法

### 比较两个字符串

```bash
python3 scripts/diff.py string "第一段文本" "第二段文本"
```

### 比较两个文件

```bash
python3 scripts/diff.py file /path/to/file1.txt /path/to/file2.txt
```

### 简洁输出

```bash
python3 scripts/diff.py file /path/to/file1.txt /path/to/file2.txt --format simple
```

### JSON 输出（适合程序处理）

```bash
python3 scripts/diff.py file /path/to/file1.txt /path/to/file2.txt --format json
```

## 示例

```bash
# 比较两段代码
python3 scripts/diff.py string "def hello(): print('hello')" "def hello(): print('Hello World')"

# 比较两个文件并显示统计
python3 scripts/diff.py file /tmp/a.txt /tmp/b.txt --stats

# 忽略空白字符差异
python3 scripts/diff.py string "a b" "a  b" --ignore-space
```

## 输出格式说明

- **标准格式**：完整 diff 输出，带颜色标注
- **简洁格式**：只显示有差异的行
- **JSON 格式**：机器可读的 JSON 输出，包含差异详情和统计
