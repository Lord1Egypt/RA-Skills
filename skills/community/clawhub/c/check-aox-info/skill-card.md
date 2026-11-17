## Description:

Looks up AOX bridge information for AO Network, including supported tokens, supported chains, and current deposit or withdrawal availability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charles-lpd](https://clawhub.ai/user/charles-lpd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer AO Network bridge questions, such as which tokens and chains are supported and whether deposits, withdrawals, or transfers are currently available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the external AOX public info API, so availability or response changes can affect answers.

Mitigation: Treat responses as current public status data and retry or verify externally when the API is unavailable or returns an error.

Risk: The skill may record lookup results to memory when considered important, which could retain status snapshots.

Mitigation: Only allow memory recording for non-sensitive public bridge status results.

## Reference(s):

- [check-aox-info ClawHub skill page](https://clawhub.ai/charles-lpd/skills/check-aox-info)
- [AOX public info API](https://api.aox.xyz/info)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON result data with agent-facing text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns closeServer availability flags and token metadata; errors are returned as JSON with success false.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
