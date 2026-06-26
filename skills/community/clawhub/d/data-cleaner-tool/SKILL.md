# Data Cleaner Pro - 数据清洗工具

## 简介

AI驱动的数据清洗工具，自动处理Excel/CSV数据中的重复、缺失、格式错误等问题。

**适用场景**：运营报表、财务数据、客户名单清洗

## 功能特性

- ✅ **智能去重** - 保留最新/最早记录
- ✅ **缺失值处理** - 填充/删除/预测
- ✅ **格式标准化** - 手机号、邮箱、日期等
- ✅ **异常值检测** - 统计方法 + 规则方法
- ✅ **批量处理** - 多个文件同时清洗

## 使用方式

### 触发词
- "清洗数据"
- "去重处理"
- "整理Excel"

### 输入
- CSV/Excel 文件路径
- 清洗规则（可选，默认智能模式）

### 输出
- 清洗后的文件
- 清洗报告（处理了xx条，删除了xx条）

## 技术栈

- **pandas**：数据处理
- **Python**：核心逻辑
- **openpyxl**：Excel支持

## 安装依赖

```bash
pip install pandas openpyxl
```

## 使用示例

```bash
# 智能清洗
python scripts/clean_data.py data.csv

# 自定义规则
python scripts/clean_data.py data.csv --dedup --fillna mean --fix-phone

# 批量处理
python scripts/batch_clean.py folder/
```

## 使用说明

- 免费使用
- 欢迎反馈问题和建议

## 适用人群

- 运营人员：整理用户数据
- 财务人员：清洗账单数据
- 行政人员：整理员工名单
- 销售人员：客户名单去重
