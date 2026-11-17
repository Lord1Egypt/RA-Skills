## Description:

Context Memory Optimizer helps OpenClaw agents manage long sessions with workspace memory pointers, token-driven compaction steps, prompt-cache guidance, and multi-agent handoff templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donnieclaw](https://clawhub.ai/user/donnieclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to reduce context overflow, memory drift, and token waste in long OpenClaw sessions. It provides guidance for persistent local memory files, compaction checkpoints, prompt-cache segmentation, and multi-agent coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory and static agent prompt changes can retain sensitive project context or affect future agent behavior.

Mitigation: Install only after reviewing the snippets, keep a clear way to inspect and delete memory files, and do not paste continuation or pre-warming snippets into privileged prompts without review.

Risk: The skill can silently read files beyond its declared memory workspace during pre-warming behavior.

Mitigation: Restrict file reads to an approved project root and review file-access permissions before enabling the skill.

## Reference(s):

- [Compression Examples](artifact/references/compression-examples.md)
- [Prompt Cache Optimization](artifact/references/prompt-cache.md)
- [Context Memory Optimizer on ClawHub](https://clawhub.ai/donnieclaw/skills/context-memory-optimizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with code and configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operator-facing instructions and templates; it does not issue shell commands itself.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter reports content version 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
