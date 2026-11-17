---
name: excel-skills
description: Excel全栈处理技能。功能：(1)工作簿创建/读取/编辑 (2)样式与格式化（含openpyxl类型陷阱规避）(3)pandas数据导入导出与清洗 (4)多Sheet管理 (5)PDF表格转Excel (6)爬虫数据导出 (7)分析报表生成 (8)飞书云端表格。当用户需要处理xlsx文件、生成Excel报表、批量数据导出、Excel格式转换时使用此技能。
---

# Excel 处理技能

> 技能版本：v1.0
> 整理日期：2026-09-12
> 依赖：Python 3.8+, openpyxl, pandas（可选 xlsxwriter, PyMuPDF）
> 来源：整合自 workspace/skills 中 office、data-analyst、data-export、crawler、pdf、feishu-sheets 六个技能的Excel能力，并固化openpyxl实战踩坑经验

## 功能概述

覆盖Excel本地文件处理的完整链路：创建、读取、编辑、样式、多Sheet、数据分析、格式转换（PDF转Excel、CSV互转），以及飞书云端电子表格操作。核心工具脚本 `scripts/excel_toolkit.py` 可直接复用。

## 环境准备

```powershell
pip install openpyxl pandas -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

## 1. 基础操作（openpyxl）

### 创建工作簿

```python
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws['A1'] = '姓名'
ws['B1'] = '年龄'
ws.append(['张三', 25])  # 批量追加行
wb.save('output.xlsx')
```

### 读取数据

```python
wb = openpyxl.load_workbook('input.xlsx', data_only=True)  # data_only=True取公式计算结果
ws = wb.active
for row in ws.iter_rows(values_only=True):
    print(row)
```

### 编辑数据

```python
wb = openpyxl.load_workbook('input.xlsx')
ws = wb.active
ws['A1'] = '新值'
wb.save('output.xlsx')
```

## 2. 样式与格式化（重点：类型陷阱规避）

openpyxl样式对象类型严格，混用必报错。遵守两条铁律：

1. **每种样式独立赋值**：Fill、Border、Alignment、Font 是不同类型，禁止封装成混合返回值后统一存储
2. **样式对象不可复用共享**：同一Style对象赋给多个单元格时，修改会影响所有已赋单元格，需要新样式就重新构造

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# 正确：每种样式独立构造、独立赋值
header_font = Font(name='微软雅黑', bold=True, size=11, color='FFFFFF')
header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
center_align = Alignment(horizontal='center', vertical='center')
thin_border = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)

for cell in ws[1]:  # 表头行
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = center_align
    cell.border = thin_border
```

### 列宽行高与冻结

```python
ws.column_dimensions['A'].width = 20
ws.row_dimensions[1].height = 24
ws.freeze_panes = 'A2'  # 冻结表头
```

### 数字格式

```python
from openpyxl.utils import get_column_letter

for row in ws.iter_rows(min_row=2):
    row[2].number_format = '#,##0.00'      # 金额
    row[3].number_format = '0.00%'          # 百分比
    row[4].number_format = 'yyyy-mm-dd'     # 日期
```

## 3. pandas 数据通道

### 多格式读取

```python
import pandas as pd

def read_data(file_path):
    """读取各种格式数据，Excel为data_only语义"""
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith(('.xlsx', '.xls')):
        return pd.read_excel(file_path, engine='openpyxl')
    elif file_path.endswith('.json'):
        return pd.read_json(file_path)
    raise ValueError(f"Unsupported format: {file_path}")
```

### 导出

```python
df.to_excel('output.xlsx', index=False, sheet_name='数据')
df.to_csv('output.csv', index=False, encoding='utf-8-sig')  # utf-8-sig防Excel打开CSV乱码

# 多DataFrame写入多Sheet
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    df1.to_excel(writer, sheet_name='汇总', index=False)
    df2.to_excel(writer, sheet_name='明细', index=False)
```

### 数据清洗（写入Excel前预处理）

```python
def clean_data(df):
    df = df.fillna({'numeric_col': df['numeric_col'].mean(), 'cat_col': '未知'})
    df = df.drop_duplicates()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df
```

## 4. 多Sheet管理

```python
# 新建Sheet并指定位置
ws2 = wb.create_sheet('分析', 1)  # 插入到第2个位置

# 遍历所有Sheet
for name in wb.sheetnames:
    print(name, wb[name].max_row, wb[name].max_column)

# 删除Sheet
wb.remove(wb['临时表'])
```

## 5. 场景化应用

### PDF表格转Excel

```python
import pdfplumber
import pandas as pd

with pdfplumber.open('input.pdf') as pdf:
    tables = pdf.pages[0].extract_tables()
pd.DataFrame(tables[0]).to_excel('output.xlsx', index=False, header=False)
```

### 爬虫数据导出

```python
df = pd.DataFrame(products)
df.to_excel('products.xlsx', index=False, engine='openpyxl')
```

### 分析报表生成（带样式）

使用 `scripts/excel_toolkit.py` 的 `write_report` 函数，一键生成表头样式、冻结首行、自适应列宽的规范报表。

## 6. 飞书云端电子表格

云端表格与本地Excel互补，数据在飞书协作场景时使用：

```python
from feishu_sheets import action

# 读取指定范围
data = action("read_range", spreadsheet_token="sst_xxx", range="Sheet1!A1:C10")

# 写入
action("write_range", spreadsheet_token="sst_xxx", range="Sheet1!A1:C3",
       values=[["姓名","年龄"],["张三","28"]])

# 末尾追加
action("append", spreadsheet_token="sst_xxx", range="Sheet1!A:C",
       values=[["王五","25"]])
```

## 7. 实战经验（踩坑记录）

1. **openpyxl样式类型混淆陷阱**（2026-07-24）：封装函数返回混合类型（Fill/Border/Alignment）时调用方极易错误存储。规避方式就是上文第2节的两条铁律：独立赋值、独立构造。
2. **脚本永久保留原则**（2026-07-24）：skill相关脚本误删后重建成本高，本技能脚本永久存放在 `scripts/` 目录下，清理临时文件时不得触碰。
3. **Windows GBK编码**：Python脚本处理中文输出到PowerShell前必须 `sys.stdout.reconfigure(encoding='utf-8')`；CSV导出用 `utf-8-sig` 保证Excel直接打开不乱码。
4. **公式读取**：`load_workbook` 默认返回公式字符串，需要计算结果时加 `data_only=True`（前提是文件曾被Excel保存过）。
5. **性能边界**：万行以内用openpyxl直接操作；十万行以上批量写入用 `ws.append()` 循环或换pandas通道，避免逐单元格赋值。
6. **xlsxwriter vs openpyxl**：xlsxwriter写速度快但不支持读取和修改既有文件；需要读写兼备用openpyxl，一次性生成大报表可用xlsxwriter。

## 核心脚本

| 脚本 | 用途 |
|------|------|
| `scripts/excel_toolkit.py` | 一站式工具：读取（xlsx/csv/json）、规范报表写出（表头样式+冻结+列宽自适应）、PDF表格转Excel、多Sheet合并 |

## 执行步骤

1. 确认操作类型：创建新表 / 读取既有表 / 修改既有表 / 数据导出 / 格式转换
2. 检查源文件存在性和编码
3. 优先复用 `scripts/excel_toolkit.py` 既有函数，不重复造轮子
4. 样式操作严格遵守第2节两条铁律
5. 执行后验证输出：行数、表头、抽样单元格值
6. 大文件操作前先备份原文件
