## Description:

Helps users organize and manage credentials in a local encrypted vault using the bundled command-line tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0 (ClawHub listing); bundled MIT applies to .py code only; documentation and theory all rights reserved

## Use Case:

Developers and users can create and manage a local credential vault, recover access, and inspect audit records using the supplied tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Giving an agent a master password, recovery key, or credential can expose sensitive secrets.

Mitigation: Keep raw secrets out of agent context and use interactive entry rather than command-line flags or environment variables.

Risk: Credential retrieval and automation paths may expose plaintext; the package should not be relied on as an AI credential broker.

Mitigation: Review how secrets are revealed and require human confirmation before granting an agent credential access.

Risk: Delete and remove operations can cause credential loss.

Mitigation: Back up the vault before destructive operations and confirm the target entry.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/credential-vault-design)
- [Vault overview diagram](references/panorama.svg)
- [Security overview diagram](references/panorama-security-radar.svg)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Text or Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The tools may create or modify local vault files; retrieved credentials may appear in command output.]

## Skill Version(s):

2.0.3 (source: ClawHub release metadata; bundled SKILL.md says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
