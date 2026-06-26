# AI Workflow Engine
## 智能工作流自动化引擎 | 让AI工作流变得像说话一样简单

<p align="center">
  <img src="https://img.shields.io/github/stars/XiLi/ai-workflow-engine" alt="Stars">
  <img src="https://img.shields.io/github/license/XiLi/ai-workflow-engine" alt="License">
  <img src="https://img.shields.io/pypi/pyversions/ai-workflow-engine" alt="Python">
</p>

---

## 📦 项目简介

**AI Workflow Engine** (智能工作流引擎) 是一套完整的AI工作流自动化框架!

- 支持**描述需求自动生成**工作流代码
- 集成**真实可用的功能**: 数据解析/Excel/数据库/图表
- 支持工作流编排/Agent协作/RAG知识库
- 可直接落地使用!

---

## ✨ 核心功能

### 🚀 描述即生成
```python
from ai_workflow import run_workflow

result = run_workflow("""
    1. 读取CSV数据
    2. 清洗去重
    3. 存入数据库
    4. 生成报表
""")
```

### 📥 数据处理
```python
from ai_workflow import DataSteps

data = DataSteps.fetch_csv("data.csv")
data = DataSteps.clean_data(data)
```

### 📊 Excel操作
```python
from ai_workflow import ExcelSteps

ExcelSteps.write_excel("output.xlsx", data)
ExcelSteps.xlsx_to_csv("input.xlsx", "output.csv")
```

### 🗄️ 数据库操作
```python
from ai_workflow import DatabaseSteps

DatabaseSteps.insert_data("app.db", "users", data)
```

### 📈 图表生成
```python
from ai_workflow import ChartSteps

ChartSteps.line_chart(data, "日期", ["销售额"], title="销售趋势")
```

---

## 📦 安装

```bash
pip install pandas openpyxl requests beautifulsoup4 matplotlib
```

---

## 💡 使用示例

### 示例1: 完整数据处理工作流
```python
from ai_workflow import run_workflow, DataSteps, ExcelSteps

# 描述方式
result = run_workflow("""
    读取CSV数据
    清洗数据
    存入数据库
    生成Excel报表
""")

# 或手动
data = DataSteps.full_clean("dirty_data.csv")
ExcelSteps.write_excel("cleaned.xlsx", data)
```

### 示例2: 数据分析
```python
from ai_workflow import DataSteps, ChartSteps

# 读取数据
data = DataSteps.fetch_csv("sales.csv")

# 生成图表
ChartSteps.line_chart(data, "date", ["sales", "profit"])
ChartSteps.bar_chart(data, "product", "sales")
ChartSteps.pie_chart(data, "category", "revenue")
```

### 示例3: 网络爬虫
```python
from ai_workflow import NetworkSteps

html = NetworkSteps.fetch_url("https://example.com")
tables = NetworkSteps.scrape_table("https://example.com/data")
```

---

## 📋 API参考

### 数据处理
| 类 | 方法 | 功能 |
|------|------|------|
| DataSteps | fetch_csv() | 读取CSV |
| DataSteps | fetch_json() | 读取JSON |
| DataSteps | fetch_xlsx() | 读取XLSX |
| DataSteps | clean_data() | 清洗数据 |
| DataSteps | full_clean() | 完整清洗 |

### Excel操作
| 类 | 方法 | 功能 |
|------|------|------|
| ExcelSteps | read_excel() | 读取 |
| ExcelSteps | write_excel() | 写入 |
| ExcelSteps | xlsx_to_csv() | 转换 |

### 数据库
| 类 | 方法 | 功能 |
|------|------|------|
| DatabaseSteps | create_table() | 创建表 |
| DatabaseSteps | insert_data() | 插入 |
| DatabaseSteps | query_data() | 查询 |
| DatabaseSteps | export_to_json() | 导出 |

### 图表
| 类 | 方法 | 功能 |
|------|------|------|
| ChartSteps | line_chart() | 折线图 |
| ChartSteps | bar_chart() | 柱状图 |
| ChartSteps | pie_chart() | 饼图 |

### 网络
| 类 | 方法 | 功能 |
|------|------|------|
| NetworkSteps | fetch_url() | 获取URL |
| NetworkSteps | parse_html() | 解析HTML |
| NetworkSteps | scrape_table() | 爬表格 |

---

## 🛠️ 依赖

```
pandas>=1.3.0
openpyxl>=3.0.0
requests>=2.25.0
beautifulsoup4>=4.9.0
matplotlib>=3.4.0
```

---

## 📄 许可证

MIT License

---

**如果对你有帮助,欢迎 ⭐ Star 支持!**

<div align="center">

**让AI工作流变得像说话一样简单!**

Made with ❤️ by XiLi

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

