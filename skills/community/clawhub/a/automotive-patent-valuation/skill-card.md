## Description:

Automotive Patent Valuation helps agents evaluate high-value automotive patents with a 14-factor model across technical, legal, and economic dimensions, mapped to SASAC high-value patent labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent, IP strategy, and automotive business users use this skill to screen and score automotive patents, benchmark competitors, review SASAC high-value patent label alignment, and produce portfolio action recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on authorized PatSnap/Zhihuiya MCP access for database-backed patent conclusions.

Mitigation: Confirm the required MCP tools are authorized before relying on live patent search, legal status, citation, family, award, license, transfer, or invalidation results.

Risk: Without the required MCP access, outputs may be limited to the scoring framework rather than evidence-backed patent valuations.

Mitigation: Treat framework-only outputs as preliminary guidance and avoid portfolio decisions until the underlying patent data is retrieved and reviewed.

## Reference(s):

- [High-Value Patent Evaluation Model v4.0](references/高价值专利评估模型_v4.0.md)
- [Zhihuiya Open Platform](https://open.zhihuiya.com/)
- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/automotive-patent-valuation)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables with narrative scoring notes and strategic recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live patent-data conclusions require authorized PatSnap/Zhihuiya MCP access; without that access, the skill can provide the scoring framework only.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
