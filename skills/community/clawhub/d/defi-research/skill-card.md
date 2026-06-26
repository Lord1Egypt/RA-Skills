## Description: <br>
Research tokens, check DEX liquidity, and get live gas prices for DeFi traders and agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kennywayn3](https://clawhub.ai/user/kennywayn3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, DeFi traders, and wallet-enabled agents use this skill to look up token prices, request deeper token research, compare DEX liquidity, and check Ethereum gas prices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid requests can involve irreversible USDC transfers or other spending by a wallet-enabled agent. <br>
Mitigation: Require manual approval for every payment, use a low-balance dedicated wallet, verify Base/USDC recipient details, and do not allow autonomous spending. <br>
Risk: The skill may rely on sensitive credentials or wallet permissions for paid access. <br>
Mitigation: Use scoped API keys and avoid broad wallet permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kennywayn3/defi-research) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Guidance] <br>
**Output Format:** [Markdown instructions with JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid endpoints may require an API key, wallet support, or a transaction hash.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
