## Description:

Orchestrate an evidence-backed patent-landscape program for product planning, R&D strategy, competitor intelligence, technology-route analysis, recommended patent packages, and portfolio planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

IP, R&D, product, strategy, and competitive-intelligence teams use this skill to scope patent-landscape questions, retrieve and de-noise patent evidence, design taxonomies, coordinate human tagging, and produce decision-ready landscape reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent-landscape findings could be mistaken for legal, FTO, infringement, validity, novelty, or enforceability opinions.

Mitigation: Keep legal conclusions out of scope, label legal and asset data as research signals, and route legal questions to qualified counsel.

Risk: Confidential project facts, patent pools, tags, or generated reports may expose sensitive business or R&D information.

Mitigation: Capture confidentiality constraints before retrieval, review generated project files before sharing, and remove unauthorized confidential columns from handoff artifacts.

Risk: Connector schemas, data coverage, or operations may be unavailable or differ from expected PatSnap services.

Mitigation: Inspect the live connector schema before tool calls, record retrieval provenance and limitations, and mark affected modules unavailable rather than simulating results.

Risk: Automated tagging or skipped checkpoint review could create unsupported taxonomy labels or false precision.

Mitigation: Require taxonomy approval, preserve the genuine human tagging handoff, and validate returned tagged files before evidence synthesis.

## Reference(s):

- [Query and Taxonomy Construction Methodology](references/query-and-taxonomy-methodology.md)
- [Patent Landscape HTML Report Blueprint](references/report-html-blueprint.md)
- [Scientific and Executive Visual Standard](references/report-visual-style.md)
- [Scenario: Industry Patent Landscape](references/scenario-industry-landscape.md)
- [Scenario: Technology Evolution](references/scenario-technology-evolution.md)
- [Scenario: Competitor Patent Profile](references/scenario-competitor-portrait.md)
- [Scenario: Technical Solution Deep Dive](references/scenario-solution-deep-dive.md)
- [Scenario: Curated Patent Package and Index](references/scenario-patent-package-and-index.md)
- [Scenario: Patent Asset and Risk Signals](references/scenario-asset-and-risk-signals.md)
- [Advanced Patent Search MCP Server](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [Patent Briefing MCP Server](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [Deep Patent Mining MCP Server](https://open.patsnap.com/marketplace/mcp-servers/patent-mining)
- [Global Core Patent Database MCP Server](https://open.patsnap.com/marketplace/mcp-servers/core-patents)
- [PatSnap MCP Marketplace](https://open.patsnap.com/marketplace/mcp-servers)
- [PatSnap Skill Hub](https://open.patsnap.com/marketplace/skill-hub)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON/CSV/HTML artifact specifications, and optional shell-command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce project deliverables such as search configuration, candidate pools, taxonomy artifacts, patent packages, tagged indexes, report manifests, and self-contained HTML reports when authorized data and connectors are available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
