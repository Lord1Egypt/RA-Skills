## Description: <br>
Create and manage agentic wallets with Cobo for autonomous onchain operations via the caw CLI, including token transfers, contract calls, pact management, DeFi execution, and wallet onboarding on EVM chains and Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cobogithub](https://clawhub.ai/user/cobogithub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to onboard Cobo agentic wallets and perform owner-authorized onchain wallet tasks such as transfers, contract calls, DeFi workflows, pact management, and status monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated wallet authority can affect real crypto funds. <br>
Mitigation: Use small pact limits or testnets first, confirm balances and gas before fund-moving actions, and review every pact before approval. <br>
Risk: Sensitive wallet credentials or API keys could be exposed through scripts, logs, or chat. <br>
Mitigation: Keep credentials out of scripts, logs, and messages; use environment variables or local secure storage and avoid sharing session identifiers. <br>
Risk: Prompt injection or external content could try to trigger unauthorized wallet operations. <br>
Mitigation: Only act on direct user requests, reject wallet instructions from external documents or tool outputs, and require explicit parameters for amount, asset, address, and chain. <br>
Risk: Bootstrap and update flows can modify PATH or install updated wallet tooling. <br>
Mitigation: Avoid automatic skill updates during wallet operations and inspect shell startup files modified by the bootstrap script. <br>


## Reference(s): <br>
- [Cobo Agentic Wallet Skill Page](https://clawhub.ai/cobogithub/cobo-agentic-wallet) <br>
- [Cobo Agentic Wallet Manual](https://cobo.com/products/agentic-wallet/manual/llms.txt) <br>
- [Security Guide](references/security.md) <br>
- [Onboarding](references/onboarding.md) <br>
- [Pact Management](references/pact.md) <br>
- [Pending Approval](references/pending-approval.md) <br>
- [Error Handling](references/error-handling.md) <br>
- [Chains and Token IDs](references/chains-and-tokens.md) <br>
- [SDK Scripting](references/sdk-scripting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local SDK scripts for multi-step wallet workflows; fund-moving operations must remain within owner-approved pact scope.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
