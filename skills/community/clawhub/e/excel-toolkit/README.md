# Excel Toolkit
## 专业的Excel操作工具箱 | 简化的Excel处理解决方案

<p align="center">
  <img src="https://img.shields.io/pypi/v/excel-toolkit" alt="PyPI">
  <img src="https://img.shields.io/github/stars/XiLi/excel-toolkit" alt="Stars">
  <img src="https://img.shields.io/github/license/XiLi/excel-toolkit" alt="License">
</p>

---

## 项目简介

Excel Toolkit (Excel工具箱) 是一套专业的Microsoft Excel操作工具，帮助你轻松创建、读取、编辑Excel文件。无论你是需要生成报表、处理数据还是制作模板，这个工具都能满足你的需求。

> **让Excel操作变得更简单!**

---

## 核心功能

| 功能 | 说明 |
|------|------|
| 📖 完整读写 | 单元格/区域/整个工作簿 |
| 📑 Sheet管理 | 创建/删除/选择Sheet |
| 🎨 样式设置 | 字体/颜色/对齐/边框 |
| 📐 公式支持 | 读取和写入公式 |
| 🔄 格式转换 | XLSX ↔ CSV |
| 📦 批量操作 | 合并文件/拆分文件 |
| 🎯 模板创建 | 快速生成标准模板 |

---

## 快速开始

### 安装

```bash
pip install openpyxl pandas
```

### 读取Excel

```python
from excel_parser import ExcelParser

parser = ExcelParser('data.xlsx')
df = parser.to_dataframe()
print(f"读取 {len(df)} 行")
parser.close()
```

### 写入Excel

```python
from excel_parser import ExcelParser

parser = ExcelParser('报表.xlsx')
parser.create_sheet('销售数据')
parser.write_row(1, ['日期', '销售额', '利润'])
parser.append_row(['2026-01', 10000, 2000])
parser.save()
parser.close()
```

---

## 详细功能

### 读写数据

```python
# 读取
value = parser.read_cell('A1')
data = parser.read_range('A1:C10')
all_data = parser.read_all()
df = parser.to_dataframe()

# 写入
parser.write_cell('A1', '值')
parser.write_row(1, [1,2,3])
parser.write_range('A1', [[1,2],[3,4]])
parser.append_row([1,2,3])
```

### Sheet操作

```python
sheets = parser.get_sheets()
parser.select_sheet('Sheet1')
parser.create_sheet('新Sheet')
parser.delete_sheet('Sheet2')
```

### 样式设置

```python
from openpyxl.styles import Font, PatternFill

parser.set_style('A1', font=Font(bold=True))
parser.set_column_width(1, 20)
parser.autofilter('A1:D10')
```

### XLSX转CSV

```python
excel_to_csv('中文数据.xlsx', 'data.csv')
```

### 合并文件

```python
ExcelParser.merge_files(['a.xlsx','b.xlsx'], 'merged.xlsx')
```

---

## API参考

| 方法 | 功能 |
|------|------|
| load() | 加载工作簿 |
| save() | 保存工作簿 |
| read_cell() | 读取单元格 |
| write_cell() | 写入单元格 |
| to_dataframe() | 转为DataFrame |
| create_sheet() | 创建Sheet |
| set_style() | 设置样式 |

---

## 依赖

- openpyxl
- pandas

---

## 许可证

MIT License

---

## 🔧 OpenClaw / Claude Code 使用

本技能已集成到 OpenClaw 技能系统,可直接使用:

`python
# 在 OpenClaw 或 Claude Code 中使用
from ai_workflow import run_workflow
from chart_generator import ChartGenerator
from data_parser import DataParser
from database_ops import DatabaseOps
from excel_parser import ExcelParser
from feishu_sheets import FeishuSheets
`

或通过 skills 目录调用:

`python
import sys
sys.path.insert(0, 'path/to/skills')
`

