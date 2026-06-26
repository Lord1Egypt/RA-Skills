---
name: "chanlun-analysis-revised"
description: "Use ChanLun Theory to analyse stock and visualize"
---
# ChanLun technical Analysis 修改版

基于缠中说禅技术理论，实现 A股、港股、美股的技术面分析，包括分型、笔、线段、中枢、背驰等核心概念的自动识别与可视化。

## 重要说明

- 修改自：https://clawhub.ai/laigen/chanlun-technical-analysis（原来的这个skill中有些错误，没有区分处理后的K线和原始K线，导致输出数据与原始K线出现错位）
- 笔的识别参考：https://github.com/neuks/Indicator
- 线段的识别参考：https://github.com/jiapengwei/czsc_in_practise
- 使用腾讯的API数据，腾讯没有北交所的数据，因此不能查询北交所股票

## 核心功能

---

## 缠论核心概念

### 1\. 分型 (Fractal)

**顶分型**: 第二 K 线高点是相邻三 K 线高点中最高的，低点也是相邻三 K 线低点中最高的

- 顶分型的最高点叫该分型的顶

**底分型**: 第二 K 线低点是相邻三 K 线低点中最低的，高点也是相邻三 K 线高点中最低的

- 底分型的最低点叫该分型的底

### 2\. K 线包含处理

**向上处理**: 两 K 线高点取高者，低点取较高者  
**向下处理**: 两 K 线低点取低者，高点取较低者

### 3\. 笔 (Stroke)

- 两个相邻的顶和底构成一笔
- 顶和底之间至少有 1 根 K 线相隔
- 笔分为向上笔和向下笔

### 4\. 线段 (Line Segment)

- 由奇数笔组成（至少 3 笔）
- 前三笔必须有重叠部分
- 分为向上线段和向下线段

### 5\. 中枢 (Pivot)

- 某级别走势中，被至少三个连续次级别走势所重叠的部分
- 对笔来说：至少三笔重叠
- 对线段来说：至少三段重叠

### 6\. 背驰 (Divergence)

- 没有趋势就没有背驰
- 比较相邻两段的 MACD 柱面积
- c 段面积 < b 段面积 = 背驰

---

## 使用方法

```bash
# 使用自然语言查询（自动生成图表和报告）
python3 scripts/chanlun_analysis.py 腾讯控股

# 指定周期
python3 scripts/chanlun_analysis.py 腾讯控股 --period day

# 指定K线数(默认500）
python3 scripts/chanlun_analysis.py 腾讯控股 --period day --bars 700
```

### 参数说明

> **注意**: 图表 PNG 是必需输出，无需额外参数，每次分析自动生成。

---

## 输出内容

每次分析**自动生成**以下文件：

### 1\. 技术分析报告 (Markdown)

报告结构（**核心结论优先**）：

### 2\. 缠论可视化图表 (PNG) - 必需输出

图表内容：

- **主图**: K 线图 + 笔连接 + 线段连接 + 中枢区域
- **副图 1**: MACD 指标 (柱状图 + DIF 线 + DEA 线)
- **副图 2**: 成交量柱状图

**图表元素说明**:

### 3\. 输出文件

### 3\. JSON 数据结构

```json
{
  "stock_code": "601688",
  "trend": "uptrend",
  "fractals": {
    "tops_count": 8,
    "bottoms_count": 7
  },
  "strokes_count": 12,
  "segments_count": 3,
  "pivots_count": 2,
  "divergence": {
    "detected": true,
    "type": "bullish",
    "confidence": 0.75
  }
}
```

---

## 买卖点定义

### 第一类买卖点

- 趋势背驰后形成的转折点
- 下跌趋势底背驰 → 第一类买点
- 上涨趋势顶背驰 → 第一类卖点

### 第二类买卖点

- 第一类买卖点后的第一次回抽
- 不回前低/前高形成

### 第三类买卖点

- 突破中枢后的回抽
- 回抽不进入中枢区间

---

## 环境要求

### 必需环境变量

### Python 依赖

```bash
pip install pandas numpy matplotlib requests
```

---

## 文件结构

```text
chanlun-technical-analysis/
├── SKILL.md                    # 技能文档
└── scripts/
    ├── chanlun_analysis.py     # 主入口脚本
    ├── chanlun_core.py         # 核心算法（分型/笔/线段）
    ├── chanlun_divergence.py   # 背驰检测
    └── chanlun_chart.py        # 图表绘制
```

---

## 注意事项

1. **数据质量**: 使用前复权数据，避免除权缺口影响
2. **周期选择**: 建议使用日线或以上周期，分钟线噪音较多
3. **主观性**: 缠论部分判断存在主观性，算法仅为辅助
4. **结合其他指标**: 建议配合成交量、基本面等综合分析

---

## 免责声明

本技能仅供学习和研究使用，不构成任何投资建议。股市有风险，投资需谨慎。