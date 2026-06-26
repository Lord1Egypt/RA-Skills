## Description: <br>
cairn is a local-first hybrid indexing and retrieval skill for user-selected code, documents, web pages, PDFs, and raw text using FTS5 search, vector embeddings, and a SQLite-backed knowledge graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrsirg97-rgb](https://clawhub.ai/user/mrsirg97-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use cairn to curate a local retrieval index over intentionally selected project materials, then query passages, entities, tags, and graph paths through CLI or MCP tools. It is suited for local grounding and code or document exploration where the operator controls what enters the index. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local files are indexed into a local SQLite database and may be retrievable later by agents connected to the MCP server. <br>
Mitigation: Index only intended sources, isolate sensitive content with a separate dbPath, and connect only agents that should be able to query that index. <br>
Risk: Agent-driven ingestion can add local paths unless deployment controls restrict the allowed source locations. <br>
Mitigation: Set CAIRN_ALLOWED_ROOTS to approved absolute paths and rely on host-side approval for MCP add or refresh calls. <br>
Risk: Web ingestion and embedded-runtime model downloads can create network egress. <br>
Mitigation: Set CAIRN_OFFLINE=1 for strict or air-gapped deployments and pre-cache required models when using the embedded runtime. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrsirg97-rgb/cairn) <br>
- [Publisher profile](https://clawhub.ai/user/mrsirg97-rgb) <br>
- [npm package](https://www.npmjs.com/package/cairn-index) <br>
- [Project source link from skill metadata](https://github.com/mrsirg97-rgb/cairn) <br>
- [Design documentation](https://github.com/mrsirg97-rgb/cairn/blob/main/docs/design.md) <br>
- [Setup documentation](https://github.com/mrsirg97-rgb/cairn/blob/main/docs/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown responses from CLI and MCP tools, with shell commands and configuration examples in documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include ranked retrieval hits, indexed source lists, entity graph results, shortest paths, tag lists, and ingestion or refresh status summaries.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
