---
name: FTShare-ashare-performance-data
description: A 股业绩大全技能集。覆盖业绩快报、业绩预告、现金流量表、利润表、资产负债表（单票历期与指定报告期全市场，market.ft.tech）。用户询问业绩快报、业绩预告、三表、单票或全市场某报告期时使用。
---

# FT A-share 业绩大全 Skills

本 skill 是 `FTShare-ashare-performance-data` 的**统一路由入口**。

根据用户问题，从下方「能力总览」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> 所有接口均以 `https://market.ft.tech` 为基础域名，使用 HTTP GET。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>` 。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> stock-performance-express-all-stocks-specific-period --year 2025 --report-type q2 --page 1 --page-size 20
python <RUN_PY> stock-performance-express-single-stock-all-periods --stock-code 000001.SZ --page 1 --page-size 50
python <RUN_PY> stock-performance-forecast-all-stocks-specific-period --year 2025 --report-type annual --page 1 --page-size 20
python <RUN_PY> stock-performance-forecast-single-stock-all-periods --stock-code 000001.SZ --page 1 --page-size 50
python <RUN_PY> stock-cashflow-single-stock-all-periods --stock-code 000001.SZ
python <RUN_PY> stock-cashflow-all-stocks-specific-period --year 2025 --report-type q2 --page 1 --page-size 20
python <RUN_PY> stock-income-single-stock-all-periods --stock-code 000001.SZ
python <RUN_PY> stock-income-all-stocks-specific-period --year 2025 --report-type q2 --page 1 --page-size 20
python <RUN_PY> stock-balance-single-stock-all-periods --stock-code 000001.SZ
python <RUN_PY> stock-balance-all-stocks-specific-period --year 2025 --report-type q2 --page 1 --page-size 20
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## 能力总览

### 1. 业绩快报 / 业绩预告

- **`stock-performance-express-all-stocks-specific-period`**：单一报告期（如 2025Q2）全市场业绩快报列表（分页）。必填：`--year`、`--report-type`；可选 `--page`、`--page-size`。
- **`stock-performance-express-single-stock-all-periods`**：单只股票历期业绩快报（分页）。必填：`--stock-code`；可选 `--page`、`--page-size`。
- **`stock-performance-forecast-all-stocks-specific-period`**：单一报告期全市场业绩预告列表（分页）。必填：`--year`、`--report-type`；可选 `--page`、`--page-size`。
- **`stock-performance-forecast-single-stock-all-periods`**：单只股票历期业绩预告（分页）。必填：`--stock-code`；可选 `--page`、`--page-size`。

### 2. 现金流量表

- **`stock-cashflow-single-stock-all-periods`**：单只股票所有报告期现金流量表。必填：`--stock-code`。
- **`stock-cashflow-all-stocks-specific-period`**：指定报告期全市场现金流量表（分页）。必填：`--year`、`--report-type`、`--page`、`--page-size`。

### 3. 利润表

- **`stock-income-single-stock-all-periods`**：单只股票所有报告期利润表。必填：`--stock-code`。
- **`stock-income-all-stocks-specific-period`**：指定报告期全市场利润表（分页）。必填：`--year`、`--report-type`、`--page`、`--page-size`。

### 4. 资产负债表

- **`stock-balance-single-stock-all-periods`**：单只股票所有报告期资产负债表。必填：`--stock-code`。
- **`stock-balance-all-stocks-specific-period`**：指定报告期全市场资产负债表（分页）。必填：`--year`、`--report-type`、`--page`、`--page-size`。

---

## 使用流程

1. **记录本文件绝对路径**，将 `/SKILL.md` 替换为 `/run.py` 得到 `<RUN_PY>`。
2. **理解用户意图**，从「能力总览」匹配对应子 skill 名称。
3. （可选）读取 `sub-skills/<子skill名>/SKILL.md` 了解接口详情与参数。
4. **执行**：`python <RUN_PY> <子skill名> [参数...]`，获取 JSON 输出。
5. **解析并输出**：以表格或要点形式展示给用户。

---

## 子 skill 与用户问法示例

| 用户问法示例 | 子 skill 名 |
|--------------|-------------|
| 「2025 年二季报/半年报业绩快报」「指定报告期全市场业绩快报」 | `stock-performance-express-all-stocks-specific-period` |
| 「某只股票历期业绩快报」 | `stock-performance-express-single-stock-all-periods` |
| 「2025 年年报业绩预告」「指定报告期全市场业绩预告」 | `stock-performance-forecast-all-stocks-specific-period` |
| 「某只股票历期业绩预告」 | `stock-performance-forecast-single-stock-all-periods` |
| 「某只股票现金流量表」「历期现金流量表」 | `stock-cashflow-single-stock-all-periods` |
| 「2025 年二季报全市场现金流量表」 | `stock-cashflow-all-stocks-specific-period` |
| 「某只股票利润表」「历期利润表」 | `stock-income-single-stock-all-periods` |
| 「2025 年二季报全市场利润表」 | `stock-income-all-stocks-specific-period` |
| 「某只股票资产负债表」「历期资产负债表」 | `stock-balance-single-stock-all-periods` |
| 「2025 年二季报全市场资产负债表」 | `stock-balance-all-stocks-specific-period` |
