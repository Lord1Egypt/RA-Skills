## Description: <br>
Security audit tool for ClawHub/OpenClaw skills with static analysis and reputation scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emeraldring3134-netizen](https://clawhub.ai/user/emeraldring3134-netizen) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and skill maintainers use this skill to run lightweight local checks on ClawHub/OpenClaw skill folders before installation or publication. Its results should support manual review, not replace a dependable security assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit result can be unreliable because the skill may mark a folder named like itself as safe without scanning it. <br>
Mitigation: Treat this as a lightweight regex checker, review findings manually, and do not rely on a Safe result as a security verdict. <br>
Risk: The skill metadata declares an optional VirusTotal API key, but the security guidance advises against providing it for this version. <br>
Mitigation: Run this version without a VirusTotal API key and avoid supplying sensitive credentials. <br>
Risk: The scanner reads files in the target folder during local analysis. <br>
Mitigation: Run it only on specific folders you intend to inspect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emeraldring3134-netizen/claw-secure-auditor) <br>
- [Declared homepage](https://github.com/YOURNAME/claw-secure-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, JSON, Guidance] <br>
**Output Format:** [Terminal text with optional JSON report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only local audit; requires python3 and can run without the optional VIRUSTOTAL_API_KEY.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
