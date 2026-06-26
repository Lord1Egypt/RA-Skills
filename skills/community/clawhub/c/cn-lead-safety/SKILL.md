---
name: cn-lead-safety
description: "Chinese-market client-intelligence safety layer for lead-discovery skills. Use for any lead-gen / customer-investigation output targeting a Chinese company (A股 / 港股 / 科创板 / 创业板 / 北交所 / 中概股 / Tushare / 巨潮 / 天眼查 / 企查查). Enforces UTF-8 literal Chinese text, lexicon lookup for recurring terms, tier-ordered data sources, inline source citations for every hard number, and no-fabrication on missing data. Pairs with the stable `aigroup-financial-services-openclaw` plugin's `cn-client-investigation` skill for downstream banker deliverables."
---

<!-- Derived from anthropics/financial-services-plugins under Apache-2.0. Lead-discovery adaptation by AIGroup, 2026-04-18. -->

# CN Lead Safety Skill

**中国大陆客户情报安全层 — 5 条 Rule**

Lead-discovery 产出的 markdown intelligence（`customer-investigation` / `key-account-briefing` / `client-initial-screening` 等）如果走中文输出，必须经过这 5 条 Rule。下游 banker workflow (`aigroup-financial-services-openclaw/datapack-builder` / `dcf-model`) 读取这份 intelligence 时，只会对自己生成的 MD 跑 provenance_verify — 上游 lead-discovery MD 的质量由本 skill 守门。

## Why this skill exists

2026-04-18 实测 MiniMax-M2.7 在 OpenClaw main agent 生成中文 markdown 时存在字符级 escape drift：
- 公司名典型 typo：寒武纪→宽厭谛79 / 营收→营收（偶发）/ 核心→校虚 / 净利→洁利 / 财务→贜务
- 硬数字（市值/营收/员工数）偶发缺 source citation → 下游无法 tracing

Lead-discovery 此前无此类防线。升级到 0.2.0 补上。

## 5 条 Mandatory Rules

### Rule 1 — UTF-8 literal over `\uXXXX`

中文字符**一律**以 UTF-8 literal 写入 markdown，**严禁** `\uXXXX` escape。

```markdown
✅ ## 贵州茅台经营概览
❌ ## \u8d35\u5dde\u8305\u53f0\u7ecf\u8425\u6982\u89c8
```

`write` / `edit` 工具原生支持中文，不需要 pre-encode。

### Rule 2 — Lexicon lookup for recurring terms

公司名 / 行业术语 / 财务指标 / 监管术语 等重复中文短语，从 **`aigroup-financial-services-openclaw`** 主包的 `cn-lexicon.js` lookup，不要让模型每次重新打字。

推荐的 cross-skill 查阅路径（主包已装在 macmini 上）：
```
~/.openclaw/extensions/aigroup-financial-services-openclaw/skills/cn-client-investigation/references/cn-lexicon.js
```

在 banker intelligence markdown 中，这些字段首选 lexicon 写法：
- Target 公司名（全称 / 简称 / ticker）— `LEXICON.company.*` + `LEXICON.industry_terms.consumer_brand.*` 等
- 财务条目（营业收入 / 归母净利润 / 扣非净利 / 毛利率 / 研发费用 / 经营现金流）— `LEXICON.finance.*`
- 监管 / 市场术语（A股 / 科创板 / 创业板 / 实际控制人 / 国资背景）— `LEXICON.cn_market.*`
- 投资评级（增持 / 中性 / 减持 / 买入 / 卖出）— `LEXICON.rating.*`

若你只产 markdown（不走 pptxgenjs slide JS），`require()` 不可用 — 则**读** lexicon.js 作为术语白名单在心中校对，不让模型自由造短语。

### Rule 3 — Tier-ordered data sources（跟 cn-client-investigation Rule 4 一致）

