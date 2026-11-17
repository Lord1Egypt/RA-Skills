## Description:

Audits a B2B website across technical SEO, content quality, competitor gaps, keyword opportunities, priority pages, execution planning, and KPI reporting, then produces Markdown and interactive HTML audit reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing teams, SEO consultants, and B2B site operators use this skill to diagnose organic search, content, competitive, keyword, and conversion-path gaps for a target website and to turn findings into a prioritized 90-day SEO plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may execute unsafe injected or third-party JavaScript when opened.

Mitigation: Treat generated HTML as untrusted, open reports in an isolated browser profile, and sanitize or escape website-derived content before sharing or publishing.

Risk: The HTML report template loads Chart.js from a remote CDN.

Mitigation: Remove the remote script or pin it with integrity controls before using reports in privileged or shared browser contexts.

Risk: The workflow fetches target and likely competitor websites during audits.

Mitigation: Audit only sites the user is comfortable fetching, avoid sensitive internal URLs, and disclose when findings rely on public web data or inferred metrics.

## Reference(s):

- [B2B SEO Audit Framework](references/seo-audit-framework.md)
- [B2B SEO KPI Framework & Reporting](references/kpi-framework.md)
- [ClawHub Skill Page](https://clawhub.ai/bettermen/skills/b2b-seo-audit)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, files, guidance]

**Output Format:** [Markdown report and interactive HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes technical and content findings, competitor gap tables, keyword opportunity maps, TOP 20 page priorities, a 90-day execution plan, and KPI reporting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
