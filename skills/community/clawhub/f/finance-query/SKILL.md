---
name: akshare-finance
description: 中国 A股/期货/基金/债券/宏观数据查询工具。基于 AKShare Python 库，无需 API Key，装完即用。触发场景：用户询问"查一下股票"、"茅台股价"、"沪深300"、"某公司财务数据"、"期货行情"、"基金净值"、"宏观数据"、"GDP"、"CPI"、"人民币汇率"、"比特币价格"等任何中国金融数据查询。
---

# AKShare Finance Skill

基于 AKShare 1.18.39，支持查询：中国 A股、指数、期货、期权、债券、基金、外汇、宏观数据、数字货币。

## 核心脚本

**`scripts/akshare_query.py`** — 所有查询统一入口

```bash
python3 /root/.openclaw/workspace/skills/akshare-finance/scripts/akshare_query.py <接口名> [参数...]
```

## 常用接口速查

### 股票行情
```bash
# 实时行情（单只或多只）
python3 akshare_query.py stock_zh_a_spot_em   # 全市场实时行情

# 历史K线
python3 akshare_query.py stock_zh_a_hist "000001.SZ" 1  # 日K
python3 akshare_query.py stock_zh_a_hist "000001.SZ" 300  # 最近300日

# 个股信息
python3 akshare_query.py stock_individual_info_em "000001.SZ"
```

### 指数
```bash
# 沪深300、上证指数等实时行情
python3 akshare_query.py stock_zh_index_spot_em

# 指数历史K线
python3 akshare_query.py stock_zh_index_hist_csindex "000300.SH" 1
```

### 财务报表
```bash
# 利润表
python3 akshare_query.py stock_financial_analysis_indicator "000001.SZ" "报告日期"
```

### 基金
```bash
# 基金净值
python3 akshare_query.py fund_open_fund_info_em "000001"

# 公募基金列表
python3 akshare_query.py fund_fund_info_sina
```

### 期货/大宗商品
```bash
# 商品期货行情
python3 akshare_query.py futures_goods_index_en

# 贵金属（黄金、白银）
python3 akshare_query.py futures precious metal
```

### 宏观数据
```bash
# GDP
python3 akshare_query.py macro_china_gdp

# CPI/PPI
python3 akshare_query.py macro_china_cpi
python3 akshare_query.py macro_china_ppi
```

### 外汇与汇率
```bash
# 人民币汇率
python3 akshare_query.py forex_rmb_iist

# 美元指数
python3 akshare_query.py currency_index
```

### 债券
```bash
# 企业债
python3 akshare_query.py bond_china_comparison
```

### 数字货币
```bash
# 比特币实时行情
python3 akshare_query.py coin_bitget
```

## 执行流程

1. 解析用户需求 → 确定 AKShare 接口名
2. 构造参数（股票代码、时间范围等）
3. 调用 `akshare_query.py` 执行
4. 整理输出，以可读格式返回给用户

## 股票代码格式

- A股：**`000001.SZ`**（深圳）、**`600001.SH`**（上海）
- 指数：**`000300.SH`**（沪深300）、**`000001.SH`**（上证指数）
- 注意：必须带 `.SZ` / `.SH` 后缀

## 注意事项

- AKShare 为爬虫数据，接口稳定性依赖源网站，偶有失败可重试
- 实时行情一般在交易日 9:30-15:00 更新
- 历史数据建议指定 `adjust` 参数（"qfq"=前复权，"hfq"=后复权）
- 财务数据 T日发布，通常 T+1 可查

## 完整接口列表

见 `references/akshare_api_list.md`，按类别整理了 AKShare 所有接口及其参数说明。
