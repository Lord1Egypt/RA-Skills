## Description:

Eridian Carapace provides OpenClaw agent hardening guidance for prompt injection defense, data leak prevention, credential protection, browser allowlisting, security audits, and sensitive-operation approvals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iampaulpatterson-boop](https://clawhub.ai/user/iampaulpatterson-boop)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Eridian Carapace to harden OpenClaw agent configurations, audit security posture, and apply runtime guardrails against prompt injection, credential exposure, data leaks, unsafe browser navigation, and unapproved sensitive operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-handling examples can permit an agent to display plaintext API keys, private keys, tokens, .env contents, or secret-bearing config files when the owner asks directly.

Mitigation: Revise the patterns before use so agents provide only redacted status checks or direct users to retrieve secrets from a password manager, secret manager, or provider console.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iampaulpatterson-boop/skills/eridian-carapace)
- [Security Patterns Reference](references/security-patterns.md)
- [Attack Vectors & Defenses](references/attack-vectors.md)
- [Security Audit Template](references/audit-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Code]

**Output Format:** [Markdown guidance with copy-paste AGENTS.md patterns, audit checklists, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; review credential-handling exceptions before adopting patterns.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
