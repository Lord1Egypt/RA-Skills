## Description:

Tracks earnings calendars and news for technology and AI companies, generates summary reports, and supports scheduled alerts for tracked symbols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newaiguy](https://clawhub.ai/user/newaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check upcoming earnings events, retrieve recent earnings news for individual or tracked companies, and generate concise earnings summaries. It is informational and is not a source of investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the skill can send company symbols and fetched financial text to Tavily and, by default, BigModel/GLM for translation.

Mitigation: Run it only where this data sharing is acceptable, configure the intended provider keys explicitly, and use --no-translate when translation is not needed.

Risk: The security evidence reports that an OPENAI_API_KEY fallback can silently be used with the BigModel/GLM translation endpoint.

Mitigation: Use only ZAI_API_KEY for translation, avoid running in environments containing OPENAI_API_KEY, or remove the fallback before deployment.

Risk: The security evidence reports an unused Playwright dependency.

Mitigation: Remove or pin the dependency before production use and review the resulting package lock or install plan.

Risk: The skill summarizes financial news and may produce incomplete or misleading financial interpretation.

Mitigation: Treat outputs as informational only, review source links and official filings before making financial decisions, and preserve the documented no-investment-advice posture.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/newaiguy/skills/ai-earnings-alert)
- [Publisher profile](https://clawhub.ai/user/newaiguy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text, Markdown summaries, and optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Tavily API key for search; translation is optional and can be disabled with --no-translate.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
