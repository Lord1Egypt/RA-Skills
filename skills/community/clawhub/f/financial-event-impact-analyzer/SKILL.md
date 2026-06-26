---
name: financial-event-impact-analyzer
description: "Analyze historical impact of financial events on related assets. Kensho-style event-driven analysis. Use when: asking about asset reactions to events (oil surge, gold rise, rate hikes), historical precedent analysis, causal indicator relationships. Outputs Chinese reports and charts."
dependencies:
  - python3
  - pandas
  - numpy
  - matplotlib
  - yfinance
  - tushare (TUSHARE_TOKEN env variable)
  - chinese-fonts: SimHei / WenQuanYi Micro Hei / Noto Sans CJK SC
env:
  TUSHARE_TOKEN:
    required: true
    description: "Tushare Pro API Token for Chinese A-share market data. Register at: https://tushare.pro/register"
    sensitive: true
  FRED_API_KEY:
    required: false
    description: "FRED API Key for US macroeconomic data (optional). Register at: https://fred.stlouisfed.org/docs/api/api_key.html"
    sensitive: true
---

# Financial Event Impact Analyzer (金融事件影响分析器)

## Overview

分析特定金融事件发生时相关资产的历史表现。类似 Kensho 的事件驱动分析：识别事件 → 查找历史先例 → 推论相关资产 → 分析历史表现。

**输出**: 中文分析报告 + 中文标注图表

---

## 环境依赖

### ⚠️ 前置检查（重要）

**每次执行前必须检查**:

| 检查项 | 命令 | 失败修复 |
|--------|------|---------|
| **中文字体** | `fc-list :lang=zh family` | `sudo apt install fonts-wqy-microhei fonts-noto-cjk` |
| **TUSHARE_TOKEN** | `echo $TUSHARE_TOKEN` | 在 ~/.bashrc 中设置 |
| **输出目录** | `mkdir -p memory/reports/` | 确保有写权限 |

**自动检查**: `generate_charts.py` 会自动执行前置检查，输出结果。

### Python 包依赖

```bash
pip install yfinance pandas numpy matplotlib tushare
```

### 🔤 中文字体依赖（重要）

图表使用中文标注，需要系统安装中文字体：

| 系统 | 安装命令 |
|------|---------|
| **Ubuntu/Debian** | `sudo apt install fonts-wqy-microhei fonts-noto-cjk` |
| **CentOS/RHEL** | `sudo yum install wqy-microhei-fonts` |
| **macOS** | 系统自带 PingFang SC / Heiti SC |
| **Windows** | 系统自带 SimHei（黑体） |

**验证字体**:
```bash
# 查看可用中文字体
fc-list :lang=zh family

# matplotlib 查找字体
python3 -c "import matplotlib.font_manager; print([f.name for f in matplotlib.font_manager.fontManager.ttflist if 'Hei' in f.name or 'Noto' in f.name])"
```

**备选字体优先级**:
1. `SimHei` (黑体，Windows/macOS)
2. `WenQuanYi Micro Hei` (Linux常用)
3. `Noto Sans CJK SC` (现代Linux)
4. `PingFang SC` (macOS)

### 数据源环境变量

```bash
export TUSHARE_TOKEN="your_token_here"  # 注册: https://tushare.pro
export FRED_API_KEY="your_key_here"     # 可选，用于 FRED 数据
```

---

## Workflow（10步工作流程）

### Step 0: 创建分析输出目录 ⭐ 重要

**目标**: 创建本次分析的专用输出文件夹，放置在 **workspace** 目录下，避免污染 skill 目录。

**命名规则**: `<indicator>_<YYYYMMDD>_<direction>`
- 例如: `brent_crude_20260328_increase`

**输出目录**: `~/.openclaw/workspace/memory/reports/<analysis_folder>/`

**目录结构**:
```
~/.openclaw/workspace/memory/reports/brent_crude_20260328_increase/
├── data/                    # 中间数据文件
│   ├── brent_crude.json
│   ├── xle.json
│   └── jets.json
│   └── ...
├── charts/                  # 图表文件
│   ├── brent_crude_vs_xle.png
│   ├── brent_crude_vs_jets.png
│   ├── performance_summary.png
│   ├── event_matrix_heatmap.png
│   └── charts_manifest.json
├── events.json              # 相似事件列表
├── related.json             # 相关资产推论
├── performance.json         # 表现分析结果
└── report.md                # 最终分析报告
```

**执行**:
```bash
# 创建输出目录（使用 workspace 绝对路径）
OUTPUT_DIR="$HOME/.openclaw/workspace/memory/reports/brent_crude_20260328_increase"
mkdir -p "${OUTPUT_DIR}/data" "${OUTPUT_DIR}/charts"
```

