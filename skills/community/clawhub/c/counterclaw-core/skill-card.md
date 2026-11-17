## Description:

Defensive interceptor for prompt injection and basic PII masking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickconstantinou](https://clawhub.ai/user/nickconstantinou)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use Counterclaw Core to scan inbound text for common prompt-injection patterns and outbound text for basic PII before an agent acts or sends messages. It is suited to defensive middleware and optional protected email workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Blocked or sensitive user content may be written to local OpenClaw memory logs.

Mitigation: Deploy only where local audit logging is acceptable, keep log storage access-controlled, or disable violation logging/use a separate audit log for untrusted input.

Risk: Optional Gmail sending can transmit PII when bypass flags are used or when protection is unavailable.

Mitigation: Use a dedicated Gmail account, verify the gog dependency and account setup, test dry-run behavior, and avoid --allow-unsafe unless sending PII is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickconstantinou/skills/counterclaw-core)
- [Publisher profile](https://clawhub.ai/user/nickconstantinou)
- [Project homepage](https://github.com/nickconstantinou/counterclaw-core)
- [Python package page](https://pypi.org/project/counterclaw-core/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Python dictionary results, Markdown audit logs, and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Core scanning is offline; optional email sending depends on gog and network access.]

## Skill Version(s):

1.1.1 (source: ClawHub release evidence; artifact metadata lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
