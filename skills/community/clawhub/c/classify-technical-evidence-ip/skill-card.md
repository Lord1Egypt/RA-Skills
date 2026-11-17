## Description:

Builds, governs, and applies evidence-backed taxonomies for technical records such as patents, scientific literature, product records, and customer requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and technical taxonomy owners use this skill to design, confirm, and apply auditable labeling taxonomies over structured technical records while preserving evidence, review routing, and provenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source records may contain confidential, personal, licensed, privileged, or export-controlled text that should not be sent to PatSnap MCP services without authorization.

Mitigation: Confirm data-owner authorization before external enrichment, minimize transmitted fields, and keep sensitive records local unless specifically authorized.

Risk: Bundled validators can miss labeling quality issues that matter for business, legal, scientific, or customer decisions.

Mitigation: Treat validator results as helpful checks and require human review or stronger validation before relying on labeled outputs for important decisions.

## Reference(s):

- [Input and Output Contract](references/input-output-contract.md)
- [Workflow Modes](references/workflow-modes.md)
- [Default Decision Rules](references/default-decision-rules.md)
- [Taxonomy Design](references/taxonomy-design.md)
- [Quality and Review](references/quality-and-review.md)
- [PatSnap MCP Orchestration](references/zhihuiya-mcp-orchestration.md)
- [Advanced Patent Search](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [Deep Patent Mining](https://open.patsnap.com/marketplace/mcp-servers/patent-mining)
- [Patent Briefing](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [Scientific and Translational Evidence](https://open.patsnap.com/marketplace/mcp-servers/scientific-translational-evidence)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with optional CSV, YAML/JSON, and XLSX labeling artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source records and adds labeling, evidence, review, taxonomy backlog, QA, task metadata, and MCP provenance fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
