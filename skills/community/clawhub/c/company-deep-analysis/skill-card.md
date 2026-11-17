## Description:

Analyzes A-share and Hong Kong-listed companies from a company name or stock code, producing company profile, industry structure, moat, financial, and relative valuation analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pm2-567](https://clawhub.ai/user/pm2-567)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users, analysts, investment managers, and researchers use this skill for preliminary research on A-share and Hong Kong-listed companies, including company profiling, competitive analysis, financial review, and valuation context. The generated analysis is for informational pre-screening and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local Python scripts, makes public web/API requests for the supplied company or stock code, and creates report files.

Mitigation: Run it in an isolated environment, pin dependencies where practical, and review generated files before using or sharing them.

Risk: Generated investment analysis may be incomplete, stale, or misleading if source data is unavailable, delayed, or interpreted incorrectly.

Mitigation: Treat outputs as informational pre-screening, verify material claims against authoritative sources, and avoid using the report as standalone investment advice.

Risk: Company names, stock codes, watchlists, or research prompts may reveal sensitive investment interests.

Mitigation: Avoid entering proprietary watchlists, confidential research context, or other sensitive business information unless the execution environment is trusted.

## Reference(s):

- [AI Internal Rules](references/ai-internal-rules.md)
- [Financial Analysis Guide](references/financial-analysis-guide.md)
- [Moat Analysis Framework](references/moat-analysis-framework.md)
- [Porter Five Forces Template](references/porter-five-forces-template.md)
- [Valuation Methods](references/valuation-methods.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML, Files, Shell commands, Guidance]

**Output Format:** [Markdown reports, HTML briefing cards, and optional JSON data outputs from local scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports full deep-analysis, financial-only, and company-profile-only modes; creates local report files and temporary market data files.]

## Skill Version(s):

1.0.12 (source: frontmatter and changelog, released 2026-08-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
