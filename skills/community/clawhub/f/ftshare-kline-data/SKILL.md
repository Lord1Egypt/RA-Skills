---
name: FTShare-kline-data
description: 非凸科技 A 股 K 线数据技能集。覆盖日/周/月/年线 OHLC K 线查询、以及单只股票一分钟级分时价格查询（market.ft.tech）。用户询问 A 股某只股票的历史 K 线、开高低收、成交量成交额、均线（MA5/MA10/MA20），或当日/多日分时、分时图数据时使用。
---

# FT AI A 股 K 线数据 Skills

本 skill 是 `FTShare-kline-data` 的**统一路由入口**。

根据用户问题，从下方「能力总览」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> 所有接口均以 `https://market.ft.tech/app` 为基础域名，使用 HTTP GET，并携带请求头 `X-Client-Name: ft-web`。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>`。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> stock-ohlcs --stock 688295.XSHG --span DAY1 --limit 50
python <RUN_PY> stock-ohlcs --stock 000001.SZ --span WEEK1
python <RUN_PY> stock-prices --stock 000001.XSHG --since TODAY
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## 能力总览

### 1. 单只股票 OHLC K 线

- **`stock-ohlcs`**：查询单只 A 股股票在指定周期、时间范围内的 K 线数据，含开高低收、成交量、成交额，以及 MA5/MA10/MA20 均线。必填参数：`--stock`（如 `688295.XSHG`）、`--span`（DAY1/WEEK1/MONTH1/YEAR1）；可选参数：`--limit`（返回条数上限）、`--until_ts_ms`（截止时间戳毫秒）。

### 2. 单只股票分时价格（一分钟级别）

- **`stock-prices`**：查询单只 A 股股票在指定时间范围内的分时数据（一分钟一根），用于分时图、当日/多日走势；含该分钟价格、成交量、成交额、均价、时间戳；响应含昨收与当前交易日。必填参数：`--stock`；时间起点二选一：`--since`（TODAY / FIVE_DAYS_AGO / TRADE_DAYS_AGO(n)）或 `--since_ts_ms`（毫秒时间戳）。

---

## 使用流程

1. **记录本文件绝对路径**，将 `/SKILL.md` 替换为 `/run.py` 得到 `<RUN_PY>`。
2. **理解用户意图**，从「能力总览」匹配对应子 skill 名称。
3. （可选）读取 `<RUN_PY>` 同级目录 `sub-skills/<子skill名>/SKILL.md` 了解接口详情与参数。
4. **执行**：`python <RUN_PY> <子skill名> [参数...]`，获取 JSON 输出。
5. **解析并输出**：以表格或要点形式展示给用户。

---

## 子 skill 与用户问法示例

| 用户问法示例 | 子 skill 名 |
|---|---|
| 「688295.XSHG 最近 50 根日线是什么？」 | `stock-ohlcs` |
| 「查看某只股票的历史 K 线数据」 | `stock-ohlcs` |
| 「某股票的开盘价、最高价、最低价、收盘价」 | `stock-ohlcs` |
| 「某股票的周线 K 线」 | `stock-ohlcs` |
| 「某股票的月线走势」 | `stock-ohlcs` |
| 「某股票的年线数据」 | `stock-ohlcs` |
| 「某股票最近成交量和成交额是多少？」 | `stock-ohlcs` |
| 「某股票的 MA5/MA10/MA20 均线」 | `stock-ohlcs` |
| 「查询某股票截止某时间点前的 K 线」 | `stock-ohlcs` |
| 「某股票今天/当日分时」 | `stock-prices` |
| 「某股票分钟级分时、分时图数据」 | `stock-prices` |
| 「某股票从五日前起的分时」 | `stock-prices` |
| 「某股票从 N 个交易日前起的走势」 | `stock-prices` |
