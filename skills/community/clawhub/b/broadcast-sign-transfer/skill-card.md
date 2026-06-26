## Description: <br>
Constructs, locally signs, and broadcasts EVM native-token and ERC20 transfers through the OKX Web3 broadcast API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangchengming666](https://clawhub.ai/user/wangchengming666) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to prepare and broadcast BSC/EVM native-token or ERC20 transfers when the recipient, amount, API credentials, and wallet private key are already configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move real crypto funds. <br>
Mitigation: Use a dedicated low-balance wallet and require separate human confirmation of recipient, chain, token, and amount before every transfer. <br>
Risk: Sensitive signed transaction data may be exposed in logs. <br>
Mitigation: Remove or disable debug logging of signed transactions and request bodies before use. <br>
Risk: Private keys and API credentials are required for operation. <br>
Mitigation: Avoid storing private keys in shell startup files; use a secrets manager or short-lived environment injection where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangchengming666/broadcast-sign-transfer) <br>
- [OKX Web3 API endpoint](https://web3.okx.com) <br>
- [BSC RPC endpoint](https://bsc-dataseed1.binance.org/) <br>
- [BscScan transaction explorer](https://bscscan.com/tx/) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples plus transfer result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns order ID, transaction hash, explorer URL, or an error message.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
