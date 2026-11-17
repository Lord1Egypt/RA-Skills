## Description:

每日新闻总结 fetches public news from BBC, SCMP, 36Kr, TechCrunch, The Verge, Microsoft, NVIDIA, and other listed sources to produce a four-section Chinese Markdown daily news report with original links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzcnyhhd](https://clawhub.ai/user/mzcnyhhd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate a Chinese daily briefing covering international news, China news, AI news, and AI technology company updates. It is also intended for optional recurring daily automation when the user wants scheduled news reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One configured BBC RSS source uses HTTP rather than HTTPS.

Mitigation: Review or replace that feed with an HTTPS source when available.

Risk: Fetched article text can contain inaccurate, stale, or untrusted content.

Mitigation: Keep source links in the report and review important items against the original publisher before relying on them.

Risk: Recurring automation may repeatedly fetch web sources and create files.

Mitigation: Enable scheduled runs only after confirming the expected cadence, storage location, and ongoing web access are acceptable.

## Reference(s):

- [News Sources Reference](references/news_sources.md)
- [ClawHub skill page](https://clawhub.ai/mzcnyhhd/skills/daily-news-summary)
- [Publisher profile](https://clawhub.ai/user/mzcnyhhd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Chinese Markdown report saved as a dated .md file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes generation time, source attribution, original URLs, a Top 5 section, and an information source table.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
