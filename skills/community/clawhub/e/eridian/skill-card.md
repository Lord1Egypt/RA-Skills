## Description:

Eridian provides runtime security hardening for OpenClaw agents against prompt injection, data exfiltration, credential leaks, and unauthorized operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iampaulpatterson-boop](https://clawhub.ai/user/iampaulpatterson-boop)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to add runtime security rules, audit checklists, and browser navigation controls to OpenClaw agents. It is intended for hardening agent configurations and reducing exposure to prompt injection, data exfiltration, credential leakage, and unauthorized operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports an unsafe credential-disclosure exception that could allow raw config files or API keys to be shown in chat.

Mitigation: Review and edit the credential rules before installation; remove exceptions that permit printing secrets and use presence checks, masked values, or local secret-manager inspection instead.

## Reference(s):

- [Security Patterns Reference](references/security-patterns.md)
- [Attack Vectors & Defenses](references/attack-vectors.md)
- [Security Audit Template](references/audit-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes copy-paste security rules, an audit checklist, and a browser allowlist example; no executable payload.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
