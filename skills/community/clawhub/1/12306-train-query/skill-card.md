## Description:

Queries China Railway 12306 train ticket availability for a requested departure station, arrival station, and travel date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuermos](https://clawhub.ai/user/fuermos)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to look up available trains, departure and arrival times, durations, and seat availability between supported 12306 stations for a specified date. The evidence describes availability lookup, not ticket purchase or credential handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live network requests disable HTTPS certificate validation, which can make ticket results and request data easier to tamper with.

Mitigation: Treat current output as untrusted and enable certificate validation before relying on results in production workflows.

Risk: Redirects are followed without restricting the destination host or protocol.

Mitigation: Constrain redirects to expected 12306 HTTPS hosts before operational use.

Risk: The server security guidance says the current release should not be used for ticket purchasing or real login/session credentials.

Mitigation: Use the skill only for availability lookup and do not provide real login, session, payment, or other sensitive credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fuermos/skills/12306-train-query)
- [fuermos Publisher Profile](https://clawhub.ai/user/fuermos)
- [China Railway 12306](https://www.12306.cn/mormhweb/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain terminal text with Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Displays train number, station names, departure and arrival times, trip duration, and seat availability when live 12306 data is returned.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
