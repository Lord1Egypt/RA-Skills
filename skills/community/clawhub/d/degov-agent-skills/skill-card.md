## Description: <br>
Load this skill when users ask about Web3 DAO governance, using the Degov Agent API as the primary source for governance facts and recent activity with web search as a secondary layer when API coverage is missing, stale, or insufficient. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boundless-forest](https://clawhub.ai/user/boundless-forest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer Web3 DAO governance questions with recent Degov Agent API data, source follow-up, and clear explanations. It is suited for DAO activity summaries, proposal explanations, governance participation guidance, and recent governance research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid Degov Agent API calls require a local Base wallet with USDC for small x402 fees. <br>
Mitigation: Ask for user consent before paid calls, use the dedicated wallet only for API payments, and fund it with only a small USDC amount. <br>
Risk: The wallet and passphrase files are sensitive local custody material. <br>
Mitigation: Keep the wallet and passphrase private, rely on encrypted wallet storage, and do not ask users to paste private keys. <br>
Risk: DAO governance answers can be incomplete if API coverage is stale, missing, or too shallow. <br>
Mitigation: Check data freshness when needed and use official DAO forums, proposal pages, governance portals, and web search as follow-up sources. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/boundless-forest/degov-agent-skills) <br>
- [Degov Agent API](https://agent-api.degov.ai) <br>
- [Base Mainnet RPC](https://mainnet.base.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and source links when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paid API consent prompts, wallet setup steps, budget guidance, and DAO source links.] <br>

## Skill Version(s): <br>
0.6.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
