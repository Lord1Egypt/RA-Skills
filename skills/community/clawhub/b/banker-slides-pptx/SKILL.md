---
name: banker-slides-pptx
description: Turn a banker-memo analysis.md + data-provenance.md into an investment-banker-craft .pptx (real tables, bar/line charts, risk heatmap, scenario grid — NOT paragraph dumps). Step 2 of 2 in the banker pipeline; pair with banker-memo-md for the MD step.
---

# Banker Slides PPTX

Step 2 of the banker pipeline: **analysis.md + data-provenance.md → slides-outline.md (structured) → .pptx with real banker visual primitives**.

## Pipeline position

```
banker-memo-md (Step 1) → analysis.md + data-provenance.md
                              │
                              ▼
                    banker-slides-pptx (THIS SKILL)
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
           slides-outline.md    (rendered by)
           (structured YAML     build_outline_deck_v2.py
            blocks per slide)        │
                                     ▼
                                   .pptx
```

## What makes this different from a generic "write some slides" prompt

Most LLM-written slide outlines are prose ("Slide 4: Key takeaway is X"). That's useless — the renderer can only emit a paragraph.

This skill forces the agent to write **structured layout data** the renderer can parse into real pptxgenjs primitives:

- `stat-cards` → `addShape` + big-number `addText` cards
- `3y-table` / `peer-table` / `scenario-table` → real `addTable()` with column widths + cell fill
- `bar-chart` / `line-chart` → real `addChart()` with X-axis + Y-series data
- `risk-heatmap` → 3×3 colored grid with risk items placed by (severity, likelihood)
- `callout-box` → full-width gold-bordered box + large-font verdict text

The prompt reads `analysis.md` already written by `banker-memo-md`, extracts the numbers, and emits structured outline blocks. The renderer does no LLM work — it's a deterministic layout emitter.

## Outline schema (what the agent writes)

Each slide uses a `## Slide N — <Title>` heading followed by `Layout:` + type-specific YAML-style fields.

### `cover`
```
## Slide 1 — Cover
Layout: cover
English-title: China Vanke Co., Ltd.
Chinese-subtitle: 万科A · 房地产开发 · 投行深度研究
Ticker: 000002.SZ
Date: 2026-04
```

### `divider` (section divider between parts)
```
## Slide N — Section Divider
Layout: divider
Chinese-title: 财务深度诊断
English-subtitle: Financial Deep-Dive
```

### `stat-cards` (3-4 big-number cards)
```
## Slide N — Executive Summary Stats
Layout: stat-cards
Cards:
- label: 2024 营收
  value: "3,431.76"
  unit: 亿元
- label: 归母净亏损
  value: "-494.78"
  unit: 亿元
  highlight: red
- label: ROE 2024
  value: "-21.82"
  unit: "%"
  highlight: red
- label: 资产负债率
  value: "73.66"
  unit: "%"
  highlight: amber
```

### `table` (3Y YoY / peer / any matrix)
```
## Slide N — 3Y Financial Trend
Layout: table
Headers: ["指标", "2022", "2023", "2024", "YoY 24v23"]
Rows:
- ["营收（亿元）", "5,038.4", "4,657.4", "3,431.8", "-26.3%"]
- ["归母净利（亿元）", "226.2", "67.7", "-494.8", "N/M"]
- ["ROE（%）", "9.45", "4.93", "-21.82", "-26.75pp"]
- ["毛利率（%）", "19.55", "15.31", "10.17", "-5.14pp"]
- ["资产负债率（%）", "76.14", "75.29", "73.66", "-1.63pp"]
Note: YoY 计算: 2024 值 - 2023 值
```

### `bar-chart` / `line-chart`
```
## Slide N — Revenue & Profit Trend
Layout: bar-chart
X-axis: ["2022", "2023", "2024"]
Y-series:
- name: 营收（亿元）
  values: [5038, 4657, 3432]
  color: "C9A84C"
- name: 归母净利（亿元）
  values: [226, 68, -495]
  color: "D4AF37"
Note: 营收 3 年 -32%，净利 2024 转负
```

### `risk-heatmap` (3×3 severity × likelihood)
```
## Slide N — Risk Heatmap
Layout: risk-heatmap
Risks:
- name: 存量减值压力
  severity: 高
  likelihood: 高
- name: 美元债重组
  severity: 高
  likelihood: 中
- name: 交付延期
  severity: 中
  likelihood: 中
- name: 数据口径风险
  severity: 中
  likelihood: 低
```

