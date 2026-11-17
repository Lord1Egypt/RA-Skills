## Description:

Use AG9 to register and verify AI agents with VeryAI Palm-backed human ownership, generate or load portable Ed25519 identities for OpenClaw, Codex, local CLI/MCP, browser, or cloud agents, call AG9 registration/signature verification APIs, and solve reverse-CAPTCHA capability challenges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oyyblin](https://clawhub.ai/user/oyyblin)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent operators use AG9 to bind an agent identity to a verified human owner, verify Ed25519 agent signatures, and produce capability attestations through AG9 reverse-CAPTCHA challenges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses durable local or cloud-stored AG9 identity keys.

Mitigation: Install only when persistent agent identity is acceptable; keep private keys local or in a cloud secret manager and send only public verification data to AG9.

Risk: The skill links stable verification data to a human verification flow.

Mitigation: Use it only when the human owner understands the AG9/VeryAI verification flow and agrees to associate the agent with that verification.

Risk: The skill recommends generated Python for remote challenge payloads without clear sandboxing.

Mitigation: Run generated challenge-solving code only in a sandbox with no access to secrets, private files, or the network.

## Reference(s):

- [AG9 API Base](https://api.ag9.ai)
- [AG9 Homepage](https://ag9.ai)
- [AG9 Interactive Demo](https://ag9.ai/demo)
- [AG9 OpenAPI Spec](https://api.ag9.ai/openapi/v1.yaml)
- [AG9 ClawHub Skill Page](https://clawhub.ai/oyyblin/skills/ag9)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON, JavaScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce registration URLs, AgentChallenge payloads, verification requests, and identity configuration guidance.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
