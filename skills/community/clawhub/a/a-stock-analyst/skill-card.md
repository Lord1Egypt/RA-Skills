## Description:

A股智投大师 is an A-share investment research assistant for market quotes, fundamentals, stock screening, watchlist management, news monitoring, and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasxing1](https://clawhub.ai/user/lucasxing1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze China A-share stocks, screen candidates by financial or market criteria, review news and fundamentals, and manage watchlist or monitoring workflows. Outputs should be treated as informational investment research rather than financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation may automatically pull in several unreviewed dependency skills.

Mitigation: Review and approve the dependency skills before installation, especially mx-data, mx-search, mx-select-stock, mx-selfselect, and stock-monitor-skill.

Risk: The skill can change a user's watchlist through external API calls without a clear confirmation step.

Mitigation: Require explicit confirmation before adding, deleting, or monitoring watchlist entries, and review prompts that request those actions.

Risk: Investment analysis may rely on delayed or limited East Money API data.

Mitigation: Treat outputs as informational research only and verify market data against authoritative trading sources before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucasxing1/skills/a-stock-analyst)
- [East Money API endpoint used by the skill](https://mkapi2.dfcfs.com/finskillshub/api/claw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with optional code snippets, shell commands, configuration guidance, and API-backed data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use East Money API data and dependency skills for stock data, search, stock screening, watchlist management, and monitoring.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
