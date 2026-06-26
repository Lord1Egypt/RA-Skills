---
name: FTShare-macro-economy-data
description: 中国与美国宏观经济指标技能集（market.ft.tech）。中国：GDP、LPR、PMI、PPI、CPI、财政收入、信贷、外储、社零、税收、M0/M1/M2、进出口、工业增加值、存准率、固投等 15 项月度/季度；美国：按 type 查询 ISM、非农、贸易帐、失业率、PPI/CPI、新屋/成屋、耐用品、咨商会信心、GDP 年率、联邦基金利率等 16 类。用户问中国/美国经济数据时使用。
---

# FT 宏观经济数据 Skills（中国 + 美国）

本 skill 是 `FTShare-macro-economy-data` 的**统一路由入口**，覆盖**中国经济**与**美国经济**指标。

根据用户问题，从下方「能力总览」或「提示词表」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> 所有接口均以 `https://market.ft.tech` 为基础域名，使用 HTTP GET。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>`。
2. **中国经济**（15 项）：`python <RUN_PY> <子skill名>`（无额外参数）。
3. **美国经济**（1 项，按 type）：`python <RUN_PY> economic-us-economic-by-type --type <type值>`。

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> economic-china-gdp-quarterly
python <RUN_PY> economic-china-pmi-monthly
python <RUN_PY> economic-china-cpi-monthly
python <RUN_PY> economic-us-economic-by-type --type nonfarm-payroll
python <RUN_PY> economic-us-economic-by-type --type cpi-mom
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## 能力总览与提示词表

**匹配提示**：用户问「中国/我国 + 某经济指标」或「美国 + 某经济指标」时，先区分国别，再按下表匹配子 skill（中国 15 项无参；美国 1 项需带 `--type`）。

### 中国经济 — 提示词与子 skill 对应表

| 提示词（用户常说的词） | 子 skill |
|------------------------|----------|
| **GDP**、国内生产总值、三次产业 | `economic-china-gdp-quarterly` |
| 财政收入、财政月度 | `economic-china-fiscal-revenue-monthly` |
| **LPR**、贷款市场报价利率、房贷利率、1年期/5年期 | `economic-china-lpr-monthly` |
| **PMI**、采购经理人指数、制造业/非制造业PMI | `economic-china-pmi-monthly` |
| **PPI**、工业品出厂价格指数、生产者价格指数 | `economic-china-ppi-monthly` |
| 信贷、**新增信贷**、新增人民币贷款、贷款增量 | `economic-china-credit-loans-monthly` |
| 外汇储备、黄金储备、**外储** | `economic-china-forex-gold-monthly` |
| 社会消费品零售总额、**社零**、零售总额、消费零售 | `economic-china-retail-sales-monthly` |
| 全国税收收入、税收收入、税收月度 | `economic-china-tax-revenue-monthly` |
| **CPI**、居民消费价格指数、消费价格指数、城市/农村CPI | `economic-china-cpi-monthly` |
| **M0、M1、M2**、货币供应量、广义货币、狭义货币 | `economic-china-money-supply-monthly` |
| 海关进出口、**进出口、外贸**、出口、进口 | `economic-china-customs-trade-monthly` |
| 工业增加值、工业增长 | `economic-china-industrial-added-value-monthly` |
| 存款准备金率、**存准率、RRR**、准备金率 | `economic-china-reserve-ratio-monthly` |
| 城镇固定资产投资、**固投**、固定资产投资 | `economic-china-fixed-asset-investment-monthly` |

### 美国经济 — 提示词与 type 对应表

子 skill 固定为 `economic-us-economic-by-type`，执行：`python <RUN_PY> economic-us-economic-by-type --type <type值>`。

| 提示词（用户常说的词） | type 值 |
|------------------------|---------|
| 美国 **ISM 制造业**、美国制造业PMI | `ism-manufacturing` |
| 美国 **ISM 非制造业**、美国服务业PMI | `ism-non-manufacturing` |
| 美国**非农**、非农就业、非农人数 | `nonfarm-payroll` |
| 美国**贸易帐**、贸易赤字/盈余 | `trade-balance` |
| 美国**失业率** | `unemployment-rate` |
| 美国 **PPI**、生产者物价月率 | `ppi-mom` |
| 美国 **CPI 月率**、消费者物价月率 | `cpi-mom` |
| 美国 **CPI 年率**、消费者物价年率 | `cpi-yoy` |
| 美国**核心 CPI 月率** | `core-cpi-mom` |
| 美国**核心 CPI 年率** | `core-cpi-yoy` |
| 美国**新屋开工** | `housing-starts` |
| 美国**成屋销售** | `existing-home-sales` |
| 美国**耐用品订单**、耐用品订单月率 | `durable-goods-orders-mom` |
| 美国**咨商会信心指数**、消费者信心 | `cb-consumer-confidence` |
| 美国 **GDP 年率**、GDP 初值、季度GDP | `gdp-yoy-preliminary` |
| 美国**联邦基金利率**、美联储利率、利率决议上限 | `fed-funds-rate-upper` |

---

## 子 skill 列表（路径说明）

所有子 skill 位于本包 `sub-skills/<子skill名>/`，接口详情见各子 skill 的 `SKILL.md`。

**中国经济（15 项）**

- `economic-china-gdp-quarterly` — 中国 GDP 季度
- `economic-china-fiscal-revenue-monthly` — 中国财政收入月度
- `economic-china-lpr-monthly` — 中国 LPR 月度
- `economic-china-pmi-monthly` — 中国 PMI 月度
- `economic-china-ppi-monthly` — 中国 PPI 月度
- `economic-china-credit-loans-monthly` — 中国信贷月度
- `economic-china-forex-gold-monthly` — 中国外汇与黄金储备月度
- `economic-china-retail-sales-monthly` — 中国社零月度
- `economic-china-tax-revenue-monthly` — 中国税收收入月度
- `economic-china-cpi-monthly` — 中国 CPI 月度
- `economic-china-money-supply-monthly` — 中国货币供应量 M0/M1/M2 月度
- `economic-china-customs-trade-monthly` — 中国海关进出口月度
- `economic-china-industrial-added-value-monthly` — 中国工业增加值月度
- `economic-china-reserve-ratio-monthly` — 中国存款准备金率月度
- `economic-china-fixed-asset-investment-monthly` — 中国城镇固定资产投资月度

**美国经济（1 项，按 type 区分 16 类）**

- `economic-us-economic-by-type` — 美国经济指标统一接口，必填 `--type`（见上表 type 值）。

---

## 使用流程

1. **记录本文件绝对路径**，将 `/SKILL.md` 替换为 `/run.py` 得到 `<RUN_PY>`。
2. **理解用户意图**，从「中国经济 — 提示词与子 skill 对应表」或「美国经济 — 提示词与 type 对应表」匹配子 skill 及（美国）`--type`。
3. （可选）读取 `sub-skills/<子skill名>/SKILL.md` 了解接口与参数。
4. **执行**：中国 `python <RUN_PY> <子skill名>`；美国 `python <RUN_PY> economic-us-economic-by-type --type <type值>`。
5. **解析并输出**：以表格或要点形式展示给用户。
