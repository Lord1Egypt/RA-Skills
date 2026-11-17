---
name: Financial Industry Data Analysis Expert
slug: finance-data-analytics
description: AI-powered financial data analysis expert — covers financial statement analysis, KPI tracking, trend analysis, data visualization, and automated reporting. Built for financial analysts, CFO offices, and data-driven decision making. Keywords: financial data analysis, KPI dashboard, data visualization, financial reporting, Python analysis, SQL queries, 金融数据分析, 财务分析, KPI追踪, 数据可视化, Python分析, 数据看板, 经营分析, 业务分析, Excel分析, Pandas分析.
version: "5.0.0"
---

# Financial Industry Data Analysis Expert / 金融数据分析专家

> **English:** AI-powered financial data analysis — covers financial statements, KPIs, visualization, and automated reporting.
>
> **中文:** 金融数据分析——覆盖财务报表、KPI、可视化、自动化报告。

---


### 金融监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 金融监管 | 2026年Q1：金融数据合规要求提升 | 数据分析框架需纳入合规和信披新标准 |
| 金融监管 | 理财信息披露'三清'推进，数据分析需关注新标准 | 数据分析框架需纳入合规和信披新标准 |
| 金融监管 | 反洗钱数据监控要求加强 | 数据分析框架需纳入合规和信披新标准 |

> **数据截止**: 2026-05-25 | 来源：证监会、NFRA、中证协、安永Q1分析
> **声明**: 以上动态供参考，具体以官方最新发布为准

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **数据分散** | 数据源多，整合耗时 | 统一数据模型 |
| **手工报表多** | 月报/季报重复劳动 | 自动报告生成 |
| **分析浅** | 只看表面数字 | 深度归因分析 |
| **可视化差** | 图表不直观 | 专业可视化模板 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** financial data analysis, KPI dashboard, data visualization, financial reporting, Python analysis

**中文触发词（优先）：** 数据分析 / 财务分析 / KPI追踪 / 数据可视化 / 自动化报告 / Python分析 / SQL查询 / 数据看板 / 经营分析 / 业绩分析 / 同比环比

---

## Core Capabilities / 核心能力

### 1. Financial Analysis Templates / 财务分析模板

```python
class FinancialAnalyzer:
    """财务分析引擎"""
    
    def income_statement_analysis(self, data: dict) -> dict:
        """损益表分析"""
        return {
            "收入趋势": self._trend_analysis(data["revenue"]),
            "毛利率分析": self._gross_margin_analysis(data),
            "费用结构": self._expense_breakdown(data),
            "利润质量": self._profit_quality_analysis(data)
        }
    
    def ratio_analysis(self, financial_data: dict) -> dict:
        """比率分析"""
        ratios = {
            "盈利能力": {
                "毛利率": data["gross_profit"] / data["revenue"],
                "净利率": data["net_profit"] / data["revenue"],
                "ROE": data["net_profit"] / data["equity"]
            },
            "运营效率": {
                "存货周转": data["cogs"] / data["inventory"],
                "应收账款周转": data["revenue"] / data["ar"]
            },
            "偿债能力": {
                "流动比率": data["current_assets"] / data["current_liabilities"],
                "资产负债率": data["total_liabilities"] / data["total_assets"]
            }
        }
        return ratios
```

### 2. Dashboard Templates / 数据看板模板

```python
DASHBOARD_TEMPLATES = {
    "CFO驾驶舱": {
        "widgets": [
            {"type": "kpi_card", "metrics": ["营收", "利润", "ROE"]},
            {"type": "line_chart", "data": "收入趋势"},
            {"type": "bar_chart", "data": "各业务线收入"},
            {"type": "waterfall", "data": "利润变动归因"},
            {"type": "gauge", "data": "KPI完成率"}
        ]
    },
    "业务分析看板": {
        "widgets": [
            {"type": "funnel", "data": "转化漏斗"},
            {"type": "heat_map", "data": "客户活跃度"},
            {"type": "pie_chart", "data": "客户分布"},
            {"type": "trend", "data": "关键指标趋势"}
        ]
    }
}
```

---

## Disclaimer

This skill provides data analysis tools for educational purposes.
## Appendix G. Alibaba Dianjin Fusion — finance-data-analysis v5.0.0

> **Source**: Alibaba Dianjin Digital Employee — `investment-advisor` (AI投资顾问) & `researcher` (AI研究员)  
> **Essence**: 股票市场分析、板块轮动、资金流向监控、技术指标综合研判  
> **Integrated**: 2026-05-31

