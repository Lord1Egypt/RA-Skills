# Chanlun Technical Analysis Expert / 缠论技术分析专家#

> **English:** AI-powered Chanlun (Zen Trading / 缠中说禅) technical analysis expert — based on the original "Teach You to Trade Stocks 108 Lessons" (教你炒股票108课) by 缠中说禅. Covers the complete Chanlun system: (1) Morphology (形态学): fractal (分型), stroke (笔), line segment (线段), central hub (中枢/zhongshu), and trend types (上涨/下跌/盘整); (2) Dynamics (动力学): divergence (背驰/beichi), MACD analysis, energy structure, and trend-typeing. Supports Shanghai Composite Index / SZSE Component / ChiNext Index analysis, individual stock Chanlun decomposition, and sector rotation analysis. Built-in Python code (integrating czsc/chan.py open-source frameworks), Chanlun buy/sell point (买卖点) quantitative identification, multi-level joint analysis framework (month→week→day→30min). Includes classic case studies (Kweichow Moutai, CATL, BYD).

**Keywords:** Chanlun, technical analysis, A-share, stock market, trading, central hub, buy sell points, quantitative trading, Chinese stock market, Python*

## ✨ Features#

- ✅ **Chanlun Morphology (Complete)** — fractal (顶/底分型), stroke (3-minimum K-line connection), line segment (stroke-based extension, 3+ strokes), central hub (3+ segments overlap), trend types (上涨/下跌/盘整)*
- ✅ **Chanlun Dynamics (Complete)** — divergence (背驰: trend + consolidation), MACD histogram area comparison, energy structure assessment, multi-level joint analysis framework*
- ✅ **Buy/Sell Points Quantification** — Type 1 (trend end), Type 2 (retest after Type 1), Type 3 (breakout without returning to hub); each with detailed identification criteria + Python code*
- ✅ **A-Share Market Analysis** — Shanghai Composite / SZSE Component / ChiNext Index decomposition with hub identification + divergence detection*
- ✅ **Individual Stock & Sector Rotation** — stock Chanlun decomposition, sector rotation analysis with hub movement, ML-assisted pattern recognition (CNN for K-line patterns)*

## 🚀 Quick Start#

```bash
# Install this skill
npx clawhub install @gechengling/chanlun-analysis-pro#

# Use in WorkBudd
/chanlun-analysis-pro "Analyze Kweichow Moutai (600519) with Chanlun, generate buy/sell points"
/chanlun-analysis-pro "Decompose Shanghai Composite Index using Chanlun theory"
```

## Python Code Framework#

```bash
pip install czsc  # Open-source Chanlun library
```

```python
from czsc import CzscStrokes, CzscAnalyzer

# Use czsc for Chanlun analysis
analyzer = CzscAnalyzer(kline_data)
strokes = analyzer.strokes   # Auto-identify strokes
segments = analyzer.segments # Auto-identify line segments
hubs = analyzer.hubs       # Auto-identify central hubs
divergence = analyzer.check_divergence()  # Divergence detection
buy_points = analyzer.find_buy_points()     # Buy point identification
```

## 📖 What's Included#

| File / 文件 | Content / 内容说明 |
|------|---------|
| `SKILL.md` | Full skill definition, trigger keywords, complete Chanlun theory |
| `references/chanlun_algorithm_python.md` | Complete Chanlun algorithm Python implementation (fractal/stroke/segment/hub/divergence) + czsc integration |
| `references/chanlun_practice_guide.md` | Practical operation guide (divergence criteria/level selection/stop-loss/trading plan) |
| `references/chanlun_analysis_templates.md` | Analysis templates (individual stock/index/sector) + Moutai/CATL/BYD cases |

---

> **中文介绍：** 缠论技术分析专家——基于《缠中说禅：教你炒股票108课》原创理论的A股技术分析Skill。覆盖缠论完整体系：形态学（分型/笔/线段/中枢/走势类型）+ 动力学（背驰/MACD买卖点/能量结构）。支持上证指数/深证成指/创业板指大盘分析、个股缠论走势分解、行业板块轮动分析。内置Python完整代码（集成czsc/chan.py开源框架）、缠论三类买卖点量化识别、多级别联立分析框架。附带贵州茅台/宁德时代/比亚迪经典案例。

**关键词：** 缠论、缠中说禅、教你炒股票、分型、笔、线段、中枢、背驰、买卖点、A股、缠论108课*

## ✨ 核心功能#

- ✅ **缠论形态学（全体系）** — 分型（顶/底）、笔（3根K线最少连接）、线段（笔的延续，3笔+重叠）、中枢（3线段+重叠区间）、走势类型（上涨/下跌/盘整）*
- ✅ **缠论动力学（全体系）** — 背驰判定（趋势背驰+盘整背驰）、MACD柱状图面积比较、能量结构评估、多级别联立分析框架*
- ✅ **三类买卖点量化识别** — 一类买点（趋势结束背驰点）、二类买点（回试不破前低）、三类买点（突破中枢不回中枢）；每类含详细识别标准+Python代码*
- ✅ **A股大盘缠论分析** — 上证指数/深成指/创业板指分解，中枢识别+背驰检测+买卖点输出*
- ✅ **个股缠论分解+板块轮动** — 任意A股个股缠论分解，板块中枢移动分析+轮动规律，支持ML辅助识别（K线形态CNN识别）*

## 🚀 快速上手#

```bash
# 安装此技能
npx clawhub install @gechengling/chanlun-analysis-pro#

# 在WorkBuddy中使用
/chanlun-analysis-pro "用缠论分析贵州茅台（600519），给出买卖点"
/chanlun-analysis-pro "分解上证指数缠论结构，判断当前走势类型"
```

## 📖 包含内容#

| 文件 | 内容说明 |
|------|---------|
| `SKILL.md` | 完整技能定义、触发关键词、缠论全体系 |
| `references/chanlun_algorithm_python.md` | 缠论完整算法Python实现（分型/笔/线段/中枢/背驰）+ AKShare数据 + czsc集成 + 可视化 |
| `references/chanlun_practice_guide.md` | 缠论实战操作指南（背驰判定标准/级别选择/止损/交易计划） |
| `references/chanlun_analysis_templates.md` | 缠论分析模板（个股/大盘/板块）+ 茅台/宁德时代/比亚迪经典案例 |
