---
name: excel-sum
description: 计算 Excel 文件第一列数值的总和。当用户请求对 Excel 文件进行求和、统计第一列总和或类似操作时使用此技能。
---

# Excel 第一列求和技能

## 技能概述

此技能用于读取 Excel 文件（.xlsx, .xls）并计算第一列所有数值的总和。

## 使用场景

当用户请求以下操作时使用此技能：
- "Excel 求和"
- "计算 Excel 第一列总和"
- "统计 Excel 第一列"
- "Excel 第一列加起来是多少"

## 使用方法

### 步骤 1：获取 Excel 文件路径

1. 询问用户 Excel 文件的完整路径
2. 如果用户没有提供文件路径，提示用户选择或输入文件路径

### 步骤 2：执行求和脚本

运行 `scripts/sum_first_column.py` 脚本：

```
python scripts/sum_first_column.py <excel文件路径>
```

### 步骤 3：返回结果

将计算结果以友好格式展示给用户，包括：
- 总和值
- 求和的单元格数量
- 是否有非数值被跳过

## 脚本说明

- `scripts/sum_first_column.py`: Python 脚本，使用 openpyxl 读取 Excel 文件并计算第一列总和

## 依赖

- Python 3.x
- openpyxl 库（用于读取 Excel 文件）

如需安装依赖：
```bash
pip install openpyxl
```
