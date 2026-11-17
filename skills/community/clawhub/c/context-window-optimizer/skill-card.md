## Description:

Optimize context window usage by summarizing older conversation segments, extracting key facts and decisions to memory, and keeping active context lean.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klemenska](https://clawhub.ai/user/klemenska)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to keep long agent conversations manageable by identifying when context is heavy, summarizing older work, and extracting decisions or key facts for later reference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local agent session transcripts that may contain secrets, sensitive content, or regulated data.

Mitigation: Run it only on sessions approved for summarization, check which transcript will be read, and avoid sessions that may contain secrets or regulated data.

Risk: Conversation-derived facts or preferences may be persisted with weak scoping or without redaction.

Mitigation: Manually review and redact extracted decisions, facts, and preferences before copying them into long-term memory or project files.

Risk: Heuristic summaries or extracted decisions may be incomplete or misleading.

Mitigation: Treat generated summaries as draft notes and compare important items against the source conversation before relying on them.

## Reference(s):

- [Context Optimization Patterns](artifact/references/patterns.md)
- [ClawHub skill page](https://clawhub.ai/klemenska/skills/context-window-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional shell commands and generated markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local OpenClaw session transcripts and may write summary or extraction files when an output path is supplied.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
