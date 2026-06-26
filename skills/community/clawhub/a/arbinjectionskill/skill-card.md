## Description: <br>
BYOCB ArbInjectionSkill scans EVM smart contracts for arbitrary call injection vulnerabilities, monitors chains in real time, and supports scanning specific addresses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CryptoToolDev](https://clawhub.ai/user/CryptoToolDev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers, smart contract auditors, and blockchain security researchers use this skill to monitor supported EVM chains or scan contract addresses for arbitrary call injection risk and user-alertable findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to run unpinned external code and install Node.js dependencies. <br>
Mitigation: Pin the external repository to a specific audited commit and inspect dependencies before running npm install. <br>
Risk: The skill recommends automatic daily updates for code that runs in the background. <br>
Mitigation: Avoid automatic git pull or npm install in production; review and test updates before deployment. <br>
Risk: The skill may send vulnerability findings through messaging channels and can use scoped API keys for deeper analysis. <br>
Mitigation: Explicitly choose approved alert channels and use scoped or revocable API keys only when scan context may leave the environment. <br>


## Reference(s): <br>
- [BYOCB ArbInjection repository](https://github.com/BringYourOwnBot/arb-injection) <br>
- [ClawHub skill page](https://clawhub.ai/CryptoToolDev/arbinjectionskill) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Shell commands, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown alerts and reports, JSON findings, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are saved under ./results/ and critical or high verdicts are intended for user alerting after verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
