## Description:

BTC and ETH market monitor with public API data, six bottom-fishing signals, and optional Discord delivery. TalentverseX

This skill is ready for commercial/non-commercial use.

## Publisher:

[liammme](https://clawhub.ai/user/liammme)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to generate lightweight BTC/ETH market summaries, oversold-signal checks, and optional Discord alerts from public market APIs. Outputs are informational and are not trading advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional cron installer can create persistent scheduled execution from unvalidated config.

Mitigation: Avoid scripts/setup_cron.sh unless the config and resulting cron entry have been inspected and the operator is prepared to remove the entry manually.

Risk: Optional Discord delivery sends the generated market report to a configured Discord channel using a bot token from the environment.

Mitigation: Enable Discord only after verifying the destination channel, bot permissions, and environment token handling.

Risk: The report depends on public market APIs and includes heuristic indicators such as an approximate MVRV proxy.

Mitigation: Treat the output as informational, verify important market data independently, and do not use it as trading advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liammme/skills/btc-monitor-talentversex)
- [Skill definition](artifact/SKILL.md)
- [Runtime docs](artifact/docs/README.md)
- [Troubleshooting](artifact/docs/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text market report with optional Discord messages and setup shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report includes BTC/ETH indicators, signal counts, coarse recommendations, and notes that outputs are informational only.]

## Skill Version(s):

4.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
