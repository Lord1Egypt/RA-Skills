## Description:

Purchase travel eSIM data plans using USDC on Base Mainnet or Sepolia testnet via x402, with eSIM delivery via a QR code installation page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inthaiguy](https://clawhub.ai/user/inthaiguy)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to search for travel eSIM data plans, quote USDC prices, complete an x402 payment flow, and return an eSIM installation link. Developers can use the included Python client and API documentation to integrate package search, quotes, purchases, and status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The payment flow relies on remote payment instructions for an irreversible USDC transfer.

Mitigation: Before approving payment, verify the exact USDC amount, recipient, token contract, and Base network in the wallet; prefer Base Sepolia testnet until payment-parameter validation is tightened.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/inthaiguy/skills/get-esim)
- [Mainnet Agent API Documentation](https://esimqr.link/api/agent/docs)
- [Testnet Agent API Documentation](https://esimqr.link/api/agent-testnet/docs)
- [Agent Landing Page](https://esimqr.link/agents)
- [Hackathon Submission](https://www.moltbook.com/m/usdc)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON API responses, Python client objects, payment headers, and eSIM installation URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network-specific output may target Base Mainnet for real purchases or Base Sepolia for test purchases; purchase results include eSIM status and installation page URLs.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
