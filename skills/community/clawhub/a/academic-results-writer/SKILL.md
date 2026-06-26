---
name: academic-results-writer
version: 1.2.1
description: "学术 Results 写作、修改与审计技能。根据统计输出、图表、caption 和草稿生成符合发表规范的 Results 段落。覆盖心理学、认知神经科学、睡眠与记忆、VR 实验、EEG/fMRI、心理测量、干预研究、问卷模型、元分析和质性研究等设计。默认输出中文，可选英文及特定期刊风格。支持 Target-paper Results Style Adaptation Mode 和来自 paper-results-reverse-engineer v3.0+ 的 Module H Writer Transfer Packet 集成。"
metadata:
  emoji: "✍️"
  version: "1.2.1"
  internal_version: "academic-results-writer-v1.2.1-stable"
  scope: "academic writing; Results section; psychology and behavioral science"
  default_language: "Chinese"
  output_mode: "draft-first-with-audit; file-output-when-long-or-requested"
---

# Academic Results Writer (v1.2.1)

Forward-writing companion to `paper-results-reverse-engineer` v3.0:
- **reverse-engineer**: deconstructs published Results structure and writing patterns
- **academic-results-writer**: generates Results text from user data in publication-ready style

---

## 1. When to Use

Activate when the user asks to: write Results from statistics, revise a draft, convert tables/figures to Results text, audit Results for Discussion leakage/causal inflation/overclaiming, adapt to journal style (心理学报/APA), or reference a target paper's Results structure for their own writing.

## 2. Core Philosophy

1. Results is a reader-guided narrative, not a data dump.
2. Functions: restate aim → brief method reminder → overview trend → invite to figure/table → key result with statistics → restrained evaluative language → compare with predictions → limited implications.
3. Results can include limited interpretation but NOT full Discussion.
4. **Three-layer separation mandatory:** Result fact / Author-facing interpretation / Discussion material.
5. **Never fabricate any statistic, sample size, p-value, effect size, figure trend, or citation.**

## Supporting-File Loading Policy (Mandatory)

Before executing any task that references a `docs/` file, read the corresponding file. The condensed rules in this SKILL.md are summaries; the full validated rule set is in `docs/`.

**Docs reading table — read the file when the trigger condition is met:**

| Trigger | Read |
|---------|------|
| Write-from-statistics / any statistical template usage | `docs/statistical-templates.md` |
| Revise-draft / Revision Mode | `docs/revision-mode.md` |
| Figure-to-results / table-to-results / figure narrative | `docs/figure-table-templates.md` |
| Target-paper-style-adaptation | `docs/target-paper-adaptation.md` |
| Module H bridge workflow | `docs/module-h-bridge.md` |
| Meta-analysis Results writing | `docs/meta-analysis-guardrails.md` |
| Sleep EEG / memory / pre-post design Results | `docs/sleep-eeg-guardrails.md` |
| Journal-style (心理学报 / APA) | `docs/journal-style.md` |
| Full audit / file-output / completeness check / quality checklist | `docs/quality-checklist.md` |

**Fail-open rule:** If the required supporting file cannot be accessed, do NOT claim the full detailed rule set was applied. Continue with the condensed SKILL.md rules and explicitly report: `supporting-file unavailable; condensed-rule mode used`.

## 3. Inputs

| Type | Examples |
|------|----------|
| Structured statistics | N, M, SD, SE, CI, r, t, F, β, b, χ², Hedges' g, OR, RR, fit indices, EEG/fMRI/behavioral/VR outputs, qualitative themes |
| Figures / Tables | Screenshots, captions, table content, user-described trends, v3.0 Module D output |
| Rough drafts | User-written Chinese/English/mixed Results drafts |
| v3.0 upstream | Study Profile, Module B/C/D/E from reverse-engineer |
| Target paper | PDF, Results section, captions, figures, v3.0 Module H |

## 4. Default Output Format

Default: Chinese, standard-depth.

1. 【结果组织建议】
2. 【可直接使用的结果段】
3. 【关键统计报告检查】
4. 【结果与讨论边界提醒】
5. 【可选替代表达】

Full audit-depth (detailed checklist, Source Ledger) only on explicit request.

### 4.1 File-Output Mode

