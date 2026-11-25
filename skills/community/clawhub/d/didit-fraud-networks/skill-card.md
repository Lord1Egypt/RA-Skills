## Description:

Use when writing backend or API-key integration code for Didit Fraud Networks (fraud ring detection). Use when the user wants to detect fraud rings, multi-accounting or identity fraud clusters, list networks of users, businesses or transaction parties linked by a shared device, IP address, face, document number, phone, email or address, filter networks by status, risk band, signal type or pattern, inspect a network's members, signals, graph, timeline or map, download a network PDF report, or check whether a session, user, business, transaction or transaction party belongs to a fraud network using Didit. Networks are built automatically from production verifications and transactions; the API is read-only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to query Didit Fraud Networks and review network membership, shared signals, and related activity during fraud investigations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flags a payout-screening workflow that may create a production transaction despite the read-only description.

Mitigation: Review the payout-screening steps and confirm the intended production transaction behavior and tool scope before use.

Risk: The security review covered only half of the skill components and has a static analysis limit.

Mitigation: Review the complete skill and its utility script before installation, as advised by the security guidance.

## Reference(s):

- [Didit Fraud Networks API reference](https://docs.didit.me/management-api/networks/list)
- [Didit Fraud Networks feature guide](https://docs.didit.me/console/networks)
- [Didit pricing](https://docs.didit.me/getting-started/pricing)
- [ClawHub skill page](https://clawhub.ai/rosasalberto/skills/didit-fraud-networks)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Code, Shell commands, PDF report]

**Output Format:** [JSON API responses and text summaries, with Python and shell examples; network reports can be downloaded as PDF.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Didit API key, organization ID, and application ID.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
