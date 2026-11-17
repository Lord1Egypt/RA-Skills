## Description:

AirnodeHub flight skill for live status, delays, cancellations, and airport boards via metered, attested AeroDataBox POST calls with approval and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metobom](https://clawhub.ai/user/metobom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer flight disruption questions with live flight status, delay, cancellation, route, gate, terminal, and airport board facts from approved AeroDataBox lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight queries and related parameters are sent to an external AeroDataBox endpoint and may incur metered charges.

Mitigation: State the planned operations and maximum call count, then require explicit approval before any POST request.

Risk: Flight status outputs could be misleading if stale, unsupported by returned data, or not cryptographically verified.

Mitigation: Report freshness, use only returned facts, calculate delays only from comparable returned timestamps, and state when attestation is not cryptographically verified.

## Reference(s):

- [AeroDataBox Airnode documentation](https://airnode-aerodatabox.fly.dev/)
- [ClawHub skill page](https://clawhub.ai/metobom/skills/flight-disruption-assistant)
- [Publisher profile](https://clawhub.ai/user/metobom)

## Skill Output:

**Output Type(s):** [Text, API calls, Guidance]

**Output Format:** [Markdown or plain text with sourced flight facts and explicit uncertainty]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bounded, user-approved POST call plans and reports only facts returned by the service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
