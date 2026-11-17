## Description:

Access Crown Town Compost account data from a shell using curl, including service history, invoices, upcoming service days, and account details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External customers and developers can look up pickup history, upcoming service days, invoices, and account details through the Crown Town Compost portal. They can also manage service or contact support when specifically requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account changes and messages can have lasting effects.

Mitigation: Require a specific user request for each change or message, replace examples with intended values, preserve existing preferences, and re-read the relevant page to verify the result.

Risk: Saved login sessions or credentials may be exposed if session files have broad permissions or passwords enter shell history.

Mitigation: Store cookies in a private directory with owner-only permissions, avoid putting passwords in shell history, and remove session files afterward.

Risk: Omitting account preference checkboxes during an update can silently turn those settings off.

Mitigation: Read current preferences first and resend every field while preserving the existing values.

## Reference(s):

- [Crown Town Compost portal](https://portal.crowntowncompost.com)
- [ClawHub release](https://clawhub.ai/chrischall/skills/crowntowncompost-mcp)
- [Publisher profile](https://clawhub.ai/user/chrischall)
- [Endpoint reference](references/endpoints.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Readable account data or JSON, with Markdown guidance and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contain private account, service, and billing information.]

## Skill Version(s):

1.2.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
