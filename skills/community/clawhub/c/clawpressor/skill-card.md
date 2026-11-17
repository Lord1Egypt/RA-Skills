## Description:

Compresses OpenClaw session context with Sumy/LexRank summarization to reduce token usage and extend session lifetime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beboxos](https://clawhub.ai/user/beboxos)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to inspect, summarize, and compact large session histories when context size slows work, increases token usage, or approaches context limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying compression rewrites OpenClaw session history and may remove details that are still useful later.

Mitigation: Run dry-run first, review the preview, keep the generated backup, and increase the keep count for important sessions.

Risk: Optional Google Sheets metrics can use local Google credentials to send compression statistics when local sheet configuration exists.

Mitigation: Review or remove the Google Sheets integration unless remote metrics are intended, and keep Google credentials out of shared workspaces.

Risk: Summarization or fallback truncation can omit important instructions, decisions, or tool results.

Mitigation: Review the compacted summary before relying on it and restore from the backup if critical context is missing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beboxos/skills/clawpressor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stream guidance; applying the provided commands can rewrite local OpenClaw session JSONL files and create backup files.]

## Skill Version(s):

1.0.0 (source: release evidence, config.yaml, CHANGELOG.md, and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
