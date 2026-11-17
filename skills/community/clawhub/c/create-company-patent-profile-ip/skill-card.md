## Description:

Creates an evidence-backed executive patent-strategy report for a company, covering portfolio position, product context, technical strengths, competition, market opportunities, risks, recommendations, and optional PatSnap solution alignment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Executives, strategy teams, R&D leaders, and IP teams use this skill to produce a decision-ready patent-strategy profile grounded in patent, literature, standards, policy, company, and market evidence. The skill is intended for evidence-bound analysis where unsupported claims are labeled as unverified rather than presented as findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process confidential company materials supplied by a user.

Mitigation: Use only approved tools and workspaces for confidential data, and avoid providing confidential inputs unless the environment is authorized for that data.

Risk: Patent records can be misread as proof of product performance, capacity, revenue, deployment, market size, regulatory compliance, partnerships, or pricing.

Mitigation: Bind material claims to the required evidence type and label unsupported claims as Unverified with owner, required evidence, and validation date.

Risk: Optional PatSnap solution alignment can become unsupported commercial positioning if current approved materials are not supplied.

Mitigation: Include solution alignment only when requested and supported by approved current materials; omit or label source-era commercial claims as unverified.

## Reference(s):

- [Advanced Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/create-company-patent-profile-ip)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Self-contained HTML report with supporting evidence register and source notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill expects scoped company, competitor, jurisdiction, reporting-period, evidence-cutoff, counting-unit, and authorized-source inputs before analysis.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
