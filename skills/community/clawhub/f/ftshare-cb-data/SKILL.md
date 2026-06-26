---
name: FTShare-cb-data
description: A 股可转债数据技能集（market.ft.tech）。覆盖可转债全量列表、单只可转债基础信息（转股价、转股价值、到期日、发行规模等）、单标的历史 K 线（支持可转债）。用户询问可转债列表、某只转债详情、转股价/转股价值、转债 K 线/历史行情时使用。
---

# FT 可转债数据 Skills

本 skill 是 `FTShare-cb-data` 的**统一路由入口**。

根据用户问题，从下方「能力总览」或「询问方式与子 skill 对应表」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> 所有接口均以 `https://market.ft.tech` 为基础域名，本技能集子 skill 无需额外请求头。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>` 。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> cb-lists
python <RUN_PY> cb-base-data --symbol_code 110070.SH
python <RUN_PY> cb-candlesticks --symbol 110070.XSHG --interval-unit Day --since-ts-millis 1767225600000 --until-ts-millis 1780272000000 --limit 10
python <RUN_PY> get-nth-trade-date --n 5
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## 可转债 — 询问方式与子 skill 对应表

| 询问方式（用户常说的词） | 子 skill |
|------------------------|----------|
| **可转债列表**、**全部可转债**、**转债代码列表**、**有哪些可转债**、可转债标的 | `cb-lists` |
| **某只可转债基础信息**、**转债详情**、**110070 转债**、**转股价/转股价值**、到期日、发行规模 | `cb-base-data` |
| **可转债 K 线**、**转债日线/周线/分钟线**、**转债历史行情**、**单标的历史 K 线**（支持转债） | `cb-candlesticks` |
| **前 N 个交易日**、**近 N 天交易日**、**往前推 N 个交易日**（查近几天 K 线时先调此接口再转时间戳） | `get-nth-trade-date` |

---

## 能力总览

- **`get-nth-trade-date`**：获取当前日期的前 N 个交易日。必填：`--n`（≥1）。查「近 N 天」K 线时先调本接口得到 `nth_trade_date`，再按东八区转为毫秒时间戳用于 K 线接口。
- **`cb-lists`**：获取可转债全量列表（全称、债券代码、正股代码、交易所）。无参数；数据为前一交易日。
- **`cb-base-data`**：查询单只可转债基础信息（简称、全称、正股代码、转股价、转股价值、转股溢价率、起息日/到期日、发行规模等，数据为前一交易日）。必填：`--symbol_code`（转债代码，可带交易所后缀如 110070.SH）。
- **`cb-candlesticks`**：查询单标的历史 K 线（**支持可转债**及 A 股）。必填：`--symbol`（带交易所后缀，如 110070.XSHG）、`--interval-unit`（Minute/Minute5/Day/Week/Month/Year）、`--since-ts-millis`、`--until-ts-millis`；可选：`--interval-value`、`--limit`、`--adjust-kind`（null/Forward/Backward）。

---

## 使用流程

1. **记录本文件绝对路径**，将 `/SKILL.md` 替换为 `/run.py` 得到 `<RUN_PY>`。
2. **理解用户意图**，从「询问方式与子 skill 对应表」或「能力总览」匹配子 skill 名称。
3. （可选）读取 `sub-skills/<子skill名>/SKILL.md` 了解接口与参数。
4. **执行**：`python <RUN_PY> <子skill名> [参数...]`，获取 JSON 输出。
5. **解析并输出**：以表格或要点形式展示给用户。
