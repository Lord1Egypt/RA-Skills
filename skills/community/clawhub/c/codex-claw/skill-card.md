## Description:

Install and verify Codex Claw for Codex Desktop AGENTS.md, Agent MD, SOUL.md, soul file, session memory, personality, and OpenClaw workspace context loading through the @openclaw/codex-claw plugin with post-compaction reinjection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[100yenadmin](https://clawhub.ai/user/100yenadmin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Codex Desktop users use this skill to install, configure, and verify the Codex Claw plugin for loading selected OpenClaw AGENTS.md and SOUL.md workspace context into fresh Codex Desktop sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs and enables an external Codex hook plugin using mutable or forced install steps.

Mitigation: Confirm trust in the exact @openclaw/codex-claw package version, verify the downloaded package before installation, and avoid forced or wildcard installs where possible.

Risk: Configured AGENTS.md and SOUL.md files may contain secrets, unsafe instructions, or local-only context that would be loaded into future Codex sessions.

Mitigation: Review and scope AGENTS.md and SOUL.md before enabling broad session loading, removing secrets and instructions that conflict with native Codex behavior.

## Reference(s):

- [Codex Claw on ClawHub](https://clawhub.ai/100yenadmin/skills/codex-claw)
- [Publisher profile: 100yenadmin](https://clawhub.ai/user/100yenadmin)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and TOML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides installation, configuration, verification, diagnostics, and review guidance for local Codex Desktop context loading.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
