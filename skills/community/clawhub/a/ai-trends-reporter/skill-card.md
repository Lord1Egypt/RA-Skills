## Description:

Generates structured AI trends and ClawHub skill recommendation reports by searching current AI news and comparing available skills against the user's installed skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lixingxun](https://clawhub.ai/user/lixingxun)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and ClawHub users use this skill to create daily, weekly, or topical AI news briefs and discover high-rated ClawHub Skills they have not installed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses network search and requires a Brave Search API key; a ClawHub token may also be provided for more accurate skill ranking.

Mitigation: Install only if use of these credentials and external search services is acceptable, and avoid enabling recurring report workflows without confirmation.

Risk: The report may use installed OpenClaw skill names to tailor recommendations.

Mitigation: Review the generated report before acting on recommendations, especially before installing additional skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lixingxun/skills/ai-trends-reporter)
- [Brave Search API](https://brave.com/search/api/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with concise recommendations and optional shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prioritized ClawHub skill recommendations and installation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
