## Description:

Provides a long-term memory system for OpenClaw agents with hot, warm, and cold memory tiers, automatic archiving, nightly reflection, and reusable skill extraction from lessons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomor1984](https://clawhub.ai/user/tomor1984)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to set up and maintain persistent OpenClaw memory files, daily logs, lessons, decisions, reflections, archives, and reusable skill drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs recurring scheduled jobs and manages persistent OpenClaw memory files.

Mitigation: Review the scripts before installation, keep cron disabled until approved, monitor scheduled-job logs, and back up memory data before running install, GC, reflection, or uninstall flows.

Risk: Unsafe path handling can write or delete outside intended memory or skills folders.

Mitigation: Do not pass lesson or skill names containing slashes, dots, or path components, and run the skill only in a backed-up workspace until the path traversal issue is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomor1984/skills/agent-memory-system-new)
- [Publisher profile](https://clawhub.ai/user/tomor1984)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [MEMORY template](artifact/templates/MEMORY-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, shell scripts, generated skill package scaffolds, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and modifies local OpenClaw memory, archive, reflection, lesson, and skill files when its scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
