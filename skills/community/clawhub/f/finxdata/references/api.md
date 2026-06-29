# FinXData API 参考

下列接口与 FinXData MCP tools 暴露的接口集合一致。按访问方式分为三类：

- 无需 API Key：`health` 和 `summary`，用于健康检查和发现当前可用接口。
- 设置 API Key 后可访问：`quota` 以及 `stock`、`market`、`economy`、`fred`、`track`、`alternative` 等常规数据接口。调用时需要配置 `FINXDATA_API_KEY`，会按账户额度、余额和频率限制处理。
- Agent 公开接口：`agent ...` 命令，对应 `/api/v1/http/agent/*`。不需要 `FINXDATA_API_KEY`，但必须提供 `--agent-type` 或 `FINXDATA_AGENT_TYPE` / `AGENT_TYPE`，服务端通过 `x-agent-type` 统计来源和频率。

需要最新机器可读清单时，以 `python3 scripts/finxdata.py summary` 为准。需要了解更新节奏、配额处理、错误解释和生活化使用场景时，读取 `usage.md`。

## 无需 API Key 的系统接口

| 命令 | 接口 | 参数 | 内容 |
|---|---|---|---|
| `health` | `GET /health` | 无 | 服务健康状态。 |
| `summary` | `GET /api/v1/summary` | 无 | 当前机器可读 API 清单，也是 MCP 工具面的事实来源。 |

## 设置 API Key 后可访问接口

运行本节接口前配置：

```bash
export FINXDATA_API_KEY="sk-..."
```

这些接口会走账户认证和额度逻辑。多数数据接口返回 `{"code": 200, "data": "<Markdown>"}`。

### 额度

| 命令 | 接口 | 参数 | 内容 |
|---|---|---|---|
| `quota` | `GET /api/quota/api-key` | 无 | 当前 API Key 的额度状态。 |

`quota` 用于回答“还能查多少次”“为什么被限制”“什么时候能再试”。重点字段包括 `daily_remaining`、`daily_used`、`daily_max`、`prepaid_balance`、`gift_remaining`、`cost_per_call`、`retry_after_seconds`。

### 股票

| 命令 | 接口 | 参数 | 内容 |
|---|---|---|---|
| `stock summary` | `/api/v1/http/stock/summary` | `code` | 股票概要和公司信息。 |
| `stock quote` | `/api/v1/http/stock/quote` | `code`，支持多个 | 股票最新行情。 |
| `stock financial` | `/api/v1/http/stock/financial` | `code`，`sections=reports` | 财务报表和指定财务板块。 |
| `stock financial-quick-analysis` | `/api/v1/http/stock/financial/quick-analysis` | `code`，`periods=4`，`refresh` | 关键财务指标快速摘要。 |
| `stock mainops` | `/api/v1/http/stock/mainops` | `code`，`years=3` | 主营业务构成。 |
| `stock kline` | `/api/v1/http/stock/kline` | `code`，`period=daily` | 股票 K 线。 |
| `stock moneyflow` | `/api/v1/http/stock/moneyflow` | `code`，`days=20` | 个股资金流向。 |
| `stock hot-reason` | `/api/v1/http/stock/hot_reason` | `code`，`days=30`，`refresh_today` | 个股题材归因历史。 |
| `stock dragon-tiger-seats` | `/api/v1/http/stock/dragon_tiger/seats` | `code`，`trade_date`，`look_back=30`，`refresh` | 个股龙虎榜上榜记录、买卖席位和机构席位统计。 |
| `stock ontology` | `/api/v1/http/stock/ontology` | `code` | 股票图谱摘要。 |
| `stock listing` | `/api/v1/http/stock/listing` | `limit=20` | 近期新股列表。 |
| `stock forecast` | `/api/v1/http/stock/forecast` | `page=1`，`page_size=50`，`refresh` | 业绩预告公告。 |
| `stock trade-calendar` | `/api/v1/http/stock/trade_calendar` | `year`，`month`，`months=3` | A 股交易日历。 |
| `stock notice-summary` | `/api/v1/http/stock/notice/summary` | `code`，`refresh` | 股票公告摘要。 |
| `stock lockup` | `/api/v1/http/stock/lockup` | `code`，`trade_date`，`forward_days=90`，`refresh` | 个股限售解禁日历，包含未来待解禁和历史解禁。 |

### 市场

| 命令 | 接口 | 参数 | 内容 |
|---|---|---|---|
| `market price` | `/api/v1/http/market/price` | `code`，支持多个 | 指数或板块行情。 |
| `market kline` | `/api/v1/http/market/kline` | `code`，`period=daily`，`limit=30` | 指数或板块 K 线。 |
| `market hot-sectors` | `/api/v1/http/market/hot_sectors` | 无 | 热门题材列表。 |
| `market hot-sector` | `/api/v1/http/market/hot_sector` | `name` 或 `theme_id`，`days=1`，`track_date` | 热门题材详情。 |
| `market hot-stocks` | `/api/v1/http/market/hot_stocks` | `track_date`，`limit=100`，`refresh` | 强势股题材归因列表。 |
| `market dragon-tiger` | `/api/v1/http/market/dragon_tiger` | `trade_date`，`min_net_buy`，`limit=100`，`refresh` | 全市场龙虎榜，包含上榜原因、买卖金额和净买入排名。 |
| `market northbound-intraday` | `/api/v1/http/market/northbound/intraday` | `trade_date`，`refresh` | 北向资金分钟流向。 |
| `market northbound-history` | `/api/v1/http/market/northbound/history` | `days=20` | 北向资金历史快照。 |

