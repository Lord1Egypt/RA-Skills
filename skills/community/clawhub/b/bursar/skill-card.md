## Description:

Pay for services from a Bursar mandate on Robinhood Chain, inside the limits its owner set. Quote, pay, buy and sell listed US stocks, and read your endowment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bursarworld](https://clawhub.ai/user/bursarworld)

### License/Terms of Use:

MIT-0

## Use Case:

External users configure this skill with a Bursar MCP server so an agent can inspect a mandate, pay approved service providers, make permitted stock trades, and check or collect endowment draws.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can spend funds, trade stocks, and collect endowment draws.

Mitigation: Inspect the mandate and quote each payment or trade; act only within its limits and stop when a quote refuses.

Risk: Job input is sent to the selected provider.

Mitigation: Exclude secrets and unnecessary personal information from job input.

Risk: The skill instructions do not independently prove that the server enforces mandate limits.

Mitigation: Use a trusted Bursar MCP server and verify its mandate checks before relying on them.

## Reference(s):

- [Bursar](https://bursar.world)
- [Bursar on ClawHub](https://clawhub.ai/bursarworld/skills/bursar)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Text]

**Output Format:** [MCP tool calls and text responses, including quote decisions and settlement details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Payment and trading requests are constrained by the mandate's configured limits.]

## Skill Version(s):

0.1.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