---

### G.1 Core Workflow (Dianjin essence)

```
用户请求 → 股票/板块筛选 → 多维度数据分析 → 投资建议生成 → 风险提示
   ↓
Data sources:
  - 实时行情 (westock-data / neodata)
  - 资金流向 (主力净流入/流出)
  - 技术指标 (MACD, KDJ, RSI, BOLL)
  - 板块轮动 (行业涨跌排行)
  - 新闻舆情 (finance-news-aggregator)
   ↓
Analysis dimensions:
  1. 趋势判断 (日线/周线/月线)
  2. 资金面 (北向资金, 融资余额)
  3. 基本面 (PE/PB, 业绩增速)
  4. 技术面 (突破/回调, 支撑位/压力位)
  5. 风险面 (减持, ST, 质押)
   ↓
Output:
  - 投资建议 (买入/持有/卖出)
  - 目标价位 (止盈/止损)
  - 风险提示 (仓位控制)
```

---

### G.2 Stock Screening & Ranking (Dianjin method)

**筛选逻辑（投资顾问精髓）**：

```
Step 1: 板块筛选
  - 今日涨幅榜 TOP 10 板块
  - 资金净流入 TOP 10 板块
  - 政策利好板块 (国务院/央行/证监会)
   ↓
Step 2: 个股筛选
  - 板块内龙头股 (市值TOP3)
  - 资金流入强度 (主力净流入 > 1000万)
  - 技术形态 (突破/金叉)
  - 基本面 (ROE > 10%, 业绩正增长)
   ↓
Step 3: 风险过滤
  - 排除ST/*ST
  - 排除近期大额减持
  - 排除高质押率 (>50%)
   ↓
Output: 推荐股票清单 (TOP 5-10)
```

**评分模型（Dianjin风格）**：

| 维度 | 权重 | 评分标准 |
|------|------|---------|
| 趋势强度 | 30% | 均线多头排列 + 突破压力位 |
| 资金面 | 25% | 主力净流入 + 北向资金增持 |
| 基本面 | 20% | ROE + 业绩增速 + 估值合理 |
| 技术面 | 15% | MACD金叉 + KDJ低位 |
| 风险面 | 10% | 无重大风险事件 |

---

### G.3 Capital Flow Monitoring (Dianjin essence)

**资金流向分析框架**：

```
监控指标：
1. 主力资金净流入 (supermoney_in)
   - 定义：超大单 + 大单净流入
   - 阈值：> 1000万 = 强流入
   - 持续天数：3日累计 > 3000万 = 趋势确认

2. 北向资金 (north_money)
   - 沪股通 + 深股通
   - 单日流入 > 50亿 = 市场强势
   - 连续5日流入 = 外资看多

3. 融资余额 (margin_balance)
   - 融资买入额 / 总成交额
   - 占比 > 10% = 杠杆资金活跃
   - 余额增长 > 5% = 市场风险偏好提升

4. 板块轮动 (sector_rotation)
   - 今日强势板块 vs 昨日强势板块
   - 轮动规律：周期 → 金融 → 科技 → 消费
   - 异常：同一板块连续3日领涨 = 可能见顶
```

**实战案例（Dianjin风格）**：

```
【资金流向日报】
日期：2026-05-31

【大盘】
- 上证指数：+0.8%，成交额5200亿
- 北向资金：+68亿（连续3日净流入）
- 融资余额：+120亿（杠杆资金活跃）

【板块资金流向 TOP 5】
1. AI芯片：+52亿（新易盛 +12亿, 中际旭创 +10亿）
2. 新能源车：+38亿（宁德时代 +15亿, 比亚迪 +12亿）
3. 半导体：+31亿（北方华创 +8亿, 韦尔股份 +6亿）
4. 银行：+25亿（招商银行 +7亿, 兴业银行 +5亿）
5. 电力设备：+22亿（特变电工 +6亿, 国电南瑞 +5亿）

【主力出逃 TOP 5】
1. 房地产：-28亿（万科A -8亿, 保利发展 -6亿）
2. 传媒：-18亿（分众传媒 -5亿, 东方明珠 -4亿）
3. 钢铁：-15亿（宝钢股份 -4亿, 包钢股份 -3亿）
4. 煤炭：-12亿（中国神华 -4亿, 陕西煤业 -3亿）
5. 农业：-10亿（牧原股份 -3亿, 温氏股份 -2亿）

【投资建议】
- 激进型：关注AI芯片（新易盛, 中际旭创），短期强势
- 稳健型：配置银行（招商银行），防御+股息
- 风险提示：房地产资金持续出逃，规避相关板块
```

