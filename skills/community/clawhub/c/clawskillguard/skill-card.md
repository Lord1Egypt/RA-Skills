## Description: <br>
ClawSkillGuard scans OpenClaw skill files and scripts for prompt injection, data exfiltration, malicious patterns, and unauthorized network calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xeonai44](https://clawhub.ai/user/xeonai44) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run local security checks before installing, auditing, or trusting OpenClaw skills from ClawHub or other external sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pattern matching can miss evasive or novel malicious behavior, so a clean result is advisory rather than a safety guarantee. <br>
Mitigation: Review important skills manually or with another scanner when stakes are high, especially before installation or deployment. <br>
Risk: The scanner skips scanning itself when the target directory is named clawskillguard, which can leave that specific target unaudited. <br>
Mitigation: Inspect ClawSkillGuard source directly or scan a renamed copy if self-audit coverage is needed. <br>


## Reference(s): <br>
- [ClawSkillGuard ClawHub listing](https://clawhub.ai/xeonai44/clawskillguard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Text or JSON scan reports with severity-labeled findings and installation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can filter reported findings by minimum severity and can scan one skill or all skills under a parent directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