### 宏观经济

| 命令 | 接口 | 参数 | 内容 |
|---|---|---|---|
| `economy china` | `/api/v1/http/economy/china` | `type` | 中国宏观经济报表。 |
| `economy china-types` | `/api/v1/http/economy/china/types` | 无 | 中国宏观经济报表类型清单。 |
| `economy us` | `/api/v1/http/economy/us` | `type` | 美国关键经济数据。 |
| `economy us-types` | `/api/v1/http/economy/us/types` | 无 | 美国经济数据类型清单。 |
| `economy calendar` | `/api/v1/http/economy/calendar` | `year`，`month`，`months=3` | 国内宏观数据发布日历。 |

### FRED

| 命令 | 接口 | 参数 | 内容 |
|---|---|---|---|
| `fred series-list` | `/api/v1/http/fred/series` | 无 | 可用 FRED 序列清单。 |
| `fred series` | `/api/v1/http/fred/series/{series_id}` | `series_id`，`observation_start`，`observation_end`，`limit` | 单个 FRED 序列观测值。 |
| `fred key-indicators` | `/api/v1/http/fred/key-indicators` | `observation_start`，`observation_end` | 重点宏观指标矩阵。 |

### 跟踪

| 命令 | 接口 | 参数 | 内容 |
|---|---|---|---|
| `track news` | `/api/v1/http/track/news` | 无 | 新闻跟踪快照。 |
| `track market` | `/api/v1/http/track/market` | 无 | 市场跟踪快照。 |
| `track notice` | `/api/v1/http/track/notice` | 无 | 公告跟踪快照。 |

## Agent 公开接口

运行本节接口不需要 API Key，但必须指定 agent 来源类型：

```bash
export FINXDATA_AGENT_TYPE="openclaw"  # 也可在命令中传 --agent-type
```

这些接口不扣注册用户额度；服务端会按 `x-agent-type` 和调用 IP 做来源统计与频率控制。适合 OpenClaw、Hermes、OpenCode 等 agent 客户端直接获取少量公开摘要数据。

| 命令 | 接口 | 参数 | 内容 |
|---|---|---|---|
| `agent market-price` | `/api/v1/http/agent/market/price` | `code`，支持多个；另需 `--agent-type` | 指数或板块行情。 |
| `agent stock-quote` | `/api/v1/http/agent/stock/quote` | `code`，支持多个；另需 `--agent-type` | 股票最新行情。 |
| `agent hot-sectors` | `/api/v1/http/agent/market/hot_sectors` | 另需 `--agent-type` | 热门题材/概念榜。 |
| `agent hot-sector` | `/api/v1/http/agent/market/hot_sector` | `name` 或 `theme_id`，`days=1`，`track_date`；另需 `--agent-type` | 热门题材详情。 |
| `agent hot-reason` | `/api/v1/http/agent/stock/hot_reason` | `code`，`days=30`；另需 `--agent-type` | 个股题材归因历史。 |
| `agent dragon-tiger` | `/api/v1/http/agent/market/dragon_tiger` | `trade_date`，`min_net_buy`，`limit=100`，`refresh`；另需 `--agent-type` | 全市场龙虎榜。 |
| `agent track-news` | `/api/v1/http/agent/track/news` | 另需 `--agent-type` | 新闻跟踪快照。 |
| `agent track-market` | `/api/v1/http/agent/track/market` | 另需 `--agent-type` | 市场跟踪快照。 |
| `agent track-notice` | `/api/v1/http/agent/track/notice` | 另需 `--agent-type` | 公告跟踪快照。 |
| `agent economy-calendar` | `/api/v1/http/agent/economy/calendar` | `year`，`month`，`months=3`；另需 `--agent-type` | 国内宏观数据发布日历。 |
| `agent ontology-abstract` | `/api/v1/http/agent/ontology/abstract` | `code`；另需 `--agent-type` | 股票图谱摘要，只返回代码、名称、摘要、分析时间和图谱版本。 |
| `agent financial` | `/api/v1/http/agent/financial` | `code`；另需 `--agent-type` | 股票业绩报表简版，只返回业绩报表关键字段。 |

## refresh 参数

带 `refresh` 或 `refresh_today` 的接口会跳过读取缓存并尝试刷新数据。只有当用户明确需要“重新拉取/刷新/当天最新”或返回结果疑似过旧时才使用；普通查询优先不加刷新参数，以减少等待时间和失败概率。

## 批量查询

- `stock quote`、`market price`、`agent market-price` 和 `agent stock-quote` 支持一次传多个 `--code`。
- `stock kline` 支持传多个代码，但脚本会逐只查询并自动间隔，避免过快触发频率限制。
- 其他接口优先单对象查询；用户给出大量股票时分批执行并摘要结果。
