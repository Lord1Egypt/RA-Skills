## Description:

Two-tier memory system for OpenClaw agents. Tier 0 = QMD semantic search for recent memories (7-14 days). Tier 1 = SQLite archive for long-term storage. Auto-archives old sessions with LLM summarization. Use when building agents that need efficient, scalable memory management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpmoregain-eth](https://clawhub.ai/user/jpmoregain-eth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add scalable memory management to OpenClaw agents by searching recent memory files and archiving older sessions into SQLite summaries. It supports manual or scheduled archive maintenance and unified lookup across recent and archived memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional README install path pipes a downloaded Ollama script directly to a shell.

Mitigation: Use a trusted packaged installer or verify any downloaded script before running it.

Risk: Scheduled archiving can summarize, move, and permanently retain potentially sensitive OpenClaw memory files in a local SQLite database.

Mitigation: Run with --dry-run first, enable the cron job only when retention is desired, protect the archive database, and define a deletion process.

Risk: LLM-based summarization can expose sensitive memory content to the local Ollama model process and may produce incomplete summaries.

Mitigation: Use --skip-llm for sensitive logs or review generated summaries before relying on archived results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpmoregain-eth/skills/agent-tiered-memory)
- [QMD Setup Guide](references/qmd-setup.md)
- [Ollama download](https://ollama.com/download)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or query local SQLite archive records and move old OpenClaw memory files when the archive script is run.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
