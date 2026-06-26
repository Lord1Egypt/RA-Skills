## Description: <br>
Trustless payment protocol for AI agents - ACTP escrow and x402 instant payments, settled in USDC on Base L2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Unima3x](https://clawhub.ai/user/Unima3x) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agent operators use this skill to configure agents that can pay for services, receive USDC payments, manage ACTP escrow flows, and use x402 for instant API payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent real-money blockchain payment authority, including mainnet USDC transactions. <br>
Mitigation: Install only when payment authority is intended; start in mock or testnet and use a dedicated low-balance wallet before any mainnet use. <br>
Risk: Examples include credential auto-detection and some defaults that users should review before running. <br>
Mitigation: Prefer encrypted keystores over raw private keys, set credential scope deliberately, and review generated commands before execution. <br>
Risk: Incorrect provider addresses or spending limits can send funds to the wrong recipient or exceed the operator's intended budget. <br>
Mitigation: Verify every provider address, network, and spending limit before payment, and release escrow only after checking the delivered work. <br>
Risk: Sensitive deliverables or transaction details could be exposed through public storage or broad logs. <br>
Mitigation: Avoid storing sensitive deliverables in public IPFS or broad logs, and keep delivery proofs limited to the data needed for verification. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/Unima3x/agirails) <br>
- [AGIRAILS Documentation](https://docs.agirails.io) <br>
- [AGIRAILS FAQ](https://agirails.app/faq) <br>
- [AGIRAILS SDK (npm)](https://www.npmjs.com/package/@agirails/sdk) <br>
- [AGIRAILS SDK (pip)](https://pypi.org/project/agirails/) <br>
- [Requester Agent Template](references/requester-template.md) <br>
- [Provider Agent Template](references/provider-template.md) <br>
- [ACTP State Machine](references/state-machine.md) <br>
- [OpenClaw Security Checklist](openclaw/security-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript and Python code blocks, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may guide agents through wallet setup, escrow state handling, payment execution, balance checks, and deployment checks.] <br>

## Skill Version(s): <br>
3.0.12 (source: server release metadata; artifact frontmatter is 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
