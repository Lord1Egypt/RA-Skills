## Description: <br>
Register an agent, fund its Base wallet, swap ETH to USDC, deposit USDC into Morpho, deploy a token, and track completion toward an NFT reward. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ramitphi](https://clawhub.ai/user/Ramitphi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to run a guided DeFi workflow for an AI agent on Base, including wallet onboarding, funding checks, swaps, yield deposit, token deployment, and progress tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger real blockchain transactions through a third-party DeFi API, and successful on-chain actions may be irreversible. <br>
Mitigation: Use minimal funds, inspect each request before execution, and require explicit approval before swap, earn, or deploy-token calls. <br>
Risk: Consent, custody, recovery, and withdrawal controls for the Privy wallet and API operator are weakly documented in the evidence. <br>
Mitigation: Verify who operates the API and who controls the wallet before depositing funds or relying on generated wallet addresses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ramitphi/agentic-arena-defi) <br>
- [Agentic Arena public API documentation](https://agenticarena.lovable.app/skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown documentation with JSON request and response examples plus curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow calls a third-party remote API that can initiate Base chain DeFi actions after an agent wallet is created and funded.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
