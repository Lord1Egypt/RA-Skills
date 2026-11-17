## Description:

Provides a human-brain-inspired framework for organizing agent memory, reviewing learned information, checking retrieval, and considering memory safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

Release metadata: MIT-0; bundled LICENSE.md: MIT for .py code only, with methodology and documentation text all rights reserved

## Use Case:

Agent users and developers use this skill to structure learning and memory, decide what to retain, review stored information, and evaluate retrieval using a local synthetic benchmark.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad memory-writing and auto-loading instructions may expose or persist more information than intended.

Mitigation: Review and narrow allowed tools, trigger phrases, and filesystem disclosure before enabling persistent memory, task spawning, or automatic loading.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/ai-brain-learning-memory)
- [Research sources and evidence](references/调研出处与证据.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance and local synthetic benchmark results in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local benchmark scores six memory-chain dimensions on a 0–5 scale; it does not measure live agent memory.]

## Skill Version(s):

2.4.5 (source: server-resolved ClawHub release; bundled SKILL.md declares 2.4.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
