## Description:

Agent Retro guides an agent through a daily retrospective that reviews session history, summarizes lessons learned, and updates memory and configuration files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangc](https://clawhub.ai/user/tangc)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill when they want an assistant to review a prior day's sessions, produce a concise retrospective, and persist lessons into memory and configuration files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect broad daily session history, which may include secrets, credentials, personal data, or unrelated tool outputs.

Mitigation: Require redaction rules before use and limit the review scope to the intended agent, date, and session files.

Risk: The workflow can permanently rewrite memory and core behavior files.

Mitigation: Require a dry-run diff, backups, and explicit approval for each file change before writing updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangc/skills/agent-retro)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown retrospective report with memory and configuration file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update daily memory files, core behavior files, backups, and a date-based completion lock.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
