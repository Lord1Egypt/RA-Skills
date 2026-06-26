## Description: <br>
Complete Ahrefs API integration for SEO analysis across Site Explorer, Keywords Explorer, Rank Tracker, Site Audit, SERP Overview, Batch Analysis, and Brand Radar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geozhu](https://clawhub.ai/user/geozhu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
SEO practitioners, marketers, and developers use this skill to query Ahrefs API data for keyword research, backlink analysis, competitor intelligence, technical audits, rank tracking, batch analysis, and brand monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ahrefs API token exposure through environment files, command output, chats, or tickets. <br>
Mitigation: Store a rotatable token in the workspace .env file with restrictive permissions, avoid commands that print the token, and do not paste token output into shared channels. <br>
Risk: Broad or batch analyses can consume Ahrefs API quota. <br>
Mitigation: Review large requests before running them, limit returned rows, select only needed columns, cache repeated results, and monitor Ahrefs usage limits. <br>
Risk: Requested features may be unavailable on the user's Ahrefs plan or may require pre-configured Ahrefs projects. <br>
Mitigation: Set AHREFS_API_PLAN to the actual subscription tier and confirm Rank Tracker or Site Audit projects exist before using those workflows. <br>


## Reference(s): <br>
- [Ahrefs API](https://ahrefs.com/api) <br>
- [Ahrefs API Documentation](https://ahrefs.com/api/documentation) <br>
- [Ahrefs API Usage Limits](https://app.ahrefs.com/account/limits-and-usage/web) <br>
- [Ahrefs API Endpoints Reference](references/api-endpoints.md) <br>
- [Ahrefs API Quick Reference](references/quick-reference.md) <br>
- [Keywords Explorer API Reference](references/keywords-explorer.md) <br>
- [Rank Tracker API Reference](references/rank-tracker.md) <br>
- [Site Audit API Reference](references/site-audit.md) <br>
- [Batch Analysis API Reference](references/batch-analysis.md) <br>
- [Brand Radar API Reference](references/brand-radar.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown with Bash and PowerShell examples plus JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Ahrefs subscription with API access; broad or batch analyses can consume Ahrefs API quota.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter, skill.json, CHANGELOG, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
