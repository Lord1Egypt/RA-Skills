## Description:

cairn gives agents and developers a local-first hybrid index for intentionally collected code, documents, web pages, PDFs, and raw text, combining full-text search, vector retrieval, and a knowledge graph in one SQLite database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrsirg97-rgb](https://clawhub.ai/user/mrsirg97-rgb)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use cairn to curate local knowledge sources and let an agent search, inspect graph relationships, answer with retrieved context, and maintain the index through CLI or MCP workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP ingest surface can persistently index unintended local or internal network data.

Mitigation: Use CAIRN_ALLOWED_ROOTS, run cairn in a contained account or directory, avoid adding untrusted URLs, and require host-side approval for MCP ingestion.

Risk: The path allowlist is defense-in-depth rather than a complete security boundary until symlink and refresh revalidation gaps are fixed.

Mitigation: Treat CAIRN_ALLOWED_ROOTS as an additional guard, keep indexed sources in a dedicated directory, and avoid relying on it as the only control for sensitive data.

Risk: Strict no-egress or air-gapped deployments can be affected by user-initiated web ingestion or first-use embedded model downloads.

Mitigation: Set CAIRN_OFFLINE=1, pre-cache required models before deployment, and use an embedded runtime configuration that references local model files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrsirg97-rgb/skills/cairn)
- [Source repository](https://github.com/mrsirg97-rgb/cairn)
- [npm package](https://www.npmjs.com/package/cairn-index)
- [Source skill definition](https://github.com/mrsirg97-rgb/cairn/blob/main/clawhub/SKILL.md)
- [Documentation](https://github.com/mrsirg97-rgb/cairn/tree/main/docs)
- [Design documentation](https://github.com/mrsirg97-rgb/cairn/blob/main/docs/design.md)
- [Graph documentation](https://github.com/mrsirg97-rgb/cairn/blob/main/docs/graph.md)
- [Setup documentation](https://github.com/mrsirg97-rgb/cairn/blob/main/docs/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured tool responses containing ranked text chunks, source metadata, graph entities, paths, tags, and setup commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on user-curated index contents and local runtime configuration.]

## Skill Version(s):

1.2.2 (source: frontmatter, agent.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
