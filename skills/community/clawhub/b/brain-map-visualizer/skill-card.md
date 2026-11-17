## Description:

Visualizes an agent's markdown vault and session journals as an interactive project-centric attention graph with categorized nodes, co-access edges, momentum fields, and directional flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highnoonoffice](https://clawhub.ai/user/highnoonoffice)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a local Brain Map view that turns markdown vault activity and session journals into a React/D3 project graph. It helps inspect attention patterns, co-access relationships, emerging projects, and graph data freshness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Networked API routes can expose journal-derived private data and rebuild actions if deployed without hardened access control.

Mitigation: Keep development localhost-only unless access control is added; for networked use, require a server-only secret, fail closed when auth is missing, and restrict rebuilds to trusted users.

Risk: Generated graph JSON can contain sensitive journal summaries and file-path metadata.

Mitigation: Review the generated JSON before sharing or publishing it, and scope WORKSPACE_DIR to the intended agent vault.

Risk: Putting access keys in client-exposed environment variables can leak the credential.

Mitigation: Use one server-only secret name consistently and avoid NEXT_PUBLIC variables for API access keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/highnoonoffice/skills/brain-map-visualizer)
- [Project homepage](https://github.com/highnoonoffice/hno-skills)
- [BrainMapProjects component](references/component.md)
- [Graph schema and API route](references/graph-schema.md)
- [Journal parser script](references/journal-parser.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with TypeScript, JavaScript, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local parser, Next.js API route, React/D3 component, and graph JSON guidance.]

## Skill Version(s):

3.3.6 (source: server release metadata; artifact frontmatter says 3.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
