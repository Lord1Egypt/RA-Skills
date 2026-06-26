---
name: etf-prices
description: 单只 ETF 分钟级分时价格（market.ft.tech）。用户问某只 ETF 分时、当日走势、多日分时、一分钟行情时使用。
---

# ETF 分时价格 - 查询单只 ETF 分钟级分时

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单只 ETF 分时价格（一分钟级别） |
| 外部接口 | `GET /app/api/v2/etfs/:etf/prices` |
| 请求方式 | GET |
| 适用场景 | 获取 A 股指定 ETF 在指定时间范围内的分时数据（一分钟一根），用于分时图、当日/多日走势；每条含该分钟的价格、成交量、成交额、均价、时间戳；支持从今天起、从五日前起、从 N 个交易日前起或从指定毫秒时间戳起；响应含昨收与当前交易日 |

## 2. 请求参数

说明：`etf` 为路径参数（必填）；时间范围由 `since` 或 `since_ts_ms` 二选一指定（不传 `since` 时必传 `since_ts_ms`）。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| etf | string | 是 | ETF 标的键（路径参数，带市场后缀） | 510050.XSHG、159915.XSHE、920036.BJ | 沪 .XSHG、深 .XSHE、北交所 .BJ |
| since | string | 条件必填 | 时间范围起点（语义） | TODAY、FIVE_DAYS_AGO、TRADE_DAYS_AGO(10) | 见下方取值说明；与 since_ts_ms 二选一 |
| since_ts_ms | long | 条件必填 | 时间范围起点（毫秒时间戳） | 1735689600000 | 须属于“今天”或“最近一个交易日”；不传 since 时必传 |

**`since` 取值说明**：

| 取值 | 含义 |
|------|------|
| TODAY | 从今天（或最近一个交易日）的第一条分时数据开始 |
| FIVE_DAYS_AGO | 从五个交易日前的第一条分时数据开始（含今天） |
| TRADE_DAYS_AGO(n) | 从 n 个交易日前的第一条分时数据开始（含今天），n 为正整数 |

## 3. 响应说明

返回指定 ETF 的分时价格列表、昨收及当前交易日。

```json
{
    "prices": [
        { "p": 2.85, "v": 12345678, "t": 35200000.0, "a": 2.849, "tm": 1735689600000 },
        { "p": 2.852, "v": 9876543, "t": 28100000.0, "a": 2.851, "tm": 1735689660000 }
    ],
    "prev_close": 2.845,
    "today": 20250312
}
```

### 根字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| prices | array | 分时价格列表，按时间正序 |
| prev_close | float | 昨收价；无时为 null |
| today | int | 当前交易日，YYYYMMDD 格式 |

### 分时单条（prices 元素）

| 字段名 | 类型 | 说明 | 单位 |
|--------|------|------|------|
| p | float | 该分钟价格 | 元 |
| v | long | 该分钟成交量 | 份 |
| t | float | 该分钟成交额 | 元 |
| a | float | 该分钟均价（若有） | 元 |
| tm | long | 该分钟对应时间戳 | 毫秒 |

## 4. 用法

通过主目录 `run.py` 调用（必填 `--etf`，且必填 `--since` 或 `--since_ts_ms` 其一）：

```bash
python <RUN_PY> etf-prices --etf 510050.XSHG --since TODAY
python <RUN_PY> etf-prices --etf 159915.XSHE --since FIVE_DAYS_AGO
python <RUN_PY> etf-prices --etf 510050.XSHG --since "TRADE_DAYS_AGO(10)"
python <RUN_PY> etf-prices --etf 510050.XSHG --since_ts_ms 1735689600000
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出 JSON，请求头已内置 `X-Client-Name: ft-claw`。

## 5. 请求示例

```
GET https://market.ft.tech/app/api/v2/etfs/510050.XSHG/prices?since=TODAY
```

## 6. 注意事项

- `since` 与 `since_ts_ms` 二选一；不传 `since` 时必须传 `since_ts_ms`
- `since_ts_ms` 须属于“今天”或“最近一个交易日”
- 分时为一分钟一根，数据量随时间范围增大而增加
- 执行方式：脚本在输出前将 `prices` 中每条记录的 `tm`（毫秒）转为北京时间 ISO 字符串（YYYY-MM-DDTHH:mm:ss）；`since` 与 `since_ts_ms` 二选一，两个都不传或两个都传时退出并提示错误。
