## Description: <br>
Monitors Fliggy flight prices for one-way and round-trip travel, tracks price changes, and reminds users when fares fall below their thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nodermachine](https://clawhub.ai/user/nodermachine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel planners use this skill to check Fliggy fares, set recurring monitors for specific routes and dates, and receive low-price alerts with price history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring flight checks and price history can retain travel-monitoring details locally. <br>
Mitigation: Set a monitoring end date and delete old monitoring tasks and memory files when they are no longer needed. <br>
Risk: Browser automation may use a logged-in travel profile and can encounter site challenges or session-sensitive pages. <br>
Mitigation: Use a dedicated travel or browser profile where possible and review any manual verification prompts before continuing. <br>
Risk: Flight prices and availability can change quickly, so alerts and trend summaries may become stale. <br>
Mitigation: Confirm current fare, fees, and availability on the booking site before purchasing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nodermachine/fliggy-flight-monitor) <br>
- [Airport codes reference](references/airport-codes.md) <br>
- [Monitor configuration examples](references/monitor-config-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with JSON configuration examples and travel booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scheduled monitor configuration, price history entries, trend summaries, and booking links.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
