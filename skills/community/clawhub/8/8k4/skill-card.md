## Description:

Trust scoring, agent discovery, profiling, wallet and identity lookup, contact, dispatch, and metadata reads or writes via 8K4 Protocol (ERC-8004).

This skill is ready for commercial/non-commercial use.

## Publisher:

[8k4-dev](https://clawhub.ai/user/8k4-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to evaluate trust for on-chain agents, discover task-suitable agents, inspect agent profiles, and prepare API calls for contact, dispatch, wallet, identity, and metadata workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact, dispatch, paid x402 lookup, metadata update, and key-generation flows can send live requests, incur payment, request signatures, or alter hosted metadata.

Mitigation: Require clear user intent before paid, write, signature, or live-send actions; prefer dry-run for contact and dispatch; manually confirm payment and metadata payloads before proceeding.

Risk: The bundled Bash helper has unsafe request construction and fragile authentication handling.

Mitigation: Fix or wrap the helper before routine use, keep API keys in environment variables, avoid sending secrets or proprietary task text, and review attacker-influenced arguments before execution.

## Reference(s):

- [8K4 Protocol API Docs](https://api.8k4protocol.com/docs)
- [8K4 Protocol Website](https://8k4protocol.com)
- [Access & Authentication](references/ACCESS.md)
- [Endpoint Reference](references/ENDPOINTS.md)
- [Safety Policy](references/SAFETY.md)
- [Scoring Reference](references/SCORING.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash, JSON, and endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl and the EIGHTK4_API_KEY environment variable when authenticated 8K4 API access is needed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
