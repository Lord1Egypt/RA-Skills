---
name: cb-candlesticks
description: 查询单标的历史 K 线（market.ft.tech），支持可转债。用户问可转债 K 线、转债日线/周线/分钟线、转债历史行情时使用。
---

# 单标的历史 K 线 - 查询单标的历史 K 线（支持可转债）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单标的历史 K 线 |
| 外部接口 | `POST /data/api/v1/market/data/stock-candlesticks` |
| 请求方式 | POST |
| 适用场景 | 根据标的代码、时间范围、周期、复权方式获取单只标的的历史 K 线数据；支持可转债（如 110070.XSHG、113050.XSHG、123045.XSHE）及 A 股，支持日/周/月/年及分钟线 |

## 2. 请求参数

说明：请求体为 JSON，所有参数在 body 中传递。`interval_unit`、`adjust_kind` 区分大小写，须使用 PascalCase（如 `Day`、`Forward`）。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 是 | 标的代码，带交易所后缀 | 110070.XSHG、113050.XSHG、123045.XSHE、600000.XSHG | 可转债上交所 .XSHG、深交所 .XSHE |
| interval_unit | string | 是 | K 线周期单位 | Day | 可选值：Minute、Minute5、Day、Week、Month、Year（首字母大写）。5 分钟线用 Minute5 |
| interval_value | int | 否 | 间隔数值，与 interval_unit 配合 | 1 | 与 Minute 等配合；5 分钟线用 Minute5 即可，可省略本参数 |
| until_ts_millis | long | 是 | 结束时间戳 | 1780272000000 | 毫秒，闭区间 |
| since_ts_millis | long | 是 | 开始时间戳 | 1767225600000 | 毫秒；可与 limit 同时使用以限制条数 |
| limit | int | 否 | 数量限制 | 10 | 返回 K 线根数上限 |
| adjust_kind | string | 否 | 复权类型 | null | 可选值：null 或 None（除权）、Forward（前复权）、Backward（后复权）；首字母大写 |

## 3. 响应说明

返回 K 线数组，按时间正序。

```json
[
  {
    "open": "10.52",
    "high": "10.68",
    "low": "10.48",
    "close": "10.61",
    "volume": 125000000,
    "turnover": "1325000000.00",
    "ts_millis": 1767312000000,
    "ts_millis_open": 1767225600000
  }
]
```

### StockCandlestick 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| open | decimal | 否 | 开盘价 | 元 |
| high | decimal | 否 | 最高价 | 元 |
| low | decimal | 否 | 最低价 | 元 |
| close | decimal | 否 | 收盘价 | 元 |
| volume | long | 否 | 成交量 | 股 |
| turnover | decimal | 否 | 成交额 | 元 |
| ts_millis | long | 否 | 收盘时间戳 | 毫秒 |
| ts_millis_open | long | 否 | 开盘时间戳 | 毫秒 |

## 4. 用法

通过主目录 `run.py` 调用（必填 `--symbol`、`--interval-unit`、`--since-ts-millis`、`--until-ts-millis`）。若使用北京时间，请在请求前自行转为毫秒时间戳（东八区）再传入。

```bash
python <RUN_PY> cb-candlesticks --symbol 110070.XSHG --interval-unit Day --since-ts-millis 1767225600000 --until-ts-millis 1780272000000 --limit 10
python <RUN_PY> cb-candlesticks --symbol 110070.XSHG --interval-unit Day --since-ts-millis 1767225600000 --until-ts-millis 1780272000000 --adjust-kind Forward
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出 JSON；本接口无需额外请求头。

## 5. 请求示例

```
POST https://market.ft.tech/data/api/v1/market/data/stock-candlesticks
Content-Type: application/json，请求体 JSON 见 2. 请求参数。
```

## 6. 注意事项

- 标的代码须带交易所后缀：可转债上交所 .XSHG、深交所 .XSHE；与 A 股同一套接口，可查转债或股票历史 K 线
- `interval_unit`、`adjust_kind` 区分大小写，必须为首字母大写的 PascalCase
- 时间戳为毫秒；`since_ts_millis`、`until_ts_millis` 为必填，可按需配合 `limit` 限制返回条数
- 展示时可将 `ts_millis`、`ts_millis_open` 转为北京时间（UTC+8）显示，例如：毫秒戳 ÷1000 后按东八区格式化为 `YYYY-MM-DD HH:MM:SS`
- 请求时若用北京时间，请先按东八区转为毫秒时间戳再传入 `--since-ts-millis`、`--until-ts-millis`
