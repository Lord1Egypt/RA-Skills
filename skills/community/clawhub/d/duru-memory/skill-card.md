## Description:

Markdown-based memory continuity system for agents using local Markdown files as the primary memory source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durugy](https://clawhub.ai/user/durugy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain local Markdown memory files, run session start and close workflows, search memory deterministically, and optionally add local semantic recall through Ollama.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains durable local agent memory that may contain sensitive or stale information.

Mitigation: Keep credential and token material out of memory files, review memory contents periodically, and back up or inspect files before compaction or forgetting.

Risk: Some helpers can write outside the memory folder when given arbitrary paths.

Mitigation: Run helpers from a controlled workspace and restrict write targets to the intended memory directory.

Risk: Persistent memory content can be sent to a configurable HTTP endpoint for embedding, tagging, or compaction.

Mitigation: Keep Ollama bound to loopback unless a remote endpoint is explicitly trusted.

Risk: Runtime dependencies are declared without a lockfile in the artifact.

Mitigation: Pin dependencies with a lockfile before production use.

## Reference(s):

- [Duru Memory ClawHub page](https://clawhub.ai/durugy/skills/duru-memory)
- [Memory file templates](artifact/references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell command output, JSON summaries, configuration files, and Markdown memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update durable local memory files and a local semantic index under the workspace memory tree.]

## Skill Version(s):

0.1.0 (source: release evidence and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
