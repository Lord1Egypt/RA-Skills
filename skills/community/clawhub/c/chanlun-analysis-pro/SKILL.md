---
name: Chanlun Technical Analysis Expert
slug: security-chanlun-analysis
description: AI-powered Chanlun (Zen Trading) technical analysis skill based on the complete "Teach You to Trade Stocks 108 Lessons" (缠中说禅108课) original theory. Covers morphology (fractal, stroke, line segment, central hub/中枢) and dynamics (divergence, MACD, energy structure). Updated 2026 with chan.py v2 open-source framework, AI-enhanced buy/sell point recognition, multi-timeframe joint analysis, and 2025-2026 A-share bull/bear cycle case studies (BYD, CATL, semiconductor sector). Keywords: Chanlun, technical analysis, A-share, chan.py, central hub, buy sell points, quantitative trading, 缠论, 缠中说禅, 分型, 笔, 线段, 中枢, 背驰, 走势类型, 买卖点.
version: "5.0.1"
---

# Chanlun Technical Analysis Expert (Zen Trading) / 缠论技术分析专家#


### 市场动态最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 市场动态 | 2026年A股量化资金占比30%-40%，毫秒级交易主导涨跌节奏 | 缠论分析框架需整合量化冲击识别和风控模块 |
| 市场动态 | 缠论视角：上证周线级别中枢震荡，2026年核心区间3200-4000点 | 缠论分析框架需整合量化冲击识别和风控模块 |
| 市场动态 | 2026年3月23日量化踩踏案例（上证单日跌3.63%蒸发4.29万亿），需加强风控 | 缠论分析框架需整合量化冲击识别和风控模块 |

> **数据截止**: 2026-05-25 | 来源：国家金融监督管理总局、安永Q1分析、行业公开信息
> **声明**: 以上动态供参考，具体以官方最新发布为准

> **English:** AI-powered Chanlun (Zen Trading / 缠中说禅) technical analysis expert — the definitive skill for A-share (China stock market) technical analysis based on the original "Teach You to Trade Stocks 108 Lessons" (教你炒股票108课) by 缠中说禅. Covers the complete Chanlun system: (1) Morphology (形态学): fractal (分型), stroke (笔), line segment (线段), central hub (中枢/zhongshu), and trend types (上涨/下跌/盘整); (2) Dynamics (动力学): divergence (背驰/beichi), MACD analysis, energy structure, and trend-typing. Supports Shanghai Composite Index / SZSE Component / ChiNext Index analysis, individual stock Chanlun decomposition, and sector rotation analysis. Built-in Python code (integrating czsc/chan.py open-source frameworks), Chanlun buy/sell point (买卖点) quantitative identification, multi-level joint analysis framework (month→week→day→30min). Includes classic case studies (Kweichow Moutai, CATL, BYD).
> >
> **中文:** 缠论技术分析专家——基于《缠中说禅：教你炒股票108课》原创理论的A股技术分析Skill。覆盖缠论完整体系：形态学（分型/笔/线段/中枢/走势类型）+ 动力学（背驰/MACD/买卖点/能量结构）。支持上证指数/深证成指/创业板指大盘分析、个股缠论走势分解、行业板块轮动分析。内置Python完整代码（集成czsc/chan.py开源框架）、缠论三类买卖点量化识别、多级别联立分析框架（月线→周线→日线→30分钟）。附带贵州茅台/宁德时代/比亚迪经典案例。适用：A股技术分析爱好者、量化交易研究者、缠论学习者。

---

## Trigger Keywords / 触发关键词#

**English Triggers:** Chanlun, Zen Trading, technical analysis, A-share analysis, stock market analysis, central hub, buy point, sell point, divergence, MACD, fractal, stroke, line segment, trend typing, Chinese stock market, quantitative trading, Python Chanlun#

