## Description:

Helps audit Agent Card signing practices in A2A protocol implementations by identifying missing signatures, weak signing schemes, and revocation gaps that allow impersonation in agent-to-agent trust handshakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to audit Agent Card signing practices in A2A protocol implementations. It checks signature presence, signing scheme strength, key transparency, revocation mechanisms, and rotation history, then provides a risk rating and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to fetch user-supplied Agent Card endpoints during an audit.

Mitigation: Use only endpoints that are intended for inspection, and avoid private or internal URLs unless the audit is authorized.

Risk: The audit evaluates publicly observable signing metadata and cannot prove private-key control or detect undisclosed signing-key compromise.

Mitigation: Treat signing results as identity assurance only and pair them with behavioral analysis or other trust checks for sensitive agent interactions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skills/agent-card-signing-auditor)
- [Publisher profile](https://clawhub.ai/user/andyxinweiminicloud)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown audit report with risk rating and remediation recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include endpoint-fetching commands for user-supplied Agent Card URLs; no persistence, credential use, or bundled code was found in security evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
