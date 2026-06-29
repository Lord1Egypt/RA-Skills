---
name: a-share-daily-report
description: "A股每日复盘报告生成器。自动采集通达信+同花顺问财数据，生成含涨停复盘、题材分组、连板梯队、资金流向等25模块的HTML报告。触发词：'生成A股日报'、'A股复盘'、'今日复盘'"
trigger_phrases:
  - "生成A股日报"
  - "A股复盘"
  - "今日复盘"
  - "市场复盘"
  - "大盘复盘"
agent_created: true
---

# A股每日复盘报告 v6

## 前置依赖

安装本 Skill 前需确保以下工具可用：

1. **通达信 MCP 连接器** (`tdx-connector`)：提供 `tdx_quotes`（实时行情）和 `tdx_screener`（条件选股）工具
2. **同花顺问财 Skill** (`iwencai`)：提供自然语言金融数据查询，需配置 API Key
3. **Python 3.11+**：运行 generate.py 生成 HTML 报告

> ⚠️ 以上依赖缺一不可。通达信 MCP 用于行情/涨停/炸板/连板数据，问财用于板块/资金流/融资融券数据。

## 三大原则

1. **2轮并行取数**：第1轮通达信MCP全并行 → 第2轮问财全并行 → 运行脚本生成
2. **数据源优先级**：通达信MCP > 同花顺问财 > 东方财富妙想
3. **人气榜优先级**：同花顺问财 > 东方财富妙想
4. **用 generate.py 生成**：写JSON → 运行脚本 → 出报告

