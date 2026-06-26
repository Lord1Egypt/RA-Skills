# AkShare 股票相关接口完整列表

> 基于 akshare v1.18.48，按功能分类整理。标注 ❌ 的接口测试失败或已废弃。

## A股行情

| 接口 | 说明 | 备注 |
|------|------|------|
| `stock_zh_a_spot_em()` | 沪深京A股实时 | ⚠️ ~70s |
| `stock_sh_a_spot_em()` | 沪A实时 | ⚠️ ~28s |
| `stock_sz_a_spot_em()` | 深A实时 | |
| `stock_bj_a_spot_em()` | 北证A股 | |
| `stock_cy_a_spot_em()` | 创业板 | |
| `stock_kc_a_spot_em()` | 科创板 | |
| `stock_new_a_spot_em()` | 新股 | |
| `stock_zh_a_st_em()` | ST股 | |
| `stock_zh_a_hist()` | 日/周/月K线 | 核心接口 |
| `stock_zh_a_hist_min_em()` | 分钟K线 | |
| `stock_zh_a_minute()` | 分时数据(旧) | |
| `stock_zh_a_daily()` | 日线(旧) | |
| `stock_intraday_em()` | 分时行情 | |
| `stock_bid_ask_em()` | 五档盘口 | |
| `stock_individual_spot_xq()` | 雪球行情 | |

## 港股

| 接口 | 说明 |
|------|------|
| `stock_hk_spot_em()` | 港股实时 ⚠️ |
| `stock_hk_daily()` | 港股日线 |
| `stock_hk_hist()` | 港股历史K线 |
| `stock_hk_hist_min_em()` | 港股分钟K线 |
| `stock_hk_main_board_spot_em()` | 主板实时 |
| `stock_hk_famous_spot_em()` | 知名港股 |
| `stock_hk_index_spot_em()` | 港股指数 |
| `stock_hk_hot_rank_em()` | 港股热股 |
| `stock_hk_valuation_baidu()` | 百度估值 |
| `stock_hk_valuation_comparison_em()` | 估值对比 |
| `stock_hk_financial_indicator_em()` | 财务指标 |
| `stock_hk_growth_comparison_em()` | 成长对比 |
| `stock_hk_scale_comparison_em()` | 规模对比 |

## 美股

| 接口 | 说明 |
|------|------|
| `stock_us_spot_em()` | 美股实时 ⚠️ |
| `stock_us_daily()` | 美股日线 |
| `stock_us_hist()` | 美股历史K线 |
| `stock_us_hist_min_em()` | 美股分钟K线 |
| `stock_us_famous_spot_em()` | 知名美股 |
| `stock_us_valuation_baidu()` | 百度估值 |
| `stock_us_pink_spot_em()` | 粉单市场 |

## 板块

| 接口 | 说明 |
|------|------|
| `stock_board_industry_name_em()` | 行业板块列表 |
| `stock_board_concept_name_em()` | 概念板块列表 |
| `stock_board_industry_cons_em(symbol)` | 行业成分股 |
| `stock_board_concept_cons_em(symbol)` | 概念成分股 |
| `stock_board_industry_hist_em()` | 行业历史K线 |
| `stock_board_concept_hist_em()` | 概念历史K线 |
| `stock_board_industry_spot_em()` | 行业实时 |
| `stock_board_concept_spot_em()` | 概念实时 |
| `stock_board_industry_hist_min_em()` | 行业分钟K线 |
| `stock_board_concept_hist_min_em()` | 概念分钟K线 |
| `stock_board_change_em()` | 板块变动 |

## 资金流向

| 接口 | 说明 |
|------|------|
| `stock_individual_fund_flow()` | 个股资金流 |
| `stock_individual_fund_flow_rank()` | 个股排名 |
| `stock_market_fund_flow()` | 大盘资金流 |
| `stock_main_fund_flow()` | 主力资金流 |
| `stock_fund_flow_big_deal()` | 大单交易 |
| `stock_fund_flow_industry()` | 行业资金流 |
| `stock_fund_flow_concept()` | 概念资金流 |
| `stock_sector_fund_flow_rank()` | 板块排名 |
| `stock_sector_fund_flow_summary()` | 板块汇总 |
| `stock_sector_fund_flow_hist()` | 板块历史 |
| `stock_fund_flow_individual()` | 个股历史 |

