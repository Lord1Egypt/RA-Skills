## Description:

Refine conversation history by deleting useless, redundant, and process-only exchanges while preserving explicit instructions, disciplines, important configs, learned skills, user memory requests, and decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sslisen](https://clawhub.ai/user/sslisen)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to clean chat transcripts, session history, and memory files into concise Markdown summaries or MEMORY.md updates while retaining important instructions, decisions, preferences, and configuration context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist chat-derived instructions into long-lived memory files.

Mitigation: Review the proposed memory update before writing it, and keep only instructions, decisions, preferences, and configuration details that should remain durable.

Risk: Transcripts may contain API keys, credentials, or sensitive configuration values that could be copied into memory summaries.

Mitigation: Use trusted transcripts, redact secrets before refinement, and require an explicit preview before any MEMORY.md or memory summary file is written.

## Reference(s):

- [Refine Principles](artifact/references/principles.md)
- [ClawHub Skill Page](https://clawhub.ai/sslisen/skills/chat-refiner)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown summaries or MEMORY.md updates, optionally with path:line citations and a concise kept-item count]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write memory/YYYY-MM-DD-summary.md, MEMORY.md, or another summary file after refining trusted transcript input.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
