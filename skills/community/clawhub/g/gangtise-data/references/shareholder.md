# 股东结构 API（Open API · top-holders）

## 简介

通过 Gangtise Open API 查询上市公司 **前十大股东** 与 **前十大流通股东** 持股明细，脚本为 `scripts/shareholder.py`。

返回包含股东名称、股东性质、持股数量/比例、较上期变动、股本性质等字段，适用于股东结构分析与机构持仓跟踪。

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--holder-type` | 是 | `top10`（前十大股东）或 `top10Float`（前十大流通股东）。 |
| `-sd` / `--start-date` | 否 | 开始日期 `yyyy-MM-dd`。仅传开始日期时，结束日期默认今天。 |
| `-ed` / `--end-date` | 否 | 结束日期 `yyyy-MM-dd`。仅传结束日期时，开始日期默认向前 3 年。 |
| `--fiscal-year` | 否 | 财报年度，逗号分隔，如 `2024,2025`。 |
| `--period` | 否 | 报告期：`q1` / `interim` / `q3` / `annual` / `latest`，逗号分隔，默认 `latest`。 |
| `--securities` | 否* | 完整证券代码，逗号分隔。 |
| `--securities-file` | 否* | CSV，须含 `security_code` 列。 |

\* 须至少提供 `--securities` 或 `--securities-file` 之一。

## 调用示例

```bash
python3 scripts/shareholder.py --holder-type top10 --securities 600519.SH
```

```bash
python3 scripts/shareholder.py --holder-type top10Float --securities 600519.SH -sd 2025-01-01 -ed 2025-12-31 --period q3
```

```bash
python3 scripts/shareholder.py --holder-type top10 --securities-file ./codes.csv --fiscal-year 2024,2025 --period q1,q3
```

## 返回说明

- 成功时会在 `workspace/gangtise/shareholder/` 下生成 `top_holders_*.csv`。
- CSV 典型字段：
  - `security_code`
  - `holder_type`
  - `date`
  - `rank`
  - `shareholder_name`
  - `shareholder_type`
  - `holding_num`
  - `holding_pct`
  - `chg_num`
  - `chg_pct`
  - `share_category`
