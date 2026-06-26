## Description: <br>
Apiosk Skill helps agents discover and call paid production APIs through USDC micropayments on Base without managing API keys or accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obcraft](https://clawhub.ai/user/obcraft) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to configure a small Apiosk wallet, discover available APIs, call selected APIs from shell, Node.js, or Python, and monitor balance and usage. It is suited to agents that need keyless API access and can tolerate per-request blockchain-backed payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real crypto funds and stores the generated wallet private key in plaintext on disk. <br>
Mitigation: Use a dedicated wallet with minimal funds, keep file permissions restrictive, and use hardware-wallet or external key-management integration for higher-value or production use. <br>
Risk: API calls send request data and wallet-linked metadata to Apiosk and can trigger automatic paid requests. <br>
Mitigation: Avoid sensitive payloads, test with small calls first, monitor balance and usage, and review spending behavior before larger workflows. <br>
Risk: The documented Foundry install path includes a remote shell installer. <br>
Mitigation: Review and verify the Foundry installation path before running it, and prefer a trusted or already-managed installation where possible. <br>
Risk: The scanner guidance says not to rely on documented daily or per-request limits unless enforcement is verified. <br>
Mitigation: Verify limit enforcement independently and keep only the amount required for immediate use in the wallet. <br>


## Reference(s): <br>
- [ClawHub Apiosk Skill](https://clawhub.ai/obcraft/apiosk) <br>
- [Apiosk Documentation](https://docs.apiosk.com) <br>
- [Apiosk Website](https://apiosk.com) <br>
- [Base Bridge](https://bridge.base.org) <br>
- [Foundry Installation](https://book.getfoundry.sh/getting-started/installation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON examples, and Python and JavaScript code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate paid API requests through configured scripts or client wrappers when used by an agent.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
