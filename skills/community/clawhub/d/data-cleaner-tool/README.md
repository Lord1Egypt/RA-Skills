# 📊 Data Cleaner Pro - 数据清洗工具

> AI驱动的数据清洗工具 | Excel/CSV全能处理

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ 功能特点

- 🚀 **智能去重** - 一键去除重复记录
- 📝 **缺失值处理** - 智能填充/删除
- 📱 **手机号修复** - 自动标准化格式
- 📅 **日期标准化** - 统一日期格式
- ⚠️ **异常值检测** - 发现数据问题
- 📦 **批量处理** - 一次处理多个文件

## 🚀 快速开始

### 安装

```bash
pip install pandas openpyxl
```

### 基本使用

```bash
# 智能清洗（自动去重+填充+修复）
python scripts/clean_data.py data.csv

# 指定输出路径
python scripts/clean_data.py data.csv --output cleaned.csv

# 自定义清洗规则
python scripts/clean_data.py data.csv --no-dedup --fillna median --fix-phone
```

### 批量处理

```bash
python scripts/batch_clean.py ./data_folder/
```

## 📋 支持的清洗操作

| 操作 | 命令 | 说明 |
|------|------|------|
| 去重 | `--no-dedup` | 默认开启，保留第一条 |
| 填充缺失值 | `--fillna mean/median/zero/none` | 默认mean |
| 修复手机号 | `--fix-phone` | 自动标准化手机号 |
| 批量处理 | `batch_clean.py` | 处理整个文件夹 |

## 📊 输出报告

每次清洗后自动生成报告：

```
📂 加载文件: data.csv
📊 原始数据: 1000行 x 10列
✓ 去重: 移除 15 条重复记录
✓ 填充缺失值: 23 处
✓ 修复手机号: 8 处

✅ 清洗完成!
📁 输出文件: data_cleaned.csv
📊 最终数据: 985行
```

## 💰 定价

完全免费使用，欢迎Star支持！

## 🎯 适用场景

- 📈 运营数据整理
- 💵 财务报表清洗
- 👥 客户名单去重
- 📋 员工信息整理
- 🛒 订单数据处理

## 📝 License

MIT License - 可以自由使用、修改、销售
