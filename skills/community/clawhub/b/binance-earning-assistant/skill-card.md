## Description:

Chinese-language assistant that summarizes current Binance earning promotions, reward activities, and Alpha airdrop previews from public sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckylion68](https://clawhub.ai/user/luckylion68)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to review Binance promotional earning opportunities, reward campaigns, deadlines, and Alpha airdrop previews in Chinese. It is intended as an informational assistant; users should verify opportunities on official pages before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Promotional and financial opportunity information may change quickly or be incomplete.

Mitigation: Verify deadlines, eligibility, and participation terms on official Binance or project pages before acting.

Risk: The skill makes external network requests to Binance and alpha123.uk and may use the configured HTTP proxy.

Mitigation: Install only when this network behavior is acceptable, and configure HTTP_PROXY deliberately if a proxy is needed.

Risk: The skill can write Markdown reports under the configured OpenClaw workspace.

Mitigation: Set OPENCLAW_WORKSPACE to an expected location and review generated exports before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luckylion68/skills/binance-earning-assistant)
- [Publisher profile](https://clawhub.ai/user/luckylion68)
- [Binance support announcement example](https://www.binance.com/zh-CN/support/announcement/65317d61d1c445f99f73a04c05233dd2)
- [Alpha123 Chinese page](https://alpha123.uk/zh/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Chinese-language Markdown and console-style activity summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May export Markdown reports under the configured OpenClaw workspace.]

## Skill Version(s):

1.0.10 (source: server release metadata; artifact metadata reports 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
