## Description:

Atlas Flight Booking helps agents authorize Atlas, search and compare exact or flexible-date flights, verify fares, choose supported baggage or seats, create and pay for orders, and check ticketing status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlas-doc](https://clawhub.ai/user/atlas-doc)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent to search exact or flexible-date flights, compare suitable offers, and continue through Atlas booking with explicit checkpoints for authorization, price increases, seat fallback, and payment approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags that the skill can automatically install or replace local executable tooling from remote sources.

Mitigation: Review before installing, and prefer preinstalling uv and atlas-flight-booking from trusted sources or running the skill only where automatic tool installation is acceptable.

Risk: The skill handles flight payments and passenger details.

Mitigation: Require explicit payment approval, avoid saving or echoing passenger data, and never retry order creation or payment after uncertain results.

## Reference(s):

- [Safe Booking Workflow](references/booking-workflow.md)
- [Atlas Flight Booking CLI Contract](references/cli-contract.md)
- [Atlas Error Handling](references/error-handling.md)
- [Passenger Input](references/passenger-input.md)
- [Price Query and Comparison Documentation](https://resources.atriptech.com/api-wen-dang/api-reference/booking-apis/price-compare-search#price-compare-search)
- [uv Installation Documentation](https://docs.astral.sh/uv/getting-started/installation/)
- [ClawHub Skill Page](https://clawhub.ai/atlas-doc/skills/atlas-flight-booking)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with CLI command execution and normalized flight-booking status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses JSON CLI envelopes internally and presents only normalized fields to the user.]

## Skill Version(s):

0.3.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
