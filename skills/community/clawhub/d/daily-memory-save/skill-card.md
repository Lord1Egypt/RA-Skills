## Description:

Daily Memory Save periodically reviews conversation history and writes daily and long-term memory files to maintain agent continuity across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[madebydia](https://clawhub.ai/user/madebydia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw users use this skill to give an agent persistent local memory across sessions by saving selected conversation context into daily notes and curated long-term memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation summaries may persist sensitive or private details in workspace memory files.

Mitigation: Install only in private workspaces, add explicit redaction rules for credentials and sensitive data, and review or delete saved memory files regularly.

Risk: Silent memory saving can reduce user awareness of what was retained.

Mitigation: Enable the documented notification mode when visibility is needed and periodically audit MEMORY.md and memory/ notes.

Risk: Repeated runs may duplicate or over-retain conversation context.

Mitigation: Read existing memory files before writing, deduplicate similar notes, and keep only genuinely new or long-term useful details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/madebydia/skills/daily-memory-save)
- [Project Homepage](https://github.com/madebydia/daily-memory-save)

## Skill Output:

**Output Type(s):** [Markdown, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown files and cron-style configuration text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local memory/YYYY-MM-DD.md and MEMORY.md files when notable conversation context exists.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
