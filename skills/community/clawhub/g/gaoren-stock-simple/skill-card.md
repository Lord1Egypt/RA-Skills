## Description:

股票简单分析 - A股/港股/美股实时行情快速查询

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoren36-arch](https://clawhub.ai/user/gaoren36-arch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to quickly query A-share, Hong Kong, and U.S. stock quotes from a Python command-line helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to third-party finance APIs.

Mitigation: Review and approve network access before installation or execution.

Risk: The artifact includes a reusable Finnhub API key.

Mitigation: Remove the bundled key and require users to provide their own API token through a secret or environment variable.

Risk: Broad natural-language triggers may activate the skill during unrelated conversations.

Mitigation: Narrow trigger phrases or require explicit user invocation before running stock lookup behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaoren36-arch/skills/gaoren-stock-simple)
- [ClawHub publisher profile](https://clawhub.ai/user/gaoren36-arch)
- [Tencent Finance quote API endpoint](https://qt.gtimg.cn/)
- [Finnhub quote API endpoint](https://finnhub.io/api/v1/quote)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text stock quote output and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and outbound network access to third-party finance APIs.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
