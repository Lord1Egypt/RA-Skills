## Description:

Hermes-optimized human-like memory system with semantic search, auto-promotion, conflict resolution, and direct integration with the Hermes memory tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cliftonwknox](https://clawhub.ai/user/cliftonwknox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Hermes agent operators use this skill to maintain durable, contextual memory across conversations, including semantic retrieval, memory promotion, and conflict handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation history may be stored, indexed, and retrieved without sufficiently explicit consent boundaries.

Mitigation: Define what may be remembered before enabling the skill and require confirmation for inferred memories.

Risk: Sensitive secrets or regulated personal data could be written into durable memory files or vector indexes.

Mitigation: Prohibit storage of secrets and regulated personal data, and review memory entries before promotion.

Risk: Stored memories may become stale, conflicting, or difficult to remove across daily files, MEMORY.md, conflict logs, Hermes memory, and vector indexes.

Mitigation: Maintain clear inspection and deletion procedures for every memory location and resolve conflicts before relying on retrieved memories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cliftonwknox/skills/elite-human-memory-hermes-optmized)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [INTEGRATION.md](artifact/INTEGRATION.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown memory files, conflict logs, retrieval guidance, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local memory files, conflict logs, and vector indexes when the host agent has the required file and embedding capabilities.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
