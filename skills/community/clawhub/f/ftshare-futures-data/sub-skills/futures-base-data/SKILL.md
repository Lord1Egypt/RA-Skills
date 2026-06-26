---
name: futures-base-data
description: 查询期货基础信息（market.ft.tech）。按交易日获取期货合约交易单位、涨跌停、保证金、交割、乘数等静态基础信息；可按 WIND 全码过滤单合约。用户问期货基础信息、合约交易单位、保证金、交割信息、期货乘数时使用。
---

# 期货 - 查询期货基础信息

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询期货基础信息 |
| 外部接口 | `GET /data/api/v1/market/data/futures/futures-base-data` |
| 请求方式 | GET |
| 适用场景 | 按交易日获取期货合约交易单位、涨跌停、保证金、交割、乘数等静态基础信息；可按 WIND 全码过滤单合约 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| trade_date | int | 否 | 交易日，格式 `YYYYMMDD` | 20260331 | 不传则使用前一交易日（CST） |
| symbol | string | 否 | WIND 合约全码 | A2605.DCE | 不传或空字符串表示该日全部合约；大小写不敏感 |

## 3. 响应说明

```json
{
  "trade_date": 20260331,
  "items": []
}
```

### ChinaFuturesBaseDataItem 结构

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| trade_date | int | 否 | 交易日 `YYYYMMDD` |
| exchange | String | 否 | 交易所 |
| symbol | String | 否 | 合约代码 |
| product | String | 否 | 品种代码 |
| symbol_cn_name | String | 否 | 合约中文名 |
| trade_unit | String | 否 | 交易单位描述 |
| price_unit | float | 是 | 报价单位 |
| put_price | String | 否 | 最小变动价位相关（源字段为文本） |
| min_put_price_info | String | 否 | 最小变动价位说明 |
| margin_info | String | 否 | 保证金说明 |
| trade_months_info | String | 否 | 可交易月份说明 |
| trade_hours_info | String | 否 | 交易时间说明 |
| last_trade_date | String | 否 | 最后交易日 |
| last_trade_date_hour | String | 否 | 最后交易时刻说明 |
| delivery_date | String | 否 | 交割日相关 |
| multiplier | float | 是 | 合约乘数 |
| list_date | int | 是 | 上市日 `YYYYMMDD` |
| de_list_tdate | int | 是 | 退市日 |
| delivery_mean | String | 否 | 交割方式等 |
| delivery_site | String | 否 | 交割地点等 |
| value_info | String | 否 | 估值相关说明 |
| price_fluctuation_info | String | 否 | 涨跌停说明 |
| position_limit_info | String | 否 | 持仓限额说明 |
| mean_cal_value | float | 是 | 均价计算相关 |
| spot_symbol | String | 是 | 现货/标的代码 |
| type_code | int | 是 | 类型编码 |
| sub_type_code | int | 是 | 子类型编码 |
| future_type | int | 是 | `1` 主力、`2` 真实、`3` 连续 |

## 4. 用法

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> futures-base-data
python <RUN_PY> futures-base-data --symbol A2605.DCE
python <RUN_PY> futures-base-data --trade-date 20260331 --symbol A2605.DCE
```

`<RUN_PY>` 为 **`FTShare-futures-data/run.py`** 的绝对路径（与本子 `SKILL.md` 所在包的根目录）。脚本输出 JSON。

## 5. 请求示例

```
GET https://market.ft.tech/data/api/v1/market/data/futures/futures-base-data?symbol=A2605.DCE
GET https://market.ft.tech/data/api/v1/market/data/futures/futures-base-data?trade_date=20260331&symbol=A2605.DCE
```

## 6. 注意事项

- `symbol` 大小写不敏感；脚本会将非空 `symbol` 统一转大写后请求。
- 无匹配时返回 `items: []` 且 HTTP 200，属于正常结果。
- 字段含义以上游返回为准；日期字段通常为 `YYYYMMDD` 或文本日期说明。
