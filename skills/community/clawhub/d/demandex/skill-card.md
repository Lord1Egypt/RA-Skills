## Description:

E-commerce demand intelligence for AI agents: Demandex mines public Reddit complaint and intent posts into scored physical-product opportunity cards and ad-hoc demand verdicts with evidence links, using free discovery endpoints and paid x402 calls for deeper results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcislo](https://clawhub.ai/user/jcislo)

### License/Terms of Use:

MIT-0

## Use Case:

External agents, developers, and e-commerce builders use this skill to discover product demand signals, inspect scored opportunity cards, and request cached or live demand verdicts for physical-product ideas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup can use a spend-capable wallet private key for paid x402 calls.

Mitigation: Use a dedicated low-balance wallet, avoid general-purpose keys, and require explicit approval before paid tool calls.

Risk: The MCP registration example runs an unpinned npm package.

Mitigation: Pin and verify the demandex-mcp package version before installation or execution.

Risk: Paid endpoints can incur per-call USDC charges.

Mitigation: Start with the free category and sample-opportunity endpoints to validate response shapes before enabling paid calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcislo/skills/demandex)
- [Demandex homepage](https://demandex.dev)
- [Demandex API](https://api.demandex.dev)
- [OpenAPI specification](https://api.demandex.dev/openapi.json)
- [Machine discovery document](https://api.demandex.dev/discovery)
- [A2A agent card](https://api.demandex.dev/.well-known/agent-card.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with endpoint tables, curl examples, MCP configuration JSON, and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes free endpoint guidance and paid x402 call guidance; paid MCP usage can require a wallet private key.]

## Skill Version(s):

0.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
