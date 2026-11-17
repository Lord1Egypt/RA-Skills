## Description:

Allows users to check the status of a blockchain transaction by submitting a TxId. Queries the AOX transaction API and returns human-readable results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charles-lpd](https://clawhub.ai/user/charles-lpd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up AOX blockchain transaction status from a transaction ID and receive a readable summary of status, amount, parties, confirmations, and timestamps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transaction identifiers submitted for lookup are sent to AOX's public API.

Mitigation: Avoid checking transaction IDs when you do not want that lookup visible to the API provider.

## Reference(s):

- [AOX Transaction API](https://api.aox.xyz/docs)
- [AOX](https://aox.xyz)
- [ClawHub skill page](https://clawhub.ai/charles-lpd/skills/check-transaction)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Markdown, Guidance]

**Output Format:** [Human-readable text or Markdown summarizing API JSON fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl when issuing shell-based lookup commands; no API key is required by the documented endpoint.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
