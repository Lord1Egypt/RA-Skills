## Description: <br>
Private payments for AI agents - no on-chain link between sender and recipient <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mmchougule](https://clawhub.ai/user/mmchougule) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use Clawpay to initiate private USDT or USDC payments on BSC through the ClawPay API while reducing visible linkage between sender and recipient wallets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent high-impact wallet and payment authority. <br>
Mitigation: Use only a dedicated low-balance wallet, require explicit confirmation for every transfer, and start with a tiny test transaction. <br>
Risk: Wallet private keys or signatures could be exposed if pasted into scripts or chat. <br>
Mitigation: Do not paste a main wallet private key into scripts or chat; keep secrets in environment variables or a dedicated secret store. <br>
Risk: Funds could be sent to an unexpected invoice address or service endpoint. <br>
Mitigation: Verify clawpay.dev and returned invoice addresses before sending funds. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mmchougule/clawpay-2) <br>
- [ClawPay API](https://clawpay.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript, shell commands, API endpoints, and example JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include wallet setup, transfer flow, status checks, and troubleshooting steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
