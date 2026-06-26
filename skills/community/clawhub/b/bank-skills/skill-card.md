## Description: <br>
Traditional banking via Wise API + on-chain token swaps on Base. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[singularityhacker](https://clawhub.ai/user/singularityhacker) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent users use this skill to let an agent query Wise balances and receiving details, initiate transfers, and operate a Base wallet for token swaps and token transfers in controlled R&D settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move real money through Wise transfers and on-chain token operations. <br>
Mitigation: Use only low-balance test accounts and require external human approval before send, send-token, or buy-token actions. <br>
Risk: The export-private-key action can reveal wallet secrets. <br>
Mitigation: Set a strong CLAWBANK_WALLET_PASSWORD and require human approval before export-private-key is available to an autonomous agent. <br>
Risk: A compromised Wise API token could expose banking functionality. <br>
Mitigation: Restrict and rotate the Wise API token, enable Wise token or IP controls where available, and avoid storing the token in shared configuration. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/singularityhacker/bank-skills) <br>
- [Skills.sh listing](https://skills.sh/singularityhacker/bank-skills/bank-skill) <br>
- [NPM package](https://www.npmjs.com/package/@singularityhacker/bank-skill) <br>
- [Wise API documentation](https://docs.wise.com/api-reference) <br>
- [Base mainnet RPC endpoint](https://mainnet.base.org) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files] <br>
**Output Format:** [JSON over stdout, with optional local wallet and sweep configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include balances, account details, transfer IDs, transaction hashes, wallet addresses, and private keys when the export-private-key action is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; packaged skill sources report 0.1.4 in SKILL.md, pyproject.toml, CHANGELOG.md, and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
