## Description:

Exports Codex CLI or Desktop sessions to Markdown, HTML, or Obsidian notes, with options for brief or redacted output, time or text filtering, incremental appends, interactive selection, session merging, watch mode, and session listing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sb679](https://clawhub.ai/user/sb679)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to export, review, share, or archive past Codex sessions while filtering content, redacting common sensitive values, or converting transcripts for Markdown, HTML, or Obsidian workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and export sensitive local Codex history, including past prompts, responses, tool output, session IDs, and workspace paths.

Mitigation: Use explicit session IDs, prefer --brief and --redact for shareable exports, and manually review generated files before sharing them.

Risk: Some metadata may remain in exported files even when redaction is enabled.

Mitigation: Inspect the final Markdown, HTML, or Obsidian output and apply additional manual redaction for sensitive project or identity details.

Risk: Installing through latest-style package commands can make the installed code change between runs.

Mitigation: Pin install versions or inspect the source package before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sb679/skills/codex-export-more)
- [Project Repository Referenced by Artifact](https://github.com/sb679/codex-export-more)
- [Upstream Codex Export Project](https://github.com/jinghan23/codex-export)
- [Development Notes](docs/DEVELOPMENT.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML, or Obsidian note files, plus concise command guidance for selecting export options.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports can include session metadata, tool call content, and local path context unless users choose brief or redacted modes and review the generated files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact package files list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
