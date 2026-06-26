## Description: <br>
AI-powered sports betting simulations with Monte Carlo analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cannedoxygen](https://clawhub.ai/user/cannedoxygen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use EdgeBets to fetch sports matchups, request Monte Carlo betting simulations, review daily picks, and check historical pick performance for NBA, NFL, MLB, and MLS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid simulations can automatically transfer real USDC from the configured Solana wallet. <br>
Mitigation: Use a dedicated low-balance wallet and verify the $1.00 USDC charge and treasury address before each paid simulation. <br>
Risk: The skill asks agents to use a Solana private key through environment configuration. <br>
Mitigation: Avoid using a primary wallet private key in agent environment variables. <br>


## Reference(s): <br>
- [EdgeBets ClawHub listing](https://clawhub.ai/cannedoxygen/edgebets) <br>
- [EdgeBets website](https://edgebets.fun) <br>
- [EdgeBets API documentation](https://api.edgebets.fun/api/v1/x402) <br>
- [EdgeBets OpenAPI specification](https://api.edgebets.fun/api/v1/x402/openapi.json) <br>
- [x402 protocol](https://x402.org) <br>
- [edgebets-sdk npm package](https://www.npmjs.com/package/edgebets-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with TypeScript or JavaScript snippets, shell setup commands, sports analysis text, and SDK/API guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and SOLANA_PRIVATE_KEY for wallet-backed use; paid simulations can spend $1.00 USDC on Solana mainnet.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
