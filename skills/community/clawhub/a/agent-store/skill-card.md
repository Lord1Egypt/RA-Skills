## Description: <br>
Use when the user wants to buy, purchase, order, pay for, or top up API keys or API credits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[levey](https://clawhub.ai/user/levey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their operators use this skill to purchase API credits or API keys through a wallet-backed ClawHub release workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend wallet funds and approve token use. <br>
Mitigation: Use a limited wallet and verify the product, price, asset, chain, recipient, approval amount, publisher, wallet CLI, and API host before each run. <br>
Risk: A successful API key purchase can change future agent model settings. <br>
Mitigation: Separately approve runtime configuration edits and model switching after reviewing the delivery result. <br>
Risk: The workflow can buy an under-described VPS product even though the public trigger text focuses on API keys and credits. <br>
Mitigation: Run only the intended product type and confirm the requested purchase target before execution. <br>


## Reference(s): <br>
- [Agent Store on ClawHub](https://clawhub.ai/levey/agent-store) <br>
- [Publisher profile](https://clawhub.ai/user/levey) <br>
- [awp-wallet](https://github.com/awp-core/awp-wallet) <br>
- [Base mainnet RPC endpoint](https://mainnet.base.org) <br>
- [Agent Store API host](https://api.tkns.store) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with shell command usage, log-file reporting, JSON delivery results, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update the agent-store provider configuration after a successful API key purchase and verification.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
