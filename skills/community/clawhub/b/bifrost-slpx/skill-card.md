## Description: <br>
Bifrost SLPx helps agents query Bifrost liquid staking data and guide vETH wallet flows through the @bifrostio/slpx-cli CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bifrost-io](https://clawhub.ai/user/bifrost-io) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Bifrost vToken rates, APY, TVL, balances, and redemption status, and to prepare guarded vETH mint, redeem, and claim workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide mint, redeem, or claim flows that may broadcast real on-chain transactions from a configured wallet. <br>
Mitigation: Use a limited-balance wallet and approve broadcasting only after verifying the chain, wallet, action, amount, and expected result. <br>
Risk: Private key or signing material exposure could compromise wallet assets. <br>
Mitigation: Keep private keys out of chat and logs, configure signing outside the agent session, and rotate any key that may have been exposed. <br>
Risk: The workflow depends on the external @bifrostio/slpx-cli package and live Bifrost or RPC services. <br>
Mitigation: Install only when you trust that package and review CLI JSON errors or unavailable-service responses before acting on results. <br>


## Reference(s): <br>
- [@bifrostio/slpx-cli package](https://www.npmjs.com/package/@bifrostio/slpx-cli) <br>
- [Command reference](references/commands.md) <br>
- [Supported tokens and chains](references/tokens-and-chains.md) <br>
- [Pre-broadcast checklist](references/pre-tx-checklist.md) <br>
- [Signing key setup](references/private-key-env.md) <br>
- [Error codes](references/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-aware explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CLI JSON output as the grounding source for agent responses.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
