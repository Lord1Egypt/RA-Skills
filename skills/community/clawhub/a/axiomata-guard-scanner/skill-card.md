## Description: <br>
Axiomata Guard Scanner helps agents review OpenClaw skills before installation by scanning skill text and files for known malicious patterns, C2 and exfiltration indicators, attack chains, rootkit or bootkit signals, and package ecosystem risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to scan OpenClaw skills before installation or during security audits. It provides threat findings, aggregate risk scores, and install-oriented decisions for manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be broadly available for general skill-installation or audit requests. <br>
Mitigation: Install it only when broad OpenClaw skill security review behavior is desired, and keep final install decisions user-directed. <br>
Risk: Scanner findings can be incomplete or incorrectly classify a skill. <br>
Mitigation: Use the scanner output as review guidance and manually inspect findings before approving, warning, neutralizing, or isolating a skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kofna3369/axiomata-guard-scanner) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with optional JSON scanner results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scanner results include threat level, score, decision, triggered vaccines, and summary fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
