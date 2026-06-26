# Module H Bridge Workflow — Full Specification

Moved from main SKILL.md §16.1.

When user provides paper-results-reverse-engineer v3.0 output containing **Module H: Writer Transfer Packet**, academic-results-writer should use Module H as the primary target-style source.

## H1–H8 Mapping to academic-results-writer

| Module H Field | Maps To |
|---------------|---------|
| H1 Target Source Identity | Source Ledger and extraction coverage |
| H2 Study Design Transfer Summary | 【设计匹配与可迁移性判断】 |
| H3 Results Organization Template | 【适配到本文的结果组织方案】 |
| H4 Paragraph-Level Writing Pattern | Paragraph writing patterns (purpose → Figure → statistics → boundary) |
| H5 Figure/Table Narrative Pattern | Figure/table narrative strategy |
| H6 Results–Discussion Boundary | 【结果与讨论边界提醒】 |
| H7 Risk Flags | Mark as "Do not transfer" or "Transfer with caution" |
| H8 Recommended Writer Mode | standard-depth / full audit-depth / design-incompatible fallback |

## Rules

1. Prefer Module H over full Module A–G for style adaptation.
2. If Module H is missing or incomplete, fall back to Study Profile + Module B–E.
3. If H7 contains risk flags, mark corresponding elements as "Do not transfer" or "Transfer with caution."
4. **Never** copy Module H wording directly into final Results paragraphs; convert to new writing plan.
5. If H1 reports extraction coverage: partial, never claim complete target Results extraction.
6. If H8 recommends design-incompatible fallback, never force normal target-paper adaptation.

## File-Output Preference

Prefer file-output mode in Module H bridge workflows when:
- H8 recommends design-incompatible fallback
- H7 contains multiple risk flags
- User requests all target-paper output sections
- Output includes long tables
- Previous chat output was truncated

## Integration with paper-results-reverse-engineer v3.0

When user provides v3.0 output:
1. **Study Profile** → Extract study design, variables, analysis strategy
2. **Module B** → Extract Results organization logic and paragraph structure
3. **Module C** → Extract statistical reporting conventions and wording patterns
4. **Module D** → Extract figure/table narrative strategy
5. **Module E** → Extract Results–Discussion boundary patterns
6. Convert to user's own data writing strategy — NOT copy original text

**V3.0 Risk Flag Rule:** If v3.0 output has flagged target paper statistical errors, table contradictions, template pollution, or causal language overreach, academic-results-writer must NOT replicate these issues. Write: "目标文献该部分存在报告风险，不建议迁移；本文写作应采用更规范表述。"

**Key principle:** Reverse-engineering reveals "how they wrote it"; forward-writing answers "how you should write it." Don't apply others' wording to your data.
