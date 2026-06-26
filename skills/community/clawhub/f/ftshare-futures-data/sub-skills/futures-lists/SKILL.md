---
name: futures-lists
description: 查询指定交易日期货合约列表（market.ft.tech）。获取指定交易日全部期货合约代码、交易所、品种、中文名及合约类型（主力/真实/连续等）。用户问期货列表、期货合约清单、某交易日期货合约时使用。也可作为名称→代码映射源：用户给中文名/品种时先查本接口拿 symbol，再调 futures-base-data 或 futures-kline。
---

# 期货 - 查询期货列表

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询指定交易日期货合约列表 |
| 外部接口 | `GET /data/api/v1/market/data/futures/futures-lists` |
| 请求方式 | GET |
| 适用场景 | 获取指定交易日全部期货合约代码、交易所、品种、中文名及合约类型（主力/真实/连续等），数据与日度期货基础信息对齐 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| trade_date | int | 否 | 交易日，格式 `YYYYMMDD` | 20260331 | 不传则使用前一交易日（CST） |

## 3. 响应说明

```json
{
  "trade_date": 20260331,
  "items": []
}
```

### ChinaFuturesListsItem 结构

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| symbol | String | 否 | 合约代码（WIND 等源格式，如含交易所后缀） |
| exchange | String | 否 | 交易所代码 |
| product | String | 否 | 品种代码 |
| symbol_cn_name | String | 否 | 合约中文名 |
| future_type | int | 是 | `1` 主力、`2` 真实、`3` 连续；源数据缺失时为 `null` |

## 4. 用法

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> futures-lists
python <RUN_PY> futures-lists --trade-date 20260331
```

`<RUN_PY>` 为 **`FTShare-futures-data/run.py`** 的绝对路径。脚本输出 JSON。

## 5. 请求示例

```
GET https://market.ft.tech/data/api/v1/market/data/futures/futures-lists
GET https://market.ft.tech/data/api/v1/market/data/futures/futures-lists?trade_date=20260331
```

## 6. 注意事项

- 返回 `trade_date` 为接口实际使用交易日。
- `future_type` 可能为 `null`，展示时建议容错处理。
- 当日合约量可能较大，展示时可按交易所或品种分组。
- 可作为“中文名/品种 → symbol（WIND 全码）”映射源：先按 `symbol_cn_name` / `product` 匹配，再调用 `futures-base-data` 或 `futures-kline`。
