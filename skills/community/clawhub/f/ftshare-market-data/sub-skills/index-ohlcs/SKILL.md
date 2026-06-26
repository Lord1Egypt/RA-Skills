---
name: index-ohlcs
description: 单只指数 OHLC K 线（market.ft.tech）。用户问某只指数的 K 线、日线/周线/月线/年线、开高低收、MA5/MA10/MA20 时使用。
---

# 指数 K 线 - 查询单只指数 OHLC K 线

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单只指数 OHLC K 线 |
| 外部接口 | `GET /app/api/v2/indices/:index/ohlcs` |
| 请求方式 | GET |
| 适用场景 | 获取 A 股指定指数在指定周期、时间范围内的 K 线（开高低收、成交量、成交额等），支持日/周/月/年线，支持截止时间与条数限制；响应中附带 MA5/MA10/MA20 |

## 2. 请求参数

说明：`index` 为路径参数（必填），`span` 为必填项，`limit` 和 `until_ts_ms` 为可选项。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| index | string | 是 | 指数标的键（路径参数，带市场后缀） | 000001.XSHG、399001.XSHE、920036.BJ | 沪 .XSHG、深 .XSHE、北交所 .BJ |
| span | string | 是 | K 线周期 | DAY1 | 可选值：DAY1（日线）、WEEK1（周线）、MONTH1（月线）、YEAR1（年线） |
| limit | int | 否 | 返回 K 线根数上限 | 50 | 不传则不限制条数，返回时间范围内全部 K 线；建议传 limit 控制条数 |
| until_ts_ms | long | 否 | 截止时间戳（毫秒），返回该时间点及之前的 K 线 | 1735689600000 | 不传则截止到「当前」 |

## 3. 响应说明

返回指定指数的 K 线数组、昨收及 MA 指标，与代码 `GetIndexOhlcsReply` 一致。

```json
{
    "has_last_empty": false,
    "prev_close": 3245.67,
    "ohlcs": [
        { "o": 3240.12, "h": 3255.88, "l": 3238.50, "c": 3252.30, "v": 280000000, "t": 350000000000.0, "otm": 1735689600000, "ctm": 1735776000000 }
    ],
    "ma5":  [ { "p": 3248.50, "ctm": 1735776000000 } ],
    "ma10": [ { "p": null, "ctm": 1735776000000 } ],
    "ma20": [ { "p": null, "ctm": 1735776000000 } ]
}
```

### 根字段

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| has_last_empty | boolean | 否 | 最后一根 K 线是否为「空」（未收盘） |
| prev_close | float | 是 | 昨收（用于涨跌幅等计算），保留 4 位小数；无昨收时为 null |
| ohlcs | array | 否 | K 线列表，按时间正序；单条结构见下表 |
| ma5 | array | 否 | 5 周期均线点，与 ohlcs 对齐 |
| ma10 | array | 否 | 10 周期均线点 |
| ma20 | array | 否 | 20 周期均线点 |

### Ohlc 单条结构（ohlcs 元素，对应 `OhlcShortKey`）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| o | float | 否 | 开盘 | 点 |
| h | float | 否 | 最高 | 点 |
| l | float | 否 | 最低 | 点 |
| c | float | 否 | 收盘 | 点 |
| v | long | 否 | 成交量 | — |
| t | float | 否 | 成交额 | 元 |
| otm | long | 否 | 该根 K 线周期开始时间（毫秒时间戳） | ms |
| ctm | long | 否 | 该根 K 线周期结束时间（毫秒时间戳） | ms |

### Ma 单条结构（ma5 / ma10 / ma20 元素，对应 `Ma`）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| p | float | 是 | 均线值，保留 4 位小数；不足周期时为 null | 点 |
| ctm | long | 否 | 对应 K 线的结束时间（毫秒时间戳） | ms |

## 4. 用法

通过主目录 `run.py` 调用（必填 `--index`、`--span`）：

```bash
python <RUN_PY> index-ohlcs --index 000001.XSHG --span DAY1 --limit 50
python <RUN_PY> index-ohlcs --index 399001.XSHE --span WEEK1 --limit 100
python <RUN_PY> index-ohlcs --index 000001.XSHG --span DAY1 --limit 20 --until_ts_ms 1735689600000
```

或在子 skill 目录下执行：`python scripts/handler.py --index 000001.XSHG --span DAY1 --limit 50`。脚本输出 JSON，请求头已内置 `X-Client-Name: ft-claw`。

## 5. 请求示例

```
GET https://market.ft.tech/app/api/v2/indices/000001.XSHG/ohlcs?span=DAY1&limit=50
```

### 完整请求示例（curl）

```bash
curl -X GET 'https://market.ft.tech/app/api/v2/indices/000001.XSHG/ohlcs?span=DAY1&limit=50' \
  -H 'X-Client-Name: ft-claw' \
  -H 'Content-Type: application/json'
```

## 6. 注意事项

- `span` 取值仅支持：DAY1、WEEK1、MONTH1、YEAR1
- 建议传 `--limit` 控制条数，避免单次返回过多
- 点位保留 4 位小数；时间戳为毫秒；数据更新时间以接口/行情源为准
