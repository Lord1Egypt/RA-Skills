## Description: <br>
Openclaw provides secure key-management guidance for AI agents handling private keys, API secrets, wallet credentials, agent-controlled funds, session keys, leak prevention, prompt injection defense, and MetaMask Delegation Framework integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zscole](https://clawhub.ai/user/zscole) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill when building agents that need to handle secrets, wallet credentials, session keys, or agent-controlled funds while reducing leakage, over-permissioning, and prompt-injection risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents that handle wallet permissions or secrets can expose funds or credentials if granted broad access. <br>
Mitigation: Use a dedicated vault, avoid giving agents master keys, and keep session keys short-lived and tightly scoped. <br>
Risk: High-value wallet operations can cause material loss if executed without oversight. <br>
Mitigation: Require confirmations for high-value operations and constrain spending, contract, method, and expiry permissions. <br>
Risk: Open delegations can grant excessive authority if they are not carefully bounded. <br>
Mitigation: Do not use open delegations unless the permissions and resulting operational risk are fully understood and constrained. <br>


## Reference(s): <br>
- [Secure Storage Patterns for Agent Secrets](artifact/references/secure-storage.md) <br>
- [Session Keys for Agent Wallet Access](artifact/references/session-keys.md) <br>
- [Leak Prevention for Agent Secrets](artifact/references/leak-prevention.md) <br>
- [Prompt Injection Defense for Agent Key Operations](artifact/references/prompt-injection-defense.md) <br>
- [Prompt Injection Defense](artifact/references/prompt-injection.md) <br>
- [Delegation Framework Integration (EIP-7710)](artifact/references/delegation-framework.md) <br>
- [MetaMask Delegation Framework Deployments](https://github.com/MetaMask/delegation-framework/blob/main/documents/Deployments.md) <br>
- [EIP-7710 Specification](https://eips.ethereum.org/EIPS/eip-7710) <br>
- [MetaMask Smart Accounts Kit](https://docs.metamask.io/smart-accounts-kit) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the 1Password CLI (`op`) for documented secure-storage workflows.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
