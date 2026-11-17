## Description:

Guides an agent in finding and managing KeePass KDBX vault entries with kpass, including password generation and TOTP use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanjelin](https://clawhub.ai/user/lanjelin)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation users use this skill to guide an agent through targeted reads and authorized changes in a dedicated KeePass vault using the kpass CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vault access can expose passwords and OTPs through agent output or retained logs.

Mitigation: Use a dedicated automation vault with limited, replaceable credentials and prevent secret values from entering model-visible output, logs, or transcripts.

Risk: Agent-initiated writes can overwrite entries or change vault credentials.

Mitigation: Require explicit authorization for sensitive changes, restrict write access where possible, and keep protected backups before writes.

Risk: Untrusted vault content can attempt to redirect agent behavior.

Mitigation: Treat entry notes and URLs as data, not instructions; constrain the agent's vault and network access outside the skill.

## Reference(s):

- [ClawHub Kpass release](https://clawhub.ai/lanjelin/skills/claw-kpass)
- [Server-resolved source repository](https://github.com/Lanjelin/openclaw-kpass)
- [kpass CLI](https://github.com/Lanjelin/kpass)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires kpass 0.2.0 or newer and access to a configured KDBX vault; secret-bearing results require an approved private execution channel.]

## Skill Version(s):

0.1.0 (source: ClawHub release; bundled skill frontmatter states 1.1.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
