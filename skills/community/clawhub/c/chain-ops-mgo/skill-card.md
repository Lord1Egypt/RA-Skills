## Description:

Find and compare gas prices across multiple EVM chains to identify the cheapest option for transactions and contract deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlrjsdl200-byte](https://clawhub.ai/user/dlrjsdl200-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to compare gas prices across EVM chains and choose lower-cost chains for transactions, contract deployments, or chain selection decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid /gas/basic and /gas/premium requests cost real USDC through x402 on Base.

Mitigation: Configure agents to ask before making paid requests, or use /gas/demo when payment is not intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlrjsdl200-byte/skills/chain-ops-mgo)
- [MGO dashboard](https://mgo.chain-ops.xyz)
- [MGO llms.txt](https://api.mgo.chain-ops.xyz/llms.txt)
- [GitHub repository](https://github.com/dlrjsdl200-byte/x402-gas-api)

## Skill Output:

**Output Type(s):** [API calls, guidance, text]

**Output Format:** [Plain text or Markdown with endpoint URLs, chain comparisons, recommendations, and payment notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some API endpoints require x402 payment on Base using USDC; the demo endpoint is free but rate limited.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
