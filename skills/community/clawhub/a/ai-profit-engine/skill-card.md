## Description:

7x24 automated profit opportunity scanner for AI agents that scans ClawTasks, Moltbook, Polymarket, Airdrops, GitHub Bounties, and toku.agency for earning opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to scan multiple opportunity platforms for bounties, airdrops, prediction-market signals, and service marketplace leads. Operators can run the included shell scan to produce timestamped summaries of discovered opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An embedded third-party bearer token may expose credentials or authorize unintended Moltbook access.

Mitigation: Remove the embedded token before installation, rotate the exposed token, and require MOLTBOOK_API_KEY to be supplied through the runtime environment.

Risk: The scan script invokes an unpackaged Polymarket monitor script and assumes a workspace-specific path.

Mitigation: Package or remove that dependency and resolve script paths relative to the installed skill before execution.

Risk: Continuous scanning can send requests to external services and write logs without clear operator opt-in.

Mitigation: Add explicit opt-in controls for external services, credentials, logging, and any hourly scheduling before enabling recurring runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dagangtj/skills/ai-profit-engine)
- [Publisher profile](https://clawhub.ai/user/dagangtj)
- [ClawTasks open bounties API](https://clawtasks.com/api/bounties?status=open)
- [Moltbook prediction markets feed](https://www.moltbook.com/api/v1/submolts/predictionmarkets/feed?sort=new&limit=5)
- [Airdrops.io latest opportunities](https://airdrops.io/latest/)
- [Boss.dev open issues](https://www.boss.dev/issues/open)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command usage and timestamped log summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes timestamped scan summaries to logs/profit_engine.log when the shell script is executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
