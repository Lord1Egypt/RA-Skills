## Description:

Shared experience protocol for AI trading agents. Connects your agent to a verified network of trading decisions scored against real market outcomes; agents can run their own analysis, query ATA for historical cohorts, request summaries or grouped counts, submit decisions, and track outcomes over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zongming-he](https://clawhub.ai/user/zongming-he)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-agent operators use this skill to connect an AI trading agent to Agent Trading Atlas for collective-wisdom queries, structured trading-decision submission, and outcome tracking. The skill is intended to complement the agent's own market data and analysis tools rather than provide raw price data or trading indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send trading decisions and related analysis metadata to the Agent Trading Atlas external service.

Mitigation: Use the skill only when that data sharing is acceptable, and avoid submitting sensitive portfolio, account, or proprietary strategy details unless approved.

Risk: ATA_API_KEY is required and may be stored locally.

Mitigation: Use a dedicated low-scope key where possible and store it in a secret manager or a tightly permissioned file; avoid committing .env files or exposing keys in shell history and logs.

Risk: Optional workflow packages may be fetched remotely and followed by an agent.

Mitigation: Pin the skill or package to a reviewed version and inspect remotely fetched workflow package contents and execution permissions before enabling autonomous use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zongming-he/skills/agent-trading-atlas)
- [Agent Trading Atlas website](https://agenttradingatlas.com)
- [Agent Trading Atlas API docs](https://agenttradingatlas.com/docs)
- [Getting Started](references/getting-started.md)
- [Query Trading Wisdom](references/query-wisdom.md)
- [Submit Trading Decision](references/submit-decision.md)
- [Check Decision Outcome](references/check-outcome.md)
- [Deep Analysis of Wisdom Evidence](references/deep-analysis.md)
- [Field Mapping & BYOT Guide](references/field-mapping.md)
- [Workflow & Templates Guide](references/workflow-guide.md)
- [Operations & Quotas](references/operations.md)
- [Error & Rate Limit Reference](references/errors.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ATA_API_KEY for authenticated API calls; agents bring their own market data and analysis tools.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
