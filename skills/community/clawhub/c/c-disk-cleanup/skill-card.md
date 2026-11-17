## Description:

A Windows C-drive cleanup assistant that scans disk usage, explains cleanup candidates in plain language, and asks for explicit confirmation before moving files or using Windows cleanup tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiamiaolou-art](https://clawhub.ai/user/jiamiaolou-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support agents use this skill to inspect a Windows C: drive, understand which files or caches may be taking space, and carry out confirmed cleanup or migration steps. It is especially aimed at non-expert Windows users who need cautious disk-space recovery with recoverable moves and clear prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup capabilities may be broader than the skill's only-move-never-delete promise.

Mitigation: Start with the read-only scan, review every proposed cleanup item, and approve only actions with exact source and destination paths.

Risk: Advanced Windows operations such as Program Files compression, DISM, CompactOS, cleanmgr automation, recycle-bin cleanup, and junction moves can affect system behavior or recoverability.

Mitigation: Decline these options unless the user understands the impact, has current backups, and can restore affected files.

Risk: Manual moves of application data or active directories can damage applications, leave partial moves, or make chat history appear missing.

Mitigation: Use official application migration or cleanup tools for chat and application data, close related processes before moves, and verify restored data before deleting old backups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiamiaolou-art/skills/c-disk-cleanup)
- [Workflow reference](references/workflow.md)
- [Troubleshooting reference](references/troubleshooting.md)
- [Glossary reference](references/glossary.md)
- [Habit configuration sample](references/habit.sample.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with PowerShell command examples and optional JSON habit configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-only; cleanup-changing actions require explicit confirmation and exact source and destination paths.]

## Skill Version(s):

1.0.1 (source: server release metadata; bundled SKILL.md frontmatter reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
