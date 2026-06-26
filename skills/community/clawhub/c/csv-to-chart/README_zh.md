# Csv To Chart

[English](./README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![版本](https://img.shields.io/badge/version-1.0-blue)

> 将表格 CSV 数据转换为可视化图表 — 支持柱状图、折线图、散点图、饼图等

## 解决什么问题

用户有原始 CSV 数据，但需要的是可视化图表而不是更多数字。这个技能解析 CSV 结构，根据数据形状选择合适的图表类型，并生成可运行的代码来渲染它。无需再导出到 Excel 才能画一个简单图表。

**触发条件：** CSV 数据 + 图表/可视化意图。

## 功能特性

- **智能图表选择** — 根据数据形状自动选择最优图表类型（分类数据→柱状图，时序数据→折线图，相关性→散点图等）
- **自动检测列类型** — 识别数值、日期、分类列并正确映射到坐标轴
- **多格式输出** — 生成 Python (matplotlib/plotly)、JavaScript (chart.js/plotly.js) 或 Mermaid 图表代码
- **处理边界情况** — 对 >7 个饼图切片发出警告，截断 >500 行数据，优雅处理缺失值

## 快速开始

### 安装

```bash
# 通过 ClawHub 安装
clawhub install csv-to-chart

# 或手动复制
cp -r csv-to-chart ~/.openclaw/skills/
```

### 使用方法

```
/csv-to-chart
```

粘贴 CSV 数据并要求生成图表——比如"用这个数据画个柱状图"。

```
/csv-to-chart/suggest
```

询问哪种图表类型适合你的数据（不生成图表）。

## 工作模式

| 模式 | 说明 |
|------|------|
| `/csv-to-chart` | 默认——读取 CSV，输出图表规格说明 + 可运行代码 |
| `/csv-to-chart/suggest` | 根据数据形状推荐最佳图表类型 |

## 示例

| 输入 | 输出 |
|------|------|
| 月度销售 CSV（月份 + 销售额） | 折线图，X 轴为月份，Y 轴为销售额 |
| 产品分类 + 数量 | 水平柱状图，>7 个分类时显示前 10 名 + "其他" |
| 两个数值列 | 带坐标轴标签的散点图 |
| 50 行数据，Q3 缺失 | 图表正常渲染，备注："3 行因 Q3 销售数据缺失已省略" |

## 目录结构

```
csv-to-chart/
├── SKILL.md          # 技能入口
├── LICENSE           # MIT 许可证
├── README.md         # 英文说明
├── README_zh.md      # 本文件
├── CONTRIBUTING.md    # 贡献指南
├── .gitignore
├── references/       # 图表类型决策树、代码模板
└── tests/            # 测试框架
```

## 许可证

本项目采用 MIT 许可证 — 详见 [LICENSE](LICENSE)。