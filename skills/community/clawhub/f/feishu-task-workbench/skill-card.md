## Description:

Feishu Task Workbench lets a Feishu/OpenClaw chat manage multiple named tasks with separate sessions, task switching, summaries, closing, and archival.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnhan98](https://clawhub.ai/user/shawnhan98)

### License/Terms of Use:

MIT-0

## Use Case:

Feishu/OpenClaw users use this skill to manage several independent workstreams from one chat window while keeping task state, routing, and summaries separate. It is intended for operational task control in environments that can grant the required cross-session capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires cross-session messaging and history access.

Mitigation: Install only in hosts where cross-session tools are intentionally allowed and scoped to the current user or workbench.

Risk: Task registry files store session routing identifiers and may expose them during status or summary operations.

Mitigation: Redact session keys and registry paths from normal user-facing replies, and reveal them only for explicit debugging.

Risk: Registry commands write local JSON task state.

Mitigation: Invoke the bundled registry helper with structured arguments and avoid shell interpolation of user-provided task titles or summaries.

## Reference(s):

- [Feishu Task Workbench](https://clawhub.ai/shawnhan98/skills/feishu-task-workbench)
- [Implementation Reference](artifact/references/implementation.md)
- [Single-Entry Multi-Task Workbench Protocol](artifact/references/protocol.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task replies should include a visible task header when routed to a concrete task.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
