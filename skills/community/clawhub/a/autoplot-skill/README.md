# AutoPlot 📊 | 自动数据可视化

> Automatically visualize any data file (CSV/Excel/JSON) with one command
> 一键自动可视化任意数据文件（CSV/Excel/JSON）

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**English**: Transform any data file into beautiful charts with one command. No Python, no coding, just results.

**中文**: 用一条命令将任意数据文件转换为精美图表。无需 Python，无需编码，直接获得结果。

---

## ✨ Features | 功能特性

- **📁 Auto-Detection | 自动识别** - Detects file format, data types, relationships | 自动识别文件格式、数据类型、关系
- **📊 Smart Charts | 智能图表** - Auto-selects best chart type (line, bar, scatter, pie) | 自动选择最佳图表类型
- **🎨 Multiple Formats | 多格式输出** - PNG, SVG, HTML (interactive), PDF | PNG、SVG、HTML（交互式）、PDF
- **🎯 Professional Themes | 专业主题** - Clean, minimal, dark, colorful styles | 简洁、极简、暗黑、多彩风格

---

## 🚀 Quick Start | 快速开始

```bash
# Auto-detect and visualize | 自动检测并可视化
python3 scripts/autoplot.py visualize data.csv

# Specify output format | 指定输出格式
python3 scripts/autoplot.py visualize sales.xlsx --format html

# Custom title and theme | 自定义标题和主题
python3 scripts/autoplot.py visualize metrics.json --title "Q4 Performance" --theme dark
```

---

## 📦 Installation | 安装

### For OpenClaw Users | OpenClaw 用户

```bash
clawhub install Zaosusu/autoplot-skill
```

### Standalone Usage | 独立使用

```bash
git clone https://github.com/Zaosusu/autoplot-skill.git
cd autoplot-skill
pip install -r requirements.txt
python3 scripts/autoplot.py --version
```

---

## 🎯 Use Cases | 使用场景

### 1. Sales Data | 销售数据
```bash
python3 scripts/autoplot.py visualize sales.csv --title "Q1 Sales Performance"
```

**Output | 输出**:
- Line chart for trends | 趋势线图
- Bar chart by month | 月度柱状图
- Correlation heatmap | 相关性热力图

### 2. Interactive Dashboard | 交互式仪表板
```bash
python3 scripts/autoplot.py dashboard metrics.json --format html
```

Open `metrics_dashboard.html` in browser for interactive exploration.
在浏览器中打开 `metrics_dashboard.html` 进行交互式探索。

---

## 🛠️ Commands | 命令

### `visualize` - Create Chart | 创建图表
```bash
python3 scripts/autoplot.py visualize <file> [options]

Options | 选项:
  --chart-type    # bar, line, scatter, pie, histogram, box
  --x-column      # X-axis column | X轴列
  --y-column      # Y-axis column | Y轴列
  --title         # Chart title | 图表标题
  --theme         # default, minimal, dark | 主题
  --format        # png, svg, html, pdf | 输出格式
```

### `analyze` - Data Analysis | 数据分析
```bash
python3 scripts/autoplot.py analyze <file> [options]

Options | 选项:
  --detailed      # Show detailed statistics | 显示详细统计
```

---

## 📊 Supported Formats | 支持格式

| Format | 格式 | Description | 描述 |
|--------|------|-------------|------|
| CSV | CSV | Comma/tab delimited | 逗号/制表符分隔 |
| Excel | Excel | .xlsx, .xls | Excel 文件 |
| JSON | JSON | Array of objects | 对象数组 |

---

## 🎨 Chart Types | 图表类型

| Type | 中文 | Best For | 适用场景 |
|------|------|----------|----------|
| Line | 折线图 | Time series, trends | 时间序列、趋势 |
| Bar | 柱状图 | Comparisons, rankings | 对比、排名 |
| Scatter | 散点图 | Correlations, clusters | 相关性、聚类 |
| Pie | 饼图 | Proportions | 比例分布 |
| Histogram | 直方图 | Distributions | 数据分布 |
| Box | 箱线图 | Statistical summaries | 统计摘要 |

---

## 📄 License | 许可证

MIT License - See [LICENSE](LICENSE) file

---

**Visualize your data effortlessly | 轻松可视化你的数据** 📈
