## Description:

Helps teams configure AI-assisted semantic content filtering, multilingual rules, account rule synchronization, compliance audit logging, and webhook notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to plan and configure team content-filtering workflows for information feeds, including semantic filtering, rule synchronization, audit logging, and webhook-based notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's command and API guidance is broad for workflows that may modify multiple accounts.

Mitigation: Use least-privilege API keys, require approval for multi-account rule changes, and review proposed commands before execution.

Risk: Content filtering and audit logs may include sensitive user or organizational data.

Mitigation: Redact or minimize sensitive content sent to external services, and define retention rules for audit logs.

Risk: Webhook delivery can expose filtered-event data or send it to the wrong destination.

Mitigation: Verify every webhook destination and require signed webhook callbacks before enabling notifications.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, code, JSON]

**Output Format:** [Markdown guidance with JSON examples, shell command examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes example response JSON and audit-report text; external API output depends on configured services.]

## Skill Version(s):

1.0.0 (source: server evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