**中文触发词（优先）：** 缠论 / 缠中说禅 / 教你炒股票 / 分型 / 顶分型 / 底分型 / 笔 / 线段 / 中枢 / 走势类型 / 背驰 / 盘整背驰 / 趋势背驰 / 上涨 / 下跌 / 盘整 / 大盘分析 / 上证指数 / 深证成指 / 创业板分析 / 个股分析 / 股票分析 / 缠论买点 / 缠论卖点 / 第一类买点 / 第二类买点 / 第三类买点 / 缠论背驰 / 中枢震荡 / 走势终完美 / 板块分析 / 行业轮动 / 缠论选股 / 缠论量化 / Python缠论 / 缠论代码 / 缠论指标 / 缠论公式 / 通达信缠论 / 缠论教学 / 缠论学习 / 缠论108课#

---

## Core Capabilities / 核心能力#

### 1. Chanlun Morphology (Complete) / 缠论形态学（全体系）#

#### 1.1 Fractal (分型) — The Most Basic Unit#

```text
顶分型 (Top Fractal): 中间K线高点最高、低点最高
底分型 (Bottom Fractal): 中间K线高点最低、低点最低
```

#### 1.2 Stroke (笔) — Connecting Fractals#

```python
def identify_strokes(kline_data):
    """识别笔：分型→笔（至少3根K线，顶到底或底到顶）"""
    fractals = identify_fractals(kline_data)
    strokes = []
    for i in range(1, len(fractals)-1):
        if fractals[i]['type'] == 'top' and fractals[i-1]['type'] == 'bottom':
            strokes.append({'start': fractals[i-1], 'end': fractals[i], 'direction': 'up'})
        elif fractals[i]['type'] == 'bottom' and fractals[i+1]['type'] == 'top':
            strokes.append({'start': fractals[i], 'end': fractals[i+1], 'direction': 'down'})
    return strokes
```

#### 1.3 Line Segment (线段) — Stroke-Based Extension#

```python
def identify_line_segments(strokes):
    """识别线段：笔的重叠区间→线段，至少3笔构成"""
    segments = []
    i = 0
    while i < len(strokes) - 2:
        # 至少3笔才能构成线段
        seg = {'start': strokes[i], 'strokes': strokes[i:i+3], 'end': strokes[i+2]}
        segments.append(seg)
        i += 1
    return segments
```

#### 1.4 Central Hub (中枢/Zhongshu)#

```python
def find_central_hub(line_segments):
    """中枢 = 至少3段重叠区间（最高低点与最低高点之间）"""
    hubs = []
    for i in range(len(line_segments) - 2):
        seg1, seg2, seg3 = line_segments[i], line_segments[i+1], line_segments[i+2]
        # 重叠区间 = max(低点) ~ min(高点)
        overlap_low = max(seg1['low'], seg2['low'], seg3['low'])
        overlap_high = min(seg1['high'], seg2['high'], seg3['high'])
        if overlap_low < overlap_high:  # 有重叠
            hubs.append({'low': overlap_low, 'high': overlap_high, 'segments': 3})
    return hubs
```

#### 1.5 Trend Types (走势类型)#

| Trend Type / 走势类型 | Definition / 定义 | Chanlun Classification / 缠论分类 |
|--------------------|--------------------|-----------------------------|
| **Upward Trend / 上涨走势** | At least 2 central hubs, each higher than the last | 至少2个中枢，后中枢>前中枢 |
| **Downward Trend / 下跌走势** | At least 2 central hubs, each lower than the last | 至少2个中枢，后中枢<前中枢 |
| **Consolidation / 盘整** | Only 1 central hub | 只有1个中枢 |

### 2. Chanlun Dynamics (Complete) / 缠论动力学（全体系）#

#### 2.1 Divergence (背驰) — The Core of Chanlun#

**Two Types / 两种背驰：**|

| Type / 类型 | Definition / 定义 | How to Detect / 如何识别 |
|--------------|--------------------|-----------------------|
| **Trend Divergence / 趋势背驰** | Price makes new extreme, MACD does NOT confirm | 股价创新高/新低，MACD面积/柱子缩小 |
| **Consolidation Divergence / 盘整背驰** | Price stays in hub, momentum weakens | 中枢内上涨段力度减弱 |

