## Description: <br>
BYOCB ArbInjectionSkill scans EVM smart contracts for arbitrary call injection vulnerabilities and can monitor chains in real time or scan specific addresses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CryptoToolDev](https://clawhub.ai/user/CryptoToolDev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Solidity and blockchain security researchers, auditors, and developers use this skill to scan EVM contracts for arbitrary CALL and DELEGATECALL injection patterns. It supports continuous monitoring of newly deployed contracts and manual scans of known addresses for authorized security review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent background monitoring can run longer than intended and send external alerts without clear user control. <br>
Mitigation: Run the skill in an isolated environment, confirm when monitoring and alerting are allowed, and limit any API keys or messaging credentials. <br>
Risk: Daily self-updates from GitHub/npm are unpinned and may change behavior unexpectedly. <br>
Mitigation: Pin a reviewed commit or release, disable the daily auto-update schedule, and review dependency changes before running npm install. <br>
Risk: High-severity scan findings may include false positives. <br>
Mitigation: Verify flagged CALL targets against the documented safe patterns before alerting or acting on a finding. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CryptoToolDev/arb-injection) <br>
- [CryptoToolDev publisher profile](https://clawhub.ai/user/CryptoToolDev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command snippets, alert text, and references to local scan result files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying scanner may save JSON and Markdown findings to a local results directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
