# Capability: Final Synthesis

## Purpose

Generate the final debate report after all rounds complete. Produces both structured JSON (`final_report.json`) and bilingual Markdown (`debate_report.md`).

## Inputs

| Parameter | Required | Default | Description |
|---|---|---|---|
| workspace_dir | Yes | - | Path to debate workspace |

## Context Files to Read

1. `config.json` — debate configuration
2. `evidence/evidence_store.json` — all evidence items
3. `claims/claim_ledger.json` — all claims with final statuses
4. `rounds/round_*/pro_turn.json` — all Pro turns
5. `rounds/round_*/con_turn.json` — all Con turns
6. `rounds/round_*/judge_ruling.json` — all Judge rulings

## Execution Steps

### 1. Categorize Claims

Review all claims in the ledger and categorize:
- **verified_facts**: Claims with status=verified, cross-source confirmed
- **probable_conclusions**: High-confidence inferences based on verified facts
- **contested_points**: Claims with status=contested, with full context

### 2. Build Contested Points Detail

For each contested point:
```json
{
  "point": "Description of the contested claim",
  "claim_ids": ["clm_xxx", "clm_yyy"],
  "pro_position": "Pro's strongest argument with evidence summary",
  "con_position": "Con's strongest argument with evidence summary",
  "key_rebuttals": [...],
  "judge_assessment": "Neutral evaluation",
  "resolution_status": "unresolved | leaning_pro | leaning_con | partially_resolved"
}
```

### 3. Build Scenario Outlook

Synthesize from all rounds' speculative scenarios:
- **base_case**: Most likely scenario based on verified facts
- **upside_triggers**: Conditions that would improve outlook
- **downside_triggers**: Conditions that would worsen outlook
- **falsification_conditions**: What would invalidate the base case

### 4. Build 24-Hour Watchlist

Identify time-sensitive items to monitor:
- Each item: what to watch, what would trigger reversal, where to monitor

### 5. Evidence Diversity Assessment

Analyze the evidence pool:
- Source type distribution (web, academic, twitter, etc.)
- Credibility tier distribution
- Geographic diversity assessment
- Perspective balance assessment
- Generate diversity_warning if pool is skewed

### 6. Generate Conclusion Profiles (10 Dimensions)

For each major conclusion, build a profile using LLM semantic judgment:

| Dimension | Values |
|---|---|
| Probability | high (>70%) / medium (30-70%) / low (<30%) |
| Confidence | high / medium / low |
| Consensus | high / partial / low |
| Evidence Coverage | complete / partial / sparse |
| Reversibility | high / medium / low |
| Validity Window | hours / days / weeks / months / indefinite |
| Impact Magnitude | extreme / high / medium / low |
| Causal Clarity | clear_chain / partial_chain / correlation_only |
| Actionability | directly_actionable / informational / requires_more_data |
| Falsifiability | easily_testable / testable_with_effort / hard_to_test |

Each dimension includes a rationale explaining the judgment.

### 7. Build Decision Matrix

```json
{
  "dimensions": [
    {
      "factor": "Factor name",
      "pro_position": "...",
      "con_position": "...",
      "evidence_strength": "strong | moderate | weak",
      "judge_note": "..."
    }
  ],
  "overall_lean": "...",
  "key_uncertainty": "...",
  "recommendation": "..."
}
```

### 8. Build Executive Summary

One-paragraph summary covering:
- What was debated
- Key findings
- Overall assessment
- Top verified facts, contested points, and watchlist items

### 9. Historical Insights

Synthesize across all rounds:
- Key parallels
- Conflicting lessons
- Meta-pattern (if any)

### 10. Speculative Frontier

Collect best speculative scenarios from all rounds:
- Include judge quality assessment for each

### 11. Write final_report.json

Write to `reports/final_report.json` following FinalReport schema.
Validate with `scripts/validate-json.sh final_report.json final_report`.

### 12. Generate debate_report.md

Write bilingual Markdown report to `reports/debate_report.md` following the EXPLICIT format from Section 8 of the spec:

```markdown
# Debate Report: {Topic}

## Executive Summary
## Decision Matrix
## Verified Facts
## Contested Points
## Key Arguments by Round
## Scenario Outlook
## Watchlist
## Evidence Inventory
## Methodology

---

# Chinese Translation / 中文翻译
(Complete translation of ALL above sections in Chinese)
```

This format is EXPLICIT, not emergent. The report MUST match this structure.

### 12a. debate_report.md Detailed Table Formats

#### Decision Matrix Table
```markdown
| Factor / 因素 | Assessment / 评估 | Confidence / 置信度 | Key Evidence / 关键证据 |
|---|---|---|---|
| {factor_name} | {judge_assessment} | High/Medium/Low | {evidence_summary} |
```

#### Verified Facts Table
```markdown
| # | Fact / 事实 | Sources / 来源 | Confidence / 置信度 |
|---|---|---|---|
| 1 | {verified_claim_text} | {publisher1}, {publisher2} | High/Medium |
```

#### Contested Points Structure (per point)
```markdown
### {point_title}
- **Status / 状态**: {resolution_status}
- **Pro Position / 正方立场**: {pro_strongest_argument + evidence}
- **Con Position / 反方立场**: {con_strongest_argument + evidence}
- **Key Rebuttals / 关键反驳**: {most impactful rebuttals from both sides}
- **Judge Assessment / 裁判评估**: {neutral evaluation of which side has stronger support}
```

#### Scenario Outlook Table
```markdown
| Scenario / 情景 | Probability / 概率 | Impact / 影响 | Key Trigger / 关键触发 |
|---|---|---|---|
| Base case | High/Medium/Low | {scope} | {trigger_conditions} |
| Upside | ... | ... | ... |
| Downside | ... | ... | ... |
```

#### Watchlist Table
```markdown
| Item / 监控项 | Reversal Trigger / 反转触发 | Source / 监控来源 | Timeframe / 时间 |
|---|---|---|---|
| {what_to_watch} | {what_would_change_conclusions} | {where_to_monitor} | 24h/48h/1w |
```

#### Evidence Inventory Table
```markdown
| ID | Source | Type | Credibility | Track | Freshness | Discovered By | Round |
|---|---|---|---|---|---|---|---|
| evi_xxx | {publisher} | web/academic/twitter | tier1-4 | fact/reasoning | current/stale/timeless | orchestrator/pro/con | 0-N |
```

#### Conclusion Profiles (per conclusion)
```markdown
### Conclusion: {conclusion_text}
| Dimension / 维度 | Value / 值 | Rationale / 依据 |
|---|---|---|
| Probability | High/Medium/Low | {why} |
| Confidence | High/Medium/Low | {why} |
| Consensus | High/Partial/Low | {why} |
| Evidence Coverage | Complete/Partial/Sparse | {gaps} |
| Reversibility | High/Medium/Low | {reversal_trigger} |
| Validity Window | Hours/Days/Weeks/Months | {expiry_condition} |
| Impact Magnitude | Extreme/High/Medium/Low | {scope} |
| Causal Clarity | Clear/Partial/Correlation | {weakest_link} |
| Actionability | Actionable/Informational/Needs Data | {suggested_action} |
| Falsifiability | Easy/Effort/Hard | {test_method} |
```

## Completion Marker

Output `DONE:final_synthesis` when complete.
