# FinXData 使用指南

## 常见场景

先判断用户是否有 `FINXDATA_API_KEY`。有 API Key 时优先使用常规数据接口；没有 API Key 且只需要 Agent 公开摘要时，使用 `agent ... --agent-type <type>`。

### 设置 API Key 后可访问场景

运行本节命令前需要配置 `FINXDATA_API_KEY`。这些接口会走账户认证、额度和频率限制。

| 用户想做什么 | 推荐命令 | 说明 |
| --- | --- | --- |
| 看一只股票的当前概况 | `python3 scripts/finxdata.py stock summary --code 600519` | 用于公司简介、主营信息和概要行情。 |
| 对比几只股票最新行情 | `python3 scripts/finxdata.py stock quote --code 600519 000001 300750` | 报价接口支持批量代码，优先一次请求完成。 |
| 查一只股票的财报明细 | `python3 scripts/finxdata.py stock financial --code 600519 --sections reports,mainops` | `reports` 查基础财报和三大报表；可按需组合 `mainops/holdernum/predict/performance/disclosure`。 |
| 快速整理财报关键指标 | `python3 scripts/finxdata.py stock financial-quick-analysis --code 600519 --periods 4` | 适合向用户摘要最近 N 期营收、净利、EPS、ROE、净利率、资产负债率和同比变化。 |
| 查股票图谱摘要 | `python3 scripts/finxdata.py stock ontology --code 600519` | 用于实体、关系和图谱摘要；回答时说明这是接口返回的图谱整理，不延展成投资建议。 |
| 看指数或板块行情 | `python3 scripts/finxdata.py market price --code 000001 BK0477` | 适合大盘指数、行业板块、概念板块。 |
| 找近期强势题材 | `python3 scripts/finxdata.py market hot-sectors` | 先看题材榜，再用 `market hot-sector` 查单个题材详情。 |
| 看市场新闻跟踪 | `python3 scripts/finxdata.py track news` | 返回新闻跟踪快照；回答时优先整理更新时间、重点新闻、相关股票或主题线索。 |
| 看市场状态跟踪 | `python3 scripts/finxdata.py track market` | 返回市场跟踪快照；适合整理大盘状态、活跃方向、情绪变化和需要继续追踪的板块线索。 |
| 看公告跟踪 | `python3 scripts/finxdata.py track notice` | 返回公告跟踪快照；回答时优先提取公告时间、公司、事项类型、重要性和后续关注点。 |
| 看龙虎榜 | `python3 scripts/finxdata.py market dragon-tiger --trade-date 2026-06-12 --limit 50` | 市场全量龙虎榜；个股席位用 `stock dragon-tiger-seats`。 |
| 查限售解禁 | `python3 scripts/finxdata.py stock lockup --code 600519 --forward-days 180` | 覆盖未来待解禁和历史解禁。 |
| 查宏观指标 | `python3 scripts/finxdata.py economy china-types` 后接 `economy china --type <type>` | 先查可用类型，再查具体报表。 |
| 查 FRED 时间序列 | `python3 scripts/finxdata.py fred series-list` 后接 `fred series --series-id FEDFUNDS` | 先查可用序列，再查观测值。 |
| 查额度 | `python3 scripts/finxdata.py quota` | 用于解释 API Key 剩余次数、余额和重置等待时间。 |

### Agent 公开场景

运行本节命令不需要 `FINXDATA_API_KEY`，但必须提供 `--agent-type`，例如 `openclaw`、`hermes`、`opencode`。这些接口不扣注册用户额度，适合 Agent 客户端直接获取公开摘要。

| 用户想做什么 | 推荐命令 | 说明 |
| --- | --- | --- |
| Agent 查指数或板块行情 | `python3 scripts/finxdata.py agent market-price --code 000001 BK0477 --agent-type openclaw` | 免费零扣费；支持多个指数/板块代码。 |
| Agent 查股票最新行情 | `python3 scripts/finxdata.py agent stock-quote --code 600519 000001 --agent-type openclaw` | 免费零扣费；支持多个股票代码。 |
| Agent 查热门题材 | `python3 scripts/finxdata.py agent hot-sectors --agent-type openclaw` | 免费零扣费；返回热门题材/概念榜。 |
| Agent 查题材详情 | `python3 scripts/finxdata.py agent hot-sector --name 人形机器人 --agent-type hermes` | 免费零扣费；适合从题材榜继续追问成分股和热度变化。 |
| Agent 查个股题材归因 | `python3 scripts/finxdata.py agent hot-reason --code 688017 --days 7 --agent-type openclaw` | 免费零扣费；适合回答某只股票近期为什么活跃。 |
| Agent 查全市场龙虎榜 | `python3 scripts/finxdata.py agent dragon-tiger --trade-date 2026-06-12 --limit 50 --agent-type hermes` | 免费零扣费；支持日期、净买入下限、条数和刷新参数。 |
| Agent 查股票图谱摘要 | `python3 scripts/finxdata.py agent ontology-abstract --code 600519 --agent-type openclaw` | 免费零扣费；只返回摘要、分析时间和版本，不返回实体关系明细。 |
| Agent 查股票业绩报表 | `python3 scripts/finxdata.py agent financial --code 300223 --agent-type openclaw` | 免费零扣费；只返回业绩报表关键字段。 |
| Agent 看新闻跟踪 | `python3 scripts/finxdata.py agent track-news --agent-type hermes` | 免费零扣费；后台会按来源头统计调用来源和频率。 |
| Agent 看市场跟踪 | `python3 scripts/finxdata.py agent track-market --agent-type hermes` | 免费零扣费；适合 Agent 客户端默认行情摘要。 |
| Agent 看公告跟踪 | `python3 scripts/finxdata.py agent track-notice --agent-type hermes` | 免费零扣费；适合整理近期公告事项。 |
| Agent 看宏观发布日历 | `python3 scripts/finxdata.py agent economy-calendar --year 2026 --month 6 --months 1 --agent-type opencode` | 免费零扣费；返回国内宏观数据发布日历。 |