## A股配色
- 涨=红(#f85149) 跌=绿(#3fb950) 背景=深色(#0b0e11/#1a1e24)

## 执行流程

### Step 1：第1轮并行（通达信MCP，11个调用一次性全发）

| # | 工具 | 参数 | 目的 |
|---|------|------|------|
| 1 | tdx_quotes | code="000001" setcode="1" hasCalcInfo="1" | 上证行情+涨跌家数+成交额 |
| 2 | tdx_quotes | code="399001" setcode="0" hasCalcInfo="1" | 深证行情+涨跌家数+成交额 |
| 3 | tdx_quotes | code="399006" setcode="0" hasCalcInfo="1" | 创业板行情 |
| 4 | tdx_quotes | code="000688" setcode="1" hasCalcInfo="1" | 科创50行情 |
| 5 | tdx_screener | message="涨停" rang="AG" pageSize="200" | 涨停股+涨停原因+封成比+连板天数 |
| 6 | tdx_screener | message="炸板股" rang="AG" pageSize="200" | 炸板股列表 |
| 7 | tdx_screener | message="跌停" rang="AG" pageSize="50" | 跌停股列表 |
| 8 | tdx_screener | message="2连板" rang="AG" pageSize="50" | 2板详情 |
| 9 | tdx_screener | message="3连板" rang="AG" pageSize="20" | 3板详情 |
| 10 | tdx_screener | message="4连板" rang="AG" pageSize="10" | 4板详情 |
| 11 | tdx_screener | message="5连板及以上" rang="AG" pageSize="10" | 5板+详情 |

⚠️ 以上11个调用互相独立，**必须同一轮全部并行发出，禁止逐个串行！**

**首板数计算**：涨停总数 - 2连板数 - 3连板数 - 4连板数 - 5连板及以上数

### Step 2：第2轮并行（问财，12个调用一次性全发）

| # | 工具 | 查询内容 | 目的 |
|---|------|----------|------|
| 1a | iwencai | "今日A股同花顺二级行业涨幅前5的板块名称涨跌幅主力净流入" | 行业涨幅榜Top5(模块10) |
| 1b | iwencai | "今日A股同花顺二级行业跌幅最大的5个板块名称涨跌幅主力净流入" | 行业跌幅榜Top5(模块10) |
| 2 | iwencai | "今日A股成交额排名前10的股票代码名称涨跌幅成交额主力净流入换手率最新价" | 成交额排行(模块16) |
| 3 | iwencai | "今日A股人气排名前10的股票代码名称涨跌幅换手率量比总市值" | 人气龙头(模块4) |
| 4 | iwencai | "今日A股主力净流入前5和主力净流出前5的股票名称净流入额" | 资金风向(模块18) |
| 5 | iwencai | "今日A股跌幅前5的股票代码名称跌幅最新价主力净流出" | 跌幅榜(模块17) |
| 6 | iwencai | "今日A股同花顺二级行业主力净流入前5的板块名称涨跌幅主力净流入" | 行业净流入Top5 |
| 7 | iwencai | "今日A股同花顺二级行业主力净流出前5的板块名称涨跌幅主力净流入" | 行业净流出Top5 |
| 8 | iwencai | "今日A股概念板块主力净流入前5的板块名称涨跌幅主力净流入" | 概念净流入Top5 |
| 9 | iwencai | "今日A股概念板块主力净流出前5的板块名称涨跌幅主力净流入" | 概念净流出Top5 |
| 10 | iwencai | "今日A股地域板块主力净流入前5的板块名称涨跌幅主力净流入" | 地域净流入Top5 |
| 11 | iwencai | "今日A股地域板块主力净流出前5的板块名称涨跌幅主力净流入" | 地域净流出Top5 |
| 12 | iwencai | "沪深两市近5日融资余额融券余额融资融券余额日期" | 融资融券(模块21) |

⚠️ 以上12个调用互相独立，**必须同一轮全部并行发出！**
⚠️ 问财用"地域"而非"地区"查询地域板块数据。
⚠️ 行业查询必须用"同花顺二级行业"而非"行业板块"，否则会返回二级+三级行业混合数据，与同花顺APP不一致。
⚠️ 板块涨跌榜需拆成涨幅/跌幅两个独立查询，合并查询问财不支持。

### 融资融券数据

已合并至第2轮问财并行查询（#12），无需单独查询。取最新一日的数据填入 `margin` 字段，与前日对比计算变化。

### 涨跌家数修正（重要！）

⚠️ `tdx_quotes` 的 `TotalBuyv/TotalSellv/PreVolInStock` 字段**只统计沪深主板+中小板**，不含北交所等，数量偏少约200-300只。

**修正方案**：在第1轮取数后，用 `tdx_screener` 查询"全部A股"统计涨跌家数，或者用通达信APP的全市场数据直接填入 `total_adv/total_dec/total_flat` 字段。

```json
"advance_decline": {
  "sh_adv": 0, "sh_dec": 0, "sh_flat": 0,
  "sz_adv": 0, "sz_dec": 0, "sz_flat": 0,
  "total_adv": 0, "total_dec": 0, "total_flat": 0
}
```

- `sh_*`/`sz_*`：来自 tdx_quotes（分市场明细展示用）
- `total_*`：来自通达信APP全市场数据或问财查询（报告主数据用）
- generate.py 会优先用 `total_*`，fallback 到 sh+sz 合计

### Step 3：整理数据写入 report_data.json

将所有取到的数据整理为以下JSON格式，写入当前工作目录的 `report_data.json`：

```json
{
  "date": "YYYY-MM-DD",
  "weekday": "周X",
  "time_label": "收盘复盘",
  "time_cutoff": "15:00",
  "market_tag": "📈 深创领涨 沪指微调",
  "market_summary": "2654涨2505跌",
  "indices": {
    "sh": {"price": 0, "chg": 0},
    "sz": {"price": 0, "chg": 0},
    "cy": {"price": 0, "chg": 0},
    "kc": {"price": 0, "chg": 0}
  },
  "advance_decline": {
    "sh_adv": 0, "sh_dec": 0, "sh_flat": 0,
    "sz_adv": 0, "sz_dec": 0, "sz_flat": 0,
    "total_adv": 0, "total_dec": 0, "total_flat": 0
  },
  "total_amount": 0,
  "amount_change": "▲较昨日放量",
  "zt_total": 0,
  "fst_zt": 0,
  "st_zt": 0,
  "st_zt_detail": "ST X只 + *ST Y只",
  "ts_zt": 0,
  "zb_total": 0,
  "dt_total": 0,
  "st_dt": 0,
  "nonst_dt": 0,
  "seal_rate": 0,
  "cy_zt": 0,
  "kc_zt": 0,
  "lianban": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0},
  "lianban_detail": {
    "2": [{"name": "", "board_type": "", "reason": "", "concepts": ""}],
    "3": [], "4": [], "5": []
  },
  "zt_stocks": [{"code": "", "name": "", "chg": 0, "reason": "", "concepts": "", "board_type": "", "first_time": "", "seal_amount": 0, "seal_ratio": 0, "open_times": 0, "lianban_days": 0, "lianban_label": ""}],
  "zb_stocks": [{"code": "", "name": "", "chg": 0, "reason": "", "concepts": "", "open_times": 0}],
  "dt_stocks": [{"code": "", "name": "", "chg": 0, "is_st": false, "reason": "", "concepts": "", "board_type": "", "lianban_days": 0}],
  "sector_up": [{"name": "", "chg": 0, "flow": 0}],
  "sector_down": [{"name": "", "chg": 0, "flow": 0}],
  "renqi_top": [{"code": "", "name": "", "price": 0, "chg": 0, "turnover_rate": 0, "volume_ratio": 0, "market_cap": "", "tags": ""}],
  "turnover_top": [{"code": "", "name": "", "price": 0, "chg": 0, "amount": 0, "turnover_rate": 0, "flow": 0}],
  "fund_in": [{"name": "", "flow": 0}],
  "fund_out": [{"name": "", "flow": 0}],
  "decline_top": [{"code": "", "name": "", "chg": 0, "price": 0, "flow": 0, "risk": ""}],
  "margin": {
    "rz_balance": "", "rz_change": "",
    "rq_balance": "", "rq_change": "",
    "total": "", "total_change": "",
    "date": ""
  },
  "sector_flow": {
    "industry_in": [{"name": "", "flow": 0}],
    "industry_out": [{"name": "", "flow": 0}],
    "concept_in": [{"name": "", "flow": 0}],
    "concept_out": [{"name": "", "flow": 0}],
    "region_in": [{"name": "", "flow": 0}],
    "region_out": [{"name": "", "flow": 0}]
  },
  "data_sources": {
    "注释": "每个key对应一个模块，值为实际数据来源。generate.py的_DEFAULT_SOURCES有默认值，此处只需覆盖降级场景"
  }
}
```

> **⚠️ 数据量要求**：`zt_stocks`/`zb_stocks`/`dt_stocks` 必须存入**全部**个股数据，不要截断。generate.py 会按题材自动分组、全部展示。

> **⚠️ 字段映射（重要）**：通达信 `tdx_screener` 返回的 `涨停原因` 字段（短概念标签，点号分隔，如"PCB概念.锂电池概念"）→ 写入 `concepts`；`原因揭秘` 字段（详细叙事）→ 写入 `reason`。两者用途不同，不要混淆。

### Step 4：运行 generate.py

```bash
python generate.py report_data.json
```

脚本自动：读 template.html + report_data.json → 生成 a-share-report-YYYY-MM-DD.html

> **data_sources 字段说明**：每个模块的数据来源标签。当某个数据源降级（如问财失败改用东财），需将对应 key 的值改为实际来源（如 `"sector": "东方财富"`）。generate.py 会读取此字段自动在报告卡片上标注正确来源，未配置则使用默认值。

### Step 5：交付

使用 `present_files` 交付 HTML 文件。

## 涨停数据字段说明（通达信 tdx_screener）

| 字段 | 含义 | 用途 |
|------|------|------|
| sec_code / sec_name | 代码/名称 | 报告展示 |
| now_price / chg | 现价/涨跌幅 | 封板状态判断 |
| 封单金额0# | 封单金额(元) | 封板强度 |
| 首次涨停时间 | HH:MM:SS | 早盘/尾盘质量 |
| 涨停打开次数 | 整数 | 0=一字板 |
| 涨停原因 | 字符串 | 短概念标签，点号分隔，如"PCB概念.锂电池概念"→写入concepts字段，用于题材分组 |
| 原因揭秘 | 字符串 | 详细叙事归因，如"全球最大PPE树脂产区停产，PCB材料持续涨价；..."→写入reason字段，用于个股归因展示 |
| 板型 | 字符串 | 一字板/换手板/T字板 |
| 封成比 | 倍 | 封单金额/成交额 |
| 连续涨停天数 | 整数 | 连板天数 |
| 上市状态 | 字符串 | ST/*ST/退市 |

## 封板/炸板判断
- 涨停打开次数==0 且 chg达涨停幅度 → 一字板封板
- 涨停打开次数1-2 → T字板
- 涨停打开次数>2 → 换手板
- 创业板(300)/科创板(688)涨跌幅≥20% → 20cm涨停

## 文件路径
- **模板（锁定不可改）**：Skill目录下 `assets/template.html`
- **生成脚本**：Skill目录下 `scripts/generate.py`
- **数据文件**：`report_data.json`（当前工作目录，临时）
- **输出**：`a-share-report-YYYY-MM-DD.html`（当前工作目录）

## 25模块→数据源映射（与SECTION_MAP顺序一致）

| # | 模块 | 数据源 |
|---|------|--------|
| 1 | Header | 计算 |
| 2 | 4指数卡片 | tdx_quotes |
| 3 | 涨跌家数 | tdx_quotes(hasCalcInfo) + 通达信APP全市场数据修正 |
| 4 | 人气龙头Top10 | iwencai |
| 5 | 涨停封板率 | tdx_screener |
| 6 | 跌停专题 | tdx_screener |
| 7 | 短线情绪全景 | tdx_screener计算 |
| 8 | 情绪监测 | tdx_screener计算 |
| 9 | 连板天梯 | tdx_screener |
| 10 | 板块涨跌榜 | iwencai(同花顺二级行业) |
| 11 | 主线分析 | tdx_screener涨停原因聚合 |
| 12 | 核心个股筛选 | tdx_screener计算 |
| 13 | 涨停复盘 | tdx_screener涨停详细 |
| 14 | 炸板分析 | tdx_screener炸板详细 |
| 15 | 短线策略 | 数据驱动生成 |
| 16 | 行情展望 | 数据驱动生成 |
| 17 | 成交额排行 | iwencai |
| 18 | 跌幅榜 | iwencai |
| 19 | 资金风向 | iwencai |
| 20 | 板块主力资金流向 | iwencai（同花顺二级行业/概念/地域各净流入+净流出Top5） |
| 21 | 个股跟踪 | tdx_screener |
| 22 | 投资策略&心态 | 数据驱动生成 |
| 23 | 特殊事件 | 涨停原因提炼 |
| 24 | 融资融券 | iwencai |
| 25 | Footer | 计算 |
