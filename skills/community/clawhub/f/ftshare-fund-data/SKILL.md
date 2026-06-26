---
name: FTShare-fund-data
description: 基金数据技能集（market.ft.tech）。覆盖基金基本信息、净值历史、累计收益率、基金概览列表、支持基金标的列表。用户询问基金详情、基金净值、基金收益、基金列表时使用。
---

# FT 基金数据 Skills

本 skill 是 `FTShare-fund-data` 的**统一路由入口**。

根据用户问题，从下方「能力总览」或「询问方式与子 skill 对应表」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> 所有接口均以 `https://market.ft.tech` 为基础域名。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>` 。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> fund-basicinfo-single-fund --institution-code 000001
python <RUN_PY> fund-cal-return-single-fund-specific-period --institution-code 159619 --cal-type 1Y
python <RUN_PY> fund-nav-single-fund-paginated --institution-code 000001 --page 1 --page-size 50
python <RUN_PY> fund-overview-all-funds-paginated --page 1 --page-size 20
python <RUN_PY> fund-support-symbols-all-funds-paginated --page 1 --page-size 20
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## 基金 — 询问方式与子 skill 对应表

| 询问方式（用户常说的词） | 子 skill |
|------------------------|----------|
| **基金基本信息**、某只**基金详情**、**基金管理人/基金经理**、**基金类型/投资目标** | `fund-basicinfo-single-fund` |
| **基金累计收益率**、**近1年/近3个月收益**、**YTD 收益**、**基金收益曲线** | `fund-cal-return-single-fund-specific-period` |
| **基金净值**、**单位净值/累计净值**、**日增长率**、**基金净值历史** | `fund-nav-single-fund-paginated` |
| **基金概览**、**所有基金信息**、**基金列表概况** | `fund-overview-all-funds-paginated` |
| **支持的基金列表**、**基金代码清单**、**所有基金标的** | `fund-support-symbols-all-funds-paginated` |

---

## 能力总览

- **`fund-basicinfo-single-fund`**：查询指定基金基础信息（名称、管理人、经理、类型、投资目标等）。必填：`--institution-code`（6 位基金代码）。若用户仅给基金名称，先通过 `fund-support-symbols-all-funds-paginated` 或 `fund-overview-all-funds-paginated` 映射代码再查。
- **`fund-cal-return-single-fund-specific-period`**：查询指定基金在指定区间的累计收益率时间序列。必填：`--institution-code`、`--cal-type`（1M/3M/6M/1Y/3Y/5Y/YTD）。建议先完成名称到代码映射后再调用。
- **`fund-nav-single-fund-paginated`**：查询指定基金净值历史（分页）。必填：`--institution-code`；可选：`--page`、`--page-size`。建议先完成名称到代码映射后再调用。
- **`fund-overview-all-funds-paginated`**：查询所有基金概览信息（分页）。可选：`--page`、`--page-size`。
- **`fund-support-symbols-all-funds-paginated`**：查询所有支持基金的标的列表（分页）。可选：`--page`、`--page-size`。

---

## 使用流程

1. **记录本文件绝对路径**，将 `/SKILL.md` 替换为 `/run.py` 得到 `<RUN_PY>`。
2. **理解用户意图**，从「询问方式与子 skill 对应表」或「能力总览」匹配子 skill 名称。
3. **若用户给的是基金名称而非代码**：先调用 `fund-support-symbols-all-funds-paginated` 或 `fund-overview-all-funds-paginated` 获取候选，确定 6 位 `institution-code`。
4. （可选）读取 `sub-skills/<子skill名>/SKILL.md` 了解接口与参数。
5. **执行**：`python <RUN_PY> <子skill名> [参数...]`，获取 JSON 输出（详情/净值/收益统一使用 `--institution-code`）。
6. **解析并输出**：以表格或要点形式展示给用户；若候选不唯一，先让用户确认再查询指标。