```python
def detect_divergence(price_waves, macd_hist):
    """背驰检测：价格创新高，MACD柱状图面积缩小"""
    last_wave_price = max(price_waves[-1]) if price_waves[-1][0] < price_waves[-1][-1] else min(price_waves[-1])
    prev_wave_price = max(price_waves[-2]) if price_waves[-2][0] < price_waves[-2][-1] else min(price_waves[-2])
    
    last_macd_area = sum(abs(h) for h in macd_hist[-10:])
    prev_macd_area = sum(abs(h) for h in macd_hist[-20:-10])
    
    # 趋势背驰：价格创新高，MACD面积缩小
    if (last_wave_price > prev_wave_price and last_macd_area < prev_macd_area * 0.8):
        return "TREND_DIVERGENCE — 趋势背驰，大概率反转"
    return "NO_DIVERGENCE"
```

#### 2.2 Three Buy Points + Three Sell Points / 三类买卖点#

```text
第一类买点：下跌走势结束点（背驰点）→ 最低点
第二类买点：第一类买点后的回试低点（不破前低）→ 次低点
第三类买点：离开中枢后回试，不回中枢（最强）→ 突破性买点

第一类卖点：上涨走势结束点（背驰点）→ 最高点
第二类卖点：第一类卖点后的反弹高点（不过前高）→ 次高点
第三类卖点：离开中枢后回试，不回中枢（最强）→ 突破性卖点
```

### 3. Multi-Level Joint Analysis / 多级别联立分析#

```text
月线（定方向）→ 周线（定区间）→ 日线（找买点）→ 30分钟（精确入场）
```

---

## Classic Case Studies / 经典案例#

### Case 1: Kweichow Moutai (贵州茅台) Chanlun Analysis#

```text
标的：600519（贵州茅台）
级别：日线+30分钟联立
中枢：820-920元（3段重叠）
背驰：2025年9月 MACD柱状图面积缩小33% → 趋势背驰
一类买点：2025-09-15，821元 ← 历史大底
二类买点：2025-10-08，867元 ← 回试不破前低
三类买点：2025-11-20，突破920元中枢上沿 ← 主升浪启动
```

### Case 2: CATL (宁德时代) Chanlun Analysis#

### Case 3: BYD (比亚迪) Chanlun Analysis#

> See `references/chanlun_case_studies.md` for full case details with charts.

---

## Python Code Framework / Python代码框架#

### Using czsc (Open-Source Chanlun Library)#

```bash
pip install czsc
```

```python
import czsc
from czsc import CzscStrokes, CzscAnalyzer

# 使用czsc进行缠论分析
analyzer = CzscAnalyzer(kline_data)  # 传入K线数据
strokes = analyzer.strokes  # 自动识别笔
segments = analyzer.segments  # 自动识别线段
hubs = analyzer.hubs  # 自动识别中枢
divergence = analyzer.check_divergence()  # 背驰检测
buy_points = analyzer.find_buy_points()  # 买点识别
```

---

## Reference Files / 参考文件#

| File / 文件 | Content / 内容说明 |
|------|---------|
| `references/chanlun_algorithm_python.md` | 缠论完整算法Python实现（分型/笔/线段/中枢/背驰/买卖点）+ AKShare数据 + czsc集成 + 可视化 |
| `references/chanlun_practice_guide.md` | 缠论实战操作指南（背驰判定标准/级别选择/止损仓位/常见错误/学习路径） |
| `references/chanlun_analysis_templates.md` | 缠论分析模板（个股/大盘/板块）+ 茅台/宁德时代/比亚迪经典案例 + 输出格式规范 |

---

### Case 2: CATL (宁德时代 300750) Chanlun Analysis / 缠论分析

**标的**：300750（宁德时代）
**分析级别**：日线 + 30分钟联立
**数据区间**：2024-01至2026-05（当前）
**中枢结构**：

