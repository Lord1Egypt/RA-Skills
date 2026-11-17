## Description:

Analyzes a specific tender using historical procurement data to advise whether to bid, suggest a price range, assess competitors, and identify risks and next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

External bidding and procurement teams use this skill to assess a tender's buyer, competitors, historical prices, bid suitability, and actionable risks before deciding how to bid.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic account setup collects device features and stores an API key locally.

Mitigation: Review the consent request and use your own ZLBX_API_KEY to skip automatic registration; protect the stored key.

Risk: HTML reports and signed or auto-login URLs may grant access when shared.

Mitigation: Share reports and access links only with intended recipients; review included links before distribution.

Risk: Bid-data queries spend account credits and incomplete historical data can affect recommendations.

Mitigation: Check estimated credit use and independently verify source data, pricing assumptions, and the final bid decision.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhiliaobiaoxun/skills/ai-bidding-strategy-advisor)
- [Analysis workflow](references/workflow.md)
- [API quick reference](references/api-quick.md)
- [Report template](references/report-template.md)
- [Account registration guidance](references/auto-register.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown report, HTML report, Guidance]

**Output Format:** [Markdown in conversation; optional shareable HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bid recommendation, pricing range, competitor analysis, source citations, and risk and action lists; full analysis uses paid API credits.]

## Skill Version(s):

1.0.9 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