### `scenario-table` (valuation scenarios)
```
## Slide N — Valuation Scenarios
Layout: scenario-table
Scenarios:
- name: 悲观
  assumption: "PE 10x · EPS -4.48 → N/M; 2025 仍巨亏"
  target: "2.0 元"
  upside: "-49%"
  color: red
- name: 基础
  assumption: "化债方案落地 + 2025 净利回正"
  target: "3.0 元"
  upside: "-24%"
  color: amber
- name: 乐观
  assumption: "政府背书 + OLED 转型兑现（类比 BOE）"
  target: "5.5 元"
  upside: "+40%"
  color: green
```

### `callout-box` (large verdict stamp)
```
## Slide N — Credit View
Layout: callout-box
Title: 授信建议
Tags: ["拒绝承做", "Sell", "Target 2-3 元"]
Message: ROE -21.82% + 资产负债率 73.66% + 经营现金流持续失血（估算）+ 2025 多个项目公司贷款逾期 → 当前节点无法给予新增授信。深圳市政府化债方案落地前，仅密切关注，不入授信池。
```

### `bullets` (fallback, sparingly)
```
## Slide N — Key Points
Layout: bullets
Points:
- 论点 1 + 数据支撑 (src: ...)
- 论点 2
```

## Deck composition (required structure)

The prompt enforces this structure (12-15 slides typical):

1. **Cover** (1 slide)
2. **Executive Summary** (1 slide, `stat-cards` layout)
3. **Section Divider: Company** (1 slide, `divider`)
4. **Company Profile** (1 slide, `table`)
5. **Section Divider: Industry** (1 slide, `divider`)
6. **Industry Position** (1 slide, `bar-chart` or `table` with peer share)
7. **Section Divider: Financial** (1 slide, `divider`)
8. **3Y Trend** (1 slide, `table`)
9. **Profitability Chart** (1 slide, `bar-chart` or `line-chart`)
10. **Section Divider: Valuation & Risk** (1 slide, `divider`)
11. **Peer Comparison** (1 slide, `table`)
12. **Valuation Scenarios** (1 slide, `scenario-table`)
13. **Risk Heatmap** (1 slide, `risk-heatmap`)
14. **Credit / Investment View** (1 slide, `callout-box`)
15. **Data Sources** (1 slide, `bullets` listing raw-data files)

Agent may merge divider slides into adjacent content when narrative is tight, but target stays 13-15.

## Hard constraints

1. **Every number in outline must already be in analysis.md** — the renderer will run `slide_data_audit` against provenance; numbers not in provenance will fail the gate
2. **Use rounded banker notation for stat cards**: "3,431.76 亿元" → display as `"3,432"` + unit `"亿"` (the underlying analysis.md has the exact value; cards round for visual)
3. **Peer comp numbers stay `[EST]`** — the table cells for peer rows should include `[EST]` suffix in value string
4. **Chart Y-series values must be numeric** (not strings), color codes 6-char hex without `#`
5. **Heatmap severity/likelihood must be one of 高/中/低** — renderer maps to 3×3 grid

## Usage

```bash
# Pre-flight: analysis.md + data-provenance.md already written by banker-memo-md
ls <deliverable>/{analysis.md,data-provenance.md}

# Build + dispatch prompt
python3 scripts/build_pptx_prompt.py <deliverable> <ts_code> <name_cn> \
        <name_en> > /tmp/prompt.md
openclaw agent --agent main --thinking high --json --timeout 600 \
        --message "$(cat /tmp/prompt.md)"
# Agent writes slides-outline.md in the deliverable dir

# Render the deck
python3 scripts/build_outline_deck_v2.py <deliverable> <ts_code> <name_cn> <name_en>

# Validate
python3 <cn-ci-scripts>/sync_provenance.py <deliverable>
python3 <cn-ci-scripts>/validate-delivery.py --strict-mcp <deliverable>
```

## Quality checklist

- [ ] slides-outline.md has 12-15 slides
- [ ] Contains ≥1 each of: `stat-cards`, `table`, `bar-chart` or `line-chart`, `risk-heatmap`, `scenario-table`, `callout-box`
- [ ] NOT all `bullets` (that's the fallback layout — using it for > 2 slides means the prompt failed)
- [ ] All numbers traceable to provenance (slide_data_audit PASS)
- [ ] Compile passes cn_typo_scan
- [ ] Rendered .pptx has actual charts (not placeholders) when outline specifies `bar-chart` / `line-chart`
