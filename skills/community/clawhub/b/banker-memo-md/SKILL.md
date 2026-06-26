---
name: banker-memo-md
description: Produce an investment-banker-grade research memo (analysis.md + data-provenance.md) from CN raw-data/ JSON snapshots. Use when the user asks for "投行 md" / "银行家级分析 md" / "banker memo markdown" on an A-share, H-share, or non-listed CN company that has raw-data/ populated by cn-client-investigation Phase 3.5. This is STEP 1 of 2 in the banker pipeline — pair with banker-slides-pptx for the deck.
---

# Banker Memo (MD)

Step 1 of the banker pipeline: **raw-data/ → analysis.md + data-provenance.md**.

This skill is the **prompt** that drives the agent to write a banker-grade research memo. It does not generate slides or run gates — those belong to `banker-slides-pptx` and `validate-delivery.py` respectively.

## Pipeline position

```
┌────────────────────┐     ┌──────────────────┐     ┌────────────────────┐
│  Phase 3.5 raw-data│ ──▶ │  banker-memo-md  │ ──▶ │ banker-slides-pptx │
│  (cn-client-inv.)  │     │  (THIS SKILL)    │     │  (step 2)          │
│  → raw-data/*.json │     │  → analysis.md   │     │  → slides-outline  │
│                    │     │  → provenance.md │     │  → .pptx           │
└────────────────────┘     └──────────────────┘     └────────────────────┘
```

## Why split from the deck skill

Earlier `banker-memo` bundled both MD + outline generation in one prompt. Problems:
- Outline was an afterthought — agent ran out of attention budget
- MD prompt constraints (8 sections, peer benchmarking, SOTP) got diluted by "also design 12 slides"
- Impossible to iterate on MD quality without re-running the slide outline

Splitting lets each prompt focus:
- This skill: **pure research discipline** — 8-section framework, data flags, 4C's credit view, specific [EST] tagging
- `banker-slides-pptx`: **pure visual design** — structured layout schema the renderer can parse into real pptxgenjs tables/charts

## Prompt template

Canonical prompt at `references/banker_memo_md_prompt.md`. Placeholders:
- `{ts_code}`, `{name_cn}`, `{industry}` — target identifiers
- `{raw_dir}` — path to `raw-data/` holding MCP JSON snapshots
- `{out_dir}` — where to write analysis.md + data-provenance.md
- `{file_list}` — auto-discovered raw-data files
- `{uscc}` — unified social credit code from PrimeMatrix filename

Build the prompt via `scripts/build_md_prompt.py`.

## Framework enforced by the prompt

### 1. Executive Summary (300-500 字)
- **一句话核心观点** (thesis) + 3 supporting bullets
- **授信 / 投资建议** (specific 额度 + 期限 + 利率 OR Buy/Hold/Sell + 目标价)
- 1-2 **关键风险**

### 2. Company Profile
- 沿革 (成立 + 上市 + 经营期限)
- 主业拆解 (industry field 展开到 sub-segments)
- 股权与资本结构 (注册资本 + 股本 + 市值 + 法人)

### 3. Industry Dynamics
- 赛道特征 (cyclicality, tech shifts, policy drivers)
- 中国位置 (份额估算, 以 [EST, per sector consensus] 标注)
- 主要对手 3-5 家 (国内 + 海外, 每家标 [EST])
- 政策驱动 (十四五 / 专项补贴 / 产业政策)

### 4. Financial Deep-Dive **(表格为主)**
- 3Y 年度对比表 (营收 / 净利 / ROE / 毛利率 / 资产负债率 + YoY)
- 季度趋势 (YTD 累积 cumulative fields 展开)
- **异常 flag** (QoQ 跳变 > 5pp 必须点出)
- **数据口径 flag** (若 income 反推 vs company_performance 不一致, 必须指出)

### 5. Peer Comparison
- 3-5 家同业表 (公司 / 代码 / 市值 / PE / PB / ROE + 备注)
- 每个 peer 数字**必须**标 `[EST, per sector consensus]` 或 `[未核实]`
- 禁用 Wind / 同花顺 / 万得 / 彭博作为来源
- 相对估值分位 (target PE vs peer median)

