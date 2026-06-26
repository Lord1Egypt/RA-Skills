## Description: <br>
Make x402 payments to access gated APIs and content. Fetch paid resources, check wallet balance, and create payment links. Use when encountering 402 Payment Required responses or when the user wants to pay for web resources with crypto. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ya7ya](https://clawhub.ai/user/ya7ya) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agents use this skill to make x402 payments for gated APIs and content, fetch paid resources, check wallet balances, and create payment links for paid content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent persistent access to a wallet private key and can trigger real-money crypto payments. <br>
Mitigation: Use a fresh low-balance wallet, start on testnet, set a low spending limit, and install only when automated x402 payments are intended. <br>
Risk: Payment requests may include sensitive URLs, headers, or request bodies. <br>
Mitigation: Use trusted payment URLs only and avoid sending sensitive headers or request bodies through paid fetch or pay commands. <br>
Risk: Payment-link and router distribution behavior can move funds or expose paid content in ways that depend on external services. <br>
Mitigation: Review link creation, router lookup, and distribution behavior before relying on it for production payments. <br>


## Reference(s): <br>
- [ClawHub Agentic X402 Release Page](https://clawhub.ai/ya7ya/agentic-x402) <br>
- [npm package: agentic-x402](https://www.npmjs.com/package/agentic-x402) <br>
- [x402 Protocol Docs](https://docs.x402.org/) <br>
- [x402 GitHub](https://github.com/coinbase/x402) <br>
- [Base Network](https://base.org/) <br>
- [21.cash](https://21.cash) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute networked x402 payment, wallet-balance, fetch, and payment-link CLI workflows when configured.] <br>

## Skill Version(s): <br>
0.2.6 (source: SKILL.md metadata, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
