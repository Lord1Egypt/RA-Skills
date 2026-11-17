## Description:

Monitors Fliggy flight prices for one-way and round-trip routes, tracks price history, and alerts users when fares fall below configured thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nodermachine](https://clawhub.ai/user/nodermachine)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and agents use this skill to query Fliggy fares, set recurring price monitors for planned trips, and receive low-price alerts with route, fare, trend, and booking-link details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring background fare checks can continue longer or more frequently than intended.

Mitigation: Confirm monitor schedules, thresholds, and end conditions explicitly before enabling a monitor.

Risk: Trip details and price history may be stored locally as monitor records.

Mitigation: Review what trip information is being recorded and delete monitor records when they are no longer needed.

Risk: Automation may use a logged-in browser profile for Fliggy sessions.

Mitigation: Use a dedicated browser profile and avoid sharing broader browsing sessions with the monitor.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nodermachine/skills/fliggy-flight-monitor)
- [Fliggy flights](https://www.fliggy.com/jipiao/)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [Airport codes reference](references/airport-codes.md)
- [Monitor configuration examples](references/monitor-config-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown responses with fare tables, price trend summaries, alert text, booking links, and JSON monitor configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recurring monitor schedules, threshold alerts, and local price history summaries.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
