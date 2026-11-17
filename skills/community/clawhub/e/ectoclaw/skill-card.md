## Description:

EctoClaw helps OpenClaw agents record actions in an immutable hash-chained audit ledger with Ed25519 signatures, Merkle proofs, policy rules, compliance exports, and security monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ectospace](https://clawhub.ai/user/ectospace)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect OpenClaw agents to an EctoClaw audit service, inspect sessions, append signed lifecycle events, verify integrity, manage policy rules, and produce compliance reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit logs may include sensitive prompts, tool outputs, memory contents, and other agent activity.

Mitigation: Point ECTOCLAW_URL only at a local or trusted private instance and protect retained logs according to the sensitivity of the captured data.

Risk: Exposing the EctoClaw service beyond localhost can make sensitive audit data reachable over the network.

Mitigation: Put any non-local deployment behind authentication and access controls before use.

Risk: The skill relies on installing and running the ectoclaw npm package.

Mitigation: Pin or review the package version before installation when supply-chain control is required.

## Reference(s):

- [EctoClaw on ClawHub](https://clawhub.ai/ectospace/skills/ectoclaw)
- [EctoClaw npm package](https://www.npmjs.com/package/ectoclaw)
- [EctoClaw website](https://ectospace.com/EctoClaw)
- [EctoClaw source repository](https://github.com/EctoSpace/EctoClaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration guidance]

**Output Format:** [Markdown summaries with HTTP request descriptions, JSON payloads, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ECTOCLAW_URL to target a local or trusted private EctoClaw service.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
