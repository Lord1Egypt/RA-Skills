## Description:

Auto-capture hourly session highlights and update daily memory files. Keeps long-term memory continuous without manual recording. Triggered by cron or manual "remember this".

This skill is ready for commercial/non-commercial use.

## Publisher:

[raydez](https://clawhub.ai/user/raydez)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to summarize recent session highlights into local daily memory files, either on an hourly schedule or through explicit phrases such as "remember this" and "log today".

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recent conversation content may be summarized into persistent local daily memory files.

Mitigation: Prefer explicit save commands, review entries before writing, and redact secrets or personal data before they are stored.

Risk: Automatic session capture and broad persistent storage may record more context than the user intended.

Mitigation: Use narrow trigger settings where possible, audit the configured memory directory periodically, and delete entries that should not be retained.

Risk: The skill lacks clear built-in review or deletion controls in the supplied evidence.

Mitigation: Add a manual review step before appending entries and maintain a deletion or retention process for ~/.openclaw/workspace/memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raydez/skills/auto-memory-keeper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown daily memory entries with supporting shell commands, Python code, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes concise timestamped entries to local daily Markdown files under the configured memory directory.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
