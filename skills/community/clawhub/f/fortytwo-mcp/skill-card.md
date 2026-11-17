## Description:

Fortytwo MCP helps an agent query Fortytwo Prime, a paid collective multi-agent inference service, for high-stakes, contested, or cross-domain questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inikitin](https://clawhub.ai/user/inikitin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route paid questions to Fortytwo Prime when a user explicitly asks for Fortytwo, needs deeper review, or asks a contested or multi-domain question. The skill also guides wallet setup, payment preflight checks, session reuse, troubleshooting, and optional streaming calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid calls sign on-chain payment authorizations without sufficient local spending controls.

Mitigation: Use a dedicated low-value wallet, require explicit confirmation before paid calls, and add local spending limits plus expected token and recipient validation before broader use.

Risk: Reusable paid-session state is stored insecurely.

Mitigation: Avoid shared hosts for paid sessions, remove saved session state after use, and store session identifiers in a permission-restricted location.

Risk: User questions are sent to Fortytwo for inference.

Mitigation: Do not submit confidential, regulated, or sensitive data unless the user and deployment owner have approved that data flow.

Risk: Runtime dependencies are not pinned.

Mitigation: Pin and review dependency versions for eth-account and web3 before production deployment.

## Reference(s):

- [Fortytwo Prime](https://platform.fortytwo.network/prime)
- [ClawHub skill page](https://clawhub.ai/inikitin/skills/fortytwo-mcp)
- [Setup and wallet configuration](references/setup.md)
- [x402 payment signing](references/payment.md)
- [Session lifecycle](references/session.md)
- [MCP streaming via progressToken](references/streaming.md)
- [x402](https://www.x402.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus plain-text Fortytwo Prime answers returned by the query script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stderr diagnostics, a saved session identifier, and incremental text deltas when the optional SSE flow is used.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
