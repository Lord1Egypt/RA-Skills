## Description: <br>
AgentsBank provides a TypeScript and JavaScript SDK that helps agents authenticate with AgentsBank, manage multi-chain crypto wallets, check balances and transaction history, sign messages, estimate fees, and submit crypto transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cryruz](https://clawhub.ai/user/cryruz) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to integrate AgentsBank wallet operations into agent workflows, including read-only balance/history queries and user-approved cryptocurrency transaction flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The SDK can move real cryptocurrency through direct send and batch-send APIs, and the server security summary did not find an enforceable approval step in the artifact. <br>
Mitigation: Require separate human approval before any send or batch-send operation, start with testnet or spending-limited credentials, and monitor wallet activity. <br>
Risk: The security guidance says not to rely on maxGasUSD as an enforced cap in this version. <br>
Mitigation: Enforce transaction, recipient, and gas limits outside the SDK before invoking write operations. <br>
Risk: Registration responses can include recovery words, which could be exposed in logs or agent-visible output. <br>
Mitigation: Never log recovery words or credentials; route secrets to a secret manager or another human-controlled secure channel. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cryruz/agentsbank) <br>
- [AgentsBank SDK Documentation](https://docs.agentsbank.online/sdk) <br>
- [AgentsBank API Reference](https://api.agentsbank.online/docs) <br>
- [AgentsBank Security Guide](https://docs.agentsbank.online/security) <br>
- [npm Package](https://www.npmjs.com/package/@agentsbankai/sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with TypeScript examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AgentsBank API credentials and network access to the configured AgentsBank API endpoint.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata, released 2026-02-11; artifact package.json and CHANGELOG contain 1.0.7 metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
