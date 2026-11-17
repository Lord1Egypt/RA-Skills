## Description:

Ahrefs Complete SEO Suite helps agents query Ahrefs API data for SEO analysis across site exploration, keyword research, rank tracking, technical audits, SERP review, batch analysis, and brand monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geozhu](https://clawhub.ai/user/geozhu)

### License/Terms of Use:

MIT

## Use Case:

Developers, SEO analysts, and marketing teams use this skill to prepare Ahrefs API requests, interpret SEO metrics, compare competitors, audit sites, research keywords, and monitor rankings or brand mentions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup and verification examples may expose an Ahrefs API token by printing .env contents or encouraging token use directly in shell commands.

Mitigation: Use a dedicated Ahrefs API token with minimum needed permissions, avoid pasting real tokens into commands, and skip examples that print credential files.

Risk: Relative JavaScript fetch examples could send the Ahrefs token or request data to an unintended host if reused without adjustment.

Mitigation: Replace relative fetch targets with explicit https://api.ahrefs.com/v3 URLs and review outbound requests before execution.

Risk: Submitted domains, URLs, and keywords are shared with Ahrefs, and batch mode can disclose many targets at once.

Mitigation: Review inputs for sensitivity before querying Ahrefs, especially for bulk analysis, and limit batches to data appropriate for the user's Ahrefs account and data-sharing expectations.

## Reference(s):

- [Ahrefs API Documentation](https://ahrefs.com/api/documentation)
- [Ahrefs API Account Settings](https://ahrefs.com/api)
- [ClawHub Skill Page](https://clawhub.ai/geozhu/skills/ahrefs)
- [Ahrefs API Endpoints Reference](references/api-endpoints.md)
- [Ahrefs API Quick Reference](references/quick-reference.md)
- [Keywords Explorer API Reference](references/keywords-explorer.md)
- [Rank Tracker API Reference](references/rank-tracker.md)
- [Site Audit API Reference](references/site-audit.md)
- [Batch Analysis API Reference](references/batch-analysis.md)
- [Brand Radar API Reference](references/brand-radar.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples, shell commands, API request guidance, and SEO analysis prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Ahrefs API endpoint suggestions, response interpretation, credential setup steps, plan-specific caveats, and cost or rate-limit guidance.]

## Skill Version(s):

1.2.0 (source: frontmatter, skill.json, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
