## Description:

Analyze a patent family from a patent identifier or PatSnap patent URL by defining the family scope, reconstructing priority and procedural relationships, comparing technical disclosures and claim focus, mapping themes, and generating a source-traceable offline HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External patent analysts, IP counsel, portfolio teams, R&D teams, competitive-intelligence teams, and due-diligence teams use this skill to map patent-family structure, relationships, jurisdictions, claim evolution, technical chronology, evidence limits, and follow-up review needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent-family analysis may be mistaken for legal advice or for an opinion on validity, enforceability, freedom to operate, or commercial value.

Mitigation: Use the report as evidence-bounded analysis and route legal conclusions or decision-critical interpretations to qualified patent counsel.

Risk: The workflow depends on PatSnap MCP services for patent retrieval and may expose patent identifiers or evidence to external patent-data connectors.

Mitigation: Confirm connector access, data-sharing authorization, and confidentiality requirements before retrieving or analyzing sensitive patent information.

Risk: Unavailable full text, stale legal status, or translation limits can affect family relationships, claim comparisons, and chronology.

Mitigation: Preserve evidence basis, cutoff dates, source locators, and unavailable states, then verify decision-relevant records with authoritative patent sources.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/yuanzhian-patsnap/skills/analyze-patent-family-ip)
- [PatSnap Patent Briefing MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [PatSnap Advanced Patent Search MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap Global Core Patent Database MCP server](https://open.patsnap.com/marketplace/mcp-servers/core-patents)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and normalized JSON for a self-contained offline HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local renderer consumes supplied normalized patent-family evidence, writes the requested HTML report, and does not retrieve patents or make network requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
