## Description:

Helps OpenClaw agents maintain persistent workspace memory with hot, warm, and cold data organization, automated archival, daily reflection records, and lesson-to-skill extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccyaolei](https://clawhub.ai/user/ccyaolei)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to give an OpenClaw workspace a structured long-term memory system, including daily logs, decisions, lessons, reflections, archive management, and reusable skill extraction from lessons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation can configure recurring cron jobs that modify the OpenClaw memory workspace.

Mitigation: Review the installation steps before use, inspect the exact cron entries, and use manual setup when background jobs are not intended.

Risk: The extraction script can write outside the intended workspace if path-like lesson or skill names are supplied.

Mitigation: Avoid absolute paths and parent-directory segments in extraction arguments until name validation and workspace confinement are enforced.

Risk: The security verdict is suspicious because the package combines automatic scheduled tasks with unsafe extraction behavior.

Mitigation: Scan and review the skill before deployment, and limit use to trusted workspaces with recoverable memory data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ccyaolei/skills/agent-memory-system)
- [Publisher Profile](https://clawhub.ai/user/ccyaolei)
- [README](artifact/README.md)
- [Skill Source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, shell scripts, and memory file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update workspace memory files, archive reports, generated skill templates, and optional cron entries when installed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
