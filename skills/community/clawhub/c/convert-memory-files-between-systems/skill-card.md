## Description:

Guides agents through converting memory-lancedb-pro memory data into markdown and importing it into memos-local-openclaw-plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2070super](https://clawhub.ai/user/2070super)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill when migrating persistent memory from memory-lancedb-pro to memos-local-openclaw-plugin. It provides guidance and companion Python scripts for checking source data, removing the old plugin configuration, importing markdown memory records into SQLite, and validating record counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rewrite OpenClaw plugin configuration.

Mitigation: Back up the OpenClaw configuration, replace example paths deliberately, inspect the planned changes, and keep a rollback copy before running the removal script.

Risk: The import flow can write persistent agent memory into a SQLite database.

Mitigation: Back up the memos database, import only trusted markdown memory files, inspect parsed records before committing, and validate record counts after import.

Risk: Companion scripts contain hard-coded example paths.

Mitigation: Update paths for the local environment and perform a dry run or manual review before executing scripts against live data.

## Reference(s):

- [Skill source](artifact/SKILL.md)
- [Import markdown to memos script](artifact/scripts/import_markdown_to_memos.py)
- [Remove memory-lancedb-pro configuration script](artifact/scripts/remove_memory_lancedb_pro.py)
- [ClawHub skill page](https://clawhub.ai/2070super/skills/convert-memory-files-between-systems)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python code snippets and file path instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose configuration edits and SQLite writes for OpenClaw memory migration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
