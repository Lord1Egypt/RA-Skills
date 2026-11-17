## Description:

Agent Life helps agents use the alf CLI to back up, sync, restore, and migrate agent memory and state to the agent-life.ai cloud using the Agent Life Format (ALF).

This skill is ready for commercial/non-commercial use.

## Publisher:

[logikoma](https://clawhub.ai/user/logikoma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to have an agent operate alf workflows for backing up, syncing, restoring, importing, and validating OpenClaw agent memory and state. It is most relevant when migrating agents or maintaining cloud backups of allowlisted agent files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask users to install alf through a mutable remote installer.

Mitigation: Prefer a direct binary download from a pinned release, or pin the installer to an immutable commit before running it.

Risk: Checksum verification can be bypassed when verification cannot complete.

Mitigation: Do not set ALF_ALLOW_UNVERIFIED; require successful checksum verification before installing.

Risk: Syncing can upload allowlisted agent memory and an encrypted credential vault to agent-life.ai.

Mitigation: Run alf export --dry-run before syncing and confirm the files and encrypted vault behavior are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/logikoma/skills/agent-life)
- [Agent Life homepage](https://agent-life.ai)
- [Agent-readable CLI documentation](https://agent-life.ai/docs/cli.md)
- [Human-readable CLI documentation](https://agent-life.ai/docs/cli)
- [ALF vault documentation](https://agent-life.ai/cli#alf-vault)
- [ALF GitHub releases](https://github.com/agent-life/agent-life-adapters/releases)
- [ALF install script source](https://github.com/agent-life/agent-life-adapters/blob/main/scripts/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The alf CLI normally emits JSON to stdout; ALF_HUMAN=1 can request human-readable stdout.]

## Skill Version(s):

1.8.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
