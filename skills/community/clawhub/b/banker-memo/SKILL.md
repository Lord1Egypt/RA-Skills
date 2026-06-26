---
name: banker-memo
description: Generate an investment-banker-grade research memo (analysis.md + slides-outline.md + data-provenance.md) from CN raw-data/ snapshots. Use when the user asks for "银行家级分析" / "投行研报" / "banker memo" / "投行级 PPT 蓝图" on an A-share, H-share, or non-listed CN company that already has raw-data/ populated by cn-client-investigation Phase 3.5.
---

# Banker Memo

Banker-grade research memo from raw-data/ snapshots — **prompt-driven, not template-driven**.

## What this skill does

Takes a deliverable dir that already has `raw-data/*.json` (produced by the CN Phase 3.5 pipeline) and **drives an agent through a senior sell-side analyst framework** to produce:

1. `analysis.md` — 8-section banker research memo (2500-4000 words, peer-benchmarked, with explicit data flags)
2. `slides-outline.md` — PPT blueprint (10-15 slides, content-driven — NOT a fixed 8-slide template)
3. `data-provenance.md` — every hard number traceable to a raw-data filename stem

## Why prompt-driven (not Python template)

The 0.9.4-era `build_deck.py` used an 8-slide Python template that stamped the same structure onto every company. Problem: the result is a **data dashboard**, not banker analysis — no industry context, no peer benchmarking, no SOTP reasoning, no "4C's" credit framework, no banker opinion.

Prompt-driven flips this: the agent (which has read thousands of real sell-side reports during training) writes the narrative; the Python layer only does orchestration (dispatch + gate audit).

## Best-fit cases

- User explicitly asks for 投行级 / banker-grade research
- Deliverable already has `raw-data/` from `cn-client-investigation` Phase 3.5
- Target is CN (A-share / H-share / non-listed with unified social credit code)
- The previous Python-templated output felt shallow / repetitive / stat-card-heavy

## When NOT to use

- raw-data/ is missing — run cn-client-investigation Phase 3.5 first
- Target is US-listed — this skill is CN-focused (industry framework / 4C's assume CN credit context)
- Just want a quick fact-sheet — use `strip-profile` skill instead

## Workflow

### Step 1 — Pre-flight
Verify `raw-data/` has:
- At least one `aigroup-market-mcp-*.json` file (for listed) OR a `primematrix-basic_info.json` (for non-listed).
- Listed companies SHOULD have 5 Tushare files (basic_info / company_performance / stock_data / daily_basic / income) for the full framework.

### Step 2 — Build parameterised prompt
Use `references/banker_prompt_template.md` and substitute placeholders:
- `{ts_code}` / `{name_cn}` / `{industry}` / `{raw_dir}` / `{out_dir}`
- `{file_list}` — discovered from `raw_dir`
- `{uscc}` — parsed from the primematrix filename prefix

A helper `scripts/build_banker_prompt.py` does this. See `references/banker_prompt_template.md` for the canonical prompt body.

### Step 3 — Dispatch agent
Run `openclaw agent --agent main --thinking high --json --timeout 600 --message "$(cat prompt.md)"`. Typical runtime 3-6 minutes per company with high-thinking.

### Step 4 — Validate output
Run the standard 7-gate `validate-delivery.py --strict-mcp` on the output dir. The banker memo obeys the same authenticity / provenance rules as Python-templated outputs — gates unchanged.

### Step 5 — PPT compile
Run `build_deck.py` (v0.9.6+) which now reads `slides-outline.md` for layout cues. Slide count = whatever the agent planned (10-15 typical, not a fixed 8).

## Hard constraints enforced by the prompt

1. Every hard number cites a raw-data filename stem, format `X 亿元（src: income）` or `Y%（src: company_performance）`
2. Wind / 万得 / 同花顺 / Bloomberg / 彭博 forbidden (redundant with `source_authenticity_check` gate)
3. No vague numbers — "XX 亿元左右" / "大约" / "估计" must be tagged `[EST]` with reasoning
4. QoQ deltas in `pp` units (avoids HARD_NUMBER regex false-positives)
5. Peer comparison numbers tagged `[EST, per sector consensus]` — never tied to a specific forbidden source

## Worked example (0.9.5 smoke test)

BOE 000725.SZ run on 2026-04-20:
- Input: `~/deliverables/bj-smoke-v2/000725_sz/raw-data/` (6 JSON files already fetched)
- Agent high-thinking runtime: ~5 minutes
- Output analysis.md: 14.8 KB (vs 1.6 KB from v0.9.5 Python template)
- Agent self-flagged `Data Flag 1`: income-derived 净利率 2.68% vs company_performance 2.09% — 0.59pp口径差异 → must verify pre-credit decision
- Agent self-flagged `Data Flag 2`: company_performance YTD 累积 ≠ Q4 单季, computed +0.74pp Q4 NPM change from diff
- Peer comp: 5 companies (TCL 科技 / 维信诺 / LG Display / 群创光电) all tagged `[EST, per sector consensus]`
- Valuation: SOTP (LCD PB 0.8-1.0x + OLED PS 1.0-1.5x) → 合理 PB 1.0-1.3x; target price 3 scenarios (3.5-4.0 / 4.2-4.5 / 5.0-5.5)
- Credit view: 4C's with specific numbers + 授信额度 50-80 亿 / 期限 1 年 / 利率 LPR+60-130bp / 增信要求 (设备抵押 60% + 应收质押 70%) / 财务承诺 (负债率<55%, 利息覆盖>2x)
- Slides outline: 12 slides (not fixed 8) — includes section dividers + bar chart (revenue/profit) + line chart (quarterly ROE) + valuation scenario table + 4-color risk card
- `validate-delivery --strict-mcp` — all applicable gates PASS

## Output standard

| File | What it is | Audit gate |
|------|-----------|-----------|
| `analysis.md` | 8-section banker memo | `provenance_verify` + `source_authenticity_check` |
| `slides-outline.md` | 10-15 slide blueprint with layout + key message per slide | consumed by `build_deck.py` |
| `data-provenance.md` | hard-number → raw-data stem mapping | `provenance_verify --strict` |

## Quality checklist

- [ ] 8 sections all present (ES / Profile / Industry / Financial / Peer / Valuation / Risk / 4C's)
- [ ] Every `\d+(亿元|%|元|倍)` in analysis.md has a provenance row
- [ ] Peer comparison has ≥3 companies, all tagged `[EST, per sector consensus]`
- [ ] Valuation section has ≥2 methods (relative + SOTP or DCF) + 3 scenarios
- [ ] Risk section uses a table with severity levels (not a bullet list)
- [ ] 4C's section gives a specific credit conclusion (额度 + 期限 + 利率 + 增信 + 财务承诺)
- [ ] `slides-outline.md` specifies layout type per slide (card / table / chart / divider)
- [ ] `validate-delivery.py --strict-mcp` OVERALL PASS