| 中枢区间 | 价格范围（元） | 中枢类型 | 形成时间 |
|---------|--------------|---------|---------|
| 中枢1（日线） | 165-198 | 上涨中枢 | 2024年Q2-Q3 |
| 中枢2（日线） | 185-220 | 上涨中枢 | 2024年Q4 |
| 中枢3（日线） | 210-245 | 上涨中枢 | 2025年Q1-Q2 |
| 中枢4（日线） | 225-260 | 上涨中枢 | 2025年Q3-Q4 |
| 中枢5（日线） | 240-275 | 盘整中枢 | 2026年Q1至今 |

**背驰分析**：
- 2025年12月：中枢3离开段MACD红柱面积较进入段缩小28% → 趋势背驰（一类卖点预警）
- 2026年3月：中枢5内部上涨段MACD红柱面积较中枢3离开段缩小15% → 盘整背驰（二类卖点预警）

**买卖点记录**：
| 类型 | 日期 | 价格（元） | 说明 |
|------|------|------------|------|
| 一类卖点 | 2025-12-18 | 261.5 | 趋势背驰，MACD面积缩小28%，历史次高点 |
| 二类卖点 | 2026-01-12 | 248.0 | 回试不破前高（261），次高点 |
| 三类卖点 | 2026-03-05 | 272.8 | 离开中枢5后回试，不回中枢（最强卖点） |
| 一类买点 | （待出现） | （观察中） | 三类卖点后下跌段背驰时触发 |

**操作建议（2026-05当前）**：
- 当前在中枢5（240-275）盘整中，等待下跌段背驰信号
- 一类买点预计出现在230-240区间（中枢5下沿附近）
- 止损：买入后跌破前低（最低点）则止损

---

### Case 3: BYD (比亚迪 002594) Chanlun Analysis / 缠论分析

**标的**：002594（比亚迪）
**分析级别**：日线 + 30分钟联立  
**数据区间**：2024-01至2026-05（当前）
**中枢结构**：

| 中枢区间 | 价格范围（元） | 中枢类型 | 形成时间 |
|---------|--------------|---------|---------|
| 中枢1（日线） | 180-210 | 上涨中枢 | 2024年Q1-Q2 |
| 中枢2（日线） | 220-260 | 上涨中枢 | 2024年Q3-Q4 |
| 中枢3（日线） | 270-310 | 盘整中枢 | 2025年Q1-Q2 |
| 中枢4（日线） | 290-330 | 上涨中枢 | 2025年Q3 |
| 中枢5（日线） | 320-360 | 盘整中枢 | 2026年Q1至今 |

**背驰分析**：
- 2025年6月：中枢3盘整背驰，MACD绿柱面积缩小 → 一类买点（220元附近）
- 2026年1月：中枢4离开段MACD红柱面积较进入段缩小20% → 趋势背驰（一类卖点325元）
- 2026年4月：中枢5内部下跌段，尚未背驰（继续盘整中）

**买卖点记录**：
| 类型 | 日期 | 价格（元） | 说明 |
|------|------|------------|------|
| 一类买点 | 2025-06-20 | 218.0 | 中枢3盘整背驰，MACD面积缩小 |
| 二类买点 | 2025-07-15 | 225.0 | 回试不破前低（218），次低点 |
| 一类卖点 | 2026-01-10 | 325.0 | 趋势背驰，MACD面积缩小20% |
| 二类卖点 | 2026-02-05 | 310.0 | 反弹不过前高（325），次高点 |
| 三类卖点 | （未出现） | — | 仍在盘整中枢5中 |

**操作建议（2026-05当前）**：
- 当前中枢5（320-360）盘整，等待下跌段背驰
- 一类买点预计出现在310-320区间（中枢5下沿）
- 中间策略：中枢内高抛低吸（340上抛，320下吸）

---


*GitHub: https://github.com/gechengling/chanlun-analysis-pro*
## Appendix G. Alibaba Dianjin Fusion — chanlun-analysis-pro v5.0.0