## 龙虎榜

| 接口 | 说明 |
|------|------|
| `stock_lhb_detail_em(start_date, end_date)` | 龙虎榜详情 |
| `stock_lhb_stock_detail_em(symbol)` | 个股龙虎榜 |
| `stock_lhb_stock_statistic_em()` | 统计 |
| `stock_lhb_jgstatistic_em()` | 机构统计 |
| `stock_lhb_jgmx_sina()` | 机构明细(新浪) |
| `stock_lhb_yybph_em()` | 营业部排行 |
| `stock_lhb_yyb_detail_em()` | 营业部详情 |
| `stock_lhb_hyyyb_em()` | 活跃营业部 |
| `stock_lhb_jgmmtj_em()` | 机构买卖统计 |

## 涨停/跌停

| 接口 | 说明 | 备注 |
|------|------|------|
| `stock_zt_pool_em(date)` | 涨停池 | |
| `stock_zt_pool_dtgc_em(date)` | 跌停池 | 仅30日 |
| `stock_zt_pool_strong_em(date)` | 强势股池 | |
| `stock_zt_pool_previous_em(date)` | 昨日涨停 | |
| `stock_zt_pool_sub_new_em(date)` | 次新股涨停 | |
| `stock_zt_pool_zbgc_em(date)` | 涨停不打开 | |

## 财务数据

| 接口 | 说明 | 备注 |
|------|------|------|
| `stock_financial_abstract_ths(symbol, indicator)` | 同花顺财务摘要 | ✅ |
| `stock_profit_sheet_by_report_em(symbol)` | 利润表 | ✅ |
| `stock_balance_sheet_by_report_em(symbol)` | 资产负债表 | ✅ |
| `stock_cash_flow_sheet_by_report_em(symbol)` | 现金流量表 | ✅ |
| `stock_yjbb_em(date)` | 业绩报表 | ✅ |
| `stock_yjyg_em(date)` | 业绩预告 | ✅ |
| `stock_yjkb_em(date)` | 业绩快报 | ✅ |
| `stock_lrb_em(date)` | 利润表(汇总) | |
| `stock_zcfz_em(date)` | 资产负债表(汇总) | |
| `stock_xjll_em(date)` | 现金流量表(汇总) | |
| `stock_sy_em(symbol)` | 收益指标 | |
| `stock_yysj_em(symbol)` | 营收数据 | |
| `stock_fhps_em(symbol)` | 分红配送 | |
| `stock_financial_analysis_indicator(symbol)` | 财务指标 | ❌ 超时 |
| `stock_financial_analysis_indicator_em(symbol, indicator)` | 财务指标(东财) | ❌ 数据异常 |

## 融资融券

| 接口 | 说明 | 备注 |
|------|------|------|
| `stock_margin_sse(start_date, end_date)` | 沪市两融 | ✅ 新参数 |
| `stock_margin_szse(date)` | 深市两融 | 旧参数 |
| `stock_margin_detail_sse(date)` | 沪市明细 | |
| `stock_margin_detail_szse(date)` | 深市明细 | |
| `stock_margin_account_info()` | 账户信息 | |
| `stock_margin_ratio_pa()` | 余额占比 | |

## 沪深港通

| 接口 | 说明 | 备注 |
|------|------|------|
| `stock_hsgt_hist_em(symbol)` | 历史净买入 | ✅ |
| `stock_hsgt_sh_hk_spot_em(symbol)` | 实时数据 | |
| `stock_hsgt_fund_flow_summary_em()` | 资金汇总 | |
| `stock_hsgt_board_rank_em()` | 板块排名 | |
| `stock_hsgt_hold_stock_em()` | 持股详情 | ❌ 数据异常 |

## 股东与公司

