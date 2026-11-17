## Description:

Check transaction status on Hymatrix bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charles-lpd](https://clawhub.ai/user/charles-lpd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check Hymatrix bridge transaction status by transaction ID or hash and interpret bridge transaction fields such as type, asset flow, amount, fees, and current state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transaction hashes provided to the skill are sent to Hymatrix's bridge scan API.

Mitigation: Use the skill only when sharing the transaction hash with Hymatrix's API is acceptable.

Risk: The skill returns bridge status data from an external API that may be unavailable or may not contain the requested transaction.

Mitigation: Treat not-found responses as lookup failures and verify important transaction status through an independent source when needed.

## Reference(s):

- [Hymatrix bridge transaction lookup API](https://api-bridgescan-dev.hymatrix.com/bridgeTx/)
- [ClawHub skill page](https://clawhub.ai/charles-lpd/skills/check-hymx-transaction)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON transaction status response with agent-facing interpretation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns success/error status and, when found, Hymatrix bridge transaction metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
