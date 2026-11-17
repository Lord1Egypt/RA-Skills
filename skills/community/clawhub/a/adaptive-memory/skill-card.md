## Description:

Hierarchical memory management for AI agents across sessions, maintaining daily notes, active context, and long-term memory with distillation from raw notes to curated knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yozu](https://clawhub.ai/user/yozu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up local workspace memory so agents can resume work across sessions, record decisions, and periodically distill daily notes into long-term memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace memory files can retain private operational context across sessions.

Mitigation: Review what is written to memory files, avoid storing secrets or credentials, and keep memory files out of public repositories when they contain private context.

Risk: Automated distillation can promote stale or incorrect daily notes into long-term memory.

Mitigation: Prefer manual or clearly user-approved distillation, and review long-term memory updates before relying on them.

## Reference(s):

- [Distillation Guide](references/distillation-guide.md)
- [Adaptive Memory ClawHub Page](https://clawhub.ai/yozu/skills/adaptive-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local workspace memory files such as MEMORY.md and files under memory/ when the initialization workflow is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
