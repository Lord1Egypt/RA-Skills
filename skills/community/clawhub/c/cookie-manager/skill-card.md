## Description:

Manages ecommerce platform cookies by checking health, keeping sessions alive, synchronizing cookie stores, and coordinating recovery workflows when multiple cookies expire.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to monitor, refresh, synchronize, and recover authentication cookies for multi-platform ecommerce workflows. It supports scheduled health checks, degraded-mode response, backup-cookie switching, and tenant-level recovery reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live authentication cookies and can synchronize them across local files, environment configuration, service configuration, and APIs.

Mitigation: Install only in a tightly controlled operations environment, restrict invocation to trusted operators, protect .env and global_config.yml, and prefer a secret manager for cookies and encryption keys.

Risk: Recovery and synchronization modes may perform broad automatic writes or switch backup cookies in production workflows.

Mitigation: Require explicit approval, dry-run review, or other operator confirmation before sync, recovery, or degraded-mode actions are allowed in production.

Risk: Configurable outbound notification endpoints can expose operational cookie status or recovery events outside the local process.

Mitigation: Review PORTAL_NOTIFY_URL and XIANYU_AUTO_REPLY_URL before installation and allow outbound notifications only to approved internal endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cookie-manager)
- [Business rules](references/business_rules.md)
- [Error codes](references/error_codes.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON result schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger local file updates, cookie synchronization, audit records, alerts, and degraded-mode status changes when executed in its target environment.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
