## Description:

Answer questions about code relationships in an indexed repository - callers, callees, impact, entry points, routes, DI wiring, dead code, cycles - using the code-crawler MCP server's SQLite property graph. Use when the question is about how symbols connect (who calls this, what breaks if I change it, where does a request enter, is this reachable) rather than about text you can find by searching. Do not crawl a repository just to answer a question about a single file you already have open.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nithin554](https://clawhub.ai/user/nithin554)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use the skill to answer structural questions about an indexed codebase, such as callers, execution paths, dependency wiring, and change impact. It helps distinguish relationship questions suited to the graph from questions better answered by reading or searching source text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command uses an unpinned npm package, so the package version may change between installs.

Mitigation: Review the package and release before installation, and pin a version when repeatable installs are needed.

Risk: The security analysis is partial because some path-like references could not be resolved.

Mitigation: Review the referenced paths and skill contents manually before installing or registering the MCP server.

## Reference(s):

- [Code Crawler project homepage](https://nithin554.github.io/code-crawler/)
- [Code Crawler on ClawHub](https://clawhub.ai/nithin554/skills/code-crawler)
- [Tool reference](artifact/reference/tools.md)
- [Edge semantics reference](artifact/reference/edge-semantics.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Natural-language text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Relationship findings should retain relevant confidence, external-target, and unresolved-edge caveats.]

## Skill Version(s):

0.1.83 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
