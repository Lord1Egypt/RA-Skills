## Description:

Persistent conversation export and replay for AI agents system for Claude Code, Caveman, OpenClaw, Hermes, MCP agents, and multi-agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laohu-aiskills](https://clawhub.ai/user/laohu-aiskills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to export, archive, and replay AI agent conversations for human review, RAG ingestion, JSONL datasets, observability, and workflow debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported conversation archives may contain sensitive prompts, file paths, tool outputs, credentials pasted into chat, or project details.

Mitigation: Review exported files before sharing or syncing them, prefer compact exports for routine use, and store full, replay, or JSONL exports in a controlled location.

## Reference(s):

- [Output Template](references/output-template.md)
- [Agent Archive ClawHub Skill Page](https://clawhub.ai/laohu-aiskills/skills/agent-archive)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSONL, RAG-ready chunks, and replay-friendly session records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports can include session metadata, table of contents, tool call records, summaries, chunk indexes, and truncated large tool outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
