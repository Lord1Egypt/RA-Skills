## Description:

APPM helps agents maintain project-level memory by creating and using `.openclaw/` mission, snapshot, and decision-log files for parallel project tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanchunlee](https://clawhub.ai/user/hanchunlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to initialize and maintain local project memory files so an agent can recover project goals, current status, key paths, decisions, and next actions across sessions or parallel projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores project summaries, paths, priorities, and next actions on disk.

Mitigation: Use it only in repositories where this local project context may be stored, and review `.openclaw/` content before sharing or committing it.

Risk: Persisted `.openclaw/` notes from shared or untrusted projects could bias an agent's project understanding.

Mitigation: Treat `.openclaw/` content as untrusted notes; user and system instructions remain authoritative.

Risk: Automatic project recall and weighting can surface stale or mis-scoped project context.

Mitigation: Confirm the active project before relying on recalled context or updating cross-project registry weights.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hanchunlee/skills/appm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown project-memory files with plain-text console output and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates `.openclaw/` templates and reads or updates local project registry data.]

## Skill Version(s):

2.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
