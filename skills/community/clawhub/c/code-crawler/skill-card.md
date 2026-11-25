## Description:

Answer questions about code relationships in an indexed repository, including callers, callees, impact, entry points, routes, dependency injection, dead code, and cycles, using the code-crawler MCP server's property graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nithin554](https://clawhub.ai/user/nithin554)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to answer questions about how symbols connect across an indexed codebase, such as what calls a method, what a change may affect, or where a request enters. It guides them to use text search or direct file reading when a graph query is not appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses unversioned npm packages, and the security analysis was partial because some references were unresolved.

Mitigation: Review the setup, package versions, unresolved references, and resulting client configuration before enabling the server.

## Reference(s):

- [Project homepage](https://nithin554.github.io/code-crawler/)
- [ClawHub skill listing](https://clawhub.ai/nithin554/skills/code-crawler)
- [Tool reference](reference/tools.md)
- [Edge semantics reference](reference/edge-semantics.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Code, Configuration, Shell commands]

**Output Format:** [Natural-language analysis and guidance, with optional Mermaid or Graphviz graph text, code examples, shell commands, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers depend on the indexed repository and may describe static-analysis confidence or unresolved relationships where relevant.]

## Skill Version(s):

0.1.87 (source: server-resolved release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
