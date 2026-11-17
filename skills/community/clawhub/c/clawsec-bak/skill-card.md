## Description:

Manage and interpret ClawSec Monitor v3.0, a proxy that inspects AI agent HTTP/HTTPS traffic, detects threats, and logs suspicious activity in real time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhc1991](https://clawhub.ai/user/zhc1991)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to operate ClawSec Monitor, inspect AI agent traffic, interpret threat logs, and generate proxy setup or troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to trust a local HTTPS interception CA, which can expose plaintext traffic to the proxy.

Mitigation: Use the tool only when intentional traffic inspection is required, prefer per-process CA trust, and avoid routing unrelated applications through the proxy.

Risk: Threat logs may contain plaintext snippets with secrets or sensitive data.

Mitigation: Protect access to /tmp/clawsec logs, delete logs when no longer needed, and scope monitoring to the specific agent traffic under review.

Risk: The provided artifact documents commands for implementation files that are not included in the artifact evidence.

Mitigation: Confirm the referenced implementation files are present and reviewed before running the documented commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhc1991/skills/clawsec-bak)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational steps, proxy configuration, threat-log interpretation, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
