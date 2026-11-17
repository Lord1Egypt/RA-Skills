## Description:

Guard purchases with A2AWire Spend Guard by checking proposed purchases against the human's spend rules, following the approve, deny, or ask decision, and recording completed purchases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ee324](https://clawhub.ai/user/ee324)

### License/Terms of Use:

MIT-0

## Use Case:

Agents with an existing A2AWire identity use this skill to check planned purchases against human-defined spending rules and record completed purchases in the identity's ledger.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bug reports may expose sensitive purchase details, identity information, or credentials.

Mitigation: Review the data-sharing instructions and remove real purchase details, identifiers, and credentials before sending a report.

Risk: The security scan is partial and cannot provide complete assurance.

Mitigation: Review the skill's data-sharing and bug-reporting instructions before installation.

## Reference(s):

- [A2AWire Spend Guard connector reference](https://a2awire.com/connectors/spend-guard/)
- [A2AWire platform reference](https://a2awire.com/llms.txt)
- [A2AWire Spend Guard MCP endpoint](https://a2awire.com/mcp/connectors/spend-guard/http)
- [ClawHub release page](https://clawhub.ai/ee324/skills/a2awire-spend-guard)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown instructions with inline curl and JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
