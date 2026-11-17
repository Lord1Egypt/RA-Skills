## Description:

GEO Analyzer submits brand and category questions to Doubao, Kimi, and DeepSeek, analyzes AI-search visibility, sentiment, citations, and competitors, and produces an interactive HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External brand marketers, product managers, content operators, and brand PR teams use this skill to measure brand visibility, sentiment, citation sources, and competitor positioning across AI search answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand, competitor, category, and query data are sent through RedFox and the named AI search platforms.

Mitigation: Use only non-confidential inputs unless the user is comfortable with that data flow, and verify the API key source, scope, expiration, and revocation process before use.

Risk: Generated HTML reports can contain unsafe unescaped content.

Mitigation: Treat reports as untrusted HTML, open them in a controlled environment, and review escaping and URL handling before sharing or deploying generated reports.

Risk: The security summary flags misleading sentiment text in generated reports.

Mitigation: Validate sentiment summaries against the underlying AI answers and source citations before using them for business decisions.

## Reference(s):

- [GEO Metrics Reference](references/geo-metrics.md)
- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/geo-analyzer-redfox)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, HTML report, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON analysis files, and an interactive HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and sends brand, category, competitor, and query data through RedFox to Doubao, Kimi, and DeepSeek; generated files are written under output/.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
