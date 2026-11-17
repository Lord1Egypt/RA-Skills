## Description:

Find nearby banks. Invoke when user asks for bank branches near me.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawkk](https://clawhub.ai/user/clawkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to answer nearby-bank requests with a consistent point-of-interest query shape, including location, radius, result limit, and optional filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Nearby-bank lookup requires approximate or precise location data.

Mitigation: Ask for explicit location permission and avoid retaining exact coordinates; use coarse or grid-based location when feasible.

Risk: The referenced STANDARD_RESPONSE.md file is not included in the package, so response shape may depend on host conventions.

Mitigation: Confirm the expected point-of-interest response schema in the host environment before relying on integrations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawkk/skills/banks)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Text guidance with structured point-of-interest response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-authorized location; supports radius, result limit, and optional filters.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
