## Description:

Documents hidden OpenClaw HTTP endpoints, debug flags, environment variables, and configuration shortcuts for power users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill as an admin-only reference for OpenClaw diagnostics, debug configuration, and power-user setup in isolated test environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guidance can weaken authentication, signature validation, sandboxing, or admin/tool restrictions when applied to an OpenClaw host.

Mitigation: Treat the skill as an admin-only reference for isolated test environments, and keep production auth, signature validation, sandboxing, and deny-list controls enabled unless a formal security review approves an exception.

Risk: Debug logging, raw stream capture, signed-in browser profiles, webhooks, and remote embedding providers can expose sensitive data.

Mitigation: Limit access to logs and profiles, redact or disable raw captures where possible, and use only approved webhook and provider endpoints with scoped credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evezart/skills/evez-cheat-codes)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; the skill does not run code itself.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
