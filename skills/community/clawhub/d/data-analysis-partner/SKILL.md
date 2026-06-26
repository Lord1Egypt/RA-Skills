---
name: data-analysis-partner
description: 智能数据分析 Skill，输入 CSV/Excel 文件和分析需求，输出带交互式 ECharts 图表的 HTML 自包含分析报告
metadata:
  {
    "openclaw": {
      "emoji": "📊",
      "requires": { "bins": ["python3"] }
    }
  }
---

# 数据分析 Skill

## 功能说明

本 Skill 提供 `analyze_data` 工具，能够：

1. 读取 CSV 或 Excel 数据文件（.csv / .xlsx / .xls）
2. 自动进行数据概览（行列数、字段类型、缺失值）
3. 执行统计分析（描述统计、相关性分析、异常值检测）
4. 根据用户需求生成针对性的分析和洞察
5. 输出带交互式 ECharts 图表的自包含 HTML 报告

## 触发场景

当用户出现以下意图时，应主动调用 `analyze_data` 工具：

- 上传了 CSV 或 Excel 文件，并提出分析需求
- 要求"帮我分析这份数据"、"生成数据报告"、"可视化这个文件"
- 要求找规律、找差异、找趋势、找异常
- 要求生成 BI 报告、数据洞察报告

## 调用方式

```
analyze_data(
  file_path: "<文件绝对路径>",
  requirements: "<自然语言分析需求>",
  output_dir: "<输出目录，可选>"
)
```

### 调用示例

**示例 1**：
用户说「帮我分析一下这个销售数据，各区域表现怎么样？」
→ 调用 `analyze_data(file_path="/path/to/sales.csv", requirements="分析各区域销售额差异，找出表现最好和最差的区域，给出改善建议")`

**示例 2**：
用户说「分析用户行为数据，找出流失节点」
→ 调用 `analyze_data(file_path="/path/to/users.xlsx", requirements="对用户行为数据做漏斗分析，找出主要流失节点，分析流失原因")`

**示例 3**：
用户说「分析产品退货率的影响因素」
→ 调用 `analyze_data(file_path="/path/to/orders.csv", requirements="分析产品退货率，找出与退货率相关的主要因素，给出降低退货率的建议")`

## 返回值说明

工具返回一个对象，包含：

| 字段 | 说明 |
|------|------|
| `report_path` | HTML 报告文件路径，可直接在浏览器打开 |
| `summary` | 结构化摘要数据（行列数、字段信息、关键洞察列表） |
| `charts_count` | 生成的图表数量 |
| `insights` | 规则引擎提取的关键洞察列表 |
| `open_command` | 打开报告的命令（如 `open /path/to/report.html`） |

## 报告结构

生成的 HTML 报告包含以下模块：

1. **执行摘要** — 核心发现概览卡片
2. **数据概览** — 字段类型、缺失值、基础统计表格
3. **数据洞察** — 规则引擎自动提取的关键发现
4. **可视化图表** — 交互式 ECharts 图表（分布图、柱状图、热力图、趋势图等）
5. **描述统计** — 数值列的 min/max/mean/std/quartile 详细统计
6. **分析结论** — 针对用户需求的分析总结

## 获取文件路径

如果用户上传了文件但未提供路径，使用以下方式获取：

```
# OpenClaw 上传文件后，路径通常在 ~/Downloads/ 或临时目录
# 可以用 list_files 工具确认
list_files("~/Downloads")
```

## 首次使用：安装 Python 依赖

本 Skill 在首次调用时会**自动尝试**创建隔离的 Python 环境并安装依赖。如果自动安装失败，请手动执行：

```bash
# 在 Skill 目录下创建虚拟环境
python3 -m venv ~/.openclaw/skills/data-analysis-partner/.venv

# 安装依赖
~/.openclaw/skills/data-analysis-partner/.venv/bin/pip install pandas numpy openpyxl xlrd
```

依赖安装优先级：
1. Skill 目录内置 `.venv`（隔离环境，推荐）
2. 系统 `python3`（需已安装 pandas/numpy）
3. 自动创建 `.venv` 并安装（首次运行时尝试）

## 隐私说明

生成的 HTML 报告通过 **CDN** 加载 ECharts 图表库：

```html
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
```

这意味着：
- 用浏览器**打开报告时**会向 `cdn.jsdelivr.net` 发出网络请求
- CDN 服务器可能记录访问 IP、时间等基础日志
- **报告本身的数据内容不会上传**，仅加载图表渲染库

如需完全离线查看，可在有网络时打开一次报告（ECharts 会被浏览器缓存），后续即可离线使用。

## 其他注意事项

- 大文件（>100MB）分析时间可能较长（30秒~2分钟）
- 超过 5 万行的数据集会自动随机抽样，原始行数在报告中标注
- HTML 报告自包含（图表配置内嵌），可发送给他人查看
