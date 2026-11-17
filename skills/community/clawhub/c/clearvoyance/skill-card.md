## Description:

Helps agents run anonymous voice or text feedback campaigns and retrieve an AI-generated report from Clearvoyance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solcoastconstruction-alt](https://clawhub.ai/user/solcoastconstruction-alt)

### License/Terms of Use:

MIT-0

## Use Case:

Teams and developers use this skill to collect candid customer, employee, or user feedback through voice or text campaigns and review the resulting report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live campaigns charge the account balance and may not be refunded if too few people respond.

Mitigation: Start in the free sandbox; show the quoted price and obtain user approval before each live launch.

Risk: Campaign content and targeted recipient email addresses are sent to an external feedback service.

Mitigation: Review campaign text and recipient emails with the user before launching; do not include email addresses in quote requests.

## Reference(s):

- [ClawHub release](https://clawhub.ai/solcoastconstruction-alt/skills/clearvoyance)
- [Clearvoyance API specification](https://clearvoyance.ai/openapi.json)
- [Clearvoyance MCP server card](https://clearvoyance.ai/.well-known/mcp.json)
- [Clearvoyance data handling](https://clearvoyance.ai/data-handling)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Campaign links, JSON results, and text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are withheld until the campaign's privacy threshold is met.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
