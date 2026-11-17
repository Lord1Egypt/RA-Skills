## Description:

Checks which tokens and chains are supported for cross-chain transfers on the Hymatrix network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charles-lpd](https://clawhub.ai/user/charles-lpd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to retrieve Hymatrix bridge token details, including supported chains, wrapped token identifiers, burn fees, and withdrawal limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A remote Hymatrix API response can direct follow-up cache requests to additional network destinations.

Mitigation: Review before installation in environments with access to internal services or cloud metadata, and restrict outbound requests to trusted Hymatrix hosts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charles-lpd/skills/check-hymx-info)
- [Hymatrix bridge information endpoint](https://api-bridgescan-dev.hymatrix.com/info)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON token list with bridge metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes chain identifiers, token identifiers, wrapped token identifiers, burn fees, fee recipients, and maximum burn amounts when available.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
