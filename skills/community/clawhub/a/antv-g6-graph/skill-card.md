## Description:

Generates AntV G6 v5 graph visualization code for network graphs, trees, flow charts, layouts, interactions, plugins, and common API-correct patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxfu1](https://clawhub.ai/user/lxfu1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to generate and review AntV G6 v5 graph visualization code, including correct initialization, data structures, layouts, behaviors, plugins, and examples for common graph patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated graph UI code may interpolate API, upload, database, or user data into innerHTML or tooltip HTML, creating script injection risk.

Mitigation: Review generated UI code before use, construct DOM with textContent where possible, or sanitize any rich HTML before rendering.

Risk: Examples may include external demo URLs or remote assets that are not appropriate for production environments.

Mitigation: Review external URLs and replace demo resources with approved application data sources or pinned internal assets.

Risk: Generated delete interactions may remove graph data without confirmation or recovery in real applications.

Mitigation: Add explicit confirmation, undo, or audit behavior before enabling destructive graph editing actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lxfu1/skills/antv-g6-graph)
- [G6 v5 graph visualization skill source](artifact/SKILL.md)
- [G6 graph basic usage](artifact/references/g6-graph-basic-usage.md)
- [G6 MDS layout cluster graph](artifact/references/g6-mds-layout-cluster-graph.md)
- [G6 graph initialization reference](artifact/references/core/g6-core-graph-init.md)
- [G6 data structure reference](artifact/references/core/g6-core-data-structure.md)
- [G6 Graph API reference](artifact/references/core/g6-core-graph-api.md)
- [G6 official graph documentation](https://g6.antv.antgroup.com/manual/graph/graph)
- [G6 official data documentation](https://g6.antv.antgroup.com/manual/data)
- [G6 official tooltip documentation](https://g6.antv.antgroup.com/manual/plugin/tooltip)

## Skill Output:

**Output Type(s):** [code, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and TypeScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on AntV G6 v5 API usage, graph data conventions, layouts, behaviors, plugins, and common error corrections.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
