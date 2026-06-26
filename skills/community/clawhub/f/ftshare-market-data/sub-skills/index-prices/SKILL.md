---
name: index-prices
description: 单只指数分钟级分时价格（market.ft.tech）。用户问某只指数分时、当日走势、多日分时、一分钟行情时使用。
---

# 指数分时价格 - 查询单只指数分钟级分时

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单只指数分时价格（一分钟级别） |
| 外部接口 | `GET /app/api/v2/indices/:index/prices` |
| 请求方式 | GET |
| 适用场景 | 获取 A 股指定指数在指定时间范围内的分时数据（一分钟一根），用于分时图、当日/多日走势；每条含该分钟的指数点位、成交量、成交额、时间戳；支持从今天起、从五日前起、从 N 个交易日前起或从指定毫秒时间戳起；响应含昨收与当前交易日 |

## 2. 请求参数

说明：`index` 为路径参数（必填）；时间范围由 `since` 或 `since_ts_ms` 二选一指定（不传 `since` 时必传 `since_ts_ms`）。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| index | string | 是 | 指数标的键（路径参数，带市场后缀） | 000001.XSHG、399001.XSHE、920036.BJ | 沪 .XSHG、深 .XSHE、北交所 .BJ |
| since | string | 条件必填 | 时间范围起点（语义） | TODAY、FIVE_DAYS_AGO、TRADE_DAYS_AGO(10) | 见下方取值说明；与 since_ts_ms 二选一 |
| since_ts_ms | long | 条件必填 | 时间范围起点（毫秒时间戳） | 1735689600000 | 须属于「今天」或「最近一个交易日」；不传 since 时必传 |

**`since` 取值说明**：

| 取值 | 含义 |
|------|------|
| TODAY | 从今天（或最近一个交易日）的第一条分时数据开始 |
| FIVE_DAYS_AGO | 从五个交易日前的第一条分时数据开始（含今天） |
| TRADE_DAYS_AGO(n) | 从 n 个交易日前的第一条分时数据开始（含今天），n 为正整数 |

## 3. 响应说明

返回指定指数的分时价格列表、昨收及当前交易日，与代码 `GetIndexPricesReply` 一致。

```json
{
    "prices": [
        { "p": 3240.12, "v": 280000000, "t": 350000000000.0, "tm": 1735689600000 },
        { "p": 3242.50, "v": 285000000, "t": 355000000000.0, "tm": 1735689660000 }
    ],
    "prev_close": 3238.50,
    "today": 20250312
}
```

### 根字段

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| prices | array | 否 | 分时价格列表，按时间正序；单条结构见下表 |
| prev_close | float | 是 | 昨收（用于分时涨跌幅等计算）；无时为 null |
| today | int | 否 | 当前交易日，YYYYMMDD 格式 |

### 分时单条结构（prices 元素，对应 `PriceShortKey`）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| p | float | 否 | 该分钟指数点位 | 点 |
| v | long | 否 | 该分钟成交量 | — |
| t | float | 否 | 该分钟成交额 | 元 |
| tm | long | 否 | 该分钟对应时间戳（毫秒） | ms |

## 4. 用法

通过主目录 `run.py` 调用（必填 `--index`，且必填 `--since` 或 `--since_ts_ms` 其一）：

```bash
python <RUN_PY> index-prices --index 000001.XSHG --since TODAY
python <RUN_PY> index-prices --index 399001.XSHE --since FIVE_DAYS_AGO
python <RUN_PY> index-prices --index 000001.XSHG --since "TRADE_DAYS_AGO(10)"
python <RUN_PY> index-prices --index 000001.XSHG --since_ts_ms 1735689600000
```

或在子 skill 目录下执行：`python scripts/handler.py --index 000001.XSHG --since TODAY`。脚本输出 JSON，请求头已内置 `X-Client-Name: ft-claw`。

## 5. 请求示例

```
GET https://market.ft.tech/app/api/v2/indices/000001.XSHG/prices?since=TODAY
```

### 完整请求示例（curl）

```bash
curl -X GET 'https://market.ft.tech/app/api/v2/indices/000001.XSHG/prices?since=TODAY' \
  -H 'X-Client-Name: ft-claw' \
  -H 'Content-Type: application/json'
```

## 6. 注意事项

- `since` 与 `since_ts_ms` 二选一；不传 `since` 时必须传 `since_ts_ms`
- `since_ts_ms` 须属于「今天」或「最近一个交易日」
- 分时为一分钟一根，数据量随时间范围增大而增加；数据更新时间以接口/行情源为准
