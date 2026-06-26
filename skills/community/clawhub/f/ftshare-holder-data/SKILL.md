---
name:  FTShare-holder-data
description: 非凸科技 A 股股东数据技能集。覆盖十大股东、十大流通股东、股东户数、股权质押总揽等接口（market.ft.tech）。用户询问 A 股某只股票的历期十大股东、股东结构变动、持股比例、股东人数变化、或全市场股权质押情况时使用。
---

# FTShare A 股股东数据 Skills

本 skill 是 ` FTShare-holder-data` 的**统一路由入口**。

根据用户问题，从下方「能力总览」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> 所有接口均以 `https://market.ft.tech` 为基础域名，使用 HTTP GET。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>`。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> stock-holder-ten --stock_code 603323.SH
python <RUN_PY> stock-holder-ften --stock_code 603323.SH
python <RUN_PY> stock-holder-nums --stock_code 603323.SH
python <RUN_PY> pledge-summary
python <RUN_PY> pledge-detail --stock_code 603323.SH
python <RUN_PY> stock-share-chg --stock_code 603323.SH
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## 能力总览

### 1. 十大股东

- **`stock-holder-ten`**：查询单只 A 股股票所有公告期的十大股东信息，含持股比例、股东明细、变动类型等。必填参数：`--stock_code`（如 `603323.SH`）。

### 2. 十大流通股东

- **`stock-holder-ften`**：查询单只 A 股股票所有公告期的十大流通股东信息，含流通持股比例、股东明细、变动类型等（`unlimit_num` 固定为 null）。必填参数：`--stock_code`（如 `603323.SH`）。

### 3. 股东人数

- **`stock-holder-nums`**：查询单只 A 股股票所有公告期的股东人数信息，含股东总人数、人数变化率、人均流通股数、人均持股金额、十大股东/流通股东持股比例等。必填参数：`--stock_code`（如 `603323.SH`）。

### 4. 股权质押总揽

- **`pledge-summary`**：查询 A 股市场所有报告期的股权质押总揽数据，含质押公司数量、质押笔数、质押总股数、质押总市值、沪深300指数及周涨跌幅。无需任何参数，返回值为数组（无分页包装）。

### 5. 股权质押个股详情

- **`pledge-detail`**：查询单只 A 股股票所有报告期的股权质押详细信息，含质押比例、质押笔数、质押市值、无限售/限售质押股数、较上年变动等。必填参数：`--stock_code`（如 `603323.SH`）；可选参数：`--page`、`--page_size`，返回值含分页信息。

### 6. 股东增减持

- **`stock-share-chg`**：查询单只 A 股股票所有报告期的股东增减持信息，含变动股东名称、变动类型（增持/减持）、变动数量、变动前后持股数量、最新股价及涨跌幅、变动日期区间、公告日期等。必填参数：`--stock_code`（如 `603323.SH`）；可选参数：`--page`、`--page_size`，返回值含分页信息。

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
| 「603323.SH 的十大股东是哪些？」 | `stock-holder-ten` |
| 「查看某只股票历期前十大股东变动」 | `stock-holder-ten` |
| 「某股票的大股东持股比例是多少？」 | `stock-holder-ten` |
| 「某股票最新一期十大股东有哪些新进股东？」 | `stock-holder-ten` |
| 「603323.SH 的十大流通股东是哪些？」 | `stock-holder-ften` |
| 「查看某只股票历期前十大流通股东变动」 | `stock-holder-ften` |
| 「某股票流通股东的持股比例是多少？」 | `stock-holder-ften` |
| 「603323.SH 的股东人数是多少？」 | `stock-holder-nums` |
| 「查看某只股票历期股东人数变化趋势」 | `stock-holder-nums` |
| 「某股票人均持股金额是多少？」 | `stock-holder-nums` |
| 「A 股市场整体股权质押情况如何？」 | `pledge-summary` |
| 「全市场质押公司数量和质押总市值是多少？」 | `pledge-summary` |
| 「查看历期股权质押总揽数据」 | `pledge-summary` |
| 「603323.SH 的股权质押详情是什么？」 | `pledge-detail` |
| 「某股票历期质押比例和质押笔数是多少？」 | `pledge-detail` |
| 「某股票最新一期股权质押市值是多少？」 | `pledge-detail` |
|| 「603323.SH 的股东增减持情况如何？」 | `stock-share-chg` |
|| 「某股票最近有哪些股东在减持？」 | `stock-share-chg` |
|| 「某股东对某股票的持股变动历史」 | `stock-share-chg` |
