---
name: excel-multi-table-merge
title: Excel多表格合并工具
description: 将工作簿中的多个表格合并为一个表格，基于指定的两列（项目名称及特征、生产规格）进行匹配汇总，合计件数和数量。
version: 1.0.0
author: MiniMax Agent
tags:
  - excel
  - merge
  - multi-table
  - openpyxl
  - data-processing
created: 2026-06-16
updated: 2026-06-16
---

# Excel多表格合并工具

## 简介

将工作簿中的多个表格合并为一个表格，基于指定的两列（项目名称及特征、生产规格）进行匹配汇总，合计件数和数量。

## 功能特性

- 自动识别各工作表的表头结构
- 基于两列完全一致的数据进行合并汇总
- 支持按关键字（梁、柱、档、板、椽、枋、机、戗）排序
- 自动过滤支架、膨胀、螺丝、镀锌等无关项目
- 读取公式计算结果（而非公式本身）

## 使用场景

当用户要求将Excel工作簿中的多个发货清单/统计表合并时使用。

## 核心代码

```python
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
from collections import defaultdict

def merge_excel_tables(input_file, output_file, ignore_keywords=None, sort_keywords=None):
    """
    合并Excel多表格

    参数:
        input_file: 输入Excel文件路径
        output_file: 输出Excel文件路径
        ignore_keywords: 需要忽略的关键词列表
        sort_keywords: 排序关键字优先级列表
    """
    if ignore_keywords is None:
        ignore_keywords = ['支架', '膨胀', '螺丝', '镀锌']

    if sort_keywords is None:
        sort_keywords = ['梁', '柱', '档', '板', '椽', '枋', '机', '戗']

    # 1. 读取数据 - 必须使用 data_only=True 获取计算后的值
    wb = openpyxl.load_workbook(input_file, data_only=True)

    # 2. 用于存储合并数据
    data_dict = defaultdict(lambda: {'count': [], 'qty': []})

    # 3. 遍历每个工作表
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]

        # 找到表头行
        header_row = None
        for row_idx in range(1, min(15, ws.max_row + 1)):
            row_values = [ws.cell(row=row_idx, column=col).value for col in range(1, 12)]
            if '序号' in str(row_values[0]) or '序号' in str(row_values):
                header_row = row_idx
                break

        if header_row is None:
            continue

        # 识别关键列
        name_col, spec_col, count_col, qty_col = identify_columns(ws, header_row)

        # 遍历数据行
        process_data_rows(ws, header_row, name_col, spec_col, count_col, qty_col,
                         data_dict, ignore_keywords)

    wb.close()

    # 4. 排序
    sorted_items = sorted(data_dict.items(), key=lambda x: get_sort_key(x, sort_keywords))

    # 5. 创建新工作簿并写入
    write_output(sorted_items, output_file)


def identify_columns(ws, header_row):
    """识别关键列索引"""
    name_col = spec_col = count_col = qty_col = None

    for col in range(1, ws.max_column + 1):
        header = ws.cell(row=header_row, column=col).value
        if header:
            header_str = str(header).strip()
            if '项目名称' in header_str or '部件名称' in header_str:
                name_col = col
            elif '生产规格' in header_str:
                spec_col = col
            elif header_str == '件':
                count_col = col
            elif '数量' in header_str and ('M)' in header_str or 'm)' in header_str):
                qty_col = col

    # 备用方案
    if name_col is None: name_col = 2
    if spec_col is None: spec_col = 4

    return name_col, spec_col, count_col, qty_col


def process_data_rows(ws, header_row, name_col, spec_col, count_col, qty_col,
                      data_dict, ignore_keywords):
    """处理数据行"""
    skip_keywords = ['包装', '合计', '税金', '总计', '说明', '甲方',
                     '现场', '施工', '制单人']

    start_row = header_row + 1
    for row_idx in range(start_row, ws.max_row + 1):
        name = ws.cell(row=row_idx, column=name_col).value
        spec = ws.cell(row=row_idx, column=spec_col).value

        name_str = str(name).strip() if name else ''
        spec_str = str(spec).strip() if spec else ''

        # 跳过空行
        if not name_str and not spec_str:
            continue

        # 过滤关键词
        if name_str and any(kw in name_str for kw in ignore_keywords):
            continue
        if spec_str and any(kw in spec_str for kw in ignore_keywords):
            continue

        # 跳过无效行
        if name_str and any(kw in name_str for kw in skip_keywords):
            continue

        # 获取件数和数量
        count = get_numeric_value(ws.cell(row=row_idx, column=count_col).value) if count_col else 0
        qty = get_numeric_value(ws.cell(row=row_idx, column=qty_col).value) if qty_col else 0

        if count > 0 or qty > 0:
            key = (name_str if name_str else spec_str, spec_str if spec_str else name_str)
            if count > 0:
                data_dict[key]['count'].append(count)
            if qty > 0:
                data_dict[key]['qty'].append(qty)


def get_numeric_value(value):
    """获取数值"""
    if isinstance(value, (int, float)):
        return value
    if value is None or value == '':
        return 0
    return 0


def get_sort_key(item, sort_keywords):
    """排序键"""
    name = item[0][0].lower()

    for i, keyword in enumerate(sort_keywords):
        if keyword in name:
            return (i, name, item[0][1])

    return (len(sort_keywords), name, item[0][1])


def write_output(sorted_items, output_file):
    """写入输出文件"""
    new_wb = openpyxl.Workbook()
    ws = new_wb.active
    ws.title = "合并清单"

    # 表头
    headers = ['序号', '项目名称及特征', '生产规格', '合计件数', '合计数量']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center')

    # 边框样式
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )

    # 写入数据
    for idx, (key, data) in enumerate(sorted_items, 1):
        total_count = sum(data['count'])
        total_qty = sum(data['qty'])

        ws.cell(row=idx+1, column=1, value=idx)
        ws.cell(row=idx+1, column=2, value=key[0])
        ws.cell(row=idx+1, column=3, value=key[1])
        ws.cell(row=idx+1, column=4, value=int(total_count) if total_count == int(total_count) else round(total_count, 2) if total_count > 0 else '')
        ws.cell(row=idx+1, column=5, value=round(total_qty, 2) if total_qty > 0 else '')

        for col in range(1, 6):
            ws.cell(row=idx+1, column=col).border = thin_border

    # 调整列宽
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 35
    ws.column_dimensions['C'].width = 30
    ws.column_dimensions['D'].width = 15
    ws.column_dimensions['E'].width = 15

    new_wb.save(output_file)


# 使用示例
if __name__ == "__main__":
    input_file = "user_input_files/发货清单.xlsx"
    output_file = "/workspace/合并发货清单汇总.xlsx"
    merge_excel_tables(input_file, output_file)
    print(f"已合并 {len(data_dict)} 个不同项目")
```

## 关键注意事项

### ⚠️ 重要：data_only=True

**必须使用 `data_only=True`** 读取Excel文件，否则会读到公式字符串（如 `=F5*3`）而非计算结果。

```python
# ✅ 正确：读取计算后的值
wb = openpyxl.load_workbook(file, data_only=True)

# ❌ 错误：读到公式字符串
wb = openpyxl.load_workbook(file)
```

### 列识别

不同工作表的列位置可能不同，需要根据表头动态识别：
- 项目名称列：表头包含"项目名称"或"部件名称"
- 生产规格列：表头包含"生产规格"
- 件数列：表头为"件"
- 数量列：表头包含"数量"和"M)"或"m)"

### 数据过滤

自动过滤：
- 忽略词：`支架`、`膨胀`、`螺丝`、`镀锌`
- 跳过行：`包装`、`合计`、`税金`、`总计`、`说明`、`甲方`、`现场`、`施工`

## 输出文件

生成的Excel文件包含5列：
| 列 | 说明 |
|---|---|
| A | 序号 |
| B | 项目名称及特征 |
| C | 生产规格 |
| D | 合计件数 |
| E | 合计数量 |