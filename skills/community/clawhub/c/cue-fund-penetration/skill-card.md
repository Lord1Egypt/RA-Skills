## Description:

Analyzes publicly disclosed holdings of Chinese public mutual funds to identify stock overlap, sector concentration, and style exposure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Individual investors, fund advisers, and portfolio researchers use it to compare public mutual fund holdings, find duplicated exposures, and assess diversification using periodic disclosure data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review flags an unpinned remote runner and remote code execution, with only partial scanner coverage.

Mitigation: Review the runner source and pin a trusted version before use; treat scan results as incomplete until the missing-path coverage issue is resolved.

Risk: The skill asks users to paste an API key into chat.

Mitigation: Provide credentials through a secure local configuration or environment variable instead of chat, and avoid exposing the key in prompts or reports.

Risk: The skill includes promotional credit and sharing prompts unrelated to portfolio analysis.

Mitigation: Omit promotional steps unless the user explicitly asks for credit or account guidance.

Risk: Portfolio conclusions are based on periodically disclosed top-ten holdings and can be stale or incomplete.

Mitigation: State the disclosure date and coverage limits, and treat the report as decision support rather than live holdings or a forecast.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/panting09266-ai/skills/cue-fund-penetration)
- [Cue service](https://cuecue.cn)
- [Runner repository referenced by the skill documentation](https://github.com/sensedeal/cue-skills)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown report with holdings overlap, sector concentration, style exposure, and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses disclosed top-ten holdings; reported positions may lag current portfolios by one to two months.]

## Skill Version(s):

1.0.14 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
