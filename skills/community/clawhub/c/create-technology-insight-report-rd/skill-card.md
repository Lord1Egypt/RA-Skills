## Description:

Create or rigorously review a source-traceable HTML technology-insight report that integrates patents, scientific literature, market and company evidence, standards, regulation, engineering evidence, technology routes, competitive context, candidate evidence gaps, emerging applications, claim-relevance screening, technical options, and decision actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

R&D, strategy, product, and IP teams use this skill to create or audit a decision-ready technology-domain insight report that combines patent, scientific, market, company, standards, regulatory, and engineering evidence. It is suited for bounded claim-relevance screening and evidence-gap analysis, not legal opinions or automatic investment, safety, regulatory, clinical, or procurement recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential R&D, patent, company, regulatory, or market material could be exposed through external sources or patent connectors.

Mitigation: Confirm research authorization and confidentiality constraints before using external tools, and withhold sensitive material unless explicit user approval is documented.

Risk: Patent screening could be mistaken for infringement, freedom-to-operate, validity, enforceability, or patentability advice.

Mitigation: Keep claim review as preliminary technical screening, use not-legal-advice language, and route material questions to a qualified patent professional.

Risk: Sparse searches, connector limits, stale facts, or missing evidence could lead to overconfident report conclusions.

Mitigation: Use evidence IDs, search logs, count-unit labels, bounded non-observation language, contradiction review, and explicit evidence-gap states.

Risk: Generated HTML reports could retain placeholders, unsafe links, local paths, external runtime dependencies, or unsupported legal overclaims.

Mitigation: Run the bundled quality checks and manual release checklist before delivery, including structure, metadata, link/runtime, cleanliness, and legal-boundary gates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/create-technology-insight-report-rd)
- [Quality checklist](references/quality_checklist.md)
- [Section 4 patent-landscape coverage and claim-screening specification](references/s4_exhaustive_search_spec.md)
- [Cross-section evidence synchronization register](references/sync_table_template.md)
- [HTML skeleton template](references/html_skeleton_template.html)
- [PatSnap advanced patent search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap patent briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Self-contained HTML report, Markdown registers/checklists, Python QA command output, and concise handoff guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report outputs are structured around sections s0-s9, evidence IDs, search logs, source registers, review status, and bounded legal and specialist-review language.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
