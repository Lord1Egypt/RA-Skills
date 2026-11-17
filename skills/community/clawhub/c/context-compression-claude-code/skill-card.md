## Description:

Compresses long agent conversations with a tiered retention strategy that preserves key goals, decisions, preferences, and active tasks while summarizing or discarding lower-value context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizlzzzz](https://clawhub.ai/user/lizlzzzz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to compact lengthy conversation history into concise summaries and maintain structured memory during manual or hook-triggered context compression.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory updates may retain conversation-derived credentials, configuration details, or other sensitive information without clear consent or redaction.

Mitigation: Require opt-in memory writes, show proposed memory changes before saving, redact or block secrets, and provide a way to inspect and delete stored memory.

Risk: Optional compaction hooks can alter agent behavior automatically when enabled.

Mitigation: Review hook configuration before installation and keep hooks disabled unless the user has confirmed the expected compaction and memory-update behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lizlzzzz/skills/context-compression-claude-code)
- [Setup hook guide](setup-hook.md)
- [Memory template](memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON and YAML hook configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a structured memory file when memory updates are approved.]

## Skill Version(s):

1.0.2 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
