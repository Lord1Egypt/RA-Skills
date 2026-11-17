# CLI 参数参考

本 skill 各脚本的常用参数集中在这里，SKILL.md 正文只留指引。

## `run_daily_panel.py`（每日复盘证据）

| 参数 | 含义 | 默认 |
|---|---|---:|
| `--fetch-workers` | cache/API 获取线程数；排查限流时设为 1 | 6 |
| `--index-kline-days` | HTML 上证/创业板/科创50 K 线展示窗口，独立于 `--market-trend-days` | 120 |
| `--money-pct-threshold` | 赚钱效应最低当日涨幅 | 7.0 |
| `--money-amount-threshold` | 赚钱效应最低成交额，单位亿元 | 2.0 |
| `--decline-pct-max` | 爆量下跌最大当日涨幅 | -3.0 |
| `--decline-volume-ratio` | 爆量下跌最低 20 日放量倍数 | 2.0 |
| `--capacity-market-cap-threshold` | 容量上涨最低总市值，单位亿元，严格大于 | 70.0 |
| `--capacity-amount-threshold` | 容量上涨最低成交额，单位亿元，严格大于 | 5.0 |
| `--capacity-pct-threshold` | 容量上涨最低当日涨幅，严格大于 | 8.0 |
| `--feature-sample-limit` | 模块 5 每组最大样本数 | 60 |
| `--discount-market-cap-threshold` | 折扣启动最低总市值，单位亿元，严格大于 | 80.0 |
| `--discount-amount-threshold` | 折扣启动最低成交额，单位亿元，严格大于 | 5.0 |
| `--discount-pct-threshold` | 折扣启动最低当日涨幅，严格大于 | 7.0 |
| `--discount-min` | 折扣启动前高折扣下界（前高之后最低价/前高收盘价），严格大于 | 0.6 |
| `--discount-max` | 折扣启动前高折扣上界，严格小于 | 0.85 |
| `--discount-high-lookback` | 折扣启动"前高"回看交易日数（取该窗口内收盘价最高日） | 200 |
| `--discount-low-recency-days` | 折扣启动回撤最低点须落在大涨日前几个交易日内（最低点新鲜度） | 5 |
| `--discount-pre-contraction-max` | 折扣启动调整缩量上限（前5日均额/前20日均额） | 0.9 |
| `--discount-volume-expansion-min` | 折扣启动当日重新放量下限（amount_vs_prev5_ratio，相对前5日缩量期） | 2.0 |
| `--cleanup YYYYMMDD` | 删除该日期临时产物（evidence/kline/context/module_context + 因子挖掘临时包），保留 report md/html | — |

## `factor_backtest.py`（特征因子挖掘）

见 `references/methodology/factor_mining.md` §五。要点：`--group discount_relaunch|custom`、`--spec FILE`、
`--min-n`、`--entry/--horizon` 选目标格、`--skip-backfill` 快速冒烟、`--refresh-basic` 修脏缓存。
产物：决策包 `factor_mining_<group>_<asof>.json`（≤150KB）+ `_detail.json`（整列 signals）。

## `factor_lab.py`（因子实验台账）

每次 `factor_backtest.py` 挖矿会把确定性摘要写入 PG `factor_experiment_log`。`factor_lab.py` 只负责查询实验和补人工 verdict：

| 命令 | 作用 |
|---|---|
| `experiments --recent N` | 列最近挖矿实验 |
| `experiments --set-verdict <g>@<w>@<hash前缀> --verdict adopted\|rejected\|observing [--note ..]` | 人工判分（只改 verdict 与说明） |

## `render_report_html.py`（HTML 展示层）

`--input reports/report_YYYYMMDD.md`、`--theme default|claude|print`。见 SKILL.md「数据获取」HTML 段。
