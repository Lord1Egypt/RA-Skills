## Description:

Helps agents search domestic Chinese flights, compare cabin prices and rules, create bookings, and manage ticket changes or refunds through Python command-line scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-zry](https://clawhub.ai/user/ryan-zry)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search flights, review cabin pricing and ticket rules, book domestic flights in China, view orders, cancel unpaid orders, and submit ticket change or refund requests.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill stores an API key and phone number locally.

Mitigation: Use private credential storage with restricted access, limit retention, and clear authentication state after use.

Risk: The workflow sends passenger PII to an external flight API and can print sensitive passenger details.

Mitigation: Collect only required data with user consent, mask PII in agent responses and logs, and avoid retaining command output.

Risk: The security evidence calls for review of transport and endpoint trust before installation.

Mitigation: Use verified TLS, review the external service endpoint, and run the skill only in controlled environments approved for booking data.

Risk: Scripts can submit booking, cancellation, change, and refund transactions.

Mitigation: Require explicit user confirmation immediately before each transactional command, including order identifiers, fees, and refund amounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-zry/skills/airticket)
- [Fenbeitong flight API endpoint](https://app-gate.fenbeitong.com/air_biz/skill/execute)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and plaintext table output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; stores authentication and seat-selection state in local JSON files; script output can include flight, fare, order, payment, change, refund, and passenger details.]

## Skill Version(s):

1.0.0 (source: release metadata, SKILL.md frontmatter, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
