---
name: astock-unified-financial
version: 2.0
description: >
  A股行情与财务数据读取的终极整合技能。融合Baostock/Akshare双数据源的全部最佳实践、
  已知踩坑经验、单位转换、代码格式处理、缓存策略、错误处理与降级策略、研发费用查询、
  公司注册属地查询等核心场景。一站式解决A股数据读取的所有问题。
  本技能将分散在多个文档中的经验融合为一份自包含的完整指南。
agent_created: true
tags: [akshare, baostock, A股, 财务数据, 行情数据, 研发费用, 单位转换, 踩坑经验, 降级策略]
---

# A股金融数据整合技能（终极版）

> **融合自**: astock-financial-data-guide / akshare-financial-data-traps / A股行情与财务数据读取经验手册  
> **最后融合日期**: 2026-05-18

---

## 目录

1. [数据源总览与选择策略](#1-数据源总览与选择策略)
2. [推荐数据源组合 & 降级链](#2-推荐数据源组合--降级链)
3. [登录模式对照](#3-登录模式对照)
4. [Baostock 接口详解](#4-baostock-接口详解)
5. [Akshare 接口详解](#5-akshare-接口详解)
6. [废弃/不可用接口一览](#6-废弃不可用接口一览)
7. [研发费用查询专项指南](#7-研发费用查询专项指南)
8. [公司注册属地查询](#8-公司注册属地查询)
9. [股票代码格式处理](#9-股票代码格式处理)
10. [核心工具函数](#10-核心工具函数)
11. [单位转换速查](#11-单位转换速查)
12. [缓存策略](#12-缓存策略)
13. [错误处理与重试](#13-错误处理与重试)
14. [数据源降级策略](#14-数据源降级策略)
15. [最佳实践模板](#15-最佳实践模板)
16. [完整踩坑记录](#16-完整踩坑记录)
17. [附录：各接口列名速查](#17-附录各接口列名速查)

---

## 1. 数据源总览与选择策略

### 1.1 数据源对比

| 数据源 | 类型 | 行情 | 财报 | 分红 | 行业 | 优势 | 劣势 | 是否需要API Key |
|--------|------|------|------|------|------|------|------|----------------|
| **Baostock** | 证券宝 | ✅日/60分K线 | ✅五大季报 | ✅ | ✅ | 稳定、免费、无需Key、数据规范 | 字段单位需确认、登录/登出模式 | ❌ |
| **Akshare-同花顺** | Akshare | ❌ | ✅摘要/现金流/利润表 | ✅巨潮 | ❌ | 数据最全、带单位标注 | 列名可能随版本变 | ❌ |
| **Akshare-新浪** | Akshare | ❌ | ✅财务指标/利润表 | ❌ | ❌ | 覆盖面广、研发费数据完整 | 单位不确定(元/万元)、列名含(%)需判断 | ❌ |
| **Akshare-东方财富** | Akshare | ✅历史行情 | ✅个股信息 | ❌ | ✅ | 行情+基本面一体 | **服务器无法访问**⚠️ | ❌ |
| **Tushare** | 第三方 | ✅ | ✅ | ✅ | ✅ | 数据全面、质量高 | **需积分+API Key** | ✅ |
| **通达信** | 本地 | ✅ | ❌ | ❌ | ❌ | 速度极快(本地读取) | 仅行情、需安装通达信 | ❌ |

### 1.2 数据源能力速查矩阵

| 功能场景 | 推荐数据源(优先级) | 备注 |
|---------|-------------------|------|
| K线行情 | Baostock(主) → 东方财富(备) → 通达信(备) | Baostock稳定免费 |
| 财务摘要 | 同花顺财务摘要(主) → 新浪财务指标(备) | 同花顺带单位标注 |
| 利润表(含研发费) | 同花顺利润表(主) → 新浪利润表(备) | 同花顺带单位，新浪纯数字(元) |
| 研发费用 | 同花顺利润表(主) → 新浪利润表(备) → 四级降级策略 | ⚠️见第7章 |
| 分红数据 | 巨潮分红(主) → Baostock(备) | 巨潮"每10股"，Baostock"元/股" |
| 行业分类 | Baostock(主) → 东方财富(备,可能不可达) | Baostock含industry和province |
| 公司注册属地 | 巨潮公司概况(主) | `stock_profile_cninfo` |
| 实时行情 | 东方财富全市场实时行情(备) | 新浪实时行情替代方案 |
| 技术指标计算 | Baostock K线 + Numba加速 | 数据量大时用磁盘缓存 |

### 1.3 踩坑优先级通道

```
Level 1: 同花顺数据源(首选)  → parse_amount/parse_percent
Level 2: 新浪数据源(备用)    → safe_float + ÷1亿调单位
Level 3: Baostock(兜底)      → safe_float + convert_share
Level 4: 东方财富(降级)      → ⚠️当前服务器不可达
```

---

## 2. 推荐数据源组合 & 降级链

### 2.1 主力推荐组合

```
主力:      Akshare(同花顺/新浪) + Baostock(补充)
行情:      Baostock K线 (稳定可靠)
财报:      Akshare同花顺(主) → 新浪(备) → Baostock(兜底)
研发费:    同花顺利润表(主) → 新浪利润表(备) → 四级降级
分红:      Akshare巨潮(主) → Baostock(备)
行业:      Baostock query_stock_industry
注册属地:  巨潮 stock_profile_cninfo
```

### 2.2 降级链速查

| 目标数据 | 降级链 |
|---------|--------|
| 研发费用 | 同花顺利润表"研发费用" → 新浪利润表"研发费用" → 同花顺备用列名 → 新浪备用列名 |
| 净利润 | 同花顺利润表 → 新浪利润表 → Baostock profit |
| 营收 | 同花顺利润表 → 新浪利润表 → Baostock profit |
| 分红 | 巨潮分红 → Baostock dividend |
| 行业 | Baostock industry → 东方财富(可能不可达) |
| 注册地 | 巨潮 profile_cninfo → (无备用) |

---

## 3. 登录模式对照

| 数据源 | 登录方式 | 生命周期 |
|--------|---------|---------|
| Baostock | `bs.login()` / `bs.logout()` | 需显式管理, 查询前必须登录 |
| Akshare | 无需登录 | 直接调用 |
| Tushare | `ts.pro_api('your_token')` | Token一次性设置 |

**Baostock登录建议**: 在程序入口登录, 程序出口登出, 中间复用连接。换股时无需登出, 仅在切换完全不同股票或退出时登出。

---

## 4. Baostock 接口详解

### 4.1 登录/登出

```python
import baostock as bs

# 登录
lg = bs.login()
if lg.error_code != '0':
    print(f"登录失败: {lg.error_msg}")

# 登出
bs.logout()

# ⚠️: 查询前必须登录, 查询后无需立即登出(可复用连接)
```

### 4.2 K线数据

```python
# 日线
rs = bs.query_history_k_data_plus(
    code="sh.600000",        # baostock格式: sh.600000 / sz.000001 / bj.430047
    fields="date,close,open,high,low,volume,amount,turn",
    start_date="2025-01-01",
    end_date="2025-12-31",
    frequency="d",           # d=日线, w=周线, m=月线
    adjustflag="3"           # 1=后复权, 2=前复权, 3=不复权
)

# 60分钟线
rs = bs.query_history_k_data_plus(
    code="sh.600000",
    fields="date,time,close,open,high,low,volume,amount",
    start_date="2025-01-01",
    end_date="2025-12-31",
    frequency="60",          # 5/15/30/60分钟
    adjustflag="3"
)

# 遍历结果
def bs_query_to_df(rs):
    """将baostock ResultData转为DataFrame"""
    rows = []
    while (rs.error_code == '0') and rs.next():
        rows.append(rs.get_row_data())
    if not rows:
        return None
    import pandas as pd
    return pd.DataFrame(rows, columns=rs.fields)
```

**⚠️ 踩坑**:
- K线返回的 close/volume 等字段都是**字符串类型**, 需手动转float
- 60分钟线需 `fields` 含 `time` 字段
- `adjustflag="3"` 不复权时, 价格为原始价格

### 4.3 财务数据(五大季报)

```python
# 盈利数据
rs = bs.query_profit_data(code="sh.600000", year=2024, quarter=4)
# 关键字段: totalShare, liqaShare, epsTTM, gpMargin, netProfit, roeAvg, roeDiluted

# 成长数据
rs = bs.query_growth_data(code="sh.600000", year=2024, quarter=4)
# 关键字段: YOYEquity, YOYAsset, YOYNI, YOYEPSBasic, YOYPNI, YOYOR, YOYGR

# 运营数据
rs = bs.query_operation_data(code="sh.600000", year=2024, quarter=4)
# 关键字段: NetProfitGrowRate, OperatingProfitGrowRate, TotalRevenueGrowRate

# 现金流数据
rs = bs.query_cash_flow_data(code="sh.600000", year=2024, quarter=4)
# 关键字段: CAToAsset, NCAToAsset, CFOToOR

# 资产负债数据
rs = bs.query_balance_data(code="sh.600000", year=2024, quarter=4)
# 关键字段: totalAssets, totalLiab, totalEquity, currentAssets, currentLiab
```

**⚠️ 踩坑**:
- **totalShare单位不确定**: 实测某些版本返回"万股"而非"股", 用 `convert_share()` 自动检测
- **所有比率字段都是小数形式**, 需×100转百分比显示
- **quarter参数**: 1-4对应Q1-Q4, 年报为Q4
- **空字符串/None**: 字段可能返回空字符串''或None, 需用 `safe_float()` 统一处理
- **这些函数不接受yearType参数**
- **totalShare无province/area/city/region字段** — 不能用于查注册属地

### 4.4 分红数据

```python
rs = bs.query_dividend_data(
    code="sh.600000",
    year=2024,
    yearType="report"    # "report"=按报告期, "operate"=按运营期
)
# 关键字段: dividCashPsBeforeTax(元/股), dividPreistNoTax(每10股送股), dividAistNoTax(每10股转增)
```

### 4.5 行业/基本信息

```python
# 行业分类
rs = bs.query_stock_industry(code="sh.600000")
# 字段: industry, industryClassification, province(省份)

# 注意: baostock的province字段只存在于query_stock_basic中？
# 实测: query_stock_industry返回字段: updateDate, code, code_name, industry, industryClassification
# 并没有province字段！注册属地请用巨潮profile_cninfo

# 股票基本信息
rs = bs.query_stock_basic(code="sh.600000")
# 字段: code, code_name, ipoDate, outDate, type, status

# 交易日查询
rs = bs.query_trade_dates(start_date="2025-01-01", end_date="2025-12-31")

# 全部股票列表
rs = bs.query_all_stock(day="2025-05-12")
```

### 4.6 Baostock 字段速查

**盈利数据(query_profit_data)**:

| 字段 | 含义 | 单位 | 转换 |
|------|------|------|------|
| totalShare | 总股本 | 股⚠️ | `convert_share()` → 亿股 |
| liqaShare | 流通股本 | 股⚠️ | `convert_share()` → 亿股 |
| epsTTM | 每股收益TTM | 元/股 | 直接使用 |
| gpMargin | 毛利率 | 小数 | ×100→% |
| netProfit | 净利润 | 元 | ÷1亿→亿元 |
| roeAvg | 平均ROE | 小数 | ×100→% |
| roeDiluted | 稀释ROE | 小数 | ×100→% |
| operatingRevenue | 营业收入 | 元 | ÷1亿→亿元 |

**成长数据(query_growth_data)**:

| 字段 | 含义 | 单位 | 转换 |
|------|------|------|------|
| YOYEquity | 净资产同比增长率 | 小数 | ×100→% |
| YOYAsset | 总资产同比增长率 | 小数 | ×100→% |
| YOYNI | 净利润同比增长率 | 小数 | ×100→% |
| YOYPNI | 归母净利润同比增长率 | 小数 | ×100→% |
| YOYOR | 营业收入同比增长率 | 小数 | ×100→% |
| YOYGR | 营业总收入同比增长率 | 小数 | ×100→% |

**分红数据(query_dividend_data)**:

| 字段 | 含义 | 单位 |
|------|------|------|
| dividCashPsBeforeTax | 税前每股现金分红 | 元/股 |
| dividPreistNoTax | 每10股送股数 | 股 |
| dividAistNoTax | 每10股转增股数 | 股 |

---

## 5. Akshare 接口详解

### 5.1 同花顺财务摘要 (`stock_financial_abstract_ths`)

```python
import akshare as ak

# 按年度
df = ak.stock_financial_abstract_ths(symbol="600000", indicator="按年度")
# 按单季度
df = ak.stock_financial_abstract_ths(symbol="600000", indicator="按单季度")
```

**⚠️ 踩坑**:
- 金额列带单位: 如 "1483.91亿"、"4.82万亿"、"3391.23万", 需用 `parse_amount()` 解析
- 比率列带%号: 如 "6.22%", 需用 `parse_percent()` 解析
- 返回DataFrame最新行在**最后**, 遍历时注意顺序
- 列名可能因akshare版本更新而变化
- **⚠️ 此接口没有"研发费用"列!** 研发费需从利润表获取

### 5.2 同花顺现金流量表 (`stock_financial_cash_ths`)

```python
df = ak.stock_financial_cash_ths(symbol="600000", indicator="按年度")
```

**⚠️ 踩坑**:
- 列名极长且包含标点符号, 硬编码容易出错
- 同一列名在不同akshare版本中可能有细微差异(空格/标点)

### 5.3 同花顺利润表 (`stock_financial_benefit_ths`) ✅含研发费

```python
df = ak.stock_financial_benefit_ths(symbol="600000", indicator="按年度")
# ⚠️ 注意: 接口名是 stock_financial_benefit_ths, 不是 stock_profit_sheet_ths(已废弃)
```

**⚠️ 踩坑**:
- 金额列带单位: 如 "1.90亿"、"227.55亿"、"6192.32万", 需用 `parse_amount` 解析
- **研发费用列在此接口有!** 列名固定为 `"研发费用"`
- 2017年以前的数据研发费列值可能为 `False`(布尔值), 表示该年度未单独披露
- 报告期格式: "2025"(纯年份), 匹配用 `str(year) in rp`
- 列名可能为: "研发费用"/"研究开发费用"/"研究与开发费用", 需多列名尝试

### 5.4 新浪利润表 (`stock_financial_report_sina` symbol="利润表") ✅含研发费

```python
df = ak.stock_financial_report_sina(stock="000063", symbol="利润表")
```

**⚠️ 踩坑**:
- **金额列单位为"元"**, 是纯数字(float), 如 `22754978000.0`, 需÷1亿转亿元
- 报告日格式: `"20251231"`, 匹配年报用 `f"{year}1231" in rp`
- 该接口同时返回季报和年报数据, 按报告日筛选即可
- **研发费用列在此接口有!** 列名固定为 `"研发费用"`
- 数据非常完整, 2017年以前的研发费也有(同花顺利润表可能返回False)

### 5.5 新浪财务指标 (`stock_financial_analysis_indicator`)

```python
df = ak.stock_financial_analysis_indicator(symbol="600000", start_year="2022")
# 按日期索引, 每行一个报告期
```

**⚠️ 踩坑**:
- **列名含(%)的毛利率列**: 返回值可能是百分比(如92.15)也可能是小数(如0.92), 需用 `convert_sina_percent()` 或 `abs(f) < 2` 判断
- **列名含(元)的金额列**: 实际单位可能是"元"也可能是"万元", 不确定! 优先用 `parse_amount` 处理, `parse_amount` 返回 None 时按"元"÷1亿
- 新浪数据通过日期索引访问: `df.loc[f"{year}-12-31"]`
- **❌ 此接口没有"研发费用"列!** 研发费需从利润表获取

### 5.6 巨潮分红数据 (`stock_dividend_cninfo`)

```python
df = ak.stock_dividend_cninfo(symbol="600000")
# 关键列: 报告时间, 派息比例(每10股派息额)
# 报告时间格式: "2024年年报"
```

**⚠️ 踩坑**:
- 派息比例是"每10股"的金额, 需÷10转为每股分红
- 匹配年报: `f'{year}年报' in str(row['报告时间'])`

### 5.7 东方财富个股信息 (`stock_individual_info_em` ⚠️服务器不可达)

```python
# ⚠️ 以下接口从当前服务器无法访问, 仅作降级参考
df = ak.stock_individual_info_em(symbol="600000")     # 个股基本信息
df = ak.stock_zh_a_hist(symbol="600000", period="daily",
                         start_date="20250101", end_date="20251231")  # 历史行情
```

### 5.8 巨潮公司概况 (`stock_profile_cninfo`) ✅推荐用于注册地

```python
df = ak.stock_profile_cninfo(symbol="600519")
# 含"注册地址"列, 值为完整地址如"贵州省仁怀市茅台镇"
```

### 5.9 新浪实时行情 (`stock_zh_a_spot_em` 替代方案)

```python
df = ak.stock_zh_a_spot_em()  # 全市场实时行情
```

### 5.10 Akshare 安全调用封装

```python
def ak_safe_call(fn, *args, default=None, **kwargs):
    """安全调用akshare接口"""
    try:
        result = fn(*args, **kwargs)
        if result is None or (hasattr(result, 'empty') and result.empty):
            return default
        return result
    except Exception as e:
        print(f"  [AK] 接口异常: {e}")
        return default
```

---

## 6. 废弃/不可用接口一览

> ⚠️ **直接从历史踩坑中整理, 不要再用**

| 接口名 | 状态 | 替代方案 |
|--------|------|---------|
| `stock_profit_sheet_ths` | ❌ 已废弃(不存在) | `stock_financial_benefit_ths` |
| `stock_financial_abstract_ths` | ❌ 无研发费列 | `stock_financial_benefit_ths` |
| `stock_financial_analysis_indicator` | ❌ 无研发费列 | `stock_financial_report_sina` |
| `stock_individual_info_em` | ❌ 服务器不可达(2026.05) | `stock_profile_cninfo` |
| `stock_info_sz_name_code(indicator=...)` | ❌ 不接受indicator参数 | 不使用 |

### 接口名易混提醒

| 易混淆名 | 正确名 |
|---------|--------|
| ❌ `stock_profit_sheet_ths` | ✅ `stock_financial_benefit_ths` |
| — | ✅ `stock_financial_report_sina(stock="000063", symbol="利润表")` |

---

## 7. 研发费用查询专项指南

### 7.1 正确查询路径

```
研发费用查询只能从利润表获取
❌ 财务摘要(stock_financial_abstract_ths)  → 无研发费列
❌ 新浪财务指标(stock_financial_analysis_indicator) → 无研发费列
✅ 同花顺利润表(stock_financial_benefit_ths) → 有"研发费用"列
✅ 新浪利润表(stock_financial_report_sina symbol="利润表") → 有"研发费用"列
```

### 7.2 四级降级策略

```
Level 1: 同花顺利润表 → "研发费用"列(首选)
Level 2: 新浪利润表   → "研发费用"列
Level 3: 同花顺利润表 → 备用列名("研究开发费用"/"研究与开发费用")
Level 4: 新浪利润表   → 备用列名(如列名有变化)
```

### 7.3 同花顺利润表获取研发费

```python
df = ak.stock_financial_benefit_ths(symbol="000063", indicator="按年度")
for _, row in df.iterrows():
    rp = str(row.get('报告期', ''))
    if '2025' in rp:
        rd = row.get('研发费用', '')  # 返回如 "227.55亿"
        if rd is not False:          # 早期年份可能为False
            p = parse_amount(rd)     # → 227.55 (亿元)
        break
```

### 7.4 新浪利润表获取研发费

```python
df = ak.stock_financial_report_sina(stock="000063", symbol="利润表")
for _, row in df.iterrows():
    rp = str(row.get('报告日', ''))
    if '20251231' in rp:
        raw_val = row.get('研发费用', '')  # 返回纯数字如 22754978000.0
        f = safe_float(raw_val)
        rd_yi = f / 100000000               # → 227.55 亿元
        break
```

### 7.5 研发费用完整容错代码

```python
def get_rd_expense(pure_code, year):
    """获取指定股票指定年度的研发费用(亿元)
    降级链: 同花顺利润表 → 新浪利润表
    """
    # Level 1: 同花顺利润表
    df = ak_safe_call(ak.stock_financial_benefit_ths, symbol=pure_code, indicator="按年度")
    if df is not None:
        rd_cols = ['研发费用', '研究开发费用', '研究与开发费用']
        for _, row in df.iterrows():
            if str(year) in str(row.get('报告期', '')):
                for col in rd_cols:
                    val = row.get(col)
                    if val is not False and val is not None:
                        p = parse_amount(val)
                        if p is not None:
                            return p
    # Level 2: 新浪利润表
    df = ak_safe_call(ak.stock_financial_report_sina, stock=pure_code, symbol="利润表")
    if df is not None:
        target = f"{year}1231"
        for _, row in df.iterrows():
            if target in str(row.get('报告日', '')):
                val = row.get('研发费用')
                f = safe_float(val)
                if f != NO_DATA:
                    return f / 100000000
    return NO_DATA
```

### 7.6 验证数据

| 股票 | 同花顺利润表 | 新浪利润表 | 一致性 |
|------|------------|-----------|--------|
| 中兴通讯000063 | 227.55亿 | 227.55亿 | ✅ |
| 茅台600519 | 1.90亿 | 1.90亿 | ✅ |

---

## 8. 公司注册属地查询

### 8.1 正确查询方法

```python
import akshare as ak
import re

# 巨潮公司概况(首选, 唯一可靠来源)
df = ak.stock_profile_cninfo(symbol="600519")
# 含"注册地址"列, 值为完整地址如"贵州省仁怀市茅台镇"

# ⚠️ baostock的query_stock_industry无province字段!
# 不要用baostock查注册属地
```

### 8.2 省份提取函数

```python
def extract_province(addr):
    """从完整注册地址提取省份"""
    if not addr:
        return ''
    # 直辖市
    for city in ['北京', '上海', '天津', '重庆']:
        if city in addr:
            return city + '市'
    # 省/自治区/特别行政区
    m = re.search(r'([\u4e00-\u9fa5]+省|[\u4e00-\u9fa5]+自治区|[\u4e00-\u9fa5]+特别行政区)', addr)
    if m:
        return m.group(1)
    return addr
```

### 8.3 验证数据

| 股票 | 巨潮注册地址 | 提取省份 |
|------|------------|---------|
| 茅台600519 | 贵州省仁怀市茅台镇 | 贵州省 ✅ |
| 中兴通讯000063 | 广东省深圳市南山区 | 广东省 ✅ |
| 宁德时代300750 | 福建省宁德市 | 福建省 ✅ |
| 隆基绿能601012 | 陕西省西安市 | 陕西省 ✅ |
| 平安银行000001 | 广东省深圳市 | 广东省 ✅ |

---

## 9. 股票代码格式处理

### 9.1 格式对照

| 格式 | 示例 | 使用场景 |
|------|------|---------|
| 纯代码 | `600000` | 用户输入、akshare接口 |
| Baostock格式 | `sh.600000` / `sz.000001` / `bj.430047` | baostock全部接口 |
| 东方财富格式 | `600000` (纯代码) | akshare东方财富接口 |
| Tushare格式 | `600000.SH` | tushare接口 |

### 9.2 市场前缀规则

| 开头数字 | 市场 | Baostock前缀 | Tushare后缀 | 说明 |
|---------|------|-------------|------------|------|
| 6, 9 | 上海证券交易所 | sh. | .SH | 9开头为科创板 |
| 0, 3 | 深圳证券交易所 | sz. | .SZ | 3开头为创业板 |
| 8, 4 | 北京证券交易所 | bj. | .BJ | 北交所 |

### 9.3 代码识别与转换

```python
def normalize_stock_code(raw):
    """统一识别股票代码, 返回 (baostock格式, 纯代码)
    支持输入: 600000 / sh.600000 / SH600000 / 430047 / bj.430047
    """
    raw = raw.strip().replace(' ', '').replace('\uff0e', '.').replace('\u3002', '.')

    if '.' in raw:
        parts = raw.split('.')
        bs_code = parts[0].lower() + '.' + parts[1]
        pure_code = parts[1]
    elif raw.startswith('6') or raw.startswith('9'):
        bs_code = 'sh.' + raw
        pure_code = raw
    elif raw.startswith('0') or raw.startswith('3'):
        bs_code = 'sz.' + raw
        pure_code = raw
    elif raw.startswith('8') or raw.startswith('4'):
        bs_code = 'bj.' + raw  # 北交所
        pure_code = raw
    else:
        raise ValueError(f"无法识别代码格式: {raw}")

    return bs_code, pure_code
```

### 9.4 注意事项

1. **北交所代码(8/4开头)**: 必须映射为 `bj.` 前缀, 不能用 `sh.` 或 `sz.`
2. **全角句号**: 用户可能输入全角句号(`．`/`。`), 需先替换为半角(`.`)
3. **大小写**: `SH.600000` 和 `sh.600000` 等价, 统一转小写
4. **排序陷阱**: 对"3.10"等字符串排序时不能用默认字符串排序, 需按数字排序:
   ```python
   sorted(selected, key=lambda k: tuple(int(x) for x in k.split('.')))
   ```

---

## 10. 核心工具函数

```python
import re
import math

NO_DATA = "无"  # 统一无数据标记

# ── safe_float ──
def safe_float(val, default=NO_DATA):
    """安全转浮点, 处理None/空串/NaN/False/超限值"""
    if val is None or val == '' or val == 'False' or val == 'NaN':
        return default
    try:
        f = float(val)
        if math.isnan(f) or math.isinf(f) or abs(f) > 1e15:
            return default
        return f
    except (ValueError, TypeError):
        return default

# ── parse_amount ──
def parse_amount(s):
    """解析带单位的金额字符串, 统一转为亿元
    '1483.91亿' → 1483.91
    '4.82万亿'  → 48200
    '3391.23万' → 0.339123
    纯数字(元)  → 原值(调用者需自行÷1亿)
    无法解析    → None
    """
    if s is None or s == '' or s == 'False':
        return None
    s = str(s).strip()
    m = re.match(r'^([-\d.]+)\s*万亿$', s)
    if m:
        return float(m.group(1)) * 10000
    m = re.match(r'^([-\d.]+)\s*亿$', s)
    if m:
        return float(m.group(1))
    m = re.match(r'^([-\d.]+)\s*万$', s)
    if m:
        return float(m.group(1)) / 10000
    try:
        return float(s)  # 纯数字, 单位需调用者判断
    except (ValueError, TypeError):
        return None

# ── parse_percent ──
def parse_percent(s):
    """解析百分比字符串
    '6.22%' → 6.22
    纯数字  → 原值(可能是小数也可能是百分比)
    """
    if s is None or s == '' or s == 'False':
        return None
    s = str(s).strip()
    m = re.match(r'^([-\d.]+)\s*%$', s)
    if m:
        return float(m.group(1))
    try:
        return float(s)
    except (ValueError, TypeError):
        return None

# ── convert_share ──
def convert_share(val):
    """Baostock totalShare/liqaShare 自动单位检测与转换(→亿股)"""
    f = safe_float(val)
    if f == NO_DATA:
        return NO_DATA
    if f < 10000 and f > 0:
        return f / 10000   # 万股→亿股
    else:
        return f / 100000000  # 股→亿股

# ── convert_sina_percent ──
def convert_sina_percent(val):
    """新浪(%)列: 判断是小数还是百分比, 统一转为百分比"""
    f = safe_float(val)
    if f == NO_DATA:
        return NO_DATA
    if abs(f) < 2:    # 小数形式如0.92
        f = f * 100
    return f           # 已是百分比如92.15

# ── extract_province ──
def extract_province(addr):
    """从完整注册地址提取省份"""
    if not addr:
        return ''
    for city in ['北京', '上海', '天津', '重庆']:
        if city in addr:
            return city + '市'
    m = re.search(r'([\u4e00-\u9fa5]+省|[\u4e00-\u9fa5]+自治区|[\u4e00-\u9fa5]+特别行政区)', addr)
    if m:
        return m.group(1)
    return addr
```

---

## 11. 单位转换速查

| 源 | 原始单位 | 目标单位 | 转换方法 | 备注 |
|----|---------|---------|---------|------|
| 同花顺金额 | "1483.91亿" | 亿元 | `parse_amount()` | 自动处理万亿/亿/万 |
| 同花顺利润表 False值 | 布尔False | — | `if val is not False:` | 视为无数据, 跳过 |
| 新浪金额(元)列 | 不确定 | 亿元 | 先`parse_amount()`, 返回None时÷1亿 | ⚠️单位可能为万元 |
| 新浪利润表金额 | 元(纯数字) | 亿元 | `val / 100000000` | 纯float, 必须÷1亿 |
| Baostock金额 | 元 | 亿元 | `val / 100000000` | netProfit等 |
| Baostock股本 | 股/万股 | 亿股 | `convert_share()` | 自动检测如果val<10000为万股 |
| Baostock比率 | 小数 | 百分比 | `val * 100` | gpMargin/roeAvg等 |
| 新浪比率(%)列 | 不确定 | 百分比 | `convert_sina_percent()` | `abs(f)<2`判断 |
| 同花顺比率 | "6.22%" | 百分比 | `parse_percent()` | 带%号 |
| 巨潮分红 | 每10股派息 | 每股分红 | `val / 10` | 派息比例列 |

---

## 12. 缓存策略

### 12.1 策略选择

| 场景 | 推荐策略 | 理由 |
|------|---------|------|
| 单股票多指标查询 | 内存字典缓存 | 数据量小, 生命周期短 |
| 多股票回测 | 磁盘CSV缓存 | 数据量大, 需跨运行复用 |
| 实时行情 | 不缓存 | 数据时效性要求高 |
| 静态财务数据 | 磁盘缓存+过期时间 | 年报季度更新, 可缓存较长时间 |

### 12.2 内存缓存(财务查询场景)

```python
class FinancialDataFetcher:
    def __init__(self):
        self._cache = {}

    def bs_query(self, func_name, year, quarter):
        cache_key = f"bs_{func_name}_{year}_{quarter}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        # ... 查询逻辑 ...
        self._cache[cache_key] = result
        return result
```

### 12.3 磁盘缓存(回测场景)

```python
import os
import pandas as pd

CACHE_DIR = "data_cache"

def get_cache_path(code, start_date, end_date, freq):
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, f"{code}_{start_date}_{end_date}_{freq}.csv")

def load_cache(path):
    if os.path.exists(path):
        return pd.read_csv(path, dtype=str)
    return None

def save_cache(path, df):
    df.to_csv(path, index=False)

# 使用示例
cache_path = get_cache_path("sh.600000", "2025-01-01", "2025-12-31", "d")
df = load_cache(cache_path)
if df is None:
    df = fetch_from_baostock(...)
    save_cache(cache_path, df)
```

---

## 13. 错误处理与重试

### 13.1 Baostock 带重试查询

```python
import time
import socket

def bs_query_with_retry(fn, max_retries=3, wait_seconds=2):
    """带重试的baostock查询"""
    for attempt in range(max_retries):
        try:
            rs = fn()
            if rs.error_code == '0':
                return rs
            else:
                print(f"  [BS] 查询错误: {rs.error_msg}, 重试 {attempt+1}/{max_retries}")
        except (socket.timeout, TimeoutError, OSError) as e:
            print(f"  [BS] 网络异常: {e}, 重试 {attempt+1}/{max_retries}")
        time.sleep(wait_seconds)
    return None
```

### 13.2 Akshare 安全调用

```python
def ak_safe_call(fn, *args, default=None, **kwargs):
    """安全调用akshare接口"""
    try:
        result = fn(*args, **kwargs)
        if result is None or (hasattr(result, 'empty') and result.empty):
            return default
        return result
    except Exception as e:
        print(f"  [AK] 接口异常: {e}")
        return default
```

### 13.3 Baostock 结果转DataFrame

```python
def bs_query_to_df(rs):
    """将baostock ResultData转为DataFrame"""
    rows = []
    while (rs.error_code == '0') and rs.next():
        rows.append(rs.get_row_data())
    if not rows:
        return None
    import pandas as pd
    return pd.DataFrame(rows, columns=rs.fields)
```

---

## 14. 数据源降级策略

### 14.1 通用降级函数

```python
def fetch_with_fallback(primary_fn, fallback_fn1=None, fallback_fn2=None):
    """带降级的数据获取: 主数据源 → 备用1 → 备用2 → "无" """
    result = primary_fn()
    if result is not None and result != NO_DATA:
        return result
    if fallback_fn1:
        result = fallback_fn1()
        if result is not None and result != NO_DATA:
            return result
    if fallback_fn2:
        result = fallback_fn2()
        if result is not None and result != NO_DATA:
            return result
    return NO_DATA
```

### 14.2 推荐降级链

| 目标 | 降级链 |
|------|--------|
| 财报 | Akshare同花顺 → 新浪 → Baostock |
| 分红 | Akshare巨潮 → Baostock |
| 行业 | Baostock → 东方财富(可能不可达) |
| 研发费 | 同花顺利润表 → 新浪利润表 → 同花顺备用列名 → 新浪备用列名 |

---

## 15. 最佳实践模板

### 15.1 FinancialDataFetcher 完整类模板

```python
import datetime
import baostock as bs

class FinancialDataFetcher:
    """财务数据获取器 - 主力+备用双源模式"""

    def __init__(self, bs_code, pure_code):
        self.bs_code = bs_code
        self.pure_code = pure_code
        self._cache = {}
        self._bs_logged_in = False
        self.now = datetime.datetime.now()
        # 判断"去年": 5月前年报可能未出, 取前年
        self.last_year = self.now.year - 2 if self.now.month < 5 else self.now.year - 1
        self.prev_year = self.last_year - 1
        self.year_before = self.last_year - 2

    # ── 登录管理 ──
    def bs_login(self):
        if not self._bs_logged_in:
            lg = bs.login()
            if lg.error_code != '0':
                return False
            self._bs_logged_in = True
        return True

    def bs_logout(self):
        if self._bs_logged_in:
            bs.logout()
            self._bs_logged_in = False

    def _ensure_bs_login(self):
        """确保已登录(在所有baostock查询前调用)"""
        if not self._bs_logged_in:
            self.bs_login()

    # ── 通用查询(带缓存) ──
    def bs_query(self, func_name, year=None, quarter=None):
        self._ensure_bs_login()
        cache_key = f"bs_{func_name}_{year}_{quarter}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        # ... 实际查询逻辑 ...
        # self._cache[cache_key] = result
        # return result
```

### 15.2 主循环模板

```python
def main():
    fetcher = None
    bs_code = None

    while True:
        if bs_code is None:
            bs_code, pure_code = input_stock_code()
            fetcher = None  # 换股时重置

        if fetcher is None:
            fetcher = FinancialDataFetcher(bs_code, pure_code)
            fetcher.bs_login()

        # ... 查询逻辑 ...

        action = wait_key_prompt()
        if action == 'exit':
            fetcher.bs_logout()
            break
        elif action == 'new_stock':
            fetcher.bs_logout()
            fetcher = None
            bs_code = None
        # 'same_stock': 保持fetcher复用缓存

# 关键原则:
# - fetcher在循环外创建, 换股时才重置
# - 换股时先bs_logout()再重建
# - 退出时bs_logout()
# - 同一股票多次查询时复用缓存
```

### 15.3 Numba加速技术指标模板

```python
from numba import jit
import numpy as np

@jit(nopython=True, cache=True, fastmath=True)
def calc_kd(close_prices, n=9, m1=3, m2=3):
    """计算KD指标 - Numba加速版"""
    length = len(close_prices)
    k_values = np.zeros(length)
    d_values = np.zeros(length)
    # ... 计算逻辑 ...
    return k_values, d_values

@jit(nopython=True, cache=True, fastmath=True)
def calc_rsi(close_prices, period=8):
    """计算RSI - Numba加速版"""
    # ... 计算逻辑 ...
    return rsi_values

# 关键参数: RSI周期=8, KD参数 n=9, m1=3, m2=3
```

---

## 16. 完整踩坑记录

### 16.1 单位陷阱

| 日期 | 踩坑内容 | 影响 | 解决方案 |
|------|---------|------|---------|
| 2026-05-12 | 新浪毛利率(%)列返回值可能是百分比也可能是小数 | 毛利率9215%而非92.15% | `abs(f)<2` 判断 |
| 2026-05-12 | Baostock roeAvg是小数而非百分比 | ROE显示0.15%而非15% | `f*100` |
| 2026-05-12 | Baostock totalShare单位可能是"万股" | 股本偏小10000倍 | 自动检测 `convert_share()` |
| 2026-05-12 | 新浪金额列(元)实际单位可能是"万元" | 研发费用/营收偏差1万倍 | 优先用parse_amount |
| 2026-05-12 | 巨潮分红"派息比例"是每10股 | 每股分红偏大10倍 | ÷10 |
| 2026-05-13 | 同花顺利润表早期年份研发费返回False(布尔值) | parse_amount解析False失败 | 加`val is not False`前置判断 |
| 2026-05-13 | 新浪利润表金额单位为元(纯数字) | 直接当亿元使用偏小1亿倍 | ÷1亿转亿元 |
| 2026-05-13 | Baostock股本单位: 股可能为万股 | 股本偏差 | `if f<10000 and f>0`检测 |

### 16.2 API陷阱

| 日期 | 踩坑内容 | 影响 | 解决方案 |
|------|---------|------|---------|
| 2026-05-12 | 东方财富API从服务器无法访问 | stock_individual_info_em超时 | 降级到其他数据源 |
| 2026-05-12 | 同花顺现金流表列名硬编码 | akshare升级后列名变化导致查不到 | 加try-except和模糊匹配 |
| 2026-05-12 | baostock query_profit_data等不接受yearType参数 | 传参报错 | 不传yearType |
| 2026-05-12 | baostock需login后才能查询 | 未登录直接查询报错 | 查询前检查登录状态 |
| 2026-05-12 | baostock K线返回值全是字符串类型 | 数值比较/计算出错 | 手动float()转换 |
| 2026-05-13 | 同花顺财务摘要无研发费列 | 研发费始终返回NO_DATA | 改用同花顺利润表 |
| 2026-05-13 | 新浪财务分析指标无研发费列 | 同上 | 改用新浪利润表 |
| 2026-05-13 | 同花顺利润表早期年份研发费返回False | parse_amount解析失败 | 加`val is not False`判断 |
| 2026-05-13 | stock_profit_sheet_ths接口不存在 | AttributeError | 正确接口是stock_financial_benefit_ths |
| 2026-05-13 | baostock query_stock_industry无province字段 | 无法查注册属地 | 改用巨潮 profile_cninfo |
| 2026-05-18 | 公司查注册属地无备用方案 | profile_cninfo失败则无替代 | 暂无备用, 注意异常处理 |

### 16.3 逻辑陷阱

| 日期 | 踩坑内容 | 影响 | 解决方案 |
|------|---------|------|---------|
| 2026-05-12 | sorted()对"3.10"字符串排序不正确 | 3.10排在3.2前面 | 按数字排序 `key=lambda k: tuple(int(x) for x in k.split('.'))` |
| 2026-05-12 | 分红终止条件逻辑错误 | 第1年就break,只取1年数据 | 删除提前终止条件 |
| 2026-05-12 | PEG中g_val==0无法匹配字符串"0" | ZeroDivisionError | 先float()再判断 |
| 2026-05-12 | 北交所代码(8/4开头)未处理 | 北交所股票无法查询 | 增加bj.前缀 |

---

## 17. 附录：各接口列名速查

### A. 同花顺财务摘要 (`stock_financial_abstract_ths`)

| 列名 | 含义 | 格式 |
|------|------|------|
| 报告期 | 年报/季报日期 | "2024-12-31" |
| 基本每股收益 | EPS | 纯数字(元) |
| 每股净资产 | BPS | 纯数字(元) |
| 每股经营现金流 | OCF/Share | 纯数字(元) |
| 净利润 | 净利润 | "1483.91亿" |
| 营业总收入 | 营收 | "4.82万亿" |
| 净资产收益率 | ROE | "6.22%" |
| 净利润同比增长率 | 净利润增速 | "15.3%" |
| 营业总收入同比增长率 | 营收增速 | "12.1%" |

> ⚠️ **此接口没有"研发费用"列!**

### B. 同花顺利润表 (`stock_financial_benefit_ths`) ✅含研发费

| 列名 | 含义 | 格式 | 备注 |
|------|------|------|------|
| 报告期 | 年报/季报 | "2025"(纯年份) | 匹配: `str(year) in rp` |
| 一、营业总收入 | 营收 | "1720.54亿" | 带单位 |
| 其中：营业收入 | 营业收入 | "1688.38亿" | 带单位 |
| 二、营业总成本 | 营业总成本 | "573.71亿" | 带单位 |
| 其中：营业成本 | 营业成本 | "114.89亿" | 带单位 |
| 销售费用 | 销售费用 | "725.35亿" | 带单位 |
| 管理费用 | 管理费用 | "83.20亿" | 带单位 |
| **研发费用** | **研发费用** | **"1.90亿"** | **✅带单位, 早期年份可能为False** |
| 财务费用 | 财务费用 | "-0.82亿" | 可能为负 |
| 三、营业利润 | 营业利润 | "1148.09亿" | 带单位 |
| 五、净利润 | 净利润 | "853.10亿" | 带单位 |
| 归属于母公司所有者的净利润 | 归母净利润 | "823.20亿" | 带单位 |

> ⚠️ 接口名是 `stock_financial_benefit_ths`, **不是** `stock_profit_sheet_ths`(已废弃)

### C. 新浪利润表 (`stock_financial_report_sina` symbol="利润表") ✅含研发费

| 列名 | 含义 | 格式 | 备注 |
|------|------|------|------|
| 报告日 | 报告日期 | "20251231" | 匹配: `f"{year}1231" in rp` |
| 营业总收入 | 营收 | 172054171890.91 | 纯数字(元) |
| 营业收入 | 营业收入 | 168838102514.79 | 纯数字(元) |
| 营业成本 | 营业成本 | 114892277570.91 | 纯数字(元) |
| 销售费用 | 销售费用 | 72534996000.68 | 纯数字(元) |
| 管理费用 | 管理费用 | 8320061659.66 | 纯数字(元) |
| **研发费用** | **研发费用** | **190112246.58** | **✅纯数字(元), ÷1亿→亿元** |
| 财务费用 | 财务费用 | -815240284.72 | 可能为负 |
| 营业利润 | 营业利润 | 114808950164.24 | 纯数字(元) |
| 净利润 | 净利润 | 85310324833.67 | 纯数字(元) |
| 归属于母公司所有者的净利润 | 归母净利润 | 82320067101.68 | 纯数字(元) |

> ⚠️ 所有金额列单位均为**元**(纯float), 需÷1亿转亿元
> ⚠️ 该接口同时返回季报+年报, 按报告日筛选即可

### D. 新浪财务指标 (`stock_financial_analysis_indicator`)

| 列名 | 含义 | ⚠️单位注意 |
|------|------|-----------|
| 销售毛利率(%) | 毛利率 | 可能是百分比或小数 |
| 净资产收益率(%) | ROE | 同上 |
| 每股经营性现金流(元) | OCF/Share | 元/股 |
| 每股净资产_调整前(元) | BPS | 元/股 |
| 主营业务收入增长率(%) | 营收增速 | 可能是百分比或小数 |
| 净利润增长率(%) | 净利润增速 | 同上 |
| 营业收入(元) | 营收 | 元(也可能是万元⚠️) |
| 研发费用(元) | 研发 | 元(也可能是万元⚠️) |

> ⚠️ **此接口没有"研发费用"列!** 上表中"研发费用(元)"仅作参考, 实测可能有或无

### E. 同花顺现金流量表 (`stock_financial_cash_ths`)

| 列名 | 含义 | 格式 |
|------|------|------|
| 经营活动产生的现金流量净额 | OCF | 带单位 |
| 购建固定资产、无形资产和其他长期资产支付的现金 | CAPEX | 带单位 |

### F. 巨潮分红 (`stock_dividend_cninfo`)

| 列名 | 含义 | 格式 |
|------|------|------|
| 报告时间 | 报告期 | "2024年年报" |
| 派息比例 | 每10股派息额 | 需÷10→每股分红 |

---

## 本技能维护说明

### 经验积累机制

当你经过多次尝试才得出正确结果时(例如参数格式试错、接口选择调整、发现文档未明示的约束等), 必须将经验简要追加到第16章的踩坑记录中。

**记录标准**:
- 只记录经过**2次及以上尝试**才成功的情况
- 格式: `| 日期 | 踩坑内容 | 影响 | 解决方案 |`
- 内容简明, 聚焦"下次遇到同样情况该怎么做"

### 数据源状态更新

- 东方财富API等不可用状态可能随时间变化, 每隔一段时间应重新验证
- Akshare接口列名可能因版本变化, 使用前建议先打印列名验证

---

*文档结束 - 持续更新中*
