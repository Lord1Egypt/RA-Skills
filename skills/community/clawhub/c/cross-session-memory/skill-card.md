## Description:

Cross-session-memory helps agents maintain persistent long-term memory across conversations using human-readable Markdown notes, a local SQLite recall index, and lint checks for broken links, duplicates, and stale project facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharinchan233](https://clawhub.ai/user/sharinchan233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add local, file-based long-term memory to bots or agents. It supports selective recall, human-readable memory editing, and routine memory hygiene checks across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory notes may contain credentials, unrelated private documents, or sensitive personal data that become searchable through the local index.

Mitigation: Use a dedicated memory directory and review notes before indexing them; do not place sensitive data there unless it is intentionally part of agent memory.

Risk: Stale project facts can mislead an agent when file paths, functions, flags, or project assumptions have changed.

Mitigation: Run the included lint check and verify stale project facts before applying recalled information.

Risk: Duplicate or broken-linked memory entries can reduce recall quality and create conflicting context.

Mitigation: Use the included lifecycle checks for duplicate descriptions and unresolved wiki-style links before relying on recalled memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sharinchan233/skills/cross-session-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and local file conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Markdown files as the source of truth and a rebuildable SQLite index for recall.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
