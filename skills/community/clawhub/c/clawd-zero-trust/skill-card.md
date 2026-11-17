## Description:

Clawd Zero Trust helps OpenClaw operators audit and apply Zero Trust hardening, including outbound allowlisting, plugin integrity checks, least-privilege tool profiles, and deployment verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanistolberg](https://clawhub.ai/user/stanistolberg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to review and harden OpenClaw deployments before or during production operation. It provides audit guidance and administrative workflows for firewall egress controls, plugin allowlists, least-privilege tool profiles, and execution policy review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full non-interactive gateway exec settings can increase impact if identity or channel controls are bypassed.

Mitigation: Constrain gateway exec before sensitive deployment, require approval for privileged execution, and verify channel allowlists against operational policy.

Risk: An unrestricted outbound 443 rule can weaken the intended provider allowlist.

Mitigation: Remove or narrow broad HTTPS egress before applying firewall policy, then verify provider-specific connectivity with dry-run, canary, and verify-all modes.

Risk: Dynamic whitelist changes can open new egress paths without sufficient review.

Mitigation: Require validation and approval for whitelist.sh inputs, review added domains and ports, and keep a change record for provider allowlist updates.

Risk: Firewall and hardening apply modes can disrupt access or alter production configuration.

Mitigation: Run audit and dry-run modes first, prefer canary where available, maintain backups, and confirm rollback steps before mutating production systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stanistolberg/skills/clawd-zero-trust)
- [Project homepage](https://github.com/stanistolberg/clawd-zero-trust)
- [Zero Trust Principles](references/zero-trust-principles.md)
- [Known Audit False Positives](references/false-positives.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run, apply, canary, verification, audit-log, plugin-integrity, and rollback workflows for administrative review.]

## Skill Version(s):

1.3.2 (source: server release metadata and CHANGELOG.md, released 2026-03-10; SKILL.md frontmatter lists 1.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
