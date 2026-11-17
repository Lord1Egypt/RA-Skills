## Description:

AutoDream Memory is an automatic memory consolidation agent skill that periodically organizes MEMORY.md and related memory files by deduplicating, merging, pruning stale entries, and converting relative dates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigkingcn](https://clawhub.ai/user/bigkingcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to keep a local OpenClaw workspace memory index and topic memory files concise, current, and easier for future agent sessions to load. It is intended for workspaces where automated memory rewriting and report generation are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rewrite persistent workspace memory, including MEMORY.md and generated memory reports.

Mitigation: Use it only in workspaces where memory rewriting is intended; review generated changes and keep backups enabled before routine use.

Risk: The setup script can create recurring execution configuration and immediately start a consolidation run.

Mitigation: Review the scheduler path and run the cycle manually or with dry-run behavior in a test workspace before enabling recurring execution.

Risk: Server security evidence reports that some promised safety controls are missing or inaccurate.

Mitigation: Confirm backup, locking, dry-run, and scheduler behavior before installing in a workspace that contains important or sensitive memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bigkingcn/skills/autodream-memory)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON files, terminal status text, and shell commands for manual or scheduled execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill updates workspace memory files and reports; the setup script can also write scheduler configuration and run the consolidation cycle.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
