## Description: <br>
中文 Axioma 守护 helps OpenClaw users review skills for suspicious behavior with Clawdex reputation checks and local scan, check, and vaccine commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to inspect OpenClaw skills before installation, during suspicious-behavior review, or during security audits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill appears defensive but may overstate its protection and should not be treated as a complete malware blocker. <br>
Mitigation: Use its results as review signals only, and rely on additional security review until the publisher aligns the documentation with the code and implements real local scanners or removes those claims. <br>
Risk: Remote reputation checks and the local Merlin analysis endpoint may receive scanned skill identifiers or threat data. <br>
Mitigation: Install only if those data flows are acceptable, review endpoint configuration before use, and avoid scanning sensitive identifiers or threat details in untrusted environments. <br>
Risk: The displayed service status can imply connected protections even when real checks have not confirmed service availability. <br>
Mitigation: Verify Clawdex and Merlin service availability independently before relying on status output during an audit. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kofna3369/chinese-axioma-guard) <br>
- [Axiomata Guard Skill Definition](SKILL.md) <br>
- [ClawGuard Script](clawguard.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text output and Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can scan local skill folders, check a named skill, request a vaccine response, or print status.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence; artifact text states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