---

### Step 1: 识别表征指标

**目标**: 将用户的事件描述映射到具体指标。

**事件 → 指标映射表**:
| 事件类型 | 表征指标 |
|---------|---------|
| 油价暴涨/暴跌 | `brent_crude` 或 `wti_crude` |
| 黄金价格变动 | `gold` |
| 利率变化 | `us_10y_treasury` 或 `fed_funds_rate` |
| VIX/波动率飙升 | `vix` |
| 美元走强/走弱 | `usd_index` |
| 通胀变化 | `cpi_us` |
| 衰退信号 | `unemployment_us` |
| 美联储缩表 | `fed_funds_rate` + `us_10y_treasury` |

**执行**:
```bash
python scripts/fetch_indicator_data.py --list
```

### Step 2: 获取历史数据

**目标**: 获取表征指标 30+ 年时序数据。

**执行**:
```bash
python scripts/fetch_indicator_data.py <indicator_id> --years 30 --output ${OUTPUT_DIR}/data/<indicator_id>.json --json
```

### Step 3: 提取当前事件特征

**目标**: 量化当前事件（变动幅度、方向、波动率）。

**执行**:
```bash
python scripts/find_similar_events.py --data ${OUTPUT_DIR}/data/<indicator_id>.json --output ${OUTPUT_DIR}/events.json
```

### Step 4: 查找历史相似事件

已在 Step 3 完成，`events.json` 包含相似事件列表。

### Step 5: 推论相关资产（多经济体分析） ⭐ 核心改动

**目标**: 基于因果关系确定受影响资产，覆盖多个经济体，**不仅限于可交易的金融资产标的**。

**因果分析框架（扩展）**:
| 维度 | 说明 | 示例 |
|------|------|------|
| **上下游** | 供应链传导效应 | 油价→能源股(受益)→航空股(受损) |
| **替代效应** | 替代产品/服务 | 油价涨→电动车需求↑ |
| **互补效应** | 联合需求模式 | 油价涨→天然气联动 |
| **金融关联** | 资本流动、风险情绪 | 美股波动→A股联动 |
| **多经济体传导** ⭐ 核心 | 跨市场传导 | 美元走强→新兴市场资本流出 |
| **宏观经济指标** ⭐ 核心 | 非交易性指标传导 | 油价暴涨→各国CPI/PPI/M2变化 |

**多经济体分析范围** ⭐ 核心改动（必须覆盖）:

| 经济体 | 分析范围 | 具体指标 | 获取方式 |
|-------|---------|---------|---------|
| **中国** | 股指 + 宏观 + 利率 + 货币 + 汇率 | 沪深300/创业板、CPI/PPI/GDP/PMI、LPR、M2/M1、USD/CNY | Tushare |
| **日本** | 股指 + 利率 + 汇率 + 宏观 | 日经225/TOPIX、10Y国债、USD/JPY、GDP/CPI/M2 | Yahoo Finance / FRED |
| **韩国** | 股指 + 汇率 + 宏观 | KOSPI/KOSDAQ、USD/KRW、GDP/CPI | Yahoo Finance / FRED |
| **欧洲** | 股指 + 利率 + 汇率 + 宏观 | 斯托克50/DAX/CAC40/富时100、德国10Y、EUR/USD、GDP/CPI/M2 | Yahoo Finance / FRED |
| **亚太新兴** | 股指 + 汇率 | 恒生指数、印度Nifty、东南亚指数、汇率 | Yahoo Finance |

**⚠️ 强制要求**: 每次分析必须覆盖以上所有经济体的**股市、宏观经济指标、利率、货币发行量、汇率**等维度，不仅限于可交易的金融资产标的（ETF、股票）。

**多经济体因果映射** (详见 `references/indicator_mapping.md`):

| 事件类型 | 中国影响 | 日本影响 | 韩国影响 | 欧洲影响 |
|---------|---------|---------|---------|---------|
| **油价暴涨** | 能源股受益，航空化工受损 | 能源股受益，制造业受损 | 能源股受益，化工受损 | 能源股受益，航空汽车受损 |
| **美元走强** | 出口股受益，资本流出压力 | 出口股受益，日元贬值 | 出口股受益，韩元贬值 | 出口股受益，欧元贬值 |
| **利率上升** | 银行保险受益，成长股受损 | 银行股受益 | 银行股受益 | 银行股受益，地产股受损 |
| **通胀上升** | 抗通胀资产受益 | 通胀摆脱通缩 | 抗通胀资产受益 | 抗通胀资产受益 |
| **VIX飙升** | 防守板块受益，成长股受损 | 防守板块受益 | 防守板块受益 | 防守板块受益 |

