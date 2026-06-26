# Data Parser Toolkit
## 智能数据文件处理工具箱

<p align="center">
  <img src="https://img.shields.io/github/stars/XiLi/data-parser-toolkit" alt="Stars">
  <img src="https://img.shields.io/github/license/XiLi/data-parser-toolkit" alt="License">
</p>

---

## 📦 项目简介

**Data Parser Toolkit** 是一套强大的智能数据文件处理工具,让数据处理变得更简单!

---

## ✨ 核心功能

- ✅ 50+功能方法
- ✅ 多格式支持 (CSV/JSON/XLSX/XLS/Parquet/SQL)
- ✅ 智能编码检测
- ✅ 自动修复损坏文件
- ✅ 一键数据清洗
- ✅ 批量格式转换
- ✅ 大文件流式处理
- ✅ 敏感数据脱敏

---

## 📦 安装

```bash
pip install pandas openpyxl chardet
```

---

## 💡 快速开始

```python
from data_parser import DataParser

parser = DataParser()
df = parser.parse("data.csv")  # 自动识别格式
df_clean = parser.clean_pipeline(df)  # 一键清洗
df_clean.to_csv("cleaned.csv", index=False)
```

---

## 📋 API

| 方法 | 功能 |
|------|------|
| parse() | 自动解析 |
| parse_csv() | CSV解析 |
| parse_json() | JSON解析 |
| parse_xlsx() | XLSX解析 |
| detect_encoding() | 编码检测 |
| clean_pipeline() | 一键清洗 |
| merge_files() | 合并文件 |
| xlsx_to_csv() | XLSX转CSV |

---

## 🛠️ 依赖

```
pandas
openpyxl
chardet
pyarrow (可选)
xlrd (可选)
```

---

## 📄 许可证

MIT License

---

**如果对你有帮助,欢迎 ⭐ Star 支持!**

<div align="center">Made with ❤️ by XiLi</div>