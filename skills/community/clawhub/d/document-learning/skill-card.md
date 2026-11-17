## Description:

Document Learning helps agents read PDF and text documents, track progress across sessions, resume work, and save document-derived summaries into long-term memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzqzuigao-ui](https://clawhub.ai/user/yzqzuigao-ui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to learn from large PDF or text documents over multiple sessions, keep per-document progress, and retrieve summaries or key concepts from memory later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist summaries or notes derived from private, proprietary, regulated, or prompt-bearing documents into long-term memory files.

Mitigation: Use the skill only with documents approved for persistent notes, review generated memory entries before reuse, and avoid or remove MEMORY.md and memory/YYYY-MM-DD.md entries when retention is not appropriate.

Risk: Document-derived notes may lack confirmation, redaction, source labeling, or deletion controls.

Mitigation: Require explicit user confirmation before retaining sensitive notes, label notes with source document names and page or chapter positions, redact sensitive details, and provide a clear deletion path for progress and memory files.

## Reference(s):

- [Memory Integration Guide](references/memory_integration.md)
- [Quick Start Guide](references/quick-start.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, progress summaries, memory notes, JSON progress files, and optional extracted text files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write MEMORY.md, memory/YYYY-MM-DD.md, .document_learning_progress.json, .multi_doc_learning_progress.json, and user-specified extracted text outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