**执行**:
```bash
python scripts/infer_related_assets.py --indicator <indicator_id> --direction <increase|decrease> --multi-economy --output ${OUTPUT_DIR}/related.json
```

**输出格式扩展**:
```json
{
  "benefited": [
    {"indicator": "xle", "reason": "能源ETF直接受益", "economy": "US"},
    {"indicator": "csi300_energy", "reason": "中国能源板块受益", "economy": "China"},
    {"indicator": "nikkei225_energy", "reason": "日本能源股受益", "economy": "Japan"}
  ],
  "harmed": [
    {"indicator": "jets", "reason": "航空ETF燃油成本上升", "economy": "US"},
    {"indicator": "csi300_airline", "reason": "中国航空股成本上升", "economy": "China"},
    {"indicator": "dax_auto", "reason": "德国汽车股成本上升", "economy": "Europe"}
  ],
  "macro_indicators": [
    {"indicator": "cpi_china", "reason": "油价上涨推升中国CPI", "economy": "China"},
    {"indicator": "cpi_eurozone", "reason": "油价上涨推升欧元区CPI", "economy": "Europe"}
  ]
}
```

### Step 6: 分析历史表现

**目标**: 计算每类资产在各历史事件期间的表现。

**执行**:
```bash
# 先获取所有相关指标数据
for indicator in $(cat ${OUTPUT_DIR}/related.json | jq -r '.benefited[].indicator, .harmed[].indicator'); do
    python scripts/fetch_indicator_data.py $indicator --years 30 --output ${OUTPUT_DIR}/data/$indicator.json --json
done

# 分析各事件期间表现
python scripts/analyze_related_performance.py \
    --events ${OUTPUT_DIR}/events.json \
    --related ${OUTPUT_DIR}/related.json \
    --data-dir ${OUTPUT_DIR}/data \
    --output ${OUTPUT_DIR}/performance.json
```

### Step 7: 生成图表（前置检查） ⭐ 核心改动

**目标**: 可视化时序对比和表现统计，确保中文不乱码，X轴标签不重叠。

**前置检查项**:
| 检查项 | 要求 | 失败处理 |
|--------|------|---------|
| **中文字体** | WenQuanYi/SimHei/Noto CJK 可用 | 安装 fonts-wqy-microhei |
| **输出目录** | 写权限正常 | 检查目录权限 |
| **matplotlib** | 已安装 | pip install matplotlib |

**图表规范**（核心改动）:

| 图表类型 | 内容 | 格式 | 要求 |
|---------|------|------|------|
| **时序对比图** | 每类资产单独一张，双Y轴叠加 | 中文标题/标签 | ⭐ **强制每一项生成单独图表** |
| **表现汇总图** | 各资产平均收益对比 | 中文标注 | - |
| **事件矩阵图** | 资产×事件收益矩阵 | 中文热力图 | - |

**时序对比图增强功能** ⭐ 核心改动:
- ✅ **红色虚线方框**：标记过往同类事件发生时间区间
- ✅ **虚线框高度覆盖整个Y轴区域**：从Y轴底部到顶部，**不能仅覆盖表征指标的数值区域**
- ✅ **事件标签**：显示事件编号和涨跌幅
- ✅ **X轴自适应**：根据数据跨度自动调整刻度间隔，避免标签重叠
- ✅ **图表宽度自适应**：长时间跨度使用更宽图表

**⚠️ 强制要求**:
- **每一项相关指标都必须生成单独的时序对比图**（不能合并或省略）
- **红色虚线框必须覆盖整个Y轴区域**（从底部到顶部），而非仅覆盖数值范围

**技术实现说明**（关键代码）:
```python
# ⭐ 核心技术：使用 ax.get_xaxis_transform() 让矩形覆盖整个Y轴区域
rect = plt.Rectangle(
    (mdates.date2num(start_date), 0),  # Y=0（图表底部）
    mdates.date2num(end_date) - mdates.date2num(start_date),
    1,  # Y高度=1（从底部到顶部，覆盖整个图表区域）
    transform=ax1.get_xaxis_transform(),  # ⭐ 关键：X轴数据坐标，Y轴axes坐标(0-1)
    clip_on=False  # 允许超出轴边界
)
```

**原理**: `ax.get_xaxis_transform()` 使用混合坐标系：
- X轴：数据坐标（实际日期）
- Y轴：axes坐标（0-1，覆盖整个图表高度）

