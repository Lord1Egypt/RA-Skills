## Description:

AB-Directolog-Skill helps an agent automate Yandex.Direct campaign management, reporting, bid analysis, and optimization through the Yandex.Direct API v5.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexburrstudio](https://clawhub.ai/user/alexburrstudio)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, agencies, and developers use this skill to let an agent inspect Yandex.Direct campaigns, request performance reports, manage bids and keywords, and prepare optimization recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent live Yandex.Direct account authority through OAuth credentials.

Mitigation: Use restricted OAuth credentials, test first on non-production or low-budget accounts, and review account access before enabling campaign changes.

Risk: Mutating examples can create or alter live advertising campaigns if run casually.

Mitigation: Review every mutating command before execution and separate read-only reporting workflows from campaign creation or bid-change workflows.

Risk: OAuth tokens or refresh responses could be exposed in markdown memory or logs.

Mitigation: Keep tokens in environment variables or a secret store, avoid saving OAuth responses in memory files, and redact command output before logging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexburrstudio/skills/ab-directolog-skill)
- [Yandex.Direct token documentation](https://yandex.ru/dev/direct/doc/ru/token)
- [Yandex OAuth](https://oauth.yandex.com)
- [Yandex developer projects](https://developer.tech.yandex.ru/projects)
- [Yandex.Direct dashboard](https://direct.yandex.ru)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline shell commands, JSON request examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Yandex.Direct API requests, reports, campaign recommendations, and token setup instructions.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
