## Description:

Use Paegents through the published SDK and API surface to register services, create usage agreements, activate bilateral escrow, route metered usage, and settle with the recommended execution mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markmcdaniels](https://clawhub.ai/user/markmcdaniels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, buyer agents, and seller agents use this skill to transact through Paegents using the public SDK and API surface for service registration, bilateral escrow agreements, metered usage, and settlement decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated calls and wallet signatures can affect Paegents payment, escrow, service, and settlement workflows.

Mitigation: Use scoped API keys, verify account and wallet context, keep private keys outside chat and broad process access, and require human review before creating agreements, signing permits, activating escrow, settling funds, deactivating services, creating webhooks, sending invites, or handling shipping addresses.

Risk: Incorrect API URL or environment configuration could send authenticated requests to the wrong endpoint or agent context.

Mitigation: Verify PAEGENTS_API_URL, PAEGENTS_API_KEY, and PAEGENTS_AGENT_ID before running authenticated calls, and prefer the published SDK over hand-built HTTP when available.

Risk: Escrow activation and settlement depend on live state such as nonces, fee permits, funding options, agreement status, and settlement availability.

Mitigation: Fetch live activation packages and settlement options, avoid hardcoded payment assumptions, poll for confirmed agreement and escrow status, and retry only through documented public flows.

Risk: Rate limits, asynchronous activation, or state errors can leave a transaction incomplete or temporarily blocked.

Mitigation: Use bounded retries with backoff, honor Retry-After when present, surface persistent throttling or unresolved activation states to a human operator, and avoid bursty polling or usage recording.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/markmcdaniels/skills/agent-payment-processor)
- [Paegents Homepage](https://paegents.com)
- [Paegents API](https://app.paegents.com/api)
- [Repository Metadata](https://github.com/MarkMcDaniels/paegents-pay-skill)
- [Quick Start](references/QUICK_START.md)
- [Payment Flows](references/PAYMENT_FLOWS.md)
- [SDK Usage](references/SDK_USAGE.md)
- [API Reference](references/API_REFERENCE.md)
- [Error Codes](references/ERROR_CODES.md)
- [Rate Limits](references/RATE_LIMITS.md)
- [OpenAPI Subset](assets/openapi-subset.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SDK examples, API references, shell commands, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide authenticated payment, escrow, service, webhook, invite, and settlement workflows that require scoped environment credentials and human approval.]

## Skill Version(s):

2.9.1 (source: SKILL.md frontmatter, OpenAPI info, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
