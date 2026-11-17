## Description:

Digital identity, authentication, and trust for AI agents, including identity verification, self-authentication, skill signing, encrypted messaging, and trust networks with vouches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[the-nexus-guard](https://clawhub.ai/user/the-nexus-guard)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to register and verify agent identities, sign content or skills, exchange trusted messages, manage credentials, and inspect trust relationships.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AIP service may receive identity metadata and signed content during normal identity, signing, trust, and messaging workflows.

Mitigation: Use the skill only when that disclosure is acceptable, and avoid signing or transmitting sensitive files or content.

Risk: Local credential files include private key material.

Mitigation: Protect aip_credentials.json with strict local permissions, never share the private key, and use AIP_CREDENTIALS_PATH when credentials need to be kept outside the workspace.

Risk: The security guidance warns that reply traffic should not be treated as sensitive until the reply path is encrypted.

Mitigation: Do not send sensitive replies through the reply workflow until encryption is confirmed for that path.

Risk: Dependencies and the execution environment may affect security-sensitive use.

Mitigation: Pin and audit dependencies before using the skill in a security-sensitive workspace.

## Reference(s):

- [AIP API Reference](references/api.md)
- [AIP Service](https://aip-service.fly.dev)
- [AIP Service API Docs](https://aip-service.fly.dev/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and text or JSON results from identity and trust operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local AIP credential files and may return signed content, encrypted messages, trust data, or SVG badge data depending on the command.]

## Skill Version(s):

1.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
