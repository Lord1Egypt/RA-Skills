# Feishu Sheets Toolkit
## 飞书表格操作工具箱 | 简化的飞书在线表格处理

<p align="center">
  <img src="https://img.shields.io/github/stars/XiLi/feishu-sheets-toolkit" alt="Stars">
  <img src="https://img.shields.io/github/license/XiLi/feishu-sheets-toolkit" alt="License">
</p>

---

## 项目简介

Feishu Sheets Toolkit (飞书表格工具箱) 是飞书在线电子表格的操作工具，帮助你自动化管理飞书Sheets。无论是数据同步、批量写入还是报表自动化，这个工具都能提升你的工作效率。

> **让飞书表格操作变得更简单!**

---

## 核心功能

| 功能 | 说明 |
|------|------|
| 🔑 Token提取 | 从URL提取表格ID |
| 📝 请求构建 | 创建/读取/写入/追加请求 |
| 🔗 数据类型 | 支持公式/链接 |
| 📤 批量操作 | 批量数据同步 |

---

## 快速开始

### Token提取

```python
from feishu_sheets import FeishuSheets

# 从URL提取Token
url = 'https://xxx.feishu.cn/sheets/shtABC123?sheet=0bxxxx'
token = FeishuSheets.extract_token(url)     # shtABC123
sheet_id = FeishuSheets.extract_sheet_id(url)  # 0bxxxx
```

### 构建请求

```python
from feishu_sheets import FeishuSheets

fs = FeishuSheets()

# 创建表格
req = fs.build_create_request('销售数据表')

# 写入数据
req = fs.build_write_request(
    spreadsheet_token='shtABC123',
    sheet_id='0bxxxx',
    range='A1:C3',
    values=[
        ['日期', '销售额', '利润'],
        ['2026-01', 10000, 2000],
        ['2026-02', 15000, 3500]
    ]
)

# 追加数据
req = fs.build_append_request(
    spreadsheet_token='shtABC123',
    sheet_id='0bxxxx',
    values=[['2026-03', 12000, 1800]]
)
```

---

## 详细功能

### Token处理

```python
# 提取spreadsheet_token
token = FeishuSheets.extract_token('https://xxx.feishu.cn/sheets/shtABC123')
# 结果: shtABC123

# 提取sheet_id
sheet_id = FeishuSheets.extract_sheet_id('https://xxx.feishu.cn/sheets/shtABC123?sheet=0bxxxx')
# 结果: 0bxxxx
```

### 请求构建

```python
# 创建表格
req = fs.build_create_request('新表格')

# 读取数据
req = fs.build_read_request('shtABC', '0bxxxx', 'A1:C10')

# 添加Sheet
req = fs.build_add_sheet_request('shtABC', 'Sheet2')

# 删除Sheet
req = fs.build_delete_sheet_request('shtABC', '0bxxxx')
```

### 特殊数据类型

```python
# 公式
formula = fs.make_formula('=SUM(A1:A10)')

# 链接
link = fs.make_link('点击查看', 'https://example.com')
```

### 插入行/列

```python
# 插入行
req = fs.build_insert_dimension_request(
    spreadsheet_token='shtABC',
    sheet_id='0bxxxx',
    dimension='ROWS',
    start_index=5,
    end_index=7
)

# 删除列
req = fs.build_delete_dimension_request(
    spreadsheet_token='shtABC',
    sheet_id='0bxxxx',
    dimension='COLS',
    start_index=2,
    end_index=3
)
```

---

## 范围格式

| 格式 | 示例 |
|------|------|
| 单个单元格 | A1, B5 |
| 区域 | A1:C10, B2:D5 |
| 整列 | A:A, B:D |
| 整行 | 1:1, 3:5 |
| 带Sheet | 0bxxxx!A1:C10 |

---

## API参考

| 方法 | 功能 |
|------|------|
| extract_token() | 提取spreadsheet_token |
| extract_sheet_id() | 提取sheet_id |
| build_create_request() | 创建表格请求 |
| build_write_request() | 写入请求 |
| build_read_request() | 读取请求 |
| build_append_request() | 追加请求 |
| build_add_sheet_request() | 添加Sheet请求 |

---

## 使用前提

- 飞书开放平台应用权限
- 配置 channels.feishu

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