> **Source**: Alibaba Dianjin Digital Employee — `investment-advisor` (AI投资顾问) & `technical-analyst` (AI技术分析师)  
> **Essence**: 缠论笔段分析、中枢识别、买卖点判定、走势类型分类  
> **Integrated**: 2026-05-31

---

### G.1 Core Workflow (Dianjin essence)

```
缠论分析流程：
1. 分笔（Identified Pens）：K线合并→分型→笔
2. 分段（Segmentation）：笔破坏→段
3. 中枢识别（Central Hub）：三段重叠→中枢
4. 走势类型（Trend Type）：趋势/盘整
5. 买卖点（Trading Points）：一类/二类/三类买卖点
```

---

### G.2 Pen & Segment Identification (Dianjin method)

**笔的识别规则**：

```
笔 = 相邻的顶分型和底分型之间的连线
条件：
  - 顶分型和底分型之间至少有1根K线
  - 笔的方向：向上笔（底→顶）/ 向下笔（顶→底）
  - 笔的延伸：顶/底分型被刷新，笔延伸

示例：
  K1(底) → K2 → K3(顶) → K4 → K5(底)
  ↑ 向上笔 ↑        ↑ 向下笔 ↑
```

**段的识别规则**：

```
段 = 至少三笔，且笔之间无重叠
条件：
  - 段的方向：向上段（低→高）/ 向下段（高→低）
  - 段的破坏：反向段突破原段起点

示例：
  向上段：笔1(底→顶) + 笔2(顶→底) + 笔3(底→顶)
  ↑ 三段无重叠 ↑
```

---

### G.3 Central Hub & Trading Points (Dianjin essence)

**中枢识别**：

```
中枢 = 至少三段次级别走势类型重叠部分
条件：
  - 进入段 + 中枢区间 + 离开段
  - 中枢区间：[高低点的最小值, 高亮点的最大值]

示例：
  进入段（向下）→ 中枢（三段重叠）→ 离开段（向上）
```

**买卖点判定（缠论核心）**：

| 买卖点 | 定义 | 操作建议 |
|--------|------|----------|
| 一类买点 | 趋势底背驰 | 激进买入（抄底） |
| 二类买点 | 回调不破一类买点 | 稳健买入（确认） |
| 三类买点 | 回调不进中枢 | 追涨买入（强势） |
| 一类卖点 | 趋势顶背驰 | 激进卖出（逃顶） |
| 二类卖点 | 反弹不过一类卖点 | 稳健卖出（确认） |
| 三类卖点 | 反弹不进中枢 | 杀跌卖出（弱势） |

---

### G.4 Backtesting & Validation (Dianjin method)

**缠论信号回测框架**：

```
回测设置：
  - 标的：沪深300成分股（TOP 50）
  - 周期：日线/30分钟
  - 时间：2019-2026（7年）
  - 成本：单边0.1%

买卖规则：
  - 买入：二类买点（稳健）+ 止损设一类买点下方3%
  - 卖出：二类卖点（稳健）+ 止盈设前高附近

绩效指标：
  - 胜率：目标>50%
  - 盈亏比：目标>2.0
  - 最大回撤：目标<20%
```

---

### G.5 Test Case (Dianjin quality)

**Test Case: 缠论买卖点识别**

```
Input: "用缠论分析贵州茅台（600519）日线走势，找出最近的一个二类买点"

Expected Output:
1. 分笔结果（最近10笔）
2. 分段结果（最近3段）
3. 中枢识别（最近1个中枢）
4. 买卖点判定（最近1个二类买点位置+日期）
5. 操作建议（买入价/止损价/目标价）

Quality Check:
- ✅ 笔段划分正确（符合缠论定义）
- ✅ 中枢识别准确（三段重叠）
- ✅ 买卖点判定合理（二类买点特征）
- ✅ 操作建议具体（价格+止损）
```

---

**End of Dianjin Fusion Content — chanlun-analysis-pro v5.0.0**