这样矩形会覆盖整个Y轴区域，无论表征指标的实际数值范围如何。

**X轴间隔自适应规则**:
| 数据跨度 | 刻度间隔 |
|:--------:|:--------:|
| ≤12个月 | 每月 |
| ≤24个月 | 每季度 |
| ≤60个月 | 半年 |
| ≤120个月 | 每年 |
| >120个月 | 每两年 |

**执行**:
```bash
python scripts/generate_charts.py \
    --primary-indicator <indicator_id> \
    --primary-data ${OUTPUT_DIR}/data/<indicator_id>.json \
    --events ${OUTPUT_DIR}/events.json \
    --related ${OUTPUT_DIR}/related.json \
    --performance ${OUTPUT_DIR}/performance.json \
    --output-dir ${OUTPUT_DIR}/charts
```

---

### Step 8: 生成报告（嵌入图片） ⭐ 新增

**目标**: 生成完整中文分析报告，将所有时序对比图嵌入 Markdown。

**报告结构**:
1. **🎯 核心结论**（优先展示）
2. 当前事件特征
3. 历史相似事件列表
4. 变动幅度表格（从最新到最早）
5. 汇总统计
6. **📈 时序对比图（嵌入Markdown）** ⭐ 新增
7. 📊 表现汇总图
8. 🔥 事件矩阵热力图
9. 分析局限性

**图片嵌入格式**:
```markdown
![图表名称](charts/图表文件.png)
```

**执行**:
```bash
python scripts/generate_report.py \
    --primary-indicator <indicator_id> \
    --events ${OUTPUT_DIR}/events.json \
    --related ${OUTPUT_DIR}/related.json \
    --performance ${OUTPUT_DIR}/performance.json \
    --charts-manifest ${OUTPUT_DIR}/charts/charts_manifest.json \
    --output-dir ${OUTPUT_DIR} \
    --output report.md
```

---

### Step 9: 展示报告和图表

**目标**: 输出完整中文报告，向 chat 窗口展示报告内容和图表。

**报告结构** (详见 `references/report_template.md`):
1. **🎯 核心结论**（优先展示）
2. 事件概述
3. 当前事件特征
4. 历史相似事件
5. 相关资产推论
6. **历史变动幅度表格**（新增，从最新到最早）
7. 历史表现汇总
8. 图表说明
9. 分析局限性

**展示要求**: 报告生成后，将完整内容输出到 chat 窗口，并附带已生成的图表图片。

---

## 图表规范详解

### 1. 时序对比图（每类资产一张）

**文件名**: `<primary_indicator>_vs_<related_indicator>.png`

**结构**:
```
┌─────────────────────────────────────────────┐
│  油价 vs 能源ETF 历史走势对比                  │  ← 中文标题
├─────────────────────────────────────────────┤
│                                             │
│  ┌───────┐  红色虚线框                        │
│  │事件区间│  标记历史事件                      │
│  └───────┘                                  │
│                                             │
│  左Y轴: 油价(美元/桶)    右Y轴: 能源ETF价格   │  ← 双Y轴中文标注
│  ── 油价曲线              ── ETF曲线          │
│                                             │
├─────────────────────────────────────────────┤
│  时间轴: 2010.01.01 - 2024.12.31            │  ← YYYY.MM.DD 格式
└─────────────────────────────────────────────┘
```

**颜色规范**:
- 🔴 **红色** = 上涨 (+)
- 🟢 **绿色** = 下跌 (-)
- ⬛ **红色虚线框** = 历史事件区间

### 2. 变动幅度表格（新增）

**格式**: Markdown 表格，按时间从最新到最早排列

| 历史事件 | 时间区间 | 表征指标变动 | 相关资产A | 相关资产B | ... |
|---------|---------|-------------|----------|----------|-----|
| **事件1**（最新） | 2024.03.15-2024.06.20 | 🔴 +42% | 🔴 +15% | 🟢 -8% | ... |
| **事件2** | 2022.02.10-2022.04.05 | 🔴 +38% | 🔴 +12% | 🟢 -5% | ... |
| **事件3** | 2020.03.09-2020.04.21 | 🟢 -55% | 🟢 -28% | 🔴 +10% | ... |
| ... | ... | ... | ... | ... | ... |

**高亮规则**:
- 相关性高（同向变动）的单元格加粗显示
- 反向变动的单元格使用不同颜色标记

---

## 指标映射参考

详见 `references/indicator_mapping.md`：

