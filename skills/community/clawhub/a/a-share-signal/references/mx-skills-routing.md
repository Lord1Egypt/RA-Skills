# 新版 mx-skills 路由参考

## 已安装 skill slug

- `mx-financial-assistant`
- `mx-finance-data`
- `mx-finance-search`
- `mx-stocks-screener`
- `mx-macro-data`
- `industry-research-report`
- `industry-stock-tracker`
- `initiation-of-coverage-or-deep-dive`
- `stock-earnings-review`

## 单票 A 股分析推荐路由

先定一条总原则：所有 `mx-skills` 请求都必须串行执行。不要并发调用多个 skill，也不要对同一个 skill 同时发起多次请求；必须等上一请求完成并确认仍需补证据后，再继续下一步，以避免限流、超时和结果回拼错位。

1. 优先 `mx-financial-assistant`
适合“帮我分析这只票”“现在能不能参与”“怎么看趋势/催化/风险”这类综合问题。

2. 按需补 `mx-finance-data`
适合补结构化字段，例如行情、估值、财务、资金、报表指标、多字段时间序列。

3. 按需补 `mx-finance-search`
适合补最新公告、研报、财经新闻、交易所动态、政策变化。

4. 仅在需要横向比较时用 `mx-stocks-screener`
适合同板块对标、同风格筛选、找可比公司池、验证相对强弱。

5. 仅在宏观变量直接影响逻辑时用 `mx-macro-data`
适合利率、汇率、通胀、地产、社融、出口、就业等宏观链条。

## 串行调用要求

- 不同 skill 之间必须串行：先 `mx-financial-assistant`，再按结果决定是否补 `mx-finance-data`、`mx-finance-search`、`mx-stocks-screener` 或 `mx-macro-data`。
- 单个 skill 内也必须串行：如果同一 skill 需要多次补充查询，必须等待上一条请求完成后再发下一条。
- `mx-finance-data` 的多标的拆批查询同样必须串行：当前批次完成后，才能继续下一批。
- 禁止“先并发拉一圈数据再统一拼装答案”的模式，这会显著增加限流、超时和口径不一致风险。

## 旧名兼容

新版目录 slug 为连字符形式，但很多旧资料仍使用下划线别名：

- `mx-financial-assistant` = `mx_financial_assistant`
- `mx-finance-data` = `mx_finance_data`
- `mx-finance-search` = `mx_finance_search`
- `mx-stocks-screener` = `mx_stocks_screener`
- `mx-macro-data` = `mx_macro_data`

在回答里可以同时提及两种写法，但默认优先使用新版 slug。

## 回退策略

- 默认只使用 `mx-skills`
- `AkShare` 只作为经用户明确同意后的额外回退
- `BaoShare` 只作为经用户明确同意、且 `AkShare` 也无法覆盖时的更后置回退

## 输出要求

- 先给结论，再给证据
- 明确关键日期、价格位和失效条件
- 明确列出本次依赖的数据来源
- 如果数据不完整、时效不足或字段缺失，必须降低结论置信度
