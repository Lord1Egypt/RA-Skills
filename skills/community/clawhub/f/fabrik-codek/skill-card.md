## Description:

Personal cognitive architecture that learns how you work, builds a knowledge graph from local sessions, profiles expertise, adapts retrieval per task, and self-corrects using outcome feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ikchain](https://clawhub.ai/user/ikchain)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to configure and operate Fabrik-Codek as a local MCP knowledge assistant for coding questions, semantic search, graph traversal, full-text search, and system health checks over their accumulated work context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release depends on an unpinned external Fabrik-Codek source install.

Mitigation: Audit or pin the external source before installation and before running the MCP server.

Risk: The skill can index Claude session transcripts and persistent local knowledge stores may contain sensitive derived content.

Mitigation: Review transcript directories before ingestion, avoid broad transcript indexing unless needed, and protect the generated ./data/ indexes as sensitive data.

Risk: Optional SSE transport could expose indexed local knowledge if bound beyond localhost.

Mitigation: Keep MCP transport on stdio or localhost-only unless firewall and access controls are explicitly configured.

## Reference(s):

- [Fabrik-Codek GitHub repository](https://github.com/ikchain/Fabrik-Codek)
- [Ollama](https://ollama.ai/)
- [Ollama model library](https://ollama.ai/library)
- [Meilisearch](https://meilisearch.com/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only skill output may include MCP configuration snippets, setup commands, and local usage guidance.]

## Skill Version(s):

1.10.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
