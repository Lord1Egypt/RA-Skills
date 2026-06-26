## Description: <br>
Create and manage agentic wallets with Unibase for autonomous onchain transactions on Ethereum, Solana, and other chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parasyte-x](https://clawhub.ai/user/parasyte-x) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to configure Unibase-backed agent wallets, list provisioned wallets, and prepare or execute onchain transactions through the Unibase proxy API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent persistent authority to send or sign real blockchain transactions. <br>
Mitigation: Install only when wallet operation is intentional, start with testnets or very small balances, and require explicit approval for every transaction or signature. <br>
Risk: A malicious or mistaken proxy endpoint could expose funds or credentials. <br>
Mitigation: Verify the publisher and proxy URL independently before configuring the skill. <br>
Risk: Repo-local plaintext JWT storage can leak wallet authority. <br>
Mitigation: Avoid storing JWTs in repo-local plaintext config and keep credentials out of source control. <br>


## Reference(s): <br>
- [Wallets Reference](references/wallets.md) <br>
- [Transactions Reference](references/transactions.md) <br>
- [Unibase Website](https://unibase.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/parasyte-x/agentic-wallet-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing instructions for authentication, wallet queries, and transaction request payloads.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
