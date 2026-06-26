# 📊 data-analysis Skill for OpenClaw

智能数据分析 Skill，输入 CSV/Excel 文件和自然语言分析需求，自动生成带 **ECharts 交互式图表**的 HTML 自包含分析报告。

## 功能特性

- 支持 `.csv` / `.xlsx` / `.xls` 文件格式
- 自动检测字段类型（数值、分类、时间、文本）
- 智能生成多种 ECharts 图表：
  - 分布直方图（数值字段）
  - 分类柱状图（分类字段）
  - 多系列对比柱状图
  - 相关性热力图
  - 时间趋势折线图（含面积填充）
  - 占比饼图
  - 缺失值分布图
- 规则引擎自动提取数据洞察（缺失值、异常值、相关性、偏态）
- 输出自包含 HTML 报告，可在浏览器中交互查看
- 支持大数据集（>5 万行自动采样）

## 安装

### 方式一：直接复制（当前已完成）

```bash
# Skill 已安装至全局目录
ls ~/.openclaw/skills/data-analysis/
```

### 方式二：OpenClaw 命令安装（发布后）

```
/skills install @custom/data-analysis
```

## 依赖环境

### 必须

- **Python 3.8+**（系统已安装）
- **pandas**：数据处理核心库
- **numpy**：数值计算

### 可选（Excel 支持）

- **openpyxl**：读取 `.xlsx` 文件
- **xlrd**：读取 `.xls` 文件

### 一键安装依赖

```bash
pip install pandas numpy openpyxl xlrd
```

## 使用方式

### 在 OpenClaw 中使用

```
你：帮我分析一下这个销售数据 /path/to/sales.csv，看各区域的差异
```

OpenClaw 会自动调用 `analyze_data` 工具，生成报告后告知你路径。

### 直接调用工具

```
analyze_data(
  file_path: "/path/to/data.csv",
  requirements: "分析各产品类别的销售额趋势，找出增长最快的类别"
)
```

### 返回值

```json
{
  "report_path": "/Users/you/Downloads/report_data_2026-03-24T10-30-00.html",
  "open_command": "open \"/Users/you/Downloads/report_data_2026-03-24T10-30-00.html\"",
  "charts_count": 7,
  "insights": ["⚠️ 字段 X 缺失率 15.3%...", "📈 A 与 B 存在强正相关..."],
  "basic_info": { "rows": 7300, "cols": 14, ... }
}
```

## 配置项

在 `openclaw.json` 中配置：

```json
{
  "skills": {
    "data-analysis": {
      "enabled": true,
      "config": {
        "outputDir": "~/Desktop/reports",
        "maxCharts": 8,
        "theme": "light"
      }
    }
  }
}
```

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `outputDir` | string | `~/Downloads` | HTML 报告输出目录 |
| `maxCharts` | number | `8` | 最多生成图表数量 |
| `theme` | string | `light` | 报告主题（当前仅 light） |

## 报告结构

生成的 HTML 报告包含：

1. **Header** — 文件名、生成时间、分析需求
2. **概览卡片** — 行数、列数、数值字段数、分类字段数、重复行、图表数、洞察数
3. **数据洞察** — 自动发现的关键问题和特征
4. **可视化图表** — 响应式 ECharts 图表网格
5. **字段信息表** — 每列的类型、缺失率、唯一值数、样本值
6. **描述统计表** — 数值列的 min/Q25/median/Q75/max/mean/std/偏度

## 文件结构

```
~/.openclaw/skills/data-analysis/
├── manifest.json       # 工具定义、权限、配置
├── SKILL.md            # AI 使用指令（告知 OpenClaw 何时及如何调用）
├── index.js            # 主逻辑：调用 Python + 生成 HTML 报告
├── scripts/
│   └── analyze.py      # Python 数据分析核心（pandas + numpy）
└── README.md           # 本文件
```

## 常见问题

**Q: 提示"缺少依赖包"或 Python 环境找不到？**

本 Skill 首次运行时会自动尝试创建 `.venv` 并安装依赖。如自动安装失败，请手动执行：

```bash
python3 -m venv ~/.openclaw/skills/data-analysis-partner/.venv
~/.openclaw/skills/data-analysis-partner/.venv/bin/pip install pandas numpy openpyxl xlrd
```

Python 环境查找优先级：
1. Skill 目录内 `.venv/bin/python3`（隔离环境）
2. 系统 `python3`（需已安装 pandas/numpy）
3. 首次运行自动创建 `.venv`

**Q: Excel 文件读取失败？**
```bash
pip install openpyxl  # .xlsx 格式
pip install xlrd      # .xls 格式
```

**Q: 图表不显示（空白）？**

ECharts 通过 CDN（jsdelivr.net）加载，需要网络连接。浏览器会缓存 ECharts 库，联网加载一次后即可离线查看。

**Q: 打开报告时有外部网络请求，有隐私风险吗？**

报告加载 ECharts 时会向 `cdn.jsdelivr.net` 发出请求，CDN 可能记录访问 IP 和时间戳等基础日志，但**报告中的数据内容不会被上传**。如在敏感环境中使用，建议先在本地缓存 ECharts 后断网查看。

**Q: 大文件分析很慢？**

超过 5 万行的数据集会自动随机采样至 5 万行进行分析，原始行数会在报告中标注。

---

*由 OpenClaw data-analysis Skill v1.0.0 提供支持*
