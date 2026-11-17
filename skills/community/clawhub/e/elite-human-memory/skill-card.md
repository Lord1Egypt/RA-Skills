## Description:

Portable Clawhub-compatible human-like memory system with layered storage (Working/Episodic/Semantic + optional Vector index), rich metadata schema, auto-promotion heuristics, conflict detection & resolution, and semantic retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cliftonwknox](https://clawhub.ai/user/cliftonwknox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add persistent, layered memory to LLM agents, including episodic notes, curated semantic memory, conflict tracking, and optional vector-based retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad automatic long-term storage and reuse of user context.

Mitigation: Configure narrow storage paths and scopes, require explicit user consent for writes beyond direct remember-this requests, and provide review/delete controls before scheduled maintenance or automatic promotion.

Risk: Sensitive information may be exposed if optional vector storage is external or loosely governed.

Mitigation: Avoid external vector stores for sensitive data unless governance is in place, and keep memory storage scoped to the intended agent and user context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cliftonwknox/skills/elite-human-memory)
- [README](artifact/README.md)
- [Integration Examples](artifact/INTEGRATION.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with storage layout, behavioral triggers, and integration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory-management instructions for the host agent; persistent storage paths and optional vector index are configured by the integrator.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact docs state 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
