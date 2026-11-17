## Description:

1688 Item One Click helps agents modify 1688 product titles, replace main images, set limited-time discounts, and publish member-feed posts through a two-step pre-check and confirmed execution workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External 1688 merchants and their agents use this skill to apply confirmed product listing, promotion, and member-feed updates from a CLI-backed workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change 1688 merchant listings, promotions, and member-feed content.

Mitigation: Require before_check to pass and obtain explicit user confirmation before every execute call.

Risk: The configured AK grants authority to perform gateway-backed merchant operations.

Mitigation: Verify the gateway destination, avoid exposing secrets in shared shells or logs, and restrict permissions on OpenClaw configuration files.

Risk: Server security evidence marks the release verdict as suspicious because write scope and credential handling need review.

Mitigation: Review the skill before installation or use, and grant only the permissions needed for the intended merchant workflow.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/1688aiinfra/skills/1688-item-one-click)
- [Configuration capability](artifact/capabilities/configure.md)
- [Before-check capability](artifact/capabilities/before_check.md)
- [Execute capability](artifact/capabilities/execute.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON responses with human-facing Markdown summaries and CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured 1688 AK; write operations use execute only after before_check and explicit user confirmation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
