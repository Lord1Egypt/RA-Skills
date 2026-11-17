# Market Tape Source Routing

本文件是 `cn-market-tape` 的运行时参考。公开说明只描述“MX 主源”和“聚合公开备用源”，不把具体站点写入用户默认回答。

## Source order

### Theme strength

- 题材映射：使用 skill 目录下的 `assets/themes/theme-data.json` 和 `theme-label-i18n.json`。
- 题材行情：使用 `mx-zixuan` 一次快速覆盖，再用 `mx-xuangu` 按代码批量补齐。
- 题材驱动：用户要求解释时，使用 `mx-search` 和 `cn-stock-move-reason` 的讨论发现层。

### Sector money flow

1. 先使用 `mx-data` 或其他 MX 聚合查询，要求返回板块/行业名称、主力净流入、主力净流出、数据时间和单位。
2. MX 不支持或字段不完整时，默认使用东方财富 `push2.eastmoney.com` 的公开批量接口；同花顺页面可作为页面级备用，`push2delay.eastmoney.com` 作为东方财富接口的延迟/故障备用。
3. 备用页面/接口只请求整页或整榜，在本地解析全量板块；不要按板块名称逐个请求。

资金榜金额通常以亿元展示。若源返回的是“主力净流入”一列，负值可用于净流出排序，但最终表格要把符号和列名写清楚。

已验证过的聚合备用接口族：

- 板块资金流：同花顺公开概念资金流页面 `data.10jqka.com.cn/funds/gnzjl/`，一次读取整榜。
- 大盘宽度/批量快照：东方财富 `push2.eastmoney.com`，只做聚合或批量请求；`push2delay.eastmoney.com` 仅在默认 host 失败时使用。
- 行业/概念板块排名：默认使用东方财富 `push2.eastmoney.com/api/qt/clist/get`，行业用 `fs=m:90+t:2`，概念用 `fs=m:90+t:3`；按 `fid=f62` 分别请求 `po=1` 的净流入和 `po=0` 的净流出，不能把同一方向榜单的末尾行当作另一方向。`f62` 为元，解析后换算为亿元；`total` 大于返回条数时要提示分页/返回上限风险。默认 host 失败时，按同一参数切换到 `push2delay.eastmoney.com`，不在失败 host 上重复重试。
- 涨停池：东方财富 `push2ex.eastmoney.com/getTopicZTPool`，按交易日读取聚合池。
- `push2.eastmoney.com` 是本 skill 的默认东方财富聚合 host；若出现 429/403/5xx、超时、DNS 失败、连接重置或非 JSON 响应，报告 host 和 endpoint family，停止继续轰击该 host，并按需切换到 `push2delay.eastmoney.com`。备用 host 也失败时，回退到已取得的当前快照或明确说明不可用。

### Intraday sector-flow series

- Board-code resolution: use an aggregate `clist/get` request on the default `push2.eastmoney.com` host for the relevant industry or concept universe, then select the exact board name/code. Typical universe selectors are `m:90+t:2` for industries and `m:90+t:3` for concepts. A capped first page is not proof that a requested board does not exist; paginate or use an exact supported resolver. A constituent-stock response is not a board-code confirmation. If the default host fails, retry the same aggregate request once through `push2delay.eastmoney.com` under the error rules.
- Minute fund-flow series: use `api/qt/stock/fflow/kline/get` on the default public host with `secid=90.<board-code>`, `klt=1`, and `lmt=240` for the current trading day. Request `fields2=f51,f52,f53,f54,f55,f56`. Accept the result only when `data.name` exactly matches the requested board. Use `push2delay.eastmoney.com` only as the one-time fallback when the default host is unavailable.
- Field mapping: `f51` timestamp; `f52` cumulative main net inflow; `f53` small-order net inflow; `f54` medium-order net inflow; `f55` large-order net inflow; `f56` super-large-order net inflow. Convert amounts to亿元 only after parsing numeric values. Adjacent differences of `f52` are per-minute changes; the raw `f52` series is cumulative.
- Use the returned `tradePeriods` and `klines` as the source of truth. Do not fill 11:31-13:00, manufacture a 09:30 point when the source starts at 09:31, or infer missing data from the sector's latest snapshot.
- Preserve each module's update time. The minute series may lag the board ranking snapshot; show both timestamps and call out the lag instead of silently merging them. If several boards are requested, use a shared time axis and 分面图 when their scales differ.
- For the chart SOP, render cumulative `f52` in亿元 with a zero line, date/time, source, unit, lunch gap, low/high, zero crossings and latest point. Calculate adjacent differences only for an explicit per-minute-change request; label that chart separately.
- The endpoint is a current-day intraday source, not a guaranteed historical minute database. If it returns an empty series, stale data, non-JSON, 429/403/5xx, timeout, DNS failure, or connection reset, report the host and endpoint family, stop increasing request volume, and fall back only to a clearly labeled current snapshot or say the chart is unavailable.
- For a chart request, use the `visualize` skill to render the cumulative main-net line with a zero axis, key turning-point annotations, the latest timestamp, source, and unit. Do not save the raw API response or chart data in the repository.

### Market breadth and limit-up pool

- 大盘指数和涨跌家数优先使用单次聚合快照接口。
- 涨停池优先使用单次聚合涨停池接口，必要时再取跌停池；不要逐只股票轮询。
- 盘中返回的涨停池会随时间变化，必须保留统计时间和交易日字段。

### Institutional survey

- 当前/最近交易日：优先 `cn-market-tape/scripts/institutional_survey_heat.py` 的低频缓存/聚合查询，或 MX 的调研记录查询。
- 如需 DTM 的当前机构调研补充，只读取当前快照 `https://daytrading.monster/tools/chinastock/data.json`；不读取历史归档或按日期分片。
- 历史数据缺失时，输出“尚不支持该时间/数据”，不要回退到当前快照。

## Request discipline

- 能用一个聚合请求解决时，不做逐股票、逐板块、逐日期循环。
- 同一 host 连续请求达到第 4 次前，加入 8-20 秒随机等待；有多个 host 时也不要并行轰击同一站点。
- 对同一 host 连续请求之间可使用更短的正常间隔，但不得用紧密循环。
- 如果出现 HTTP 429、403、5xx、超时、DNS 失败、连接重置或返回非 JSON：立即报告 host、endpoint family、错误类型和已尝试次数，然后停止继续增加该 host 的请求量。
- 不因一次错误切换到更多高频重试；优先使用已获得的聚合快照、缓存或 MX。

## Timestamp and fallback rules

- 每个模块都记录 `data_date`、`updated_at` 或等价时间字段；没有时间字段时标记时间不确定。
- 盘中结果只能描述为“截至该时间的快照”，不能写成全天结论。
- 同一交易日重复查询资金流时，优先比较同来源、同口径、同单位的上一个聚合快照；来源或口径变化时只展示当前表并标记不可比。
- 盘后结果必须校验目标交易日；周末和节假日使用最近交易日并明确说明。
- 公开备用源只补齐 MX 不支持的字段，不替换题材强弱的 MX 成分行情层。
- 当备用源口径与 MX 不一致时，两者分开列出，不做未经说明的加总或平均。
