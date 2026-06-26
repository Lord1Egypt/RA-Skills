## Description: <br>
Generate EIP-681 Ethereum payment links and QR codes for any EVM chain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bevanding](https://clawhub.ai/user/bevanding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create payment requests, invoices, donation links, and mobile-friendly checkout links for ETH or supported ERC-20 tokens across configured EVM networks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated payment links may encode an unintended recipient address, token contract, network, or amount. <br>
Mitigation: Verify the generated payment details in the wallet before sharing links or making payments. <br>
Risk: The configured Ethereum DAI token address is malformed. <br>
Mitigation: Avoid Ethereum DAI payment links until the token address is corrected and independently verified. <br>
Risk: QR code generation depends on local Python packages. <br>
Mitigation: Install qrcode and pillow in a virtual environment before generating QR files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bevanding/evm-payment) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, configuration, guidance] <br>
**Output Format:** [Human-readable CLI text, JSON output, EIP-681 and MetaMask links, transaction payload details, and optional PNG QR code files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 plus qrcode and pillow for QR code generation; generated payment details should be verified in a wallet before use.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
