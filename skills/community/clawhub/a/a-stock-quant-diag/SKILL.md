---
name: "a-stock-quant-diag"
description: "A-Share Quantitative Diagnosis (中英双语): 通用A股量化诊断方法论，调akshare/baostock数据，从技术面/估值分位/资金面/机构持仓/同行对比5维评分，输出买卖建议 | General A-share stock quantitative diagnosis methodology using akshare/baostock: 5-dimension scoring (technical, valuation, institutional, capital flow, peer comparison) for buy/sell recommendations"
---

# 通用A股个股量化诊断方法论

> **目标**：给定任意A股代码，AI自主完成80分以上的量化诊断
> **数据源**：akshare + baostock（互备）
> **适用**：任何沪深/创业板/科创板个股

---

## 一、整体流程（Pipeline）

```
Step 1  数据采集
  ├─ 长期K线 → 技术面指标
  ├─ 估值数据 → 估值分位
  ├─ 基金重仓 → 机构持仓变化
  ├─ 财务数据 → 业绩基本面
  ├─ 主营构成 → 业务拆解
  └─ 十大股东 → 筹码结构

Step 2  同板块/行业对比
  ├─ 识别个股所属申万一级行业 + 概念板块
  ├─ 选Top 3–10同板块标的横向对比
  └─ 计算板块均值/中位数 → 判断相对便宜/贵

Step 3  五维评分矩阵
  ├─ ⭐ 业绩兑现 (权重20%)
  ├─ ⭐ 估值安全 (权重25%)
  ├─ ⭐ 筹码结构 (权重20%)
  ├─ ⭐ 技术面 (权重20%)
  └─ ⭐ 情绪/资金 (权重15%)

Step 4  三档目标价测算
  ├─ 乐观（PE历史40%分位）
  ├─ 中性（历史均值/中位）
  └─ 悲观（历史70-80%分位）

Step 5  操作建议输出
  ├─ 评级：强烈推荐/推荐/观望/回避/强烈回避
  ├─ 目标建仓区间 + 止损位
  └─ 关键催化事件
```

---

## 二、数据采集详解

### 2.1 技术面（baostock优先，历史>1年场景）

```python
import baostock as bs
import pandas as pd

lg = bs.login()
rs = bs.query_history_k_data_plus("sz.000988",
    "date,open,high,low,close,volume,turn,amount,pctChg",
    start_date='2023-01-01', end_date='2026-07-23',
    frequency="d", adjustflag="2")
rows = []
while rs.error_code == '0' and rs.next():
    rows.append(rs.get_row_data())
df = pd.DataFrame(rows, columns=rs.fields)
for c in ['open','high','low','close','volume','turn','amount','pctChg']:
    df[c] = pd.to_numeric(df[c], errors='coerce')
bs.logout()
```

**提取指标：**
```python
last = df['close'].iloc[-1]
ret_5   = (last / df['close'].iloc[-6] - 1) * 100
ret_20  = (last / df['close'].iloc[-21] - 1) * 100
ret_60  = (last / df['close'].iloc[-61] - 1) * 100
ret_250 = (last / df['close'].iloc[-min(251, len(df))] - 1) * 100

h60  = df['close'].tail(60).max();  dd60  = (last / h60 - 1) * 100
h250 = df['close'].tail(250).max(); dd250 = (last / h250 - 1) * 100
ma20  = df['close'].tail(20).mean()
ma60  = df['close'].tail(60).mean()
ma250 = df['close'].tail(250).mean()
dist_ma250 = (last / ma250 - 1) * 100

turn20 = df['turn'].tail(20).mean()
turn90 = df['turn'].tail(90).mean()
turn_r = turn20 / turn90 if turn90 > 0 else 1
amt20  = df['amount'].tail(20).mean()
amt90  = df['amount'].tail(90).mean()
amt_r  = amt20 / amt90 if amt90 > 0 else 1
```

### 2.2 估值分位（akshare stock_value_em 含全历史数据）

```python
import akshare as ak
df_v = ak.stock_value_em(symbol="000988")
df_v['数据日期'] = pd.to_datetime(df_v['数据日期'])
df_v = df_v.sort_values('数据日期')
latest = df_v.iloc[-1]
pe_now = latest['PE(TTM)']
pb_now = latest['市净率']
ps_now = latest['市销率']

# 分时间窗
df_5y = df_v[df_v['数据日期'] >= (df_v['数据日期'].max() - pd.Timedelta(days=365*5))]
df_3y = df_v[df_v['数据日期'] >= (df_v['数据日期'].max() - pd.Timedelta(days=365*3))]
df_1y = df_v[df_v['数据日期'] >= (df_v['数据日期'].max() - pd.Timedelta(days=365))]

def pct(series, val):
    s = series.dropna()
    return (s < val).sum() / len(s) * 100 if len(s) > 0 else 0

# 输出示例：
# PE-TTM 66.2 | 5y分位92.1% | 中位33.0 | [18.5,109.2]
# PB 9.63 | 5y分位92.7% | 中位3.73 | [1.98,15.88]
```