| 接口 | 说明 |
|------|------|
| `stock_zh_a_gdhs(symbol)` | 股东户数 |
| `stock_gdfx_free_top_10_em(symbol)` | 十大流通股东 |
| `stock_gdfx_top_10_em(symbol)` | 十大股东 |
| `stock_main_stock_holder(symbol)` | 主要股东 |
| `stock_hold_management_detail_em(symbol)` | 高管持股 |
| `stock_individual_info_em(symbol)` | 公司概况 |
| `stock_repurchase_em(symbol)` | 股票回购 |
| `stock_changes_em(symbol)` | 公司变动 |
| `stock_institute_hold(symbol)` | 机构持仓 |
| `stock_institute_recommend()` | 机构推荐 |
| `stock_analyst_rank_em()` | 分析师排名 |

## 限售解禁

| 接口 | 说明 |
|------|------|
| `stock_restricted_release_queue_em()` | 解禁队列 |
| `stock_restricted_release_summary_em()` | 解禁汇总 |
| `stock_restricted_release_detail_em(symbol)` | 个股详情 |
| `stock_restricted_release_stockholder_em()` | 股东解禁 |

## 市场估值

| 接口 | 说明 | 备注 |
|------|------|------|
| `stock_a_all_pb()` | 全A市净率 | ✅ |
| `stock_a_ttm_lyr()` | 全A市盈率 | 无参数 |
| `stock_dxsyl_em()` | 股息率 | ⚠️ ~21s |
| `stock_zh_valuation_baidu(symbol, indicator)` | 百度估值 | |
| `stock_zh_valuation_comparison_em(symbol)` | 估值对比 | |
| `stock_buffett_index_lg()` | 巴菲特指数 | |

## 指数

| 接口 | 说明 |
|------|------|
| `stock_zh_index_spot_em()` | A股指数实时 |
| `stock_zh_index_daily_em(symbol)` | 指数日线 |
| `index_stock_cons_csindex(symbol)` | 中证成分 |
| `index_stock_cons_weight_csindex(symbol)` | 成分权重 |
| `index_stock_cons_sina(symbol)` | 新浪成分 |

## 研报与新闻

| 接口 | 说明 |
|------|------|
| `stock_research_report_em()` | 研报 |
| `stock_news_em(symbol)` | 个股新闻 |
| `stock_hot_keyword_em()` | 热门词 |
| `stock_hot_rank_em()` | 热搜排名 |
| `stock_comment_em(symbol)` | 股吧评论 |

## 新股/IPO

| 接口 | 说明 | 备注 |
|------|------|------|
| `stock_new_ipo_cninfo()` | 新股列表 | ✅ 替代旧接口 |
| `stock_ipo_declare_em()` | 新股申购 | ✅ |
| `stock_ipo_info()` | IPO信息 | |
| `stock_ipo_review_em()` | IPO审核 | |
| `stock_ipo_summary_cninfo()` | IPO汇总 | |
| `stock_new_ipo_em()` | ❌ 已废弃 | 改用 cninfo |
| `stock_new_ipo_start_em()` | ❌ 已废弃 | |

## AH股

| 接口 | 说明 |
|------|------|
| `stock_zh_ah_spot_em()` | AH实时对比 |
| `stock_zh_ah_daily(symbol)` | AH历史 |
| `stock_zh_ah_name()` | AH名称列表 |

## B股

| 接口 | 说明 |
|------|------|
| `stock_zh_b_spot_em()` | B股实时 |
| `stock_zh_b_daily()` | B股日线 |
| `stock_zh_ab_comparison_em()` | AB股对比 |

## 已知问题

| 接口 | 问题 | 建议 |
|------|------|------|
| `stock_lhb_detail_em(date)` | 参数已改为 start_date/end_date | 使用新参数 |
| `stock_margin_sse(symbol)` | 参数已改为 start_date/end_date | 使用新参数 |
| `stock_financial_analysis_indicator()` | 经常超时 | 用 `_em` 版替代 |
| `stock_financial_analysis_indicator_em()` | 部分股票返回 None | 先检查数据可用性 |
| `stock_hsgt_hold_stock_em()` | 偶发 NoneType 错误 | 重试或用 hist 版 |
| `stock_zt_pool_dtgc_em(date)` | 仅支持最近30交易日 | 注意日期范围 |
| `stock_margin_szse(date)` | 仍用旧 date 参数 | 注意参数格式 |
