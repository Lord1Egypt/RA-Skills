## Description:

Cognitive Memory helps agents set up a persistent multi-store memory system with episodic, semantic, procedural, and core stores, decay-based recall, reflection cycles, knowledge graphs, and audit trails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icemilo414](https://clawhub.ai/user/icemilo414)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add persistent memory to a ClawHub or OpenClaw workspace, including setup, memory routing, reflection approval, and audit-tracked memory updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent workspace memory can retain sensitive, stale, or misleading information across future agent sessions.

Mitigation: Install only when persistent memory is desired, review and narrow the AGENTS.md memory block before use, and keep user approval gates for reflection and memory changes.

Risk: The init and upgrade scripts create or modify workspace files and may initialize git and commit current files.

Mitigation: Inspect the scripts before running them and avoid executing them in repositories with unrelated uncommitted changes or secret files.

Risk: Shared memory access and external memorySearch provider settings can broaden exposure of stored memory content.

Mitigation: Avoid broad sub-agent memory access and inspect memorySearch provider settings before enabling external indexing.

## Reference(s):

- [Cognitive Memory ClawHub Page](https://clawhub.ai/icemilo414/skills/cognitive-memory)
- [Architecture Reference](references/architecture.md)
- [Reflection Process](references/reflection-process.md)
- [Routing Prompt](references/routing-prompt.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and generated memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates workspace memory files; reflection output is gated by user approval and capped by documented token budgets.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
