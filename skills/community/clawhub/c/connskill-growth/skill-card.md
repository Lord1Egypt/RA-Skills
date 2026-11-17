## Description:

connskill-growth lets agents buy per-call growth services from agent.connskill.com with USDC over x402, including SEO and SERP data, site audits, SMS numbers, receive-only inboxes, EU-hosted chat or embeddings, and x402 seller trust checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-skill](https://clawhub.ai/user/conn-skill)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to request paid growth-service data or actions, such as keyword research, SERP reports, site audits, SMS verification numbers, receive-only inboxes, EU-hosted LLM calls, and x402 seller trust checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can authorize paid x402 calls using a Base wallet private key.

Mitigation: Use a dedicated low-balance wallet, set X402_MAX_USD to a strict per-call cap, and avoid using a main wallet key.

Risk: The optional MCP server is installed through an executable package that may change unless pinned and reviewed.

Mitigation: Prefer pinned, reviewed package versions and run the server or bundled script in a restricted environment with minimal filesystem access.

Risk: SMS verification numbers and receive-only inboxes can be misused for third-party account verification.

Mitigation: Use SMS and inbox endpoints only where there is clear authorization and policy approval for the target service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/conn-skill/skills/connskill-growth)
- [Publisher profile](https://clawhub.ai/user/conn-skill)
- [CONNSKILL Growth Services homepage](https://agent.connskill.com)
- [OpenAPI catalogue](https://agent.connskill.com/openapi.json)
- [x402 service price catalogue](https://agent.connskill.com/.well-known/x402)
- [Agent readme](https://agent.connskill.com/llms.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses from referenced services]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid calls may require X402_WALLET_KEY and should be bounded by X402_MAX_USD.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