| Tier | 源 | Lead-discovery 常用入口 |
|------|-----|-----------------------|
| T1 | 巨潮资讯网 cninfo.com.cn / Tushare Pro | `web_fetch` cninfo PDF；`aigroup-market-mcp__basic_info / company_performance / stock_data` |
| T2 | 上交所/深交所/港交所官网；天眼查 / 企查查；国家信用 gsxt.gov.cn | `web_fetch` 官网；`aigroup-tianyancha-mcp`（如装）|
| T3 | Wind / 同花顺 / 东方财富；FMP / Finnhub（港股/中概股）| `aigroup-fmp-mcp / finnhub-mcp` |
| T4 | 财新 / 21世纪 / 中证 / 上证 / 财联社 / 澎湃 / 第一财经 | `brave-web-search` + `web_fetch` |

**按 tier 依次 try，不要跳级**。T1 失败 → 再 T2 / T3 / T4；只有 T1-T3 全空才用 T4 媒体信息且必须标 "单源报道"。

### Rule 4 — Inline source citation for every hard number

Lead-discovery intelligence MD 中每个硬数字（`digit + 亿/万/%/RMB/USD/元/CNY/HKD/M/B`）必须**内联**source citation，格式形如：

```markdown
✅ 2024 年前三季度营业收入 **1,088 亿元**（来源：巨潮资讯 2024 年三季报，2024-10-27；Tushare Pro income_all 校验）。

✅ 截至 2026-04-17 收盘总市值 **20,150 亿元**（来源：东方财富 Choice，2026-04-17 T+0；Tushare stock_data 同日对齐）。

❌ 公司 2024 Q3 营收 1,088 亿元，盈利能力持续增强。   ← 数字没 source，下游无法 tracing
```

`verify_intelligence.py` （本 skill 附带）会扫 MD，每个硬数字都要有**临近** "来源：" / "Source:" 或脚注引用，否则退回 exit 1。

### Rule 5 — No fabrication on missing data

T1-T4 都查不到或 MCP 返回权限错误（402/403）时：
- **DO**：标 `数据不可得` / `N/A（source unavailable）` + 简述尝试路径
- **DO NOT**：估算一个"合理数字"顶上

```markdown
✅ 2024 年员工数量：**数据不可得**（尝试路径：巨潮资讯年报未披露员工表、天眼查 MCP 返回 403）。
❌ 2024 年员工数量：约 5,000 人。   ← 无源凭空估算
```

## Phase 0: pre-flight (触发)

当 user input 或 target context 出现以下任一触发词，**先加载本 skill 的 5 条 Rule**，再选对应 lead-discovery skill（customer-investigation / client-initial-screening 等）开始工作：

- 市场/监管：中国 / A股 / 港股 / 科创板 / 创业板 / 北交所 / 中概股 / H股 / 证监会
- 源系统：巨潮资讯 / cninfo / Tushare / 天眼查 / 企查查 / Wind / 东方财富
- Ticker 形态：`*.SH` / `*.SZ` / `*.BJ` / `*.HK`
- 显式中文公司名（茅台 / 寒武纪 / 海光 / 华为 / 小米 / 美的 etc.）

## Phase 5: 交付前 QA

```bash
python3 ~/.openclaw/extensions/aigroup-lead-discovery-openclaw/skills/cn-lead-safety/scripts/verify_intelligence.py \
    path/to/intelligence.md
# exit 0 → clean；exit 1 → 有硬数字缺 citation
```

补 citation 后重跑。**不要** `--no-verify` 或类似 bypass —— 上游情报没 source，下游 banker 交付 provenance_verify 也救不了。

## What this skill does NOT do

- 不产 pptx（那是 financial-services 的 ppt-deliverable 范畴）
- 不跑 typo scan（那是 financial-services 的 cn_typo_scan.py 范畴；lead-discovery 只出 markdown，中文错字下游财服 skill 读到后会被 compile 阶段的 typo gate 拦）
- 不自己带 cn-lexicon 副本（主包有，跨插件引用）

## Output contract

每个 lead-discovery skill 的 markdown 输出必须：
1. 文件扩展名 `.md`，UTF-8 no BOM
2. 标题第一行 `# <中文公司名> — <intelligence 类型>`
3. 数据来源 section 标注 tier
4. 硬数字 100% 内联 source citation
5. 数据不可得处明确标 "N/A / 数据不可得"
6. `verify_intelligence.py` exit 0
