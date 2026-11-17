## Description:

Use when an AI Agent needs to operate an llm-wiki knowledge base: ingest source files into Markdown wiki pages, answer questions from the wiki, run status, lint, link, relink, merge, query, index, and Zotero relocation tasks, preserve provenance and temporal metadata, or use Zotero as a literature-discovery layer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nemo4110](https://clawhub.ai/user/nemo4110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill to maintain a plain Markdown knowledge base, ingest source material with provenance, query wiki pages, and run helper commands for health checks, linking, indexing, and Zotero-backed literature workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation instructions include remote installer and Git-based install paths that may fetch mutable code.

Mitigation: Install from a pinned release or reviewed commit, and avoid copy-pasting remote installer pipes without review.

Risk: Zotero and MCP configuration can expose credentials or library access if handled carelessly.

Mitigation: Treat Zotero/MCP configuration as security-sensitive, avoid printing or committing credentials, and prefer memory-only authorization for write workflows.

Risk: Zotero writes may land through a different backend than the user selected.

Mitigation: Before enabling Zotero writes, verify the target library and write backend, then perform read-after-write verification against the intended backend.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nemo4110/skills/041-llm-wiki)
- [Karpathy llm-wiki inspiration](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Zotero MCP operating protocol](docs/ZOTERO_MCP_INTEGRATION.md)
- [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp)
- [uv documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, configuration examples, and generated or updated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing operational guidance and file changes in the user's local wiki workspace.]

## Skill Version(s):

1.5.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