**估值判断规则：**
| 分位 | 含义 | 动作 |
|---|---|---|
| 0-30% | 低估值 | 考虑买入 |
| 30-70% | 合理 | 持有 |
| 70-90% | 偏高 | 谨慎 |
| **>90%** | **极端高位** | **强烈回避/减仓** |

**行业特例说明：** 银行/保险用PB取代PE；周期股看PB分位；成长股（AI/半导体）PE常高，给弹性空间。如PEG<1.5可适当放松。

### 2.3 机构持仓变化（akshare stock_report_fund_hold）

```python
df_q1 = ak.stock_report_fund_hold(symbol="基金持仓", date="20260331")
row = df_q1[df_q1['股票代码'] == code]
# 输出：持有基金家数、持股总数、持股市值、持股变化(增仓/减仓)、持股变动比例

df_q2 = ak.stock_report_fund_hold(symbol="基金持仓", date="20260630")
```

**判断规则：**
| 基金家数变化 | 仓位变化 | 解读 |
|---|---|---|
| ↑ 增 | ↑ 增 | 共识看多 ✅ |
| ↓ 减 | ↓ 减 | 共识看空 ❌ |
| ↑ 增 | ↓ 减 | 分歧：散户接盘 ⚠️ |
| ↓ 减 | ↑ 增 | 分歧：少数集中 ⚠️ |

### 2.4 财务基本面（akshare stock_financial_abstract_ths）

```python
fin = ak.stock_financial_abstract_ths(symbol=code, indicator="按报告期")
# 取最近6期
# 关键列：营业总收入、营业总收入同比增长率、净利润、净利润同比增长率、销售毛利率、净资产收益率-摊薄
```

**关注点：** 营收增速趋势（加速/减速/稳定）、净利增速趋势、毛利率方向变化、ROE水平。

### 2.5 主营构成（akshare stock_zygc_em）

```python
biz = ak.stock_zygc_em(symbol=f"SZ{code}")  # 创业板SZ，沪市SH
biz_prod = biz[biz['分类类型'] == '按产品分类']
# 关键列：主营构成（产品名）、主营收入、收入比例、毛利率
```

**目的：** 识别业务是多元还是单一、各业务毛利高低及其行业竞争力。

### 2.6 十大流通股东（akshare）

```python
sh = ak.stock_gdfx_free_top_10_em(symbol=f"sz{code}", date="20260331")
# 识别：大股东增减持、社保/QFII/保险态度、北向持股变化
```

---

## 三、同行板块对比

### 3.1 识别个股所属板块

方案选一：
- **实时行情** `stock_zh_a_spot_em()` 含板块归属
- **主动识别**：根据主营业务关键词 > 申万行业 > 概念板块

**对比标的筛选（3-8只）：**
1. 同申万三级行业前5龙头
2. 剔除ST/次新/异常标

### 3.2 板块内指标对比

对每个对比标的技术面 + 估值 + 资金面 → 同上全流程

**核心对比矩阵字段：**
```python
[PE-TTM, PE分位5y, PB分位5y, 250日涨幅, 距60日高, 距MA250,
换手比20/90, Q1营收增速, Q1净利增速, 基金家数Q1, 基金家数Q2, 基金变动比例]
```

**输出**：排序榜 — 找出板块中最便宜、最贵、机构最集中、最被抛弃的标的，判断相对位置。

---

## 四、五维评分矩阵（Score=0~100）

### 维度1：业绩兑现（权20%）

| 条件 | 分 |
|---|---|
| 最新净利增速 > +50% | 100 |
| +30% ~ +50% | 80 |
| +10% ~ +30% | 60 |
| +0% ~ +10% | 40 |
| < 0% | 20 |
| < -50%（暴雷） | 0 |

**加速度加分**：营收增速连续2期加速 +20

### 维度2：估值安全（权25%）

| PE分位5y | 分 |
|---|---|
| <20% | 100 |
| 20-40% | 80 |
| 40-60% | 60 |
| 60-80% | 40 |
| 80-90% | 20 |
| >90% | 0 |

**PEG惩罚**：PEG>2.0 → 得分砍半

### 维度3：筹码结构（权20%）

| 基金家数变化 | 仓位变化 | 分 |
|---|---|---|
| ↑ | ↑ | 100 |
| ↑ | ↓ | 40 |
| ↓ | ↑ | 30 |
| ↓ | ↓ | **0** |

