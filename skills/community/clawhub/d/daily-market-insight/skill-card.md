## Description:

Daily Market Insight automates daily market news collection, analysis, trend forecasting, and Feishu report publication using a multi-agent workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a851445115](https://clawhub.ai/user/a851445115)

### License/Terms of Use:


## Use Case:

Market analysts, finance teams, and agents use this skill to collect daily macroeconomic, technology, geopolitical, and commodities news, summarize sentiment and market impact, forecast trends for A-share, Hong Kong, and U.S. markets, and publish a Feishu report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically publish financial analysis to Feishu with limited user-control details.

Mitigation: Use it only in Feishu spaces and groups where automated publication is approved, and review recipient settings before enabling unattended runs.

Risk: The workflow asks the agent to run local opencode CLI commands and initialize git in the working directory.

Mitigation: Run it in an approved workspace where opencode CLI execution and local git initialization are allowed.

Risk: The generated market analysis includes forecasts and investment suggestions based on collected news.

Mitigation: Treat outputs as informational analysis, preserve the skill's investment-disclaimer posture, and require human review before financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a851445115/skills/daily-market-insight)
- [Publisher profile](https://clawhub.ai/user/a851445115)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown market report, Feishu document content, group message text, and inline shell command.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduled daily at 10:00 when configured; creates local report and log files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
