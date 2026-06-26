## Description: <br>
Flight Price Monitor helps agents search FlyAI/Fliggy airfare prices, set threshold alerts, schedule recurring checks, and maintain local price history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuckonit](https://clawhub.ai/user/zuckonit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and assistants use this skill to look up one-way or round-trip flight prices, monitor routes against a budget threshold, and summarize fare trends from repeated checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fare prices and availability can change between lookup and booking. <br>
Mitigation: Tell users that quotes are current at lookup time and that the booking page remains authoritative. <br>
Risk: Configured monitoring can over-poll third-party services or continue longer than intended. <br>
Mitigation: Use reasonable schedules, define stop conditions, and document how to pause or remove scheduled tasks. <br>
Risk: Optional API credentials may be configured for the external flight-search service. <br>
Mitigation: Use a limited API key when available and verify the npm package source before installation. <br>
Risk: Local price-history files can retain route and travel-date preferences. <br>
Mitigation: Store histories under the documented path and delete them when monitoring is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zuckonit/flight-price-monitor) <br>
- [FlyAI](https://open.fly.ai/) <br>
- [Fliggy Flights](https://www.fliggy.com/jipiao/) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [search-flight Parameters](references/search-flight-params.md) <br>
- [Price History Template](references/price-history-template.md) <br>
- [Cron Payload Examples](references/cron-payload-examples.md) <br>
- [Airport Codes](references/airport-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with fare tables, alert summaries, optional booking links, and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append price records to local Markdown history files when monitoring is configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
