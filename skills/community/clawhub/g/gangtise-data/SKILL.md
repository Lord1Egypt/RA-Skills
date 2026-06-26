---
name: gangtise-data
description: 通过 Gangtise 金融 Open API 拉取结构化量化数据，包括日K行情、财务三大报表、主营构成与估值分位等。需在 scripts 目录配置授权（.authorization），证券参数须为完整代码（如 600519.SH）。当用户需要可落盘的表格化行情与基本面数据时使用。
version: 1.4.3
metadata:
  requires:
    env:
      - GTS_ACCESS_KEY
      - GTS_SECRET_KEY
    config:
      - path: scripts/.authorization
        required: false
        description: 用于配置ak/sk, 内容为{"accessKey": "<ak>", "secretAccessKey": "<sk>"}。与GTS_ACCESS_KEY和GTS_SECRET_KEY使用其一即可。如果同时存在，则以GTS_ACCESS_KEY和GTS_SECRET_KEY为准，建议环境变量配置不成功时使用文件配置。
  envVars:
    - name: GTS_ACCESS_KEY
      required: true
      description: 用于和GTS_SECRET_KEY一起获取临时 authorization
    - name: GTS_SECRET_KEY
      required: true
      description: 用于和GTS_ACCESS_KEY一起获取临时 authorization
---

# 搜索

## 概览

本技能在**本机**调用 `scripts/*.py`，请求 **Gangtise Open API**（`open.gangtise.com`），得到**结构化、可保存为 CSV** 的结果（由 `scripts/utils.py` 中的 `format_response` 写入工作区 `workspace/gangtise/` 下对应子目录）。

当前脚本覆盖：

- **估值分析**（多指标并发、历史分位）：`scripts/valuation.py`
- **A 股日 K**（可选全市场、`--adjust` 不复权/前复权/后复权；前复权默认，复权因子来自独立接口）：`scripts/quote.py`
- **主营构成**（按产品/行业/地区，可并发全维度）：`scripts/main_business.py`
- **股东结构**（前十大股东/前十大流通股东）：`scripts/shareholder.py`
- **财务报表**（利润表/资产负债表/现金流量表）：`scripts/financial.py`
- **盈利预测**（券商一致预期多指标）：`scripts/earning_forecast.py`

使用场景：

- 需要**精确数值、时间序列或宽表**，并保存为 **CSV** 做后续分析或制图。
- 已具备或可查到 **完整证券代码**（本技能**不做**简称/键盘精灵解析）。

与其他技能的区别：

| 项目 | `gangtise-data`（本技能） | `gangtise-file` | `gangtise-kb` |
|------|---------------------------|-----------------|---------------|
| 数据形态 | **结构化数值表**（行情、财务、估值等），可落盘 CSV | **文件索引**：按类型/证券/日期等筛文档，返回 ID、元数据、摘要，可下载全文 | **语义检索**：返回与查询相关的**内容片段**，偏阅读与推理 |
| 典型问题 | 「这只股票某段区间的收盘价、利润表科目是多少」 | 「最近有哪些研报/公告、ID 是什么」 | 「文档里怎么论述某观点、结论是什么」 |
| 调用方式 | 本机脚本 + `scripts/.authorization` | 本机脚本 + 授权 | 本机脚本 + 授权 |

（中文说明：本技能解决「**是多少、表格化**」；要先**列文件再下载**用 `gangtise-file`；要**读原文片段、问答**用 `gangtise-kb`。）

**授权**：在 `scripts/` 下放置 `.authorization`，内容为 `long-term-token`，或 `accessKey` + `secretAccessKey`（将自动换 token）。详见 `scripts/utils.py`。

调用脚本时若使用 `-sd` / `-ed`，请注意**当前真实日期与年份**。

**报告期（财务 / 主营）**：命令行统一使用 **Q1 / Q2 / Q3 / Q4 / Q0**（分别对应一季报、中报、三季报、年报、最新一期）；脚本内再映射为 Open API 所需枚举（详见各 `references`）。

调用各脚本前，请阅读对应 **[references](./references/)** 中的参数与返回说明。

## 使用说明