## 更新节奏

| 数据类别 | 更新口径 |
| --- | --- |
| 股票报价、市场价格、K 线 | 请求时读取短缓存或补取；交易时段通常更频繁，非交易时段缓存更长。 |
| 热门题材、强势股、龙虎榜、北向资金 | 交易日内有缓存和刷新机制；带 `refresh` 或 `refresh_today` 的接口可跳过缓存尝试刷新。 |
| 股票财务、主营、公告摘要、限售解禁 | 读取缓存或本地数据，缺失或指定 `refresh` 时尝试补取；财务类通常跟随公告披露节奏。 |
| 新股上市、业绩预告、A 股交易日历 | 后台每日定时更新。 |
| 中国宏观、宏观发布日历 | 后台每日检查并补齐当前周期数据；发布日历滚动维护未来月份。 |
| FRED | 后台按日检查，单个指标按自己的发布频率刷新。 |
| Track 新闻、市场、公告 | 默认每小时更新。 |

回答用户“数据多久更新一次”时，不要给所有接口一个固定分钟数。按接口类别说明，并提醒以返回数据的日期、报告期或快照时间为准。

## 配额和限制

常规数据接口需要 `FINXDATA_API_KEY`，会消耗或检查账户额度。Agent 公开接口不需要 API Key，不扣注册用户额度，但必须提供 `--agent-type`，并受来源统计、IP 频率和服务端保护策略限制。

`quota` 只反映 API Key 账户额度，不代表 Agent 公开接口的剩余次数。`quota` 返回字段含义：

| 字段 | 含义 |
| --- | --- |
| `daily_remaining` | 今日试用剩余调用次数。 |
| `daily_used` | 今日已经使用的试用次数。 |
| `daily_max` | 今日试用总额度。 |
| `prepaid_balance` | 预付费余额。 |
| `gift_remaining` | 管理员赠送的剩余次数。 |
| `gift_expires_at` | 赠送额度过期时间，可能为空。 |
| `cost_per_call` | 单次调用成本，按服务端配置返回。 |
| `retry_after_seconds` | 全部额度用尽时，距离可再次尝试的大致秒数。 |

常规 API Key 接口超出配额时：

- 先运行 `python3 scripts/finxdata.py quota`。
- 如果 `retry_after_seconds` 有值，告诉用户大约何时重置；试用额度按 `Asia/Shanghai` 00:00 重置。
- 如果有预付费或赠送额度，说明可继续使用；否则建议减少批量查询、等待重置或联系服务方升级/充值。
- 如果是频率限制而非总额度不足，建议降低并发、分批查询，批次之间等待数秒。

Agent 公开接口失败时：

- 如果返回缺少来源标识，检查是否传了 `--agent-type` 或设置了 `FINXDATA_AGENT_TYPE` / `AGENT_TYPE`。
- 如果返回频率限制，降低调用频率或稍后重试；这类限制不通过 `quota` 查询。
- 如果需要更全数据、更高频调用或账户级额度管理，改用设置 API Key 后可访问的常规接口。

## 失败处理

脚本失败时会返回：

```json
{"ok": false, "code": "quota_limited", "message": "当前 API Key 已触发额度或频率限制..."}
```

常见 `code`：

| code | 给用户的解释 |
| --- | --- |
| `missing_api_key` | 本地没有配置 API Key，需要先申请并导出 `FINXDATA_API_KEY`。 |
| `auth_failed` | API Key 错误、过期或没有接口权限。 |
| `quota_limited` | 额度用尽或调用太频繁；先查 `quota`。 |
| `not_found` | 接口、股票代码、日期或指标类型不存在。 |
| `network_timeout` / `network_connect_failed` | 网络或服务连接问题；脚本已重试，稍后再试。 |
| `service_unavailable` | 服务或上游数据暂时不可用；脚本已重试，稍后再试。 |

不要把技术错误原样转给普通用户。用“发生了什么、现在能做什么、是否已经重试”三句话解释。

## 示例结果

典型数据接口返回：

```json
{
  "code": 200,
  "data": "### 600519 股票概要\n\n| 项目 | 值 |\n| --- | --- |\n| 最新价 | ... |"
}
```

面向用户回答时，优先整理成：

- 查询对象：股票/指数/指标名称和代码。
- 数据时间：交易日、报告期、公告日或快照日期。
- 核心结果：价格、涨跌幅、排名、金额、报告期指标等。
- 数据状态：是否命中缓存、是否暂无数据、是否需要换日期或加 `refresh`。

## FAQ

**为什么查不到当天数据？**  
可能是非交易日、数据源尚未发布、日期参数不是交易日，或本地缓存还没有刷新。先换最近交易日；支持 `refresh` 的接口可尝试加 `--refresh`。

**为什么第一次查询比较慢？**  
部分接口会在缓存或本地数据缺失时补取数据，首次请求通常比缓存命中慢。

**可以一次查很多代码吗？**  
报价类接口支持批量代码；K 线等接口会逐只查询并自动间隔。大批量查询建议分组，避免触发频率限制。

**返回的是 Markdown 怎么办？**  
`data` 字段常是 Markdown 表格。回答用户时提取重点，不必完整复述全部表格，除非用户要求导出或保留原始结果。

**是否能用于投资决策？**  
只能用于数据查询和信息整理。不要输出确定性买卖建议；需要分析时说明局限和数据日期。