### 6. Valuation
- 当前 PE/PB/PS (from daily_basic)
- 历史区间 (PB 历史 min-max, 是否破净)
- **SOTP** 分部估值 (成熟业务 PB / 成长业务 PS 等)
- **3 档目标价**: 悲观 / 基础 / 乐观 + 假设 + 空间

### 7. Risk Factors
- **表格**: 经营 / 财务 / 行业 / 治理 / 数据 5 类
- 每项有量化依据 + 严重程度 (高 / 中 / 低)

### 8. Credit / Investment View
**信贷口径 (4C's)**:
- **Character**: 国资背景 / 实控人稳定 / 治理透明度
- **Capacity**: 营收规模 + 偿债能力指标
- **Capital**: 注册资本 + 净资产结构
- **Collateral**: 抵押物 specialised 程度 + 清算折价

**具体授信建议**: 额度区间 + 期限 + 利率 (LPR+bp) + 增信要求 + 财务承诺

**投资口径**: Buy / Hold / Sell + 目标价 + 催化剂 + 反向风险

## Hard constraints (enforced by prompt, checked by gates)

1. **每个硬数字必须溯源**: `X 亿元（src: income）` 或 `Y%（src: company_performance）`
2. **禁用 Wind / 万得 / 同花顺 / Bloomberg / 彭博** — 这些不是安装的 MCP, `source_authenticity_check` gate 会拦截
3. **不写模糊数字** — "约 XX 亿" / "大约" 必须加 `[EST]` + 推理依据
4. **Q4 单季变化用 pp 单位** — `+3.18pp` 不要 `%` (避开 HARD_NUMBER 误判)
5. **Peer 数字必须标 `[EST, per sector consensus]`** — 永远不能挂一个权威名称
6. **Data Flag 自审** — 若发现 income 反推 vs company_performance 净利率差异 > 0.3pp, 必须单独一段 `> Data Flag N:` 提示需要人工核实

## Output files

Writes **only two files** to `{out_dir}/`:
1. `analysis.md` — 2500-4500 字 8 节 memo
2. `data-provenance.md` — 每个硬数字一行: `| 指标 | 数值 | 单位 | 来源文件 stem | MCP tool |`

**Not** slides-outline.md — that's the `banker-slides-pptx` skill's job.

## Usage

```bash
# Pre-flight: raw-data/ already populated by cn-client-investigation Phase 3.5
ls <deliverable_dir>/raw-data/*.json

# Build + dispatch prompt
python3 scripts/build_md_prompt.py <ts_code> <name_cn> <industry> \
        <raw_dir> <out_dir> > /tmp/prompt.md
openclaw agent --agent main --thinking high --json --timeout 600 \
        --message "$(cat /tmp/prompt.md)"

# Agent writes analysis.md + data-provenance.md

# Close any discipline gaps (agent's own provenance table sometimes misses
# numbers it wrote into prose; this post-process bridges the last mile)
python3 <cn-ci-scripts>/sync_provenance.py <out_dir>

# Now hand off to banker-slides-pptx for Step 2
```

## Quality checklist

- [ ] 8 sections all present (ES / Profile / Industry / Financial / Peer / Valuation / Risk / 4C's)
- [ ] Every `\d+(亿元|%|元|倍)` in analysis.md has a provenance row (or `[EST]` tag)
- [ ] Peer comparison has ≥3 companies, all tagged `[EST, per sector consensus]`
- [ ] Valuation section has ≥2 methods (relative + SOTP or DCF) + 3 scenarios
- [ ] Risk section is a **table** with severity levels (not a bullet list)
- [ ] 4C's section gives a specific credit conclusion (额度 + 期限 + 利率 + 增信 + 财务承诺)
- [ ] At least 1 `> Data Flag N:` self-audit paragraph (if income vs company_performance diverge)
- [ ] `provenance_verify.py` PASS + `source_authenticity_check.py` PASS
