## Description:

Cognitive Memory Temp sets up a multi-store agent memory system for recall, decay-based forgetting, reflection-based consolidation, semantic graph tracking, and auditable memory changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linbei2007](https://clawhub.ai/user/linbei2007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to initialize and configure persistent workspace memory for agents that need recall, knowledge graph organization, reflection cycles, and audit trails across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files may retain sensitive personal data or operational context longer than intended.

Mitigation: Install only in a dedicated workspace, avoid storing credentials or sensitive personal data, and review memory diffs before accepting changes.

Risk: Initialization and upgrade scripts create and modify workspace files and can initialize git audit tracking.

Mitigation: Review scripts before execution, run them only in the intended workspace, and inspect generated files and git changes before committing.

Risk: Forget behavior is described as soft archival, so removed memories may remain in git history or backups.

Mitigation: Treat forget as search hiding rather than secure deletion, and use separate data retention controls for information that must be erased.

## Reference(s):

- [Cognitive Memory Temp ClawHub Skill](https://clawhub.ai/linbei2007/skills/cognitive-memory-temp)
- [linbei2007 ClawHub Profile](https://clawhub.ai/user/linbei2007)
- [Architecture Reference](artifact/references/architecture.md)
- [Reflection Process Reference](artifact/references/reflection-process.md)
- [Routing Prompt Reference](artifact/references/routing-prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, shell command snippets, JSON configuration, and workspace memory template files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Initializes persistent memory files and provides reflection, routing, upgrade, and audit guidance for agent workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
