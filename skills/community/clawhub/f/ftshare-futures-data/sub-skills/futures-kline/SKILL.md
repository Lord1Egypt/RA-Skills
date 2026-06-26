---
name: futures-kline
description: 查询期货 K 线（market.ft.tech）。按合约查询 1 分钟、日线，以及多分钟/周月季年聚合周期 K 线；支持时间范围与条数限制。用户问期货K线、期货日线/分钟线、周线/月线、期货历史行情时使用。若用户只给中文名/品种，先用 futures-lists 映射 symbol。
---

# 期货 - 查询期货K线

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询期货K线 |
| 外部接口 | `GET /data/api/v1/market/data/futures/kline` |
| 请求方式 | GET |
| 适用场景 | 按合约查询期货 K 线：支持 1 分钟、日线，以及由分钟线合成的多周期（如 5/15/30/60 分钟）、由日线合成的周/月/季/年；可按时间范围与条数限制拉取 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 是 | WIND 合约全码：`{合约}{到期月}.{交易所}` | A2605.DCE | 大小写不敏感 |
| interval | string | 否 | K 线周期 | 1min | 默认 `1min` |
| start | int64 | 否 | 起始时间，毫秒时间戳 | 1772294400000 | `start/end` 需同时传入 |
| end | int64 | 否 | 结束时间，毫秒时间戳（闭区间） | 1774972799999 | 禁止只传 `end` |
| limit | int | 否 | 最大返回条数 | 500 | 默认 500 |

### interval 取值

| 取值 | 说明 |
|------|------|
| `1min` / `1m` | 一分钟 K 线 |
| `5min` / `5m`、`15min` / `15m`、`30min` / `30m`、`60min` / `1h` | 由一分钟线按时间轴分桶聚合 |
| `daily` / `1d` | 日 K 线 |
| `weekly` / `1w` / `week` | 由日线聚合（自然周） |
| `monthly` / `1mo` / `month` | 由日线聚合（月末） |
| `quarterly` / `1q` / `quarter` | 由日线聚合（季末） |
| `yearly` / `1y` / `year` | 由日线聚合（年末） |

## 3. 响应说明

```json
{
  "items": [],
  "total": 0
}
```

- `total`：满足时间条件的 K 线总条数（可能大于 `items` 长度，受 `limit` 截断）
- `items`：通常按时间升序返回（以上游行为为准）

### KlineItem 结构

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| symbol | String | 否 | 合约代码（返回形态以服务端为准） |
| datetime | int64 | 否 | K 线时间，毫秒时间戳 |
| trade_date | int32 | 否 | 交易日 `YYYYMMDD` |
| open / high / low / close | float | 否 | OHLC |
| volume | int64 | 否 | 成交量 |
| amount | float | 否 | 成交额 |
| vwap | float | 否 | 成交均价 |
| open_interest | float | 否 | 持仓量 |
| dominant_contract | String | 是 | 主连相关 |
| forward_factor / backward_factor | float | 是 | 复权相关 |

## 4. 用法

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> futures-kline --symbol A2605.DCE
python <RUN_PY> futures-kline --symbol A2605.DCE --interval 30min --limit 50
python <RUN_PY> futures-kline --symbol A2605.DCE --interval daily --start 1772294400000 --end 1774972799999 --limit 100
python <RUN_PY> futures-kline --symbol A2605.DCE --interval weekly --limit 52
```

`<RUN_PY>` 为 **`FTShare-futures-data/run.py`** 的绝对路径。

## 5. 请求示例

```
GET https://market.ft.tech/data/api/v1/market/data/futures/kline?symbol=A2605.DCE
GET https://market.ft.tech/data/api/v1/market/data/futures/kline?symbol=A2605.DCE&interval=30min&limit=50
GET https://market.ft.tech/data/api/v1/market/data/futures/kline?symbol=A2605.DCE&interval=daily&start=1772294400000&end=1774972799999&limit=100
GET https://market.ft.tech/data/api/v1/market/data/futures/kline?symbol=A2605.DCE&interval=weekly&limit=52
```

## 6. 注意事项

- `start` 与 `end` 必须同时传；只传其中一个会报参数错误。
- `symbol` 大小写不敏感；脚本会统一转大写后请求。
- `total` 可能大于 `items` 长度（被 `limit` 截断）。
- `start/end` 建议使用东八区毫秒时间戳；脚本会校验时间戳为毫秒级（建议 13 位）且 `start <= end`。
- 若用户只给中文名/品种（如“豆一2605”），先 `futures-lists` 匹配出 `symbol`，再调用本接口。