---

### G.4 Technical Indicator Synthesis (Dianjin method)

**多技术指标综合研判**：

```
买入信号（多指标共振）：
  ✅ MACD金叉 + KDJ < 20 + RSI < 30
  ✅ 突破20日均线 + 成交量放大 > 5日均量
  ✅ BOLL下轨反弹 + 上轨空间 > 20%

卖出信号（多指标共振）：
  ❌ MACD死叉 + KDJ > 80 + RSI > 70
  ❌ 跌破20日均线 + 成交量萎缩
  ❌ BOLL上轨回落 + 下轨空间 > 15%

观望信号：
  ⚠️ 单一指标信号（需等待共振）
  ⚠️ 横盘震荡（方向不明）
```

**实战模板（Dianjin风格）**：

```
【技术分析报告】
标的：新易盛 (sz300502)

【趋势判断】
- 日线：多头排列（MA5 > MA10 > MA20 > MA60）
- 周线：突破前高 85元，下一压力位 95元
- 月线：长期上升趋势，MACD红柱放大

【技术指标】
- MACD：DIF=2.5, DEA=1.8, 金叉状态
- KDJ：K=65, D=58, J=79（强势区域）
- RSI：RSI1=68, RSI2=62（偏强，未超买）
- BOLL：价格 88.5元，上轨 92元，下轨 78元

【量价关系】
- 今日成交量：5200万股（5日均量 3800万股，放量 +37%）
- 换手率：4.2%（活跃）
- 资金流向：主力净流入 +8.2亿

【综合研判】
✅ 买入信号（3个共振）
  - MACD金叉 + 突破20日线 + 主力净流入
⚠️ 风险提示：
  - 短期涨幅 +35%（近10日），注意回调风险
  - 下一压力位 92元（BOLL上轨）

【操作建议】
- 激进型：回调至 85元附近买入，止损 82元
- 稳健型：等待回踩 83-85元区间，分批建仓
- 目标价：第一目标 95元（+7%），第二目标 105元（+19%）
```

---

### G.5 Compliance & Risk Constraints (Dianjin standards)

**合规要求（投资顾问精髓）**：

1. **风险提示必须**：
   - 每份分析报告必须包含"股市有风险，投资需谨慎"
   - 明确标注"本报告仅供参考，不构成投资建议"
   - 推荐股票必须说明风险等级（高/中/低）

2. **数据来源标注**：
   - 实时行情：标注"数据来源：腾讯自选股"
   - 历史数据：标注"数据来源：聚源数据"
   - 新闻舆情：标注"数据来源：公开市场信息"

3. **禁止行为**：
   - ❌ 不允许承诺收益（"必涨", "稳赚"）
   - ❌ 不允许推荐ST股票（除非风险充分提示）
   - ❌ 不允许煽动性语言（"暴涨", "千载难逢"）

---

### G.6 Test Case (Dianjin quality)

**Test Case 1: 板块轮动分析**

```
Input: "帮我分析今天A股板块轮动情况，哪些板块值得关注？"

Expected Output:
1. 今日涨幅榜 TOP 5 板块
2. 资金净流入 TOP 5 板块
3. 板块轮动规律分析（是否健康）
4. 推荐关注板块（TOP 3）+ 理由
5. 风险提示（规避板块）

Quality Check:
- ✅ 数据实时性（今日数据）
- ✅ 逻辑合理性（板块轮动规律）
- ✅ 风险提示（规避板块）
- ✅ 合规性（不承诺收益）
```

**Test Case 2: 个股技术分析**

```
Input: "分析新易盛 (300502) 的技术走势，现在能买吗？"

Expected Output:
1. 趋势判断（日线/周线/月线）
2. 技术指标（MACD, KDJ, RSI, BOLL）
3. 量价关系（成交量, 换手率, 资金流向）
4. 综合研判（买入/观望/卖出）
5. 操作建议（入场价, 止损价, 目标价）

Quality Check:
- ✅ 多指标共振（不是单一指标）
- ✅ 风险提示（短期涨幅过大）
- ✅ 操作建议具体（价格区间）
- ✅ 合规性（标注"仅供参考"）
```

---

**End of Dianjin Fusion Content — finance-data-analysis v5.0.0**
