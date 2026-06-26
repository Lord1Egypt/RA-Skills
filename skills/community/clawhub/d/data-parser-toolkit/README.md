# Data Parser Toolkit
## 智能数据文件处理工具箱 | 全方位数据解析解决方案

<p align="center">
  <a href="https://pypi.org/project/data-parser-toolkit/">
    <img src="https://img.shields.io/pypi/v/data-parser-toolkit" alt="PyPI">
  </a>
  <img src="https://img.shields.io/github/stars/XiLi/data-parser-toolkit" alt="Stars">
  <img src="https://img.shields.io/github/license/XiLi/data-parser-toolkit" alt="License">
  <img src="https://img.shields.io/pypi/pyversions/data-parser-toolkit" alt="Python">
</p>

---

## 📦 项目简介

**Data Parser Toolkit** (数据解析工具箱) 是一套强大的智能数据文件处理工具,专门解决数据处理中的各种烦心事。

无论你是数据分析师、开发者还是普通用户,这个工具都能帮助你轻松应对各种数据文件难题:

- CSV文件打开乱码,不知道用什么编码?
- JSON文件损坏无法解析?
- Excel文件显示"文件损坏"?
- 批量转换文件格式太麻烦?
- 数据清洗太耗时?
- 大文件处理内存溢出?

> **让数据处理变得更简单!**

---

## ✨ 核心特性

### 🚀 50+功能方法

| 类别 | 功能 | 方法 |
|------|------|------|
| 📄 多格式解析 | 自动识别格式 | `parse()` |
| | CSV解析 | `parse_csv()` |
| | JSON解析 | `parse_json()` |
| | XLSX解析 | `parse_xlsx()` |
| | XLS解析 | `parse_xls()` |
| | Parquet解析 | `parse_parquet()` |
| | SQL解析 | `parse_sql_insert()` |
| 🔍 智能检测 | 编码检测 | `detect_encoding()` |
| | 损坏检测 | `detect_corruption()` |
| | 格式检测 | `detect_format()` |
| 🧹 数据清洗 | 一键清洗 | `clean_pipeline()` |
| | 过滤表尾 | `filter_footer_rows()` |
| | 删除空列 | `drop_empty_columns()` |
| | 类型推断 | `infer_types()` |
| | 列名标准化 | `normalize_columns()` |
| | 去重 | `remove_duplicates()` |
| 🔄 格式转换 | XLSX转CSV | `xlsx_to_csv()` |
| | 批量转换 | `convert_folder()` |
| | 编码转换 | `convert_encoding()` |
| 📊 数据处理 | 合并文件 | `merge_files()` |
| | 拆分文件 | `split_file()` |
| | 增量对比 | `get_new_records()` |
| 💾 大文件 | 流式读取 | `stream_csv()` |
| | 分块处理 | `process_chunks()` |
| 🌐 网络 | URL读取 | `parse_from_url()` |
| | 重试机制 | `parse_with_retry()` |
| | 备用方案 | `parse_with_fallback()` |
| 🛡️ 安全 | 敏感脱敏 | `mask_sensitive()` |
| | 数据校验 | `validate_data()` |
| 📅 日期处理 | 自动解析 | `parse_date()` |
| | 格式转换 | `convert_date_format()` |
| ⚙️ 配置 | 设置配置 | `set_config()` |
| | 获取配置 | `get_config()` |
| | 缓存 | `set_cache()` |

### 🎯 解决的核心痛点

| 痛点 | 解决方案 |
|------|----------|
| CSV文件打开乱码 | 🔍 智能编码自动检测 |
| JSON文件损坏 | 🔧 损坏检测+自动修复 |
| Excel文件损坏 | ⚠️ 损坏检测+提示 |
| 批量转换格式 | ⚡ 批量一键转换 |
| 数据清洗耗时 | 🧹 一键清洗pipeline |
| 大文件内存溢出 | 💾 流式分块处理 |
| 网络不稳定 | 🔄 自动重试机制 |

---

## 📦 安装

### 基础安装

```bash
pip install pandas openpyxl chardet
```

### 完整安装 (推荐)

```bash
pip install pandas openpyxl chardet pyarrow xlrd matplotlib
```

### 开发安装

```bash
git clone https://github.com/XiLi/data-parser-toolkit.git
cd data-parser-toolkit
pip install -e .
```

---

## 💡 快速开始

### 3行代码入门

```python
from data_parser import DataParser

parser = DataParser()
df = parser.parse("data.csv")  # 自动识别格式

print(f"✅ 读取成功! 共 {len(df)} 行数据")
```

### 完整示例

```python
from data_parser import DataParser

parser = DataParser()

# 1. 自动识别格式解析
df = parser.parse("data.csv")

# 2. 一键数据清洗
df_clean = parser.clean_pipeline(df)

# 3. 保存
df_clean.to_csv("cleaned.csv", index=False)
print("✅ 清洗完成!")
```

---

## 💡 详细示例

### 示例1: 自动识别多种格式

```python
from data_parser import DataParser

parser = DataParser()

# 自动识别格式
df_csv = parser.parse("data.csv")
df_json = parser.parse("data.json")
df_xlsx = parser.parse("data.xlsx")
df_parquet = parser.parse("data.parquet")
```

### 示例2: 智能编码检测

```python
from data_parser import DataParser

parser = DataParser()

# 自动检测文件编码
encoding = parser.detect_encoding("data.csv")
# 返回: 'utf-8', 'gbk', 'gb2312', 'latin1' 等

# 读取
df = parser.parse_csv("data.csv", encoding=encoding)
```

### 示例3: 检测文件是否损坏

```python
from data_parser import DataParser

parser = DataParser()

# 检测XLSX是否损坏
result = parser.detect_corruption("data.xlsx")
print(result)
# {'valid': True/False, 'errors': [...]}
```

### 示例4: 一键数据清洗

```python
from data_parser import DataParser

parser = DataParser()

# 一键清洗 (自动完成: 去重/过滤空列/类型推断)
df_clean = parser.clean_pipeline("dirty_data.csv")

# 或手动分步
df = parser.parse("data.csv")
df = parser.filter_footer_rows(df)  # 过滤表尾汇总行
df = parser.drop_empty_columns(df)  # 删除空列
df = parser.remove_duplicates(df)  # 去重
```

### 示例5: XLSX转CSV (解决中文乱码)

```python
from data_parser import DataParser

parser = DataParser()

# 转换为带BOM的UTF-8,Excel可直接打开
parser.xlsx_to_csv(
    input_path="中文数据.xlsx",
    output_path="中文数据.csv",
    encoding="utf-8-sig"  # 关键: Excel兼容编码
)
```

### 示例6: 批量转换文件夹

```python
from data_parser import DataParser

# 将文件夹内所有XLSX转CSV
DataParser.convert_folder(
    input_dir="D:/数据文件/xlsx",
    output_dir="D:/数据文件/csv",
    output_format="csv"
)
```

### 示例7: 日期智能解析

```python
from data_parser import DataParser

parser = DataParser()

# 自动识别各种日期格式
dates = [
    "2026-01-01",      # 标准
    "2026.01.01",      # 点分隔
    "2026/01/01",      # 斜杠
    "2026年01月01日",  # 中文
    "20260101",        # 纯数字
    1776181258815      # 时间戳
]

for d in dates:
    result = parser.parse_date(d)
    print(f"{d} → {result}")
```

### 示例8: 合并多个文件

```python
from data_parser import DataParser

parser = DataParser()

# 合并多个CSV
parser.merge_files(
    ["file1.csv", "file2.csv", "file3.csv"],
    "merged.csv"
)
```

### 示例9: 增量数据对比

```python
from data_parser import DataParser

parser = DataParser()

# 获取新增数据
new_records = parser.get_new_records(
    old_path="data_v1.csv",
    new_path="data_v2.csv",
    key_columns=["id", "code"]  # 主键
)

print(f"新增 {len(new_records)} 条记录")
```