**北向调整**：增持>+20% +20 | 减持>-10% -20

### 维度4：技术面（权20%）

| 距MA250 | 基础分 |
|---|---|
| >+20% | 60 |
| +5%~+20% | 80 |
| -5%~+5% | 60 |
| -5%~-15% | 30 |
| <-15% | 0 |

**惩罚因子：**
- 20日涨幅< -20%（崩盘）→ -30
- 换手比<0.7（萎缩）→ -10

### 维度5：情绪/资金（权15%）

| 换手比(20/90) | 分 |
|---|---|
| 1.2~2.0（温和放量） | 100 |
| 0.8~1.2（正常） | 70 |
| >2.0（过度投机） | 30 |
| <0.6（无人问） | 20 |

**惩罚：** 250日涨幅>+300% → -30 | 连续跌停 → -20

---

## 五、三档目标价测算

```python
target_optimistic = pe_median * 0.7 * eps   # 保守，略低于均值
target_neutral    = pe_median * eps
target_pessimistic= pe_median * 1.3 * eps

# 概率权重
期望价 = target_optimistic*0.2 + target_neutral*0.5 + target_pessimistic*0.3
潜在下行% = (期望价 / 现价 - 1) * 100
```

**eps来源**：取最近4期TTM净利 / 总股本，或上一完整年度净利/总股本。

---

## 六、评级输出

| 总分 | 潜在下行 | 评级 | 动作 |
|---|---|---|---|
| ≥80 | — | ⭐⭐⭐⭐⭐ 强烈推荐 | 可建仓30%+ |
| ≥60 | <10% | ⭐⭐⭐⭐ 推荐 | 可建仓15% |
| ≥40 | — | ⭐⭐⭐ 观望 | 不加不减 |
| ≥20 | — | ⭐⭐ 回避 | 减仓50% |
| <20 | >-30% | ⭐ 强烈回避 | 清仓/不建仓 |

---

## 七、akshare 函数速查表

| 功能 | 函数 | 参数示例 | 说明 |
|---|---|---|---|
| 实时行情 | `stock_zh_a_spot_em()` | 无参 | 全市场5100+ |
| 日K线 | `stock_zh_a_hist()` | symbol, period=daily | 最多8000条 |
| 估值数据 | `stock_value_em()` | symbol="000988" | 含PE/PB/PS历史2000+条 |
| 财务摘要 | `stock_financial_abstract_ths()` | symbol, indicator=按报告期 | 季报年报 |
| 基金重仓 | `stock_report_fund_hold()` | symbol=基金持仓, date=Q末日期 | 全市场 |
| 概念板块 | `stock_board_concept_name_em()` | 无参 | 约300+板块 |
| 板块成分 | `stock_board_industry_cons_em()` | symbol="半导体" | 申万行业 |
| 主营构成 | `stock_zygc_em()` | symbol="SZ000988" | 加SZ/SH前缀 |
| 十大流通股本 | `stock_gdfx_free_top_10_em()` | symbol="sz000988" | 加sz/sh前缀 |
| 北向持股 | `stock_hsgt_hold_stock_em()` | market="北向" | 全市场 |
| 资金流向 | `stock_individual_fund_flow()` | stock, market | 大单净流入 |
| 个股信息 | `stock_individual_info_em()` | symbol | 基本面总览 |

**baostock备选**（更长历史）：
```python
bs.query_history_k_data_plus("sh.600519", ...)
# code: sh.xxxxxx / sz.xxxxxx
# adjustflag: 1-不复权 2-后复权 3-前复权
```

---

## 八、已验证案例

本方法论已成功验证3只：

1. **中际旭创(300308)** — 光模块龙头
   - 拥挤度>150, 估值95%+分位 → 强烈回避
   - 后续：20日跌-19%，距高点-22%

2. **华工科技(000988)** — 多元科技
   - 业绩优秀(Q1+56%) 但 PE 92%分位 + 公募减仓
   - 评级：观望 → 等待60-70元

3. **英维克(002837)** — 液冷温控龙头
   - Q1净利-82%暴雷 + PE 87%分位 + 36家基金清仓
   - 评级：强烈回避，预期下行-46%

---

## 九、注意事项

1. **数据时效**：基金重仓滞后1-2月；财务Q末后45天披露
2. **特例**：ST/退市/停牌/次新(上市<1年)不适用
3. **行业弹性**：银行保险用PB替代PE；周期看PB；成长PE弹性处理
4. **PEG宽松**：如PEG<1.5，PE偏高也可适当放松
5. **过拟合**：历史统计非未来保证，结合行业逻辑判断
6. **降级方案**：akshare失败→baostock→web_fetch/其他数据源

> **编写**：2026-07-23 | **akshare** 1.18.64 | **baostock** | 华子
