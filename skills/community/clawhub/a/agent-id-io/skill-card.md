## Description:

OpenClaw skill for the agent-id.io identity and trust service. Use it to register an AI agent, authenticate with challenge/response, manage passkeys and cryptographic keys, verify domains/repos/websites, handle sponsorships, and inspect public agent profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plak](https://clawhub.ai/user/plak)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to register and authenticate AI agents with agent-id.io, manage agent passkeys and cryptographic keys, perform ownership verification for domains, repositories, and websites, and handle sponsorship workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill manages long-lived agent identity private keys and short-lived authentication tokens.

Mitigation: Install only when the publisher and agent-id.io service are trusted, generate encrypted key output from the start, and keep tokens in restricted local storage for the minimum time needed.

Risk: Plaintext key or token files can remain in temporary paths or local working directories.

Mitigation: Avoid plaintext /tmp key or token files where possible; when temporary plaintext files are unavoidable, use restrictive permissions and delete them immediately after use.

Risk: Changing AGENT_ID_API can redirect production credentials or signed requests to an unintended endpoint.

Mitigation: Use AGENT_ID_API with production tokens only when the destination is explicitly trusted and uses HTTPS.

Risk: Deriving SSH and PGP keys from the agent master seed expands the impact of master-key compromise.

Mitigation: Treat SSH and PGP derivation as a separate opt-in decision and protect the master seed as the root credential for all derived identities.

## Reference(s):

- [Agent-ID API Reference v1](references/api.md)
- [agent-id.io API](https://agent-id.io/v1)
- [ClawHub skill page](https://clawhub.ai/plak/skills/agent-id-io)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, JSON, files]

**Output Format:** [Markdown guidance with bash commands, Python helper scripts, JSON request and response payloads, and generated key or token files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated secrets and tokens require secure local storage and short-lived operational handling.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
