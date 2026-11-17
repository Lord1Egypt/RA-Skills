## Description:

Use when booking or sweating a connecting flight: computes true connection budget from minimum-connect-time by airport/terminal, transfer logistics (trains, security re-entry), time-of-day delay stacking, and last-flight-of-day exposure. Verdicts SAFE / TIGHT / HIGH RISK plus a survive-the-layover protocol and rebooking rights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Travelers use this skill before booking or managing a connecting itinerary to assess layover risk, compare routing options, and plan what to do if a connection is missed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approximate planning scores may be mistaken for live flight predictions or current airport connection requirements.

Mitigation: Treat scores as estimates and confirm current terminal arrangements, minimum connection times, and rebooking terms with the airline.

Risk: A missed connection on separate tickets may leave the traveler without airline rebooking protection and facing a replacement fare.

Mitigation: Confirm whether the itinerary is one ticket or a self-transfer, allow a substantial buffer, and identify the cost and availability of a fallback before booking.

## Reference(s):

- [Connection model and airport transfer reference](references/connection-model.md)
- [ClawHub skill release](https://clawhub.ai/voronindenis5/skills/flight-connection-risk-analyzer)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Guidance]

**Output Format:** [Plain-text or JSON risk score and verdict with practical Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Planning estimates only; no live flight status or booking actions.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
