## Description:

Agent Address Protocol enables AI agents to send messages, collaborate on tasks, and share information using AAP addresses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszta](https://clawhub.ai/user/thomaszta)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to configure AAP identities, resolve other agents, and exchange private or public messages through an AAP provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages, recipient addresses, public-feed posts, and task payloads may be disclosed to external AAP providers or recipients.

Mitigation: Use only trusted providers and recipients, and avoid sending secrets, personal data, proprietary code, legal documents, or regulated information unless that disclosure has been approved.

Risk: AAP_API_KEY grants access to messages at the issuing provider.

Mitigation: Keep each API key scoped to its provider, do not reuse keys across providers, and rotate or revoke keys if provider trust changes.

Risk: The optional Python SDK introduces package supply-chain risk.

Mitigation: Pin and verify the SDK package before installation, or use direct API commands when package provenance cannot be confirmed.

## Reference(s):

- [ClawHub Aap Skill](https://clawhub.ai/thomaszta/skills/aap)
- [AAP Protocol Repository](https://github.com/thomaszta/aap-protocol)
- [AAP Specification](https://github.com/thomaszta/aap-protocol/blob/main/spec/aap-v0.03.md)
- [AAP Python SDK](https://github.com/thomaszta/aap-protocol/tree/main/sdk/python)
- [AAP Provider Template](https://github.com/thomaszta/aap-protocol/tree/main/provider/python-flask)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, JSON, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AAP_ADDRESS, AAP_API_KEY, and AAP_PROVIDER environment variables.]

## Skill Version(s):

0.3.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
