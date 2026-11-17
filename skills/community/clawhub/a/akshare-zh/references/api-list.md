# AKShare 完整接口列表

> 本文件收录 AKShare 的主要接口，按数据类别分组。完整最新列表见 https://akshare.akfamily.xyz/tutorial.html

## 股票

### A 股

| 接口 | 说明 |
|:---|:---|
| stock_zh_a_spot_em | 东财 A 股实时行情 |
| stock_zh_a_hist | A 股 K 线数据（日/周/月） |
| stock_zh_a_daily | 新浪 A 股日线 |
| stock_zh_a_minute | A 股分钟数据 |
| stock_individual_info_em | 东财个股信息 |
| stock_individual_fund_flow | 个股资金流 |
| stock_market_fund_flow | 大盘资金流 |
| stock_sector_spot | 板块行情 |
| stock_zh_a_st | ST 股行情 |
| stock_zt_pool_em | 涨停板池 |
| stock_cyq_em | 筹码分布 |
| stock_lhb_detail_em | 龙虎榜详情 |
| stock_lhb_jgmmtj_em | 龙虎榜机构买卖统计 |
| stock_lhb_jystatistic_em | 龙虎榜交易统计 |
| stock_comment | 股市评论 |
| stock_hot_keyword_em | 热搜词条 |
| stock_hot_rank_em | 热度排名 |
| stock_hot_follow_em | 关注排名 |
| stock_news_em | 个股新闻 |

### 港股

| 接口 | 说明 |
|:---|:---|
| stock_hk_spot_em | 东财港股实时行情 |
| stock_hk_hist | 港股 K 线数据 |
| stock_hk_index_daily | 港股指数日线 |

### 美股

| 接口 | 说明 |
|:---|:---|
| stock_us_spot | 美股实时行情 |
| stock_us_hist | 美股历史数据 |
| stock_us_daily | 美股日线 |

### 台股

| 接口 | 说明 |
|:---|:---|
| stock_tw_spot | 台湾股票实时行情 |
| stock_tw_daily | 台湾股票日线 |

## 期货

### 交易所数据

| 接口 | 说明 |
|:---|:---|
| get_cffex_daily | 中金所每日交易数据 |
| get_cffex_rank_table | 中金所前 20 会员持仓明细 |
| get_czce_daily | 郑商所每日交易数据 |
| get_rank_table_czce | 郑商所前 20 会员持仓明细 |
| get_dce_daily | 大商所每日交易数据 |
| get_dce_rank_table | 大商所前 20 会员持仓明细 |
| get_gfex_daily | 广期所每日交易数据 |
| get_ine_daily | 上海国际能源交易中心每日交易数据 |
| futures_settlement_price_sgx | 新交所期货每日交易数据 |
| get_futures_daily | 中金所每日基差数据 |
| get_rank_sum | 四大交易所前 5/10/15/20 会员持仓排名 |
| futures_settle | 期货交易所结算参数 |

### 期货实时/历史

| 接口 | 说明 |
|:---|:---|
| futures_zh_spot | 期货实时行情 |
| futures_zh_daily_sina | 期货日线（新浪） |
| futures_foreign_hist | 外盘期货历史 |
| futures_main_sina | 主力合约（新浪） |
| futures_continuous_sina | 连续合约（新浪） |

## 期权

| 接口 | 说明 |
|:---|:---|
| option_finance_board | 期权金融面板 |
| option_current_em | 期权实时行情（东财） |
| option_cffex_daily | 中金所期权日线 |
| option_dce_daily | 大商所期权日线 |
| option_czce_daily | 郑商所期权日线 |
| option_sse_daily | 上交所期权日线 |
| option_shfe_daily | 上期所期权日线 |

## 基金

### 开放式基金

| 接口 | 说明 |
|:---|:---|
| fund_open_fund_daily_em | 开放式基金实时行情（东财） |
| fund_open_fund_info_em | 开放式基金详情 |
| fund_etf_fund_daily_em | ETF 基金实时行情 |
| fund_etf_spot_em | ETF 实时行情 |
| fund_etf_hist_em | ETF 历史数据 |
| fund_lof_spot_em | LOF 实时行情 |
| fund_lof_hist_em | LOF 历史数据 |

### 基金份额/净值

| 接口 | 说明 |
|:---|:---|
| fund_etf_scale_szse | 深交所 ETF 基金份额 |
| fund_etf_scale_sse | 上交所 ETF 基金规模 |
| fund_etf_fund_info_em | ETF 基金信息 |

### 货币基金

| 接口 | 说明 |
|:---|:---|
| fund_money_fund_daily_em | 货币基金实时行情 |
| fund_money_fund_info_em | 货币基金详情 |

## 债券

| 接口 | 说明 |
|:---|:---|
| bond_gb_zh_sina | 中国国债收益率（新浪） |
| bond_gb_us_sina | 美国国债收益率（新浪） |
| bond_zh_us_rate | 中美国债收益率 |
| bond_zh_hs_cov | 可转债行情 |
| bond_zh_hs_cov_min | 可转债分钟数据 |
| bond_zh_us_rate_start | 中美国债收益率（起始） |

## 外汇

| 接口 | 说明 |
|:---|:---|
| fx_spot_quote | 外汇实时行情 |
| fx_hist_data | 外汇历史数据 |
| currency_boc_safe | 中国银行外汇牌价 |
| currency_pair_map | 货币对映射 |

## 指数

| 接口 | 说明 |
|:---|:---|
| index_zh_a_hist | 中国股票指数历史 |
| index_zh_a_hist_min | 中国股票指数分钟 |
| index_global_hist | 全球指数历史 |
| index_zh_a_hist_pre_min | 预估指数 |
| stock_zh_index_daily | 指数日线（新浪） |

## 加密货币

| 接口 | 说明 |
|:---|:---|
| crypto_hist | 加密货币历史 |
| crypto_spot | 加密货币实时 |
| crypto_bitcoin_coinmarketcap | CoinMarketCap 比特币 |
| crypto_ethereum_coinmarketcap | CoinMarketCap 以太坊 |

## 宏观经济

| 接口 | 说明 |
|:---|:---|
| macro_china_gdp | 中国 GDP |
| macro_china_cpi | 中国 CPI |
| macro_china_pmi | 中国 PMI |
| macro_china_ppi | 中国 PPI |
| macro_china_money_supply | 货币供应量 |
| macro_china_social_finance | 社会融资 |
| macro_china_fdi | 外商直接投资 |
| macro_china_import_export | 进出口 |
| macro_china_lpr | LPR 利率 |
| macro_china_foreign_exchange | 外汇储备 |
| macro_usa_gdp | 美国 GDP |
| macro_usa_cpi | 美国 CPI |
| macro_usa_pmi | 美国 PMI |
