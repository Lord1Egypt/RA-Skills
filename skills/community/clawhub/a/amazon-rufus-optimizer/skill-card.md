## Description:

Amazon Rufus Optimizer helps Amazon sellers simulate Rufus-style shopping conversations, diagnose intent-tag coverage, rewrite listing copy, and identify cross-category scenarios for listing optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon marketplace sellers and listing optimization teams use this skill to evaluate whether product copy covers Rufus-style buyer intents, then generate advisory improvements for scenario wording, audience tags, and cross-category positioning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rufus visibility scores and simulated recommendation outcomes may be mistaken for verified Amazon ranking data.

Mitigation: Treat scores and simulations as advisory copywriting guidance, then validate listing changes against Amazon policy, marketplace performance data, and human review before publishing.

Risk: Chinese-language guidance and examples may be misapplied to listings in other locales.

Mitigation: Review translated or localized copy with a fluent marketplace operator before publishing customer-facing listing text.

## Reference(s):

- [Amazon Rufus Optimizer ClawHub Page](https://clawhub.ai/wangm-a3/skills/amazon-rufus-optimizer)
- [Rufus Intent Taxonomy](artifact/references/intent-taxonomy.md)
- [Rufus Keyword Analyzer](artifact/scripts/rufus-keyword-analyzer.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style reports with scored diagnostics, simulated conversation outcomes, keyword coverage analysis, and prioritized recommendations; the analyzer script can also emit JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and depend on user-provided product names, ASINs, listing copy, bullet points, categories, and selling-point keywords.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
