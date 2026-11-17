## Description:

Reviews European patent application claims against EPC/EPO practice and returns structured findings on claim defects, legal and drafting risks, and concrete amendment options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent practitioners, inventors, and drafting teams use this skill to review European patent claims for EPC readiness, including clarity, support, sufficiency, added-matter, novelty/inventive-step positioning, unity, and amendment strategy. It is especially suited to Chinese or Europe-bound patent drafts where structured Chinese-language review and optional EPC-style wording suggestions are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential patent drafts, search queries, or related prosecution materials may be sent through configured PatSnap MCP services.

Mitigation: Use the skill only after confirming organizational approval for the connected PatSnap services and the specific patent materials being reviewed.

Risk: If PatSnap MCP services are not configured or authenticated, database-supported analysis and real-time retrieval may not be available.

Mitigation: Perform the documented MCP connectivity check before use and treat disconnected output as framework-only guidance.

Risk: Novelty and inventive-step comments can be incomplete when no prior-art search results or closest prior art are supplied.

Mitigation: Clearly label any review that lacks external prior-art search evidence and base conclusions on provided closest prior art or document content only.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/european-patent-claims-review)
- [PatSnap Open Platform](https://open.zhihuiya.com/)
- [PatSnap MCP server marketplace](https://open.zhihuiya.com/marketplace/mcp-servers)
- [PatSnap authentication guide](https://open.zhihuiya.com/devportal/guides/authentication)
- [PatSnap developer documentation](https://open.patsnap.com/devportal)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown with tables and structured Chinese-language review sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include claim-specific risk tables, grouped review comments, conservative/balanced/fallback amendment options, specification-alignment recommendations, and missing-information notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
