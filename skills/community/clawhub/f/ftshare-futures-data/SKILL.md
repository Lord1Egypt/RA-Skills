---
name: FTShare-futures-data
description: 非凸科技期货数据技能集（market.ft.tech）。覆盖指定交易日合约列表、期货合约基础信息（交易单位、保证金、交割等）、期货 K 线（分钟/日及周月季年聚合）。用户询问期货合约列表、某合约基础信息、期货 K 线或历史行情时使用。用户只给中文名/品种时，先用 futures-lists 做名称到 symbol 映射，再调基础信息或 K 线。
---

# FT 期货数据 Skills

本 skill 是 `FTShare-futures-data` 的**统一路由入口**。

根据用户问题，从下方「能力总览」或「子 skill 与用户问法示例」匹配子 skill，通过 `run.py` 执行并解析响应。

> 所有接口均以 `https://market.ft.tech` 为基础域名，路径前缀为 `/data/api/v1/market/data/futures`，使用 HTTP GET；**无需** `X-Client-Name` 等额外请求头（脚本不设置自定义头）。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>`。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> futures-lists --trade-date 20260331
python <RUN_PY> futures-base-data --trade-date 20260331 --symbol A2605.DCE
python <RUN_PY> futures-kline --symbol A2605.DCE --interval 30min --limit 50
python <RUN_PY> futures-kline --symbol A2605.DCE --interval daily --start 1772294400000 --end 1774972799999 --limit 100
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## 典型调用顺序

1. **先要合约代码（名称→代码映射）**：用户只说中文名/品种（如“豆一2605”“螺纹2505”）时，先 `futures-lists --trade-date <YYYYMMDD>`，在 `items` 里按 `symbol_cn_name` / `product` 匹配，得到 `symbol`（WIND 全码，如 `A2605.DCE`）。
2. **基础信息**：`futures-base-data --trade-date <可选> --symbol <WIND全码>`。
3. **K 线**：`futures-kline --symbol <WIND全码> [--interval] [--start --end] [--limit]`。`--start` 与 `--end` 必须成对传入。

**毫秒时间戳**：若需交易日边界转 `start/end`，可使用 `FTShare-kline-data`（或本仓库其他包）中的 `get-nth-trade-date` 得到日期后再换算为东八区毫秒时间戳。

---

## 能力总览

- **`futures-lists`**：查询指定交易日期货合约列表。可选：`--trade-date`（YYYYMMDD）；不传默认前一交易日（CST）。`GET /data/api/v1/market/data/futures/futures-lists`
- **`futures-base-data`**：查询期货基础信息。可选：`--trade-date`、`--symbol`；不传 `--symbol` 则该日全部合约。`GET /data/api/v1/market/data/futures/futures-base-data`
- **`futures-kline`**：查询期货 K 线。必填：`--symbol`；可选：`--interval`、`--start`、`--end`、`--limit`。`GET /data/api/v1/market/data/futures/kline`

---

## 使用流程

1. **记录本文件绝对路径**，将 `/SKILL.md` 替换为 `/run.py` 得到 `<RUN_PY>`。
2. **理解用户意图**，从「能力总览」匹配子 skill。
3. **若用户给的是中文名/品种而非 symbol**：先调 `futures-lists` 做名称映射，拿到 `symbol` 后再查 `futures-base-data` 或 `futures-kline`。
4. （可选）读取 `sub-skills/<子skill名>/SKILL.md` 了解参数与响应字段。
5. **执行**：`python <RUN_PY> <子skill名> [参数...]`。
6. **解析并输出**：以表格或要点形式展示。

---

## 子 skill 与用户问法示例

| 用户问法示例 | 子 skill 名 |
|---|---|
| 「期货列表」「某日全部期货合约」「合约代码清单」 | `futures-lists` |
| 「豆一2605 对应代码是什么」「按中文名找期货代码」 | 先 `futures-lists`（按 `symbol_cn_name`/`product` 匹配） |
| 「A2605 基础信息」「保证金/交割/乘数/交易单位」 | `futures-base-data` |
| 「期货 K 线」「分钟线/日线/周线」「某合约历史行情」 | `futures-kline` |
