## Description:

Monitors Fliggy flight prices for one-way and round-trip itineraries, supports fare alerts, tracks price history, and guides scheduled searches through FlyAI CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuckonit](https://clawhub.ai/user/zuckonit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query current flight fares, monitor selected routes against a price threshold, record price history, and summarize fare trends for travel planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned global FlyAI CLI installation, so behavior can change when the CLI package changes.

Mitigation: Pin and audit the CLI version before deployment, and run `flyai search-flight --help` in the target environment to confirm supported flags.

Risk: Scheduled monitoring can persist travel routes, dates, thresholds, and fare history under `memory/flight-monitor/`.

Mitigation: Confirm where scheduled task data and history files are stored, limit retained travel details, and document how users can delete monitoring history.

Risk: The optional FlyAI API key could be exposed or over-scoped if configured casually.

Mitigation: Keep any API key scoped to the minimum required access, store it in the runtime's secret mechanism, and avoid printing it in logs or shared history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zuckonit/skills/flight-price-monitor)
- [Fliggy flights](https://www.fliggy.com/jipiao/)
- [FlyAI](https://open.fly.ai/)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [Airport codes reference](references/airport-codes.md)
- [Cron payload examples](references/cron-payload-examples.md)
- [Price history template](references/price-history-template.md)
- [Search flight parameters](references/search-flight-params.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with flight result tables, alert summaries, command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include booking links and persistent Markdown price-history entries when monitoring is configured.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
