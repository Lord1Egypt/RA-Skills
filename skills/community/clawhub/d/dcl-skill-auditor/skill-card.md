## Description: <br>
DCL Skill Auditor reviews pasted ClawHub skill files before installation and returns a structured PASS, WARN, or BLOCK verdict with an audit proof. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daririnch](https://clawhub.ai/user/daririnch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and agent operators use this skill as a pre-install checkpoint for ClawHub skills. It helps review pasted SKILL.md, script, and manifest content for credential exposure, prompt injection, suspicious shell or network behavior, obfuscation, permission abuse, and behavior mismatch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner verdict is advisory and may not catch every issue in a target skill. <br>
Mitigation: Treat PASS, WARN, or BLOCK output as a helper judgment and review material findings before installation or deployment. <br>
Risk: Target skill content pasted for review could include API keys, private keys, wallet seed phrases, or other secrets. <br>
Mitigation: Redact secrets from skill files before pasting them into the agent for analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daririnch/dcl-skill-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Guidance] <br>
**Output Format:** [Structured JSON with PASS, WARN, or BLOCK verdict and audit proof] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes risk score, skill hash, analysis hash, findings, checked categories, timestamp, and proof identifier.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
