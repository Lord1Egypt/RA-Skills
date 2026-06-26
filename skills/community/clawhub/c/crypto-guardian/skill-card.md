## Description: <br>
Provides cryptocurrency wallet security guidance for AI agents managing wallets, private keys, seed phrases, and on-chain assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayh-25](https://clawhub.ai/user/ayh-25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Crypto Guardian as a checklist and incident-response guide for reducing key exposure, unsafe signing, excessive token approvals, and wallet-drain risks when AI agents interact with crypto assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes inconsistent guidance about storing wallet secrets in environment files. <br>
Mitigation: Treat the skill as general checklist material only; do not place seed phrases or raw private keys in .env files, workspace files, chat, memory, or any AI-visible context. <br>
Risk: Agent-assisted wallet workflows can expose signing authority or enable unintended transactions. <br>
Mitigation: Prefer hardware wallets, wallet connectors, watch-only monitoring, limited token approvals, and explicit human confirmation for every signing action. <br>


## Reference(s): <br>
- [Crypto Guardian ClawHub page](https://clawhub.ai/ayh-25/crypto-guardian) <br>
- [Base Token Approval Checker](https://basescan.org/tokenapprovalchecker) <br>
- [Revoke.cash](https://revoke.cash/) <br>
- [Safe Wallet](https://app.safe.global/) <br>
- [Ledger phishing guidance](https://www.ledger.com/stop-phishing-attacks) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown checklist with incident-response steps and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet-handling, signing, token-approval, multisig, and incident-response checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
