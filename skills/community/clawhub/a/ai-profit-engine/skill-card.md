## Description: <br>
7x24 automated profit opportunity scanner for AI agents that scans ClawTasks, Moltbook, Polymarket, airdrops, GitHub bounty sources, and toku.agency for earning opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to monitor multiple online opportunity sources for potential bounties, market signals, airdrops, and service marketplace leads. It is intended for automated discovery and logging, not autonomous financial decision-making. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script embeds a third-party bearer token. <br>
Mitigation: Remove and rotate the token before use, and require credentials through environment variables or a secret manager. <br>
Risk: The skill runs shell and network behavior across multiple contacted services. <br>
Mitigation: Review and edit the script before installation, document each contacted service, and run it only in a constrained environment appropriate for the user. <br>
Risk: Wallet monitoring and hourly scheduling can create ongoing collection or retention concerns. <br>
Mitigation: Make wallet monitoring explicit and opt-in, and avoid hourly cron use until local scripts and log retention are understood. <br>


## Reference(s): <br>
- [AI Profit Engine on ClawHub](https://clawhub.ai/dagangtj/ai-profit-engine) <br>
- [ClawTasks open bounties API](https://clawtasks.com/api/bounties?status=open) <br>
- [Moltbook prediction markets feed](https://www.moltbook.com/api/v1/submolts/predictionmarkets/feed?sort=new&limit=5) <br>
- [Airdrops.io latest airdrops](https://airdrops.io/latest/) <br>
- [Boss.dev open issues](https://www.boss.dev/issues/open) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown instructions and timestamped log output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes opportunity summaries to logs/profit_engine.log and prints service-specific counts or parsing status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