Auto-activates when output is long (>1800-2500 Chinese characters, or target-paper 8-section, or Module H bridge, or design-incompatible fallback, or previous truncation).

Output path: `~/Desktop/OpenClaw_Paper_Analysis/outputs_md/results_writer/{FirstAuthor}_{Year}_{ShortName}_Results_Adaptation.md`

Chat shows only: path + 3-5 core findings + self-check + manual review items. Never paste full long text into chat.

**File completeness check:** No `...(truncated)...`, no `TODO`/`待补充`/`[填写]`, all requested sections present. If check fails, patch once; if still failing, report failure in chat.

Full specification: `docs/quality-checklist.md`

## 5. Task Router

| User Says | Task Type |
|-----------|-----------|
| "根据统计结果写 Results" | `write-from-statistics` |
| "润色/修改这段结果" | `revise-draft` |
| "根据这张表/图写结果段" | `table-to-results` / `figure-to-results` |
| "检查结果部分有没有问题" | `audit-only` |
| "改成心理学报/APA 风格" | `journal-style` |
| "参考这篇论文的 Results 写法" | `target-paper-style-adaptation` |

**Workflow:** Identify task type → Build Results plan → Write → Audit before final answer.

## 6. Statistical Reporting — Key Guardrails

Templates for all analysis types are in `docs/statistical-templates.md`. Key guardrails:

- **Correlation ≠ causation.** Never write "X 影响 Y" for correlational results.
- **Non-significant ≠ no difference.** Never write "证明两组相同" for p > .05.
- **Cross-sectional mediation:** All direct/indirect/total effects must carry "统计" prefix (统计总效应/统计直接效应/统计间接效应). Hard self-check.
- **Bootstrap count:** Never auto-fill 5000/10000 unless user provides the count.
- **Proportion mediated:** Never write "相当部分/很大一部分/主要通过" unless user provides the proportion.
- **ANOVA derived marginal means:** If user only provides cell means, never write estimated marginal M without annotation.
- **LMM dummy-coding:** Lower-order coefficients must be interpreted per reference level, not as generic "main effects."
- **p > .05–.10:** "approached significance / 接近但未达到传统显著性水平" — never "no change" or "did not differ."
- **No "predicted/as expected"** unless user explicitly provides hypothesis direction.
- **Figure error bars:** Strictly distinguish SD/SE/CI. Never write "标准差参见图" when caption says ±1 SE.
- **No visual judgment** without actual image screenshot. Use "根据用户提供的均值" not "从图中可以明显看出".
- **Variable translation fidelity:** self-esteem → 自尊, depressive symptoms → 抑郁症状 (not 抑郁/抑郁症). Consistent throughout.
- **p-value format:** Never mix `p = .021` and `p = 0.021` in same output.

**Meta-analysis hard-self-check guardrails (output auto-fails if violated):**
- No "校正后效应仍显著" without p-value for adjusted effect
- No "结果稳健/结论稳定" when I² ≥ 50%
- No "Q 检验显著，因此选择随机效应模型"

Full meta-analysis rules: `docs/meta-analysis-guardrails.md`

**Sleep EEG guardrails:**
- No "睡眠促进/巩固/导致" without wake/sleep control design
- No "仅出现在/不存在于" for EEG-behavior correlation differences without Fisher z comparison context
- Default pre-post wording: "睡前至睡后行为变化" not "睡后记忆提升"

Full sleep/EEG rules: `docs/sleep-eeg-guardrails.md`

## 7. Writing Templates

Chinese: `docs/writing-templates.md` — overall trend, figure/table invitation, key result, non-significant, marginal significance, limited implication sentences.

English: `docs/writing-templates.md` — APA-style templates for all common scenarios.

## 8. Figure/Table Narrative

Core rules: don't just say "see Figure X"; first state question, then structure, then key pattern, then statistical support. Never fabricate statistical values invisible from figure. Full specification: `docs/figure-table-templates.md`

## 9. Results vs Discussion Boundary

**Allowed in Results:** Result trends, statistical evidence, direct comparison with hypotheses, limited interpretation, brief implications, minimal limitation notes.

**Belongs in Discussion:** Extended theory, long literature comparison, mechanism inference, practice recommendations, full future research plans, causal claims beyond data.

## 10. Certainty Continuum

