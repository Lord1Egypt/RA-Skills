---
name: csv-wizard
description: 交互式数据清洗 CLI，支持自动类型推断、缺失值处理、重复检测
author: openclaw
version: 1.0.0
commands:
  /clean-csv: 清洗和转换 CSV 文件
---

# CSV Wizard — 交互式数据清洗工具

强大的 CSV 数据清洗和转换工具，提供自动类型推断、缺失值处理、重复检测等功能。

## 功能特性

- 🔍 自动类型推断（数字、日期、布尔值、分类变量）
- 🧹 缺失值检测与多种填充策略
- 📊 数据统计摘要与预览
- 🔄 重复行检测与删除
- 📝 列名标准化与重命名
- 🎯 数据格式转换与导出

## 使用方法

### 基本清洗

```bash
/clean-csv data.csv --output clean-data.csv
```

### 交互式清洗（推荐）

```bash
/clean-csv data.csv --interactive
```

### 预览数据信息

```bash
/clean-csv data.csv --info
```

### 处理缺失值

```bash
/clean-csv data.csv --fill-missing mean --output result.csv
```

### 删除重复行

```bash
/clean-csv data.csv --drop-duplicates --output result.csv
```

## 选项说明

| 选项 | 说明 |
|------|------|
| `--info` | 显示数据基本信息 |
| `--preview` | 预览前 N 行数据 |
| `--fill-missing` | 缺失值填充策略（drop/mean/median/mode/constant） |
| `--drop-duplicates` | 删除重复行 |
| `--standardize-names` | 标准化列名（snake_case） |
| `--interactive` | 交互式模式 |
| `--output` | 输出文件路径 |

## 缺失值填充策略

- `drop` - 删除包含缺失值的行
- `mean` - 使用列均值填充（仅数值列）
- `median` - 使用中位数填充（仅数值列）
- `mode` - 使用众数填充
- `constant` - 使用固定值填充（需配合 `--fill-value`）

## 示例

```bash
# 查看数据摘要
/clean-csv sales.csv --info

# 清洗数据：删除重复行 + 填充缺失值
/clean-csv sales.csv --drop-duplicates --fill-missing median --output clean-sales.csv

# 交互式清洗
/clean-csv data.csv --interactive

# 仅标准化列名
/clean-csv data.csv --standardize-names --output output.csv
```

## 输出说明

清洗后的 CSV 文件将保留原始格式，同时：
- 自动处理编码问题（统一为 UTF-8）
- 移除首尾空格
- 标准化布尔值（True/False）
