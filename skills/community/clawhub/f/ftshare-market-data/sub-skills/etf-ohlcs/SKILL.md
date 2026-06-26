---
name: etf-ohlcs
description: 单只 ETF OHLC K 线（market.ft.tech）。用户问某只 ETF 的 K 线、日线/周线/月线、开高低收、MA5/MA10/MA20 时使用。
---

# ETF K 线 - 查询单只 ETF OHLC K 线

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单只 ETF OHLC K 线 |
| 外部接口 | `GET /app/api/v2/etfs/:etf/ohlcs` |
| 请求方式 | GET |
| 适用场景 | 获取 A 股指定 ETF 在指定周期、时间范围内的 K 线（开高低收、成交量、成交额等），支持日/周/月/年线，支持截止时间与条数限制；响应中附带 MA5/MA10/MA20 |

## 2. 请求参数

说明：`etf` 为路径参数（必填），`span` 为必填项，`limit` 和 `until_ts_ms` 为可选项。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| etf | string | 是 | ETF 标的键（路径参数，带市场后缀） | 510050.XSHG、159915.XSHE、920036.BJ | 沪 .XSHG、深 .XSHE、北交所 .BJ |
| span | string | 是 | K 线周期 | DAY1 | 可选值：DAY1（日线）、WEEK1（周线）、MONTH1（月线）、YEAR1（年线） |
| limit | int | 否 | 返回 K 线根数上限 | 50 | 不传则不限制条数；建议传 limit 且不超过 2000 |
| until_ts_ms | long | 否 | 截止时间戳（毫秒），返回该时间点及之前的 K 线 | 1735689600000 | 不传则截止到“当前” |

## 3. 响应说明

返回指定 ETF 的 K 线数组、昨收及 MA 指标。

```json
{
    "has_last_empty": false,
    "prev_close": 2.845,
    "ohlcs": [
        { "o": 2.85, "h": 2.865, "l": 2.84, "c": 2.862, "v": 125000000, "t": 358000000.0, "otm": 1649174400000, "ctm": 1649260799999 }
    ],
    "ma5":  [ { "p": null, "ctm": 1649260799999 }, ... ],
    "ma10": [ { "p": null, "ctm": 1649260799999 }, ... ],
    "ma20": [ { "p": null, "ctm": 1649260799999 }, ... ]
}
```

### 根字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| has_last_empty | boolean | 最后一根 K 线是否为“空”（未收盘） |
| prev_close | float | 昨收价，保留 4 位小数；无昨收时为 null |
| ohlcs | array | K 线列表，按时间正序 |
| ma5 / ma10 / ma20 | array | 5/10/20 周期均线点，与 ohlcs 对齐 |

### Ohlc 单条（ohlcs 元素）

| 字段名 | 类型 | 说明 | 单位 |
|--------|------|------|------|
| o | float | 开盘价 | 元 |
| h | float | 最高价 | 元 |
| l | float | 最低价 | 元 |
| c | float | 收盘价 | 元 |
| v | long | 成交量 | 份 |
| t | float | 成交额 | 元 |
| otm | long | 该根 K 线周期开始时间 | 毫秒 |
| ctm | long | 该根 K 线周期结束时间 | 毫秒 |

### Ma 单条（ma5/ma10/ma20 元素）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| p | float | 均线价格，不足周期时为 null |
| ctm | long | 对应 K 线结束时间（毫秒） |

## 4. 用法

通过主目录 `run.py` 调用（必填 `--etf`、`--span`）：

```bash
python <RUN_PY> etf-ohlcs --etf 510050.XSHG --span DAY1 --limit 50
python <RUN_PY> etf-ohlcs --etf 159915.XSHE --span WEEK1 --limit 100
python <RUN_PY> etf-ohlcs --etf 510050.XSHG --span DAY1 --limit 20 --until_ts_ms 1735689600000
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出 JSON，请求头已内置 `X-Client-Name: ft-claw`。

## 5. 请求示例

```
GET https://market.ft.tech/app/api/v2/etfs/510050.XSHG/ohlcs?span=DAY1&limit=50
```

## 6. 注意事项

- `span` 取值仅支持：DAY1、WEEK1、MONTH1、YEAR1
- 建议传 `--limit` 且不超过 2000，避免单次返回过多
- 价格保留 4 位小数；脚本在输出前将 ohlcs 的 otm/ctm、ma5/ma10/ma20 的 ctm 转为北京时间 ISO 字符串（YYYY-MM-DDTHH:mm:ss），便于大模型与用户直接阅读时间。