| Strength | English | 中文 |
|----------|---------|------|
| Strongest | demonstrates / shows | 表明 / 显示 |
| Moderate | suggests | 提示 |
| Weaker | appears to | 可能提示 |
| Tentative | may suggest | — |
| Cautious | is consistent with | 与……一致 |
| Weakest | raises the possibility that | 提供了初步证据 |

- Experimental/RCT: stronger wording allowed, with operationalization boundaries
- Cross-sectional/correlational: only "相关/关联/预测/提示"
- Mediation models: NOT real causal mechanisms
- Qualitative: "参与者叙述显示/研究者解释为"

## 11. Do-Not Rules (Core)

See Failure Modes table below for full list. Most unique / frequently violated:

- ❌ Never fabricate statistics / add unsolicited significance / carry over previous test data (context-carryover hallucination).
- ❌ Never write correlation as causation / p > .05 as "proven no effect" / drop "统计" prefix from cross-sectional mediation.
- ❌ Never mix p-value formats in same output / auto-fill bootstrap count / write visual judgment without actual image.
- ❌ Never use target paper statistics/conclusions/sentences as user data; never claim adaptation without accessible target.
- ❌ Never claim "robust" for meta-analysis with I² ≥ 50% / write "Q-test significant → therefore random-effects."
- ❌ Never write "sleep-enhanced/consolidated" without control design.
- ❌ Never overload chat with full long output → file-output mode; never omit sections to avoid truncation.
- ❌ Never ignore Module H H7 risk flags or H8 recommended mode.

## 12. Failure Modes

| # | Failure | Description |
|---|---------|-------------|
| 1 | Statistical hallucination | Fabricating statistics |
| 2 | Over-claiming | Exaggerating results |
| 3 | Discussion leakage | Discussion content in Results |
| 4 | Causal inflation | Correlation written as causation |
| 5 | Null-result misuse | Non-significant written as "proven no difference" |
| 6 | Figure misreading | Misreading charts |
| 7 | Template mismatch | Wrong template for analysis type |
| 8 | Journal-style mismatch | Ignoring target journal format |
| 9 | Over-polishing | Sacrificing accuracy for style |
| 10 | Missing main result | Only auxiliary analyses reported |
| 11 | Unclear hierarchy | Main vs auxiliary mixed |
| 12 | Unsupported implication | Implications without data support |
| 13 | Context-carryover hallucination | Previous test data leaking into current revision |
| 14 | Target-paper over-imitation | Copying original sentences, data, or conclusions |
| 15 | Design-mismatch transfer | Forcing incompatible structure (fMRI → survey) |
| 16 | Target-data contamination | Target paper statistics written as user results |
| 17 | Target-paper risk replication | Replicating target paper's reporting errors |
| 18 | Target-metadata hallucination | Inferring target metadata from domain knowledge |
| 19 | Target-source collapse | Mistaking user data/draft for target paper |
| 20 | Missing-target false adaptation | Claiming adaptation without accessible target |
| 21 | Remote-source ambiguity | web_fetch without reporting source/coverage |
| 22 | Partial-extraction overclaim | Claiming full extraction on partial read |
| 23 | Design-incompatible overtransfer | Presenting incompatible target as driving structure |
| 24 | Test-context carryover | Internal test names in formal output |
| 25 | Chat truncation loss | Sections lost due to chat truncation |
| 26 | False complete after truncation | Claiming complete after truncation |
| 27 | File-output omission | Missing sections in file-output |
| 28 | File-output echo | Pasting full file content back to chat |

## 13. Quality Checklist (Summary)

Before final output, verify: statistics from user input, no missing df/p/CI/ES, no fabricated values, no Discussion leakage, no causal inflation, no "proven no effect" for non-significance, target journal format respected, figure/table narrative clear. Full checklist: `docs/quality-checklist.md`

## 14. Integration with paper-results-reverse-engineer v3.0

When v3.0 output provided: Study Profile → design/variables; Module B → organization; Module C → stats patterns; Module D → figure narrative; Module E → boundary patterns. **Risk Flag Rule:** flagged errors/contradictions must NOT be replicated. Write: "目标文献该部分存在报告风险，不建议迁移。"

Full spec: `docs/module-h-bridge.md`, `docs/target-paper-adaptation.md`.

## 15. Module H Bridge Workflow

