## Description:

Dual-brain memory skill for correction handling, rewrite quality, post-task reflection, and semantic recall of historical pitfalls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenni666](https://clawhub.ai/user/chenni666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to maintain correction-driven memory across sessions. It combines explicit Markdown rules with Pinecone semantic recall for prior corrections, reflections, errors, and historical pitfalls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Corrections, task summaries, and root-cause notes may be persisted to Pinecone and local cross-session memory.

Mitigation: Use a limited Pinecone key and a non-production namespace, keep secrets out of prompts and traces, and regularly review ~/dual-brain-memory-guardian/.

Risk: Untrusted or ambiguous corrections may be promoted into durable Markdown behavior rules.

Mitigation: Disable Markdown promotion for uncertain corrections and require explicit confirmation before treating durable or global rules as binding.

Risk: Stored memory may leak across projects or sessions if tenant, project, and domain scoping are not used carefully.

Mitigation: Keep metadata scoped by tenant, project, and domain, require explicit opt-in for cross-session patterns, and verify both local and vector deletion when forgetting data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenni666/skills/dual-brain-memory-guardian)
- [Publisher profile](https://clawhub.ai/user/chenni666)
- [Node.js download](https://nodejs.org/en/download)
- [Skill definition](artifact/SKILL.md)
- [Setup guide](artifact/setup.md)
- [Runtime operations](artifact/operations.md)
- [Security boundaries](artifact/boundaries.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON/configuration snippets, and generated local memory files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, and PINECONE_API_KEY; stores local memory under ~/dual-brain-memory-guardian and vector memory in Pinecone tenant namespaces.]

## Skill Version(s):

1.0.3 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
