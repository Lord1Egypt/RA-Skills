---
name: ftai-market-data
description: 非凸科技A股市场数据技能集。覆盖 A 股股票列表、实时行情、IPO信息、大宗交易、融资融券、个股详情与估值等接口。
---

# FT AI Market Data Skills

本 skill 是 `ftai-market-data` 的**统一路由入口**。

根据用户问题，从下方「能力总览」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> 所有接口均以 `https://market.ft.tech` 为基础域名，使用 HTTP GET。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>` 。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> stock-list-all-stocks
python <RUN_PY> stock-ipos --page 1 --page_size 20
python <RUN_PY> stock-ipos --all
python <RUN_PY> block-trades
python <RUN_PY> margin-trading-details --page 1 --page_size 20
python <RUN_PY> margin-trading-details --all
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## 能力总览

### 1. 股票数据（A 股）

- **`stock-list-all-stocks`**：获取全部 A 股股票的代码和名称列表（沪深京），自动返回最新交易日数据。无需任何参数。

- **`stock-quotes-list`**：查询 A 股行情列表（分页），支持按板块筛选、多字段排序。必填参数：`--order_by`、`--page_no`、`--page_size`；可选 `--filter`、`--masks`。请求头需携带 `X-Client-Name: ft-web`（脚本已内置）。

- **`stock-ipos`**：获取 A 股 IPO 列表，含发行价格、发行数量、申购日期、上市日期等，支持分页查询。必填参数：`--page`、`--page_size`；支持 `--all` 自动翻页拉取全量数据。

- **`block-trades`**：查询 A 股大宗交易列表，含买卖方营业部、成交价、成交量、溢价率等。无需任何参数，直接返回数组。

- **`margin-trading-details`**：获取 A 股融资融券明细列表，含融资余额、融资买入额、融资偿还额、融券余量等，按融资净买入额降序排列，支持分页查询。必填参数：`--page`、`--page_size`；支持 `--all` 自动翻页拉取全量数据。

- **`stock-security-info`**：查询单只股票的实时行情与估值指标，含开高低收、多周期涨跌幅、市盈率、市净率、每股净资产等。必填参数：`--symbol`（带市场后缀，如 `600519.SH`）。接口域名为 `https://ftai.chat`。

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
| 「列出所有 A 股股票」 | `stock-list-all-stocks` |
| 「A 股有哪些股票代码？」 | `stock-list-all-stocks` |
| 「获取全市场股票列表」 | `stock-list-all-stocks` |
| 「A 股行情列表、按涨跌幅排序、分页」 | `stock-quotes-list` |
| 「科创板/创业板股票行情列表」 | `stock-quotes-list` |
| 「查看 A 股 IPO 列表」 | `stock-ipos` |
| 「最近有哪些新股上市？」 | `stock-ipos` |
| 「查询某只股票的发行价格 / 申购日期」 | `stock-ipos` |
| 「查看今天的大宗交易记录」 | `block-trades` |
| 「哪些股票有大宗交易？买卖方是谁？」 | `block-trades` |
| 「大宗交易溢价率最高的是哪只？」 | `block-trades` |
| 「融资净买入最多的股票有哪些？」 | `margin-trading-details` |
| 「查看最新的融资融券明细数据」 | `margin-trading-details` |
| 「哪只股票融资余额最高？」 | `margin-trading-details` |
| 「查一下贵州茅台的股价」 | `stock-security-info` |
| 「000001.SZ 的市盈率是多少？」 | `stock-security-info` |
| 「某只股票的市值、涨跌幅、估值」 | `stock-security-info` |
