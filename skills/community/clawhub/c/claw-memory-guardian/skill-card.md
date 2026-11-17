## Description:

Claw Memory Guardian helps OpenClaw users maintain local long-term memory, daily work logs, search indexes, backups, and git-based recovery points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[betsymalthus](https://clawhub.ai/user/betsymalthus)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to preserve session context, record project progress, search prior notes, and create local backups after interruptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores long-lived local memory, backups, and git history that may contain sensitive information.

Mitigation: Avoid storing secrets, regulated data, customer details, or confidential business information unless storage, backup, and sharing controls have been reviewed.

Risk: The generated autosave script can run in the background and operate on workspace memory files.

Mitigation: Review workspace configuration before running autosave, monitor running autosave processes, and stop them manually before uninstalling or changing storage policy.

Risk: Installation replaces an existing skill directory or memory-guardian executable in the configured workspace.

Mitigation: Check for existing memory-guardian binaries and skill directories before installation, and back up any existing memory data first.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/betsymalthus/skills/claw-memory-guardian)
- [README](README.md)
- [Usage Examples](EXAMPLES.md)
- [Skill Documentation](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI text with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local memory files, backup directories, search indexes, and git commits in the configured OpenClaw workspace.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
