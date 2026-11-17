## Description:

BYOCB ArbInjectionSkill scans EVM smart contracts for arbitrary call injection vulnerabilities, monitors chains in real time, and supports scans of specific addresses.

This skill is for research and development only.

## Publisher:

[cryptotooldev](https://clawhub.ai/user/cryptotooldev)

### License/Terms of Use:


## Use Case:

Solidity and blockchain security researchers and auditors use this skill to monitor major EVM chains for newly deployed contracts, scan bytecode for arbitrary CALL/DELEGATECALL patterns, and review findings before issuing alerts. It is intended for educational and authorized security research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs mutable external code and recommends recurring unattended git pull/npm install updates.

Mitigation: Use a pinned and reviewed release with included source and lockfile, and avoid unattended update schedules.

Risk: The skill may send vulnerability alert data to connected messaging providers.

Mitigation: Confirm exactly what alert data will be sent and run the skill with minimal credentials and filesystem access.

Risk: False positives could cause misleading high-severity alerts.

Mitigation: Review generated findings against the documented safe patterns before notifying users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cryptotooldev/skills/arb-injection)
- [ClawHub publisher profile](https://clawhub.ai/user/cryptotooldev)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and local JSON/Markdown finding files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are saved under ./results/ and high-severity findings are intended to trigger user alerts after false-positive review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
