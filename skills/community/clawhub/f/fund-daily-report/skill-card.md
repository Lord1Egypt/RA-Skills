## Description:

Generate daily fund performance reports with NAV changes, market commentary, and portfolio updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and investment-reporting agents use this skill to generate daily Chinese fund market summaries covering NAV growth, ETF attention, industry fund flow, and high-attention A-share stocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact embeds a third-party data-service login that may be used automatically.

Mitigation: Remove and rotate the exposed credentials, and require users to provide credentials through environment variables or a secret manager.

Risk: Some report sections use proxy or attention metrics rather than verified fund-flow or holdings data.

Mitigation: Clearly label estimated sections in generated reports and require review before using the output for investment decisions.

Risk: Unpinned dependencies can change data access behavior or report calculations over time.

Mitigation: Pin dependency versions and review changes before deployment.

## Reference(s):

- [README](README.md)
- [ClawHub Skill Page](https://clawhub.ai/paudyyin/skills/fund-daily-report)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text fund report with tabular sections and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report sections may include estimated fund-flow, holdings, and attention metrics derived from public market data APIs.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