### 1. 估值数据（估值分析）

基于 open **估值分析**接口，并发拉取 peTtm / psTtm / pbMrq / peg / pcfTtm / em，并组装为与后端类似的宽表列（含「在 N 年中所处分位」）。`-sd/-ed` 默认均为当天。

```bash
python3 scripts/valuation.py --securities 600519.SH,000858.SZ
```

```bash
python3 scripts/valuation.py --securities-file ./codes.csv -sd 2023-01-01 -ed 2026-12-31
```

详见 [估值数据调用指导](./references/valuation.md)。

### 2. 行情数据（日 K）

基于 open **日 K** 接口；`-sd/-ed` 默认均为当天；**`--all-market`** 时不传证券列表（数据量可能极大，需配合日期与 `limit`）。

```bash
python3 scripts/quote.py --securities 00700.HK -sd 2026-04-23 -ed 2026-04-23
```

```bash
python3 scripts/quote.py --securities-file ./codes.csv --limit 8000
```

详见 [行情数据调用指导](./references/quote.md)。

### 3. 主营构成

基于 open **main-business** 接口；不传 `--breakdown` 时并发拉取 **product / industry / region** 三种拆分。`--period` 仅支持 **Q2**（中报）或 **Q4**（年报）。

```bash
python3 scripts/main_business.py --securities 000651.SZ
```

```bash
python3 scripts/main_business.py --securities 600519.SH --breakdown product --period Q4
```

详见 [主营构成调用指导](./references/main_business.md)。

### 4. 股东结构（前十大 / 前十大流通）

基于 open **capital-structure/top-holders** 接口；通过 `--holder-type` 切换 `top10`（前十大股东）与 `top10Float`（前十大流通股东）。支持日期区间筛选（`-sd/-ed`）或按财报年度筛选（`--fiscal-year`），并可叠加报告期筛选（`--period`）。

```bash
python3 scripts/shareholder.py --holder-type top10 --securities 600519.SH
```

```bash
python3 scripts/shareholder.py --holder-type top10Float --securities 600519.SH -sd 2025-01-01 -ed 2025-12-31 --period q3
```

```bash
python3 scripts/shareholder.py --holder-type top10 --securities-file ./codes.csv --fiscal-year 2024,2025 --period q1,q3
```

详见 [股东结构调用指导](./references/shareholder.md)。

### 5. 财务数据（三大报表）

基于 open **financial-report** 系列接口，支持 `income`/`balance`/`cashflow`；`--period` 使用 `Q1~Q4,Q0`（默认 `Q0`），`--granularity` 支持 `accumulated|quarterly`（默认 `accumulated`，仅利润表/现金流量表生效）；默认 `fieldList=[]` 返回全部科目。

```bash
python3 scripts/financial.py --securities 600519.SH
```

```bash
python3 scripts/financial.py --table-type balance --securities 600519.SH --period Q4
```

```bash
python3 scripts/financial.py --table-type income --granularity quarterly --securities 600519.SH --fiscal-year 2025 --period Q2 --field-list totalOpRev,totalOpCost,netProfit,basicEPS
```

```bash
python3 scripts/financial.py --securities-file ./codes.csv --field-list netProfit,basicEarningsPerShare
```

详见 [财务数据调用指导](./references/financial.md)。

### 6. 盈利预测（券商一致预期）

基于 open **earning_forecast** 接口，支持通过 `--securities`/`--securities-file` 并发查询多只证券在指定日期区间的券商一致预期；支持通过 `--consensus-list` 选择指标，不传则默认返回全部可选字段。`-sd/-ed` 默认均为当天。返回会展开为 `security_code | date | 预测年份 | ...` 的扁平表；若单日查询当日无数据，会仅向前回退一天重试一次。

```bash
python3 scripts/earning_forecast.py --securities 600519.SH,000858.SZ -sd 2026-03-20 -ed 2026-03-25
```

```bash
python3 scripts/earning_forecast.py --securities-file ./codes.csv -sd 2026-03-20 -ed 2026-03-25 --consensus-list netIncome,eps,pe
```

详见 [盈利预测调用指导](./references/earning_forecast.md)。