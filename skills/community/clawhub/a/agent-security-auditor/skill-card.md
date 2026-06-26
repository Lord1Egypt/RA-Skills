## Description: <br>
Audits ERC-8004 agents by analyzing metadata, endpoints, payment configuration, and reputation signals to identify security risks and generate reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aviclaw](https://clawhub.ai/user/aviclaw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit ERC-8004 Trustless Agents before interacting with them, focusing on metadata quality, service endpoints, x402 payment configuration, and reputation signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit contacts an Ethereum RPC endpoint, which can expose request patterns or consume RPC quota. <br>
Mitigation: Use a trusted or dedicated RPC endpoint for sensitive audits and monitor quota usage. <br>
Risk: Agent-controlled metadata URLs are fetched during audit workflows and may be unreliable or untrusted. <br>
Mitigation: Run the tool from an environment appropriate for inspecting untrusted metadata and review generated findings before acting on them. <br>
Risk: RPC URLs may contain API keys that could appear in terminal logs or saved command history. <br>
Mitigation: Avoid sharing logs that include RPC URLs and prefer environment-specific credentials with limited scope. <br>


## Reference(s): <br>
- [Agent Security Auditor on ClawHub](https://clawhub.ai/aviclaw/agent-security-auditor) <br>
- [ERC-8004 Reference](references/ERC-8004.md) <br>
- [ERC-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004) <br>
- [ERC-8004 Discussion Forum](https://ethereum-magicians.org/t/erc-8004-trustless-agents/25098) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The audit script accepts an agent address, optional RPC URL, chain ID, output file path, and verbose flag.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
