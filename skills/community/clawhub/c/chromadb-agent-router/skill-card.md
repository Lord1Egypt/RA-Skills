## Description:

Local semantic message routing for multi-agent systems that routes messages to agents using ChromaDB embeddings, keyword scoring, and action verb context without external APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mars375](https://clawhub.ai/user/mars375)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add local intent routing to multi-agent systems, message buses, and command handling flows. It is suited for routing English and French messages to specialized agents while keeping routing data local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared or stale ChromaDB cache contents can affect routing behavior when route definitions change.

Mitigation: Use a private cache directory and clear or rebuild the cache when routes are updated.

Risk: Unpinned Python dependencies may change embedding or routing behavior across installs.

Mitigation: Pin and review the Python dependency chain before deployment in shared or security-sensitive systems.

Risk: Messages sent through the local API may contain sensitive content even though the router is designed for local operation.

Mitigation: Avoid sending sensitive messages through the API until cache location, model provenance, and deployment access controls are controlled.

## Reference(s):

- [Routing Research Notes](references/ROUTING-RESEARCH.md)
- [ChromaDB Agent Router on ClawHub](https://clawhub.ai/mars375/skills/chromadb-agent-router)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with Python, shell, and JSON examples; router API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local ChromaDB cache is persisted under /tmp/semantic_router_cache unless the cache directory is overridden.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
