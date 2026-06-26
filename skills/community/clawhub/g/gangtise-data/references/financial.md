# 财务数据调用指导（Open API · financial-report）

## 简介

通过 Gangtise Open API 获取上市公司财务报表数据，支持三类报表：

- 利润表（`income-statement`）
- 资产负债表（`balance-sheet`）
- 现金流量表（`cashflow-statement`）

脚本：`scripts/financial.py`。

- 默认 `fieldList=[]`，表示返回全部科目（以接口返回为准）。
- 会删除数值列全空的行、数值列全空的列，并剔除 `category`、`announcementDate`（若返回）。
- 科目英文名按内置映射转中文；未映射字段保持原名。
- 数值列统一保留两位小数。
- 输出会把 `证券简称`、`证券代码`、`财报截止日期` 规范为 `security_abbr`、`security_code`、`date` 并放在前面。

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `-t` / `--table-type` | 否 | 报表类型：`income`/`利润表`、`balance`/`资产负债表`、`cashflow`/`现金流量表`。默认 `income`。 |
| `-sd` / `--start-date` | 否 | 开始日期 `yyyy-MM-dd`。与 `endDate` 同时有值时覆盖 `fiscalYear` 的筛选（按接口规则）。 |
| `-ed` / `--end-date` | 否 | 结束日期 `yyyy-MM-dd`。 |
| `--fiscal-year` | 否 | 财报年度，逗号分隔，如 `2025,2026`。对应请求体 `fiscalYear`。 |
| `--period` | 否 | 报告期：**Q1 / Q2 / Q3 / Q4 / Q0**，逗号分隔；默认 **Q0**，即最新一期。 |
| `-g` / `--granularity` | 否 | 财报口径：`accumulated`（累计值，默认）/ `quarterly`（单季度值）。仅对 `income`、`cashflow` 生效；`balance` 仅支持 `accumulated`。 |
| `--report-type` | 否 | 报表类型，逗号分隔：`consolidated` / `consolidatedRestated` / `standalone` / `standaloneRestated`。默认 **`consolidated`**。 |
| `--field-list` | 否 | 指定科目**英文字段名**，逗号分隔；**不传**则 `fieldList=[]` 取全部。 |
| `--securities` | 否* | **完整证券代码**，逗号分隔。 |
| `--securities-file` | 否* | CSV 须含列 **`security_code`**。 |

\* 须至少提供 `--securities` 或 `--securities-file` 之一。

## 约束与说明

- 仅支持完整证券代码（如 `600519.SH`）。
- `--period` 仅支持 `Q1/Q2/Q3/Q4/Q0`，会映射到接口 `period`：`q1/interim/q3/annual/latest`。
- `--granularity` 仅支持 `accumulated/quarterly`（兼容中文别名“累计/单季度”）；其中 `quarterly` 仅适用于利润表和现金流量表。
- 报表类型别名支持中英文，例如：`profit/pl/利润表 -> income`、`bs/资产负债表 -> balance`、`cf/现金流量表 -> cashflow`。
- 若某报告期仅部分科目有值，行会保留；整行数值全空会删除。

## 调用示例

**最新一期合并利润表（默认 Q0）：**

```bash
python3 scripts/financial.py --securities 600519.SH
```

**查询资产负债表：**

```bash
python3 scripts/financial.py --table-type balance --securities 600519.SH
```

**查询现金流量表（中文别名）：**

```bash
python3 scripts/financial.py --table-type 现金流量表 --securities 600519.SH
```

**利润表切换为单季度口径（quarterly）：**

```bash
python3 scripts/financial.py --table-type income --granularity quarterly --securities 600519.SH --fiscal-year 2025 --period Q2 --field-list totalOpRev,totalOpCost,netProfit,basicEPS
```

**现金流量表切换为单季度口径（quarterly）：**

```bash
python3 scripts/financial.py --table-type cashflow --granularity quarterly --securities 600519.SH --fiscal-year 2023,2024,2025 --period Q2 --field-list netFinCashFlows
```

**指定年度与三季报：**

```bash
python3 scripts/financial.py --securities 600519.SH --fiscal-year 2025 --period Q3 --report-type consolidated
```

**按日期区间 + 仅年报（Q4）：**

```bash
python3 scripts/financial.py --securities 600519.SH -sd 2024-01-01 -ed 2026-03-24 --period Q4
```

**仅部分科目：**

```bash
python3 scripts/financial.py --securities 600519.SH --field-list netProfit,basicEarningsPerShare
```

**从文件读取证券：**

```bash
python3 scripts/financial.py --securities-file ./codes.csv
```

## 返回说明

- **成功**：在 `workspace/gangtise/financial/` 下生成 **`financial_*.csv`**，返回文案含路径与样例。
- **失败**：授权失败、证券无效、`table-type` 非法、`period` 非法、过滤后无数据等。

## 返回数据示例（CSV 结构）

| security_abbr | security_code | date | 报告期 | 报表类型 | 一、营业总收入 | … | 六、净利润 | … |
|---------------|---------------|------|--------|----------|----------------|---|------------|---|
| 贵州茅台 | 600519.SH | 2022-03-31 | 2022年一季报 | 合并报表 | … | … | … | … |

（中间列为对应报表科目中文名；未映射的英文字段名将原样保留。）
