## Description:

Gate partner affiliate data and application skill for querying partner commissions, referral volume, and affiliate program eligibility or application status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External Gate partners use this skill to retrieve read-only affiliate commission, transaction, subordinate, eligibility, and application-status information through a configured Gate MCP session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured Gate MCP credentials can expose partner rebate, referral user, commission, trading volume, fee, and application-status data.

Mitigation: Use a Gate API key limited to Rebate:Read and rely only on the locally configured MCP session rather than pasting secrets into chat.

Risk: Ambiguous commission requests or relative dates can lead to unintended query windows or metrics.

Mitigation: Normalize date ranges in UTC+8, reject future timestamps, and clarify commission intent when the generic word "commission" is insufficient.

Risk: Naive aggregation of returned records can misstate commissions, volume, or fees.

Mitigation: Apply the skill's asset-aware and business-rule aggregation guidance, respect pagination and 30-day endpoint limits, and disclose truncation or splitting.

## Reference(s):

- [Gate Exchange Affiliate Runtime Rules](references/gate-runtime-rules.md)
- [Gate Affiliate MCP Specification](references/mcp.md)
- [Gate Skills Repository](https://github.com/gate/gate-skills)
- [Gate API Key Management](https://www.gate.com/myaccount/profile/api-key/manage)
- [Gate Affiliate Portal](https://www.gate.com/referral/affiliate)
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/skills/gate-exchange-affiliate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown partner reports and concise text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only responses based on the configured Gate MCP session; does not request or store API secrets in chat.]

## Skill Version(s):

1.0.5 (source: evidence.release.version; artifact frontmatter version: 2026.4.8-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
