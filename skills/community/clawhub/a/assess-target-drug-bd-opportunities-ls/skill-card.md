## Description:

Integrate target biology, disease rationale, drug pipeline, clinical, patent, scientific, regulatory, company, and transaction evidence for target or targeted-asset R&D and business-development decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

R&D, portfolio, and business-development teams use this skill to assess targets or targeted assets for initiation reviews, asset screens, partnering theses, landscape updates, and evidence-based go/no-go decisions. It helps separate sourced facts, analyst inference, assumptions, recommendations, uncertainty, and evidence gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential company, target, or asset materials may be used with external MCPs or sources available in the user's environment.

Mitigation: Confirm that the materials are approved for those services before retrieval or analysis.

Risk: Patent, legal, medical, financial, valuation, and regulatory outputs may be mistaken for specialist advice.

Mitigation: Use the report as planning support and require qualified specialist review before material decisions.

Risk: Pipeline, trial, patent-status, deal, guideline, and regulatory facts can change after the analysis cutoff.

Mitigation: Refresh dynamic evidence at the decision date and preserve source dates, retrieval dates, and verification status.

Risk: Incomplete pagination, source caps, or unavailable tools can create misleading coverage claims.

Mitigation: Report retrieved, deduplicated, analyzed, excluded, and missing counts by module, and label partial or unavailable coverage.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuanzhian-patsnap/skills/assess-target-drug-bd-opportunities-ls)
- [Deep 21-Section Target and Drug BD Report Specification](references/legacy-report-spec.md)
- [PatSnap Target Disease MCP](https://open.patsnap.com/marketplace/mcp-servers/target-disease)
- [PatSnap Drug Asset MCP](https://open.patsnap.com/marketplace/mcp-servers/drug-asset)
- [PatSnap Clinical Trials MCP](https://open.patsnap.com/marketplace/mcp-servers/clinical-trials)
- [PatSnap Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [PatSnap Scientific Translational Evidence MCP](https://open.patsnap.com/marketplace/mcp-servers/scientific-translational-evidence)
- [PatSnap Regulatory Guidelines MCP](https://open.patsnap.com/marketplace/mcp-servers/regulatory-guidelines)
- [PatSnap Current Awareness MCP](https://open.patsnap.com/marketplace/mcp-servers/current-awareness)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Markdown report by default; self-contained HTML when the deep report specification is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an executive recommendation, evidence register, coverage summary, evidence gaps, risks, and measurable go/no-go conditions.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
