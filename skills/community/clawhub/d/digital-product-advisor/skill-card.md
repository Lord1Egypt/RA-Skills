## Description:

Use when helping a user choose consumer electronics products through source-aware market research, comparison, and recommendation. MVP focuses on Bluetooth earbuds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fina1ee](https://clawhub.ai/user/fina1ee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to produce source-aware Bluetooth earbud buying recommendations tailored to budget, region, marketplace availability, brand scope, phone ecosystem, and use case. It can also export the recommendation as a Markdown report when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product prices, availability, discounts, and regional value can change quickly.

Mitigation: Browse current official/spec, review/testing, and price/availability sources for the user's market before recommending products.

Risk: Numeric scores may look more objective than the source evidence supports.

Mitigation: Treat scores as decision aids, explain assumptions and missing evidence, and include tradeoffs and confidence level in the report.

Risk: Saved Markdown reports may be written to an unexpected custom folder.

Mitigation: Use the default reports/earbuds/ folder unless the user provides another path, generate safe filenames, and report the exact saved path.

## Reference(s):

- [Digital Product Advisor on ClawHub](https://clawhub.ai/fina1ee/skills/digital-product-advisor)
- [Bluetooth Earbuds Buying Logic](artifact/references/bluetooth-earbuds.md)
- [Parameter Model](artifact/references/parameters.md)
- [Scoring Framework](artifact/references/scoring-framework.md)
- [Source Quality](artifact/references/source-quality.md)
- [Markdown Export Policy](artifact/references/export-policy.md)
- [Report Template](artifact/templates/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown buying reports, concise recommendation guidance, optional JSON-shaped candidate data, and optional local Markdown report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include shortlist tables, scenario picks, tradeoffs, product links or labeled search links, sources checked, and a confidence level.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
