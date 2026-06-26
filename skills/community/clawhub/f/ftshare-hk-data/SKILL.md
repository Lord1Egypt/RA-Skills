---
name: FTShare-hk-data
description: 港股数据技能集（market.ft.tech）。覆盖公司介绍、分页估值分析（PE/PB/PS/股息率）、单票基础视图（板块/上市状态/市值/股本）、日/月/季/年 K 线（历史k线，T日18点更新当日数据）（前复权/不复权）。用户询问港股公司简介、港股估值、市盈率市净率、港股基础信息、市值总股本、港股 K 线/日线/月线、港股历史行情时使用。
---

# FT 港股数据 Skills

本 skill 是 `FTShare-hk-data` 的**统一路由入口**。

根据用户问题，从下方「能力总览」或「询问方式与子 skill 对应表」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> 所有接口均以 `https://market.ft.tech` 为基础域名，本技能集子 skill 无需额外请求头。

### 时区与交易日历

港股交易时间遵循 **港交所交易日历（UTC+8 / 东八区）**。

- 所有 **YYYYMMDD / YYYY-MM-DD** 日期字段均为东八区交易日。
- `update_time`（如 `20260324120000`）等时间戳字段也基于东八区。
- 调用方传入日期时无需手动转时区——接口本身按东八区解释。
- 若 Agent 所在系统时区非东八区，在计算「今天」「昨天」等相对日期时，应先转为东八区日期再传参。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>` 。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> company-hk --trade_code 00700.HK
python <RUN_PY> hk-valuatnanalyd --trade_code 00700.HK --page 1 --page_size 20
python <RUN_PY> hk-valuatnanalyd --page 1 --page_size 20
python <RUN_PY> hk-view --hk_code 00700.HK
python <RUN_PY> hk-candlesticks --trade-code 00700.HK --interval-unit day --until-date 2026-03-24 --since-date 2026-03-01 --limit 20
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## 港股 — 询问方式与子 skill 对应表

| 询问方式（用户常说的词） | 子 skill |
|------------------------|----------|
| **港股公司简介**、**港股公司介绍**、**00700 公司信息**、**腾讯控股 港股 介绍**、成立日期、注册资本、法人代表、主营业务 | `company-hk` |
| **港股估值**、**估值分析**、**市盈率/市净率/市销率**、**股息率**、**港股全市场估值分页**、PE TTM、PB、换手率 | `hk-valuatnanalyd` |
| **港股基础视图**、**港股一览**、**单票市值/总股本**、**主板/上市状态**、**关联 A 股代码**（与历史分页估值区分，要「当前视图」） | `hk-view` |
| **港股 K 线**、**港股日线/月线/季线/年线**、**00700 历史行情**、OHLC、前复权港股 | `hk-candlesticks` |

---

## 能力总览

| 子 skill | 说明 |
|----------|------|
| `company-hk` | 按 `trade_code`（如 `00700.HK`）查询港股公司介绍 |
| `hk-valuatnanalyd` | 分页查询港股估值分析；可选 `trade_code` 过滤单票，不传为全市场 |
| `hk-view` | 按 `hk_code` 查询单票基础视图（板块、上市状态、股本、市值、估值指标） |
| `hk-candlesticks` | 按 `trade_code` 查询日/月/季/年 K 线；`until_date` 必填，`since_date` 可选 |

---

## 子 skill 文档

各子目录内另有 `SKILL.md`，含接口路径、参数与响应字段说明；执行时以本目录 `run.py` 为准。