### 示例10: 敏感数据脱敏

```python
from data_parser import DataParser
import pandas as pd

parser = DataParser()

# 创建测试数据
df = pd.DataFrame({
    "name": ["张三"],
    "phone": ["13812345678"],
    "email": ["test@example.com"],
    "id_card": ["320123199001011234"]
})

# 脱敏
df_masked = parser.mask_sensitive(df)

print(df_masked)
#       name      phone              email              id_card
# 0     张三  138****5678  t***@example.com  3201**********1234
```

### 示例11: 流式读取大文件

```python
from data_parser import DataParser

parser = DataParser()

# 流式读取,不占用大量内存
chunks = parser.stream_csv("big_data.csv", chunk_size=50000)

for chunk in chunks:
    # 处理每块数据
    process(chunk)
```

### 示例12: 从URL读取

```python
from data_parser import DataParser

parser = DataParser()

# 从网络URL读取
df = parser.parse_from_url("https://example.com/data.csv")
```

### 示例13: 重试机制

```python
from data_parser import DataParser

parser = DataParser()

# 网络不稳定? 自动重试3次
df = parser.parse_with_retry("https://example.com/data.csv")

# 尝试多种方式解析
df = parser.parse_with_fallback("data.csv")
```

---

## 📋 完整API参考

### 核心解析方法

| 方法 | 参数 | 功能 |
|------|------|------|
| `parse()` | path | 自动识别格式解析 |
| `parse_csv()` | path, encoding | CSV解析 |
| `parse_json()` | path | JSON解析 |
| `parse_xlsx()` | path, sheet | XLSX解析 |
| `parse_xls()` | path, sheet | XLS解析 |
| `parse_parquet()` | path | Parquet解析 |
| `parse_sql_insert()` | path | SQL INSERT解析 |

### 编码相关

| 方法 | 功能 |
|------|------|
| `detect_encoding()` | 检测文件编码 |
| `convert_encoding()` | 转换文件编码 |

### 清洗方法

| 方法 | 功能 |
|------|------|
| `clean_pipeline()` | 一键清洗 |
| `filter_footer_rows()` | 过滤表尾 |
| `drop_empty_columns()` | 删除空列 |
| `remove_duplicates()` | 去重 |
| `infer_types()` | 类型推断 |
| `normalize_columns()` | 列名标准化 |

### 工具方法

| 方法 | 功能 |
|------|------|
| `detect_corruption()` | 检测损坏 |
| `xlsx_to_csv()` | XLSX转CSV |
| `merge_files()` | 合并文件 |
| `get_new_records()` | 增量对比 |
| `stream_csv()` | 流式读取 |

### 配置方法

| 方法 | 功能 |
|------|------|
| `set_config()` | 设置配置 |
| `get_config()` | 获取配置 |
| `set_cache()` | 设置缓存 |

---

## 🛠️ 依赖

```txt
pandas>=1.3.0
openpyxl>=3.0.0
chardet>=4.0.0

# 可选
pyarrow>=5.0.0    # Parquet支持
xlrd>=2.0.0       # XLS支持
matplotlib>=3.4.0  # 图表
```

---

## 📊 支持的格式

| 格式 | 扩展名 | 状态 |
|------|--------|------|
| CSV | .csv | ✅ |
| JSON | .json | ✅ |
| Excel | .xlsx | ✅ |
| Old Excel | .xls | ✅ |
| Parquet | .parquet | ✅ |
| SQL | .sql | ✅ |

---

## 📝 示例代码

运行示例:

```bash
python examples.py
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

## 📄 许可证

MIT License - 免费商用

---

## ⭐ 支持

**如果对你有帮助,欢迎 ⭐ Star 支持!**

---

<div align="center">

**让数据处理变得更简单!**

Made with ❤️ by [XiLi](https://github.com/XiLi)

</div>

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

