## Description:

A Stock Daily Review generates scheduled A-share market closing reports with market overview, portfolio tracking, technical analysis, sector review, watchlist ideas, and next-day action plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lkx161](https://clawhub.ai/user/lkx161)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can use this skill to prepare a daily A-share market review, monitor configured holdings, summarize technical signals, and draft next-day trading considerations. The generated report is informational and should not be treated as personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio holdings and cost-basis data may be sensitive because the configured portfolio is used in generated reports and may be delivered to WeChat.

Mitigation: Only configure portfolio data you are comfortable including in generated reports and downstream delivery channels.

Risk: Dependency skills can affect the market data, analysis, and generated recommendations.

Mitigation: Verify dependency skills before installation and prefer pinned or reviewed versions.

Risk: Generated market commentary and action plans may be inaccurate or unsuitable for a user's financial situation.

Mitigation: Treat outputs as informational analysis, review them before use, and do not rely on them as investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lkx161/skills/a-stock-daily-review)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with market summaries, portfolio tables, technical analysis, recommendations, and action-plan sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduled daily report intended for WeChat delivery after portfolio configuration.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
