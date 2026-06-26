---
name: BaoStock 金融数据
description: 获取A股历史K线数据、季频财务数据、宏观经济数据、板块成分股等
read_when:
  - 获取股票历史K线数据
  - 查询财务数据基本面
  - 获取宏观经济数据
  - 查询板块成分股
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["python3","pip"],"packages":["baostock"]}}}
allowed-tools: Bash(baostock:*)
---

# BaoStock 金融数据技能

> 调用免费开源的A股金融数据平台 - 无需注册即可获取历史K线、财务数据、宏观数据

## 安装

```bash
pip install baostock
```

## 快速开始

```python
import baostock as bs
import pandas as pd

# 登录系统
lg = bs.login()
print('login respond error_code:', lg.error_code)
print('login respond error_msg:', lg.error_msg)

# 获取历史K线数据
rs = bs.query_history_k_data_plus(
    "sh.600000",
    "date,code,open,high,low,close,volume,amount",
    start_date='2024-01-01',
    end_date='2024-12-31',
    frequency="d",
    adjustflag="3"
)

# 转换为DataFrame
data_list = []
while (rs.error_code == '0') & rs.next():
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)
print(result)

# 登出系统
bs.logout()
```

## API 清单

### 1. 登录与登出

| 函数 | 说明 |
|------|------|
| `login()` | 登录系统 |
| `logout()` | 登出系统 |

### 2. 历史K线数据

| 函数 | 说明 |
|------|------|
| `query_history_k_data_plus()` | 获取历史A股K线数据（日/周/月/分钟线） |

**参数说明：**
- `code`: 股票代码（sh.600000 或 sz.000001）
- `fields`: 指标列表，逗号分隔
- `start_date`: 开始日期（YYYY-MM-DD）
- `end_date`: 结束日期（YYYY-MM-DD）
- `frequency`: 数据类型（d=日线, w=周线, m=月线, 5/15/30/60=分钟线）
- `adjustflag`: 复权类型（1=后复权, 2=前复权, 3=不复权）

**常用指标：**
```
date,code,open,high,low,close,volume,amount,adjustflag,turn,tradestatus,pctChg
peTTM,pbMRQ,psTTM,pcfNcfTTM,isST
```

### 3. 除权除息信息

| 函数 | 说明 |
|------|------|
| `query_dividend_data()` | 查询除权除息信息 |

**参数：**
- `code`: 股票代码
- `year`: 年份
- `yearType`: 年份类型（report=预案公告年份, operate=除权除息年份）

### 4. 复权因子

| 函数 | 说明 |
|------|------|
| `query_adjust_factor()` | 查询复权因子信息 |

**参数：**
- `code`: 股票代码
- `start_date`: 开始日期
- `end_date`: 结束日期

### 5. 季频财务数据

| 函数 | 说明 |
|------|------|
| `query_profit_data()` | 季频盈利能力 |
| `query_operation_data()` | 季频营运能力 |
| `query_growth_data()` | 季频成长能力 |
| `query_balance_data()` | 季频偿债能力 |
| `query_cash_flow_data()` | 季频现金流量 |
| `query_dupont_data()` | 季频杜邦指数 |

**参数：**
- `code`: 股票代码
- `year`: 统计年份
- `quarter`: 统计季度（1/2/3/4）

**主要返回字段：**
- 盈利能力：roeAvg, npMargin, gpMargin, netProfit, epsTTM
- 营运能力：NRTurnRatio, INVTurnRatio, CATurnRatio
- 成长能力：YOYEquity, YOYNI, YOYEPSBasic
- 偿债能力：currentRatio, quickRatio, cashRatio
- 现金流量：CAToAsset, CFOToOR, CFOToNP

### 6. 季频公司报告

| 函数 | 说明 |
|------|------|
| `query_performance_express_report()` | 季频业绩快报 |
| `query_forecast_report()` | 季频业绩预告 |

### 7. 证券基本资料

| 函数 | 说明 |
|------|------|
| `query_stock_basic()` | 证券基本资料 |

**参数：**
- `code`: 股票代码（可选）
- `code_name`: 股票名称（支持模糊查询）

**返回字段：**
- code, code_name, ipoDate, outDate, type, status

### 8. 证券元信息

