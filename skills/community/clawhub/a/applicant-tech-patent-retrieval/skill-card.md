## Description:

Guides applicant-first, technology-limited patent retrieval by expanding applicant entities, defining topic boundaries, building PatSnap/Zhihuiya search formulas, deduplicating by application or simple family, and producing Markdown or Word retrieval reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent analysts, IP teams, and agent developers use this skill to run structured patent searches for a specified applicant within a confirmed technology topic. It is suited to formula-only strategy work and executed retrieval workflows that produce deduplicated datasets and traceable reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent queries, result data, and generated reports may flow through configured PatSnap/Zhihuiya MCP services.

Mitigation: Review MCP permissions and API-key setup before use, and only process data approved for those services.

Risk: The workflow uses fixed Chinese templates and PatSnap/Zhihuiya terminology that may not fit every locale.

Mitigation: Verify output language, field labels, and formula syntax before using the results in English or other non-Chinese workflows.

Risk: Skipping applicant, topic, or gate confirmation can produce overbroad, underbroad, or premature patent search formulas.

Mitigation: Require the visible pre-retrieval validation package and user confirmation before final formulas, retrieval, deduplication, or report completion.

## Reference(s):

- [Applicant Retrieval Workflow](references/applicant-retrieval-workflow.md)
- [Topic Limitation Workflow](references/topic-limitation-workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/yuanzhian-patsnap/skills/applicant-tech-patent-retrieval)
- [PatSnap/Zhihuiya MCP Service Marketplace](https://open.zhihuiya.com/marketplace/mcp-servers)
- [PatSnap/Zhihuiya Authentication Guide](https://open.zhihuiya.com/devportal/guides/authentication)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, files]

**Output Format:** [Markdown reports, PatSnap/Zhihuiya search formulas, optional Word reports, and representative patent datasets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-confirmed applicant and topic gates before final formulas or retrieval; executed retrieval depends on configured PatSnap/Zhihuiya MCP services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
