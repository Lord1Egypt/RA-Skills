## Description:

Provides keyless on-chain RPC reads for agents to check balances, gas price, transaction status, token supply, ENS, and nonce across Base, Ethereum, Optimism, Arbitrum, and Polygon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rccola990-cloud](https://clawhub.ai/user/rccola990-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to read public blockchain state without managing RPC keys or running a node. It is suited for balance checks, gas lookups, transaction confirmation checks, token supply reads, ENS resolution, and nonce queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to a paid x402 flow for each request.

Mitigation: Review the quoted 402 price before payment and set agent spending limits appropriate for the workflow.

Risk: Public blockchain query details are sent to an external service endpoint.

Mitigation: Use the skill only for queries that are acceptable to disclose to the provider, and avoid sending sensitive operational context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rccola990-cloud/skills/cheap-onchain-rpc-reads)
- [Publisher profile](https://clawhub.ai/user/rccola990-cloud)
- [Balance read endpoint](https://store.agentexchange.work/chain/balance?address=0x...&chain=base)
- [Gas price endpoint](https://store.agentexchange.work/chain/gas?chain=base)
- [Transaction status endpoint](https://store.agentexchange.work/chain/tx?hash=0x...&chain=base)
- [ENS lookup endpoint](https://store.agentexchange.work/chain/ens?name=vitalik.eth)
- [Free sample endpoint](https://store.agentexchange.work/samples)

## Skill Output:

**Output Type(s):** [guidance, API Calls, shell commands]

**Output Format:** [Markdown with HTTP GET examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide the agent toward paid x402 HTTP reads of public blockchain data.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
