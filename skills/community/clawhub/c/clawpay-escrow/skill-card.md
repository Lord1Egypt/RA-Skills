## Description: <br>
Send and receive escrow payments on Solana using ClawPay, including locking funds, confirming delivery, releasing payments, checking receipts, and verifying agent reputation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jakemeyer125-design](https://clawhub.ai/user/jakemeyer125-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to create and manage Solana escrow payments between agents, including buyer payment, seller delivery confirmation, settlement, refund, receipt lookup, and reputation checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to sign real Solana escrow transactions using local wallet key files. <br>
Mitigation: Use a dedicated low-balance wallet, set SOLANA_KEYPAIR_PATH to one explicit keypair file, and require confirmation of wallet, network, recipient public key, amount, fees, and escrow address before any transaction is signed. <br>
Risk: The payment SDK install command does not pin a package version. <br>
Mitigation: Verify or pin the clawpay package version and review the package source before installation in sensitive environments. <br>
Risk: Broad payment-related activation could lead to unintended escrow creation, release, or refund attempts. <br>
Mitigation: Confirm the user's intent before payment actions and check escrow status before attempting release or refund. <br>


## Reference(s): <br>
- [ClawPay Escrow ClawHub listing](https://clawhub.ai/jakemeyer125-design/clawpay-escrow) <br>
- [ClawPay website](https://claw-pay.com) <br>
- [ClawPay SDK on PyPI](https://pypi.org/project/clawpay/) <br>
- [ClawPay SDK GitHub repository linked by the skill](https://github.com/jakemeyer125-design/ClawPay-SDK) <br>
- [Solana Explorer program address](https://explorer.solana.com/address/F2nwkN9i2kUDgjfLwHwz2zPBXDxLDFjzmmV4TXT6BWeD) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute payment-related SDK calls only after explicit user confirmation of wallet, network, recipient, amount, fees, and escrow address.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