When input contains Module H Writer Transfer Packet, use it as primary target-style source:

| H Field | Maps To |
|---------|---------|
| H1 | Source Ledger + extraction coverage |
| H2 | Design-match judgment |
| H3–H5 | Results organization + paragraph/figure/table narrative |
| H6 | Results–Discussion boundary |
| H7 | Risk flags → "Do not transfer" |
| H8 | Writer mode / output depth selection |

Prefer Module H over full A–G. Never copy H wording directly into Results. If H8 says design-incompatible, never force normal adaptation. Full spec: `docs/module-h-bridge.md`.

## 16. Journal-Specific Style

**心理学报:** Chinese, `p = 0.001` format, restrained tone, "结果表明" preferred.

**APA 7th:** English, `p = .001` format, effect sizes mandatory.

**Format consistency rule:** Never mix `p = .021` and `p = 0.021` in same output.

Full specification: `docs/journal-style.md`

## 17. Revision Mode

Workflow: Assess draft → mark statistics/boundary/wording issues → provide revised version → annotate changes with reasons.

### Output Format

**1. 【草稿评估】**
- **优点：** what the draft does well (clear structure, correct stat reporting pattern, etc.)
- **统计报告问题：** missing df / CI / ES, p-value precision, fabricated values, wrong stat translation
- **Results–Discussion 边界问题：** Discussion leakage, causal inflation, over-interpretation
- **措辞 / 因果语言问题：** "证明"/"导致" on correlational data, overclaiming, missing cautionary language

**2. 【修订版】**
- Directly replaceable Results paragraph(s)
- 不自动补入本轮未提供的统计值 — leave placeholders or mark as "需补充"
- 不把教学性提醒写进正式 Results 正文 — keep teaching notes in【修改说明】or【边界提醒】

**3. 【修改说明】**
- 按句或按问题说明修改原因
- 标注哪些内容建议移到 Discussion
- 标注哪些统计值本轮未提供、需用户确认 (category B/C)

**Source-boundary rule:** Only add statistics from current round's user input or draft; never carry over from previous rounds/memory. Missing statistics → report as "本轮未提供" (category B) or "需用户确认" (category C).

**Null-result warnings** default to【统计报告检查】/【修改说明】, not formal Results text.

**File-output:** If revision is long or full audit is needed, switch to file-output mode (§4.1).

Full specification: `docs/revision-mode.md`

## 18. Target-Paper Results Style Adaptation Mode

**Core principle:** structure/style modeling, NOT content imitation.

**Gating Rule:** 8-section output ONLY when target accessible + ≥3 specific evidence points extracted. Otherwise → fallback: Source Ledger status + reason + standard Results.

**Must:** Source Ledger mandatory, design-match check, write user Results from user data only, fail-closed on missing target.
**Must NOT:** copy sentences/data/conclusions/style from target; infer metadata; force incompatible structures.

Full specification (all 19 subsections): `docs/target-paper-adaptation.md`. See also §19 Source Integrity.

## 19. Source Integrity & Anti-Plagiarism

1. Transfer organization logic only — never copy original sentences
2. Reference reporting order only — never copy target statistics
3. Adapt figure narrative approach only — never copy figure interpretations
4. Never write target's theoretical interpretations or conclusions into user Results
5. Never mimic author-specific personal writing style
6. Write "参考目标文献的 Results 结构" not "模仿作者写法"
7. Incompatible design → must state non-transferable
8. "尽量像原文一样写" → "保留相似结构和语气，但使用全新表述和用户自己的数据"
9. Never generate near-substitute paragraphs that could replace target paper

## 20. Example Usage

See `examples/` for: write-from-anova, revise-draft, figure-to-results, target-paper-adaptation, module-h-bridge.

---

> **Public version:** 1.2.1 | **Internal version:** academic-results-writer-v1.2.1-stable
> **Scope:** Academic Results section writing for psychology and behavioral science
> **Default:** Chinese output, standard-depth, file-output when long
> **Key features:** Target-paper Results Style Adaptation Mode, Module H bridge workflow, anti-plagiarism guardrails, design-incompatible fallback, hard-self-check meta-analysis and EEG guardrails
> **Documentation:** `docs/` for full specifications, `examples/` for usage examples, `CHANGELOG.md` for version history
