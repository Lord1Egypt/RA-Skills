---
name: FTShare-index-data
description: A 股指数数据技能集（market.ft.tech）。覆盖单只指数详情、指数分页列表（排序/筛选）、指数 K 线（日/周/月/年线）、指数分钟级分时。用户询问某只指数行情、指数列表、指数 K 线或分时时使用。
---

# FT 指数数据 Skills

本 skill 是 `FTShare-index-data` 的**统一路由入口**。

根据用户问题，从下方「能力总览」或「询问方式与子 skill 对应表」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> 所有接口均以 `https://market.ft.tech` 为基础域名，请求头需携带 `X-Client-Name: ft-web`（各子 skill 脚本已内置）。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>` 。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> index-description-all
python <RUN_PY> index-detail --index 000001.XSHG
python <RUN_PY> index-list-paginated --order_by "change_rate desc" --page_size 20 --page_no 1
python <RUN_PY> index-ohlcs --index 000001.XSHG --span DAY1 --limit 50
python <RUN_PY> index-prices --index 000001.XSHG --since TODAY
python <RUN_PY> get-nth-trade-date --n 5
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## 指数 — 询问方式与子 skill 对应表

| 询问方式（用户常说的词） | 子 skill |
|------------------------|----------|
| **全部指数基础信息**、**指数列表（PB/PE）**、**有哪些指数**、指数 **简称/全称**、**市净率/市盈率 TTM** | `index-description-all` |
| 某只 **指数详情**、**上证指数行情**、**沪深300** 点位/涨跌幅、指数名称/成交 | `index-detail` |
| **指数列表**、**全市场指数**、**按涨跌幅排序的指数**、**筛选某类指数** | `index-list-paginated` |
| 某只指数的 **K 线**、**上证指数日线/周线/月线/年线**、指数 **开高低收**、**MA5/MA10/MA20** | `index-ohlcs` |
| 某只指数 **分时**、**上证指数当日分时**、指数 **一分钟行情**、**多日分时走势** | `index-prices` |
| **前 N 个交易日**、**近 N 天交易日**、**往前推 N 个交易日**（查近几天 K 线时先调此接口再转时间戳） | `get-nth-trade-date` |

---

## 能力总览

- **`get-nth-trade-date`**：获取当前日期的前 N 个交易日。必填：`--n`（≥1）。查「近 N 天」K 线时先调本接口得到 `nth_trade_date`，再按东八区转为毫秒时间戳用于 index-ohlcs 等。
- **`index-description-all`**：查询全部指数基础信息（symbol、全称、简称、pb、pe_ttm）。无需参数；`GET /data/api/v1/market/data/index-description-all`。
- **`index-detail`**：查询单只指数详情（名称、行情点位、成交、涨跌幅、多周期涨跌幅等）。必填：`--index`；可选 `--masks`。若用户仅给名称，先通过 `index-description-all` 或 `index-list-paginated` 确认代码再查。
- **`index-list-paginated`**：指数分页列表，支持分页、排序、筛选。可选：`--order_by`/`--ob`、`--filter`、`--masks`、`--page_size`、`--page_no`。
- **`index-ohlcs`**：查询单只指数 OHLC K 线（开高低收、成交量、成交额），附带 MA5/MA10/MA20。必填：`--index`、`--span`（DAY1/WEEK1/MONTH1/YEAR1）；可选 `--limit`、`--until_ts_ms`。建议先完成名称到代码映射后再调用。
- **`index-prices`**：查询单只指数分钟级分时价格。必填：`--index`；时间范围二选一：`--since`（TODAY、FIVE_DAYS_AGO、TRADE_DAYS_AGO(n)）或 `--since_ts_ms`。建议先完成名称到代码映射后再调用。

---

## 使用流程

1. **记录本文件绝对路径**，将 `/SKILL.md` 替换为 `/run.py` 得到 `<RUN_PY>`。
2. **理解用户意图**，从「询问方式与子 skill 对应表」或「能力总览」匹配子 skill 名称。
3. **若用户给的是指数名称/简称**：先调用 `index-description-all` 或 `index-list-paginated` 获取候选，确定标准代码（如 `000001.XSHG`）。
4. （可选）读取 `sub-skills/<子skill名>/SKILL.md` 了解接口与参数。
5. **执行**：`python <RUN_PY> <子skill名> [参数...]`，获取 JSON 输出（详情/K 线/分时统一使用代码参数 `--index`）。
6. **解析并输出**：以表格或要点形式展示给用户；若候选代码不唯一，先让用户确认再查询指标。
