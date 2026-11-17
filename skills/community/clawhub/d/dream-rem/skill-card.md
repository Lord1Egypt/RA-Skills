## Description:

Deeply consolidates memory by extracting daily journal entries into topic files and cleaning outdated content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jofiction918](https://clawhub.ai/user/jofiction918)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to periodically consolidate agent memory, keep MEMORY.md as a compact index, and move durable information into topic files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring unattended memory consolidation can rewrite or delete stored memory without a confirmation or backup step.

Mitigation: Install only when automatic memory consolidation is desired; keep backups of MEMORY.md, topics/, and memory/heartbeat-state.json, and prefer manual runs when deletions should be reviewed first.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status reports with file edits and optional shell command configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and rewrite MEMORY.md, topics/, and memory/heartbeat-state.json; scheduled execution can run unattended.]

## Skill Version(s):

3.0.13 (source: server release metadata; artifact frontmatter lists 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