| 函数 | 说明 |
|------|------|
| `query_trade_dates()` | 交易日查询 |
| `query_all_stock()` | 证券代码查询 |

### 9. 宏观经济数据

| 函数 | 说明 |
|------|------|
| `query_deposit_rate_data()` | 存款利率 |
| `query_loan_rate_data()` | 贷款利率 |
| `query_required_reserve_ratio_data()` | 存款准备金率 |
| `query_money_supply_data_month()` | 货币供应量/月 |
| `query_money_supply_data_year()` | 货币供应量/年 |

### 10. 板块数据

| 函数 | 说明 |
|------|------|
| `query_stock_industry()` | 行业分类 |
| `query_sz50_stocks()` | 上证50成分股 |
| `query_hs300_stocks()` | 沪深300成分股 |
| `query_zz500_stocks()` | 中证500成分股 |

## 股票代码规则

- `sh.xxxxxx` - 上海证券交易所（6位数字）
- `sz.xxxxxx` - 深圳证券交易所（6位数字）
- `sh.000001` - 上证指数
- `sh.000300` - 沪深300指数

## ⚠️ 股票筛选默认规则 (重要)

> **"全市场扫描" = 全部A股股票 ，不包括沪深300/上证50/中证500等成分股**
> 
> 除非特别指明"沪深300"、"上证50"，否则默认都是全部A股

| 字段 | 值 | 说明 |
|------|-----|------|
| `type` | `1` | 仅A股股票 (排除指数/ETF/可转债) |
| `status` | `1` | 仅上市状态 (排除退市/停牌) |

```python
# 获取上市中的A股股票列表 (全市场)
rs = bs.query_stock_basic()
data = []
while rs.next():
    data.append(rs.get_row_data())
df = pd.DataFrame(data, columns=rs.fields)
stocks = df[(df['type'] == '1') & (df['status'] == '1')]
# 约 5,191 只A股 (全市场)

# 仅沪深300成分股 (需特别指明)
rs = bs.query_hs300_stocks()
```

## ⚠️ 全市场扫描执行规则

> 全市场扫描 (5,000+股票) 耗时长，**必须提示用户确认后再执行**

### 执行流程

1. **提示用户** → 显示扫描范围、预估时间
2. **等待确认** → 用户确认后才开始执行
3. **分批执行** → 每50只显示进度，避免被限流
4. **完成后汇总** → 输出结果列表

### 提示语示例

```
⚠️ 即将进行全市场扫描
- 扫描范围：全部A股股票
- 预估时间：约30-60分钟
- 扫描进行中，请稍候...
```
/
## 示例代码

### 获取单只股票K线

```python
import baostock as bs
import pandas as pd

lg = bs.login()

# 获取浦发银行日K线
rs = bs.query_history_k_data_plus(
    "sh.600000",
    "date,code,open,high,low,close,volume,amount,pctChg",
    start_date='2024-01-01',
    end_date='2024-12-31'
)

data_list = []
while (rs.error_code == '0') & rs.next():
    data_list.append(rs.get_row_data())
    
df = pd.DataFrame(data_list, columns=rs.fields)
print(df)

bs.logout()
```

### 获取多只股票基本资料

```python
import baostock as bs

lg = bs.login()

# 获取所有股票
rs = bs.query_stock_basic()
while rs.next():
    print(rs.get_row_data())

bs.logout()
```

### 获取财务数据

```python
import baostock as bs

lg = bs.login()

# 获取浦发银行2024年Q2盈利能力
rs = bs.query_profit_data(code="sh.600000", year=2024, quarter=2)
while rs.next():
    print(rs.get_row_data())

bs.logout()
```

### 获取板块成分股

```python
import baostock as bs

lg = bs.login()

# 获取上证50成分股
rs = bs.query_sz50_stocks()
while rs.next():
    print(rs.get_row_data())

bs.logout()
```

## 注意事项

1. **无需注册** - BaoStock 免费使用，无需注册
2. **数据范围** - 支持1990年至今的历史数据
3. **更新频率** - 日K线盘后更新
4. **复权说明** - 使用涨跌幅复权法，与同花顺/通达信可能有差异
5. **频率限制** - 请勿频繁请求，建议添加适当延时

---

## 技术分析 (MyTT 集成)

