# 行情数据 API（Open API · 日K / 分钟K）

## 简介

通过 Gangtise Open API 查询 A/港股**历史日 K**与 A 股**分钟 K**，脚本 **`scripts/quote.py`**。

日 K 默认**前复权**：不再从日 K 接口拉取 `adjustFactor` 字段，改为调用 **`/adjustFactor`**（`QUOTE_ADJUST_FACTOR_URL`）获取复权因子后，在脚本侧计算**开高低收**及**昨收、涨跌额、涨跌幅**的复权序列（列名带 `（前复权）` 或 `（后复权）`）。**不复权**时不请求复权因子接口，输出原始 OHLC 与涨跌字段。

复权因子接口按自然月拆分请求并合并，以降低单次超过 10000 行的风险；若仍不足以覆盖全部分页场景，请缩短日期区间分批拉取。

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `-sd` / `--start-date` | 否 | 开始日期 `yyyy-MM-dd`。未指定时默认**今天**。 |
| `-ed` / `--end-date` | 否 | 结束日期 `yyyy-MM-dd`。未指定时默认**今天**。 |
| `--securities` | 否* | **完整证券代码**，逗号分隔。与 `--all-market` **二选一**。 |
| `--securities-file` | 否* | CSV 须含列 **`security_code`**。 |
| `--all-market` | 否 | 不传 `securityList`，按接口约定拉**全市场**（数据量可能极大，请配合日期与 `limit`）。 |
| `--limit` | 否 | 单次 K 线请求最大行数，默认 `5000`，上限 `10000`。复权因子请求同样受上限约束（脚本按月拆分）。 |
| `--type` | 否 | `daily`（默认，日K）或 `minute`（分钟K，仅 A 股，且不支持 `--all-market`）。 |
| `--adjust` | 否 | **仅日 K**。`forward` / `qfq` / `前复权`（默认）、`backward` / `hfq` / `后复权`、`none` / `raw` / `不复权`。分钟 K 忽略复权（勿显式传非 `none`）。 |

\* 指定证券时须提供 `--securities` 或 `--securities-file`；全市场时使用 `--all-market` 且不要同时传证券列表。

## 约束与说明

- **仅支持完整证券代码**，不支持简称解析。
- **前复权**：\(P'(t) = P(t) \times F(t)/F(t_{\text{latest}})\)，其中 \(t_{\text{latest}}\) 为本次结果中该证券**最后交易日**，\(F\) 来自独立 **adjustFactor** 接口。
- **后复权**：\(P'(t) = P(t) \times F(t)/F(t_{\text{earliest}})\)，其中 \(t_{\text{earliest}}\) 为本次结果中该证券**首个交易日**。
- **不复权**：原始行情字段名仍为 `开盘价`、`收盘价` 等（导出列名以脚本为准）。
- `minute` 类型支持 `securities` 并发拉取并聚合；不支持全市场拉取；不支持复权。

## 调用示例

```bash
python3 scripts/quote.py --securities 600519.SH -sd 2026-04-01 -ed 2026-04-23
```

```bash
python3 scripts/quote.py --securities 600519.SH -sd 2026-04-01 -ed 2026-04-23 --adjust backward
```

```bash
python3 scripts/quote.py --securities-file ./codes.csv --limit 8000
```

```bash
python3 scripts/quote.py --type minute --securities 600519.SH,000001.SZ -sd "2026-04-23 10:00:00" -ed "2026-04-23 15:00:00"
```

## 返回说明

- **成功**：在 `workspace/gangtise/quote/` 下生成 **`quote_*.csv`**，返回文案含路径与样例。
- **失败**：如授权失败、无数据、参数错误、复权因子缺失等。

## 返回数据示例（CSV 列）

当前实现会在写出前**去掉 `security_abbr` 列**，仅保留 **`security_code`** 等（以实际脚本为准）。

日 K **前复权**时典型列为：`开盘价（前复权）`、`最高价（前复权）`、`最低价（前复权）`、`收盘价（前复权）`、`昨收价（前复权）`、`涨跌额（前复权）`、`涨跌幅（前复权）`、`成交量`、`成交额` 等。