| 类别 | 可用指标 |
|------|---------|
| **大宗商品** | brent_crude, wti_crude, gold, silver, copper, aluminum, natural_gas |
| **美股指数** | sp500, nasdaq, dow_jones, russell2000, vix |
| **美股行业ETF** | xlk, xle, xlf, xlv, xli, jets, iyr, gdx, tlt |
| **外汇** | usd_cny, usd_index, eur_usd |
| **美债** | us_10y_treasury, us_2y_treasury |
| **FRED宏观** | fed_funds_rate, cpi_us, gdp_us, unemployment_us |
| **A股指数** | csi300, sse_composite, chinext, sse50 |

---

## 事件 → 相关资产因果逻辑

### 油价暴涨 (`oil_price_increase`)

| 类别 | 资产 | 效果 | 原因 |
|------|------|------|------|
| **受益** | 能源ETF (xle) | ↑ | 收入增加 |
| **受益** | 黄金 (gold) | ↑ | 通胀对冲 |
| **受损** | 航空ETF (jets) | ↓ | 燃油成本增加 |
| **受损** | 工业ETF (xli) | ↓ | 能源成本上升 |

### 黄金暴涨 (`gold_price_increase`)

| 类别 | 资产 | 效果 | 原因 |
|------|------|------|------|
| **受益** | 黄金矿业ETF (gdx) | ↑ | 直接受益 |
| **受益** | 白银 (silver) | ↑ | 贵金属联动 |
| **受损** | 股市 (sp500) | ↓ | 避险信号 |
| **受损** | 金融ETF (xlf) | ↓ | 风险规避 |

### 加息 (`interest_rate_increase`)

| 类别 | 资产 | 效果 | 原因 |
|------|------|------|------|
| **受益** | 金融ETF (xlf) | ↑ | 利差扩大 |
| **受益** | 美元指数 (usd_index) | ↑ | 资本流入 |
| **受损** | 债券ETF (tlt) | ↓ | 利率上升 |
| **受损** | REITs (iyr) | ↓ | 融资成本 |
| **受损** | 成长股 (nasdaq) | ↓ | 估值压制 |

### VIX飙升 (`vix_increase`)

| 类别 | 资产 | 效果 | 原因 |
|------|------|------|------|
| **受益** | 防守板块 (xlp, xlv) | ↑ | 避险 |
| **受益** | 黄金 (gold) | ↑ | 风险规避 |
| **受损** | 股市 (sp500) | ↓ | 风险规避 |
| **受损** | 金融ETF (xlf) | ↓ | 风险规避 |

### 美联储缩表 (`fed_balance_sheet_reduction`)

| 类别 | 资产 | 效果 | 原因 |
|------|------|------|------|
| **受益** | 美元指数 (usd_index) | ↑ | 流动性收紧 |
| **受益** | 金融ETF (xlf) | ↑ | 利差扩大 |
| **受损** | 债券ETF (tlt) | ↓ | 收益率上行 |
| **受损** | 成长股 (nasdaq) | ↓ | 流动性压制 |

---

## 输出要求

### 图表
- **语言**: 中文标题、标签、图例
- **时间格式**: YYYY.MM.DD
- **颜色**: 🔴 红色 = 上涨 (+)，🟢 绿色 = 下跌 (-)
- **事件标记**: 红色虚线框（历史），红色实线框（当前）
- **双Y轴**: 左轴表征指标，右轴关联资产

### 报告
- **语言**: 中文
- **格式**: Markdown 表格
- **结构**: 结论优先 → 详细统计
- **署名**: 🐂

---

## 示例：油价暴涨分析

**用户输入**: "分析历史上油价快速上涨后各类资产的表现情况"

**工作流程**:
1. 创建输出目录 → `~/.openclaw/workspace/memory/reports/brent_crude_20260328_increase/`
2. 识别 → `brent_crude`
3. 获取 → 30年布伦特原油数据 → `${OUTPUT_DIR}/data/brent_crude.json`
4. 提取 → 当前: 90天内+40%（上涨）
5. 查找 → 5次历史油价暴涨事件 → `${OUTPUT_DIR}/events.json`
6. 推论 → 能源ETF(受益)、航空ETF(受损)、黄金(对冲) → `${OUTPUT_DIR}/related.json`
7. 分析 → 各资产在各历史事件期间的收益 → `${OUTPUT_DIR}/performance.json`
8. 图表 → 时序对比图(每类资产一张)、表现汇总图 → `${OUTPUT_DIR}/charts/`
9. 报告 → 中文分析报告 + 变动幅度表格 → `${OUTPUT_DIR}/report.md`

---

## 参考文件

- `references/indicator_mapping.md`: 完整指标列表和数据源
- `references/report_template.md`: 中文报告模板结构