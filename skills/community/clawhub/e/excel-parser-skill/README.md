# Excel Parser Skill

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/excel-parser-skill.svg)](https://badge.fury.io/py/excel-parser-skill)

Excel内容解析技能，使用 [python-calamine](https://github.com/dimastbk/python-calamine) 库提取Excel文件内容。支持多种Excel格式，包括旧版的 `.xls` 和新版的 `.xlsx`、`.xlsm` 等。

## ✨ 功能特性

- 🚀 **高性能**: 基于Rust的python-calamine库，解析速度极快
- 📊 **多格式支持**: 支持 .xls、.xlsx、.xlsm、.xltx、.xltm 格式
- 🔄 **自动降级**: 当python-calamine失败时，自动使用xlrd/openpyxl
- 📦 **自动安装**: 缺少依赖时自动尝试安装
- 📝 **结构化输出**: 提供完整的工作表结构和文本格式结果
- 🌐 **跨平台**: 支持Windows、Linux、macOS

## 📦 安装

### 从 PyPI 安装

```bash
pip install excel-parser-skill
```

### 从源码安装

```bash
git clone https://github.com/yourusername/excel-parser-skill.git
cd excel-parser-skill
pip install -e .
```

## 🚀 快速开始

### 基本使用

```python
from excel_parser import ExcelParser

# 创建解析器实例
parser = ExcelParser()

# 解析Excel文件
result = parser.parse_excel('path/to/your/file.xlsx')

# 查看结果
print(f"工作表数量: {result['sheet_count']}")
print(f"总单元格数: {result['total_cells']}")
print(f"使用引擎: {result['engine']}")

# 查看工作表数据
for sheet in result['sheets']:
    print(f"\n工作表: {sheet['name']}")
    print(f"行数: {sheet['row_count']}, 列数: {sheet['column_count']}")
```

### 转换为文本格式

```python
from excel_parser import ExcelParser

parser = ExcelParser()
text = parser.parse_excel_to_text('path/to/your/file.xls')
print(text)
```

### 使用主函数

```python
from excel_parser import process_excel

result = process_excel('path/to/your/file.xlsx')
print(result['text'])
```

### 命令行使用

```bash
python -m excel_parser your_file.xlsx
```

## 📖 详细文档

详细的使用文档请查看 [SKILL.md](./SKILL.md)

## 🛠️ 支持的文件格式

| 格式 | 扩展名 | 支持状态 |
|------|--------|----------|
| Excel 97-2003 | .xls | ✅ 支持 |
| Excel 2007+ | .xlsx | ✅ 支持 |
| Excel 宏 | .xlsm | ✅ 支持 |
| Excel 模板 | .xltx, .xltm | ✅ 支持 |

## 📤 输出格式

### 结构化数据

```python
{
    "text": "解析的文本内容",
    "sheets": [
        {
            "name": "Sheet1",
            "rows": [["A1", "B1"], ["A2", "B2"]],
            "row_count": 2,
            "column_count": 2
        }
    ],
    "sheet_count": 1,
    "total_cells": 4,
    "engine": "python-calamine"
}
```

### 文本格式

```
=== Excel文件: example.xlsx ===
工作表数量: 1
总单元格数: 4
使用引擎: python-calamine

--- 工作表: Sheet1 ---
行数: 2, 列数: 2

1: A1	B1
2: A2	B2
```

## 🔧 故障排除

### 常见问题

**Q: 安装失败怎么办？**

A: 确保Python版本>=3.7，并尝试：
```bash
pip install --upgrade pip
pip install excel-parser-skill
```

**Q: 解析失败怎么办？**

A: 检查文件是否损坏，或尝试使用备用引擎：
```python
# 会自动降级到xlrd/openpyxl
result = parser.parse_excel('file.xls')
```

**Q: 支持哪些Python版本？**

A: 支持Python 3.7及以上版本。

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用 [MIT](LICENSE.txt) 许可证。

## 🙏 致谢

- [python-calamine](https://github.com/dimastbk/python-calamine) - 高性能Excel解析库
- [xlrd](https://github.com/python-excel/xlrd) - 旧版Excel支持
- [openpyxl](https://openpyxl.readthedocs.io/) - 新版Excel支持

## 📞 联系方式

- GitHub Issues: [https://github.com/yourusername/excel-parser-skill/issues](https://github.com/yourusername/excel-parser-skill/issues)
- Email: your.email@example.com

---

如果这个项目对你有帮助，请给个 ⭐️ Star！
