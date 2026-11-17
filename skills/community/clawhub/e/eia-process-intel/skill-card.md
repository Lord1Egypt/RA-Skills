## Description:

Turns Chinese EIA filings into investment due-diligence intelligence by extracting structured facts, grading field credibility, cross-validating capacity, yield, and emissions, inferring process and equipment signals, and recording provenance-tracked ledger entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianzhiceng297-boop](https://clawhub.ai/user/tianzhiceng297-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and due-diligence teams use this skill to analyze Chinese environmental impact assessment filings, verify capacity and yield claims, infer process routes and equipment tiers, identify regulatory-gaming signals, and build a reusable fact ledger.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may create or append project-scoped eia-ledger records that persist source-derived deal intelligence.

Mitigation: Choose the due-diligence workspace deliberately, avoid confidential filings unless local persistence is acceptable, and review ledger writes before keeping them.

Risk: Cross-case aggregation and mapping-library updates can turn case-specific signals into reusable judgments.

Mitigation: Review cross-case results and mapping updates before accepting them, and keep disclosed facts separate from inferred conclusions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tianzhiceng297-boop/skills/eia-process-intel)
- [Field credibility grading](references/field-credibility.md)
- [Cross-validation recipes](references/cross-validation.md)
- [Ledger schema](references/ledger-schema.md)
- [Semiconductor equipment mapping library](references/mappings/semiconductor-equipment.md)
- [Fictional IR detector format demo](examples/format-demo-ir-detector-en.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown reports, structured tables, and JSONL ledger entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append project-scoped eia-ledger JSONL files when the user permits persistent local records.]

## Skill Version(s):

0.3.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