> 本技能集成了 MyTT 技术分析库，当用户说"分析xxx的技术面"时，自动调用技术分析功能。

### 使用方式

| 用户输入 | 系统行为 |
|----------|----------|
| "分析中金黄金的技术面" | 调用 baostock + MyTT → 输出标准化技术分析报告 |
| "查询中金黄金的K线数据" | 仅调用 baostock → 输出原始K线数据（不经过MyTT） |

### 标准分析报告格式

当用户要求技术分析时，必须输出以下标准化格式：

#### 1. 均线系统
- MA5, MA10, MA20, MA30, MA60
- 均线方向判断（↗上涨/↘下跌/→持平）
- 金叉/死叉/多头/空头信号

#### 2. MACD 指标
- DIF, DEA, MACD 三个值
- 金叉/死叉判断
- 多头/空头判断

#### 3. KDJ 指标
- K, D, J 三个值
- 超买/超卖判断（K>80超买，K<20超卖）
- 金叉/死叉判断

#### 4. RSI 指标
- RSI 值
- 强弱判断（>70超买，<30超卖，50中性）

#### 5. BOLL 布林带
- 上轨、中轨、下轨
- 股价位置判断（突破上轨/跌破下轨/在中轨附近）

#### 6. 综合判断
- 短期评分 (1-5星)
- 中期评分 (1-5星)
- 操作建议

### 技术分析脚本

```bash
# 命令行使用
python3 scripts/technical_analysis.py sh.600489

# 或指定其他股票
python3 scripts/technical_analysis.py sz.000001
```

### 输出示例

```
📈 中金黄金 (sh.600489) 技术分析报告
更新时间: 2026-03-14 22:13:42
============================================================

【均线系统】
├── MA5: 31.47 元 (方向: ↘)
├── MA10: 32.17 元 (方向: ↘)
├── MA20: 31.39 元 (方向: ↗)
├── MA30: 32.28 元 (方向: ↗)
├── MA60: 28.35 元 (方向: ↗)
└── 信号: MA5<MA10 死叉, MA20>MA60 多头

【MACD指标】
├── DIF: 0.4310
├── DEA: 0.7290
└── MACD: -0.5960
    信号: 空头 死叉

【KDJ指标】
├── K: 24.53
├── D: 34.17
└── J: 5.26
    信号: 死叉, 超卖

【RSI指标】
├── RSI(6): 52.08
├── RSI(12): 52.08
└── RSI(24): 52.08
    信号: 偏强

【BOLL布林带】
├── 上轨: 33.93
├── 中轨: 31.39
└── 下轨: 28.84
    信号: 在中轨附近

【综合判断】
├── 短期: ⭐⭐ (2/5)
├── 中期: ⭐⭐⭐⭐ (4/5)
└── 建议: 中性震荡

============================================================
数据来源: BaoStock + MyTT
```

### 可用技术指标 (完整列表)

本技能集成了以下 MyTT 指标函数：

| 分类 | 指标 | 说明 |
|------|------|------|
| 趋势 | MACD | 指数平滑异同移动平均线 |
| 趋势 | DMI | 动向指标 |
| 趋势 | TRIX | 三重指数平滑平均线 |
| 趋势 | EXPMA | EMA指数平均数 |
| 趋势 | BBI | 多空指标 |
| 均线 | MA | 简单移动平均 |
| 均线 | EMA | 指数移动平均 |
| 均线 | SMA | 中国式SMA |
| 超买超卖 | KDJ | 随机指标 |
| 超买超卖 | RSI | 相对强弱指标 |
| 超买超卖 | WR | 威廉指标 |
| 超买超卖 | CCI |顺势指标 |
| 超买超卖 | ROC | 变动率指标 |
| 超买超卖 | MTM | 动量指标 |
| 通道 | BOLL | 布林带 |
| 通道 | KTN | 肯特纳交易通道 |
| 通道 | TAQ | 唐安奇通道 |
| 能量 | OBV | 能量潮 |
| 能量 | VR | 容量比率 |
| 能量 | MFI | 资金流量指标 |
| 能量 | ASI | 振动升降指标 |
| 能量 | EMV | 简易波动指标 |
| 形态 | BRAR | 情绪指标 |
| 形态 | PSY | 心理线 |
| 形态 | DPO | 区间震荡线 |
