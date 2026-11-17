## Description:

Token on-chain analysis via Gate-Info MCP: holder distribution, on-chain activity, and large or unusual transfers for supported tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request token-level on-chain reports that summarize holder distribution, on-chain activity, and large or unusual transfers using Gate-Info MCP data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: On-chain summaries may be mistaken for investment advice.

Mitigation: Present reports as informational financial context and include the skill's no-investment-advice posture.

Risk: Results depend on the Gate-Info MCP server available in the runtime environment.

Mitigation: Verify the intended Gate-Info MCP server is installed and available before using the skill.

Risk: Unsupported Smart Money or unavailable MCP data could lead to overstatement.

Mitigation: Clearly state unavailable dimensions, skip missing sections, and avoid approximating unsupported data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaixianggeng/skills/gate-info-tokenonchain-staging)
- [gate-runtime-rules.md](references/gate-runtime-rules.md)
- [info-news-runtime-rules.md](references/info-news-runtime-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown structured report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are informational and should avoid fabricated on-chain data, speculative price predictions, and buy/sell advice.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
