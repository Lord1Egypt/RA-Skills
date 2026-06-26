## Description: <br>
Lightning-fast crypto swaps. 240+ coins, best rates, done in minutes. Chat, CLI, or web - however you prefer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoyoemily](https://clawhub.ai/user/yoyoemily) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query supported currencies, compare exchange rates, create LightningEX crypto swap orders, and monitor order status through chat, CLI, or a local web UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support real crypto swap workflows involving wallet addresses, deposit addresses, networks, amounts, and fees. <br>
Mitigation: Before sending funds, verify the asset, network, amount, fees, destination address, deposit address, and support process through trusted LightningEX channels. <br>
Risk: Users must trust the third-party npm package and the LightningEX service used by the CLI and local web UI. <br>
Mitigation: Install only after confirming the package and service are trusted for the user's environment, and do not provide private keys or seed phrases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yoyoemily/crypto-swap) <br>
- [LightningEX API endpoint](https://api.lightningex.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured CLI or UI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can call LightningEX endpoints to list currencies, quote rates, validate wallet addresses, place orders, and poll order status.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
