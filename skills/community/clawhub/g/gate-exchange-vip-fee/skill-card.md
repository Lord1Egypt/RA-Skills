## Description:

Helps agents answer Gate users' VIP tier and spot or futures trading fee questions by querying read-only Gate MCP account and wallet fee tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External Gate users use this skill to retrieve their current VIP tier and spot or futures maker/taker fee rates through read-only Gate MCP queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read account details during setup or detection even when the user asks only for fee data.

Mitigation: Use a Gate credential limited to Account:Read and Wallet:Read, with no trading or withdrawal permissions.

Risk: The skill depends on mutable external runtime rules that can change outside this package.

Mitigation: Review the linked runtime rules before installing or updating the skill.

Risk: Fee results are account-level, and an invalid trading pair can still return default account fee values.

Mitigation: Label returned rates as account-level fees and note that a requested pair may not have been validated.

## Reference(s):

- [Gate VIP Fee MCP Specification](references/mcp.md)
- [Gate VIP & Fee Query Scenarios](references/scenarios.md)
- [Gate MCP](https://github.com/gateio/gate-mcp)
- [Gate Runtime Rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- [Gate API Key Management](https://www.gate.io/myaccount/profile/api-key/manage)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only responses summarize VIP level and spot or futures maker/taker fees; account values are user-specific and API keys must not be exposed.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
