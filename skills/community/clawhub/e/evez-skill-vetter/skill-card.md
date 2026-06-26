## Description: <br>
Security review for OpenClaw skills before installation, covering static analysis, permission auditing, dependency checks, suspicious patterns, data exfiltration risks, secret exposure, and risk scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to perform a first-pass review of third-party OpenClaw skills before installation. It helps identify suspicious patterns, broad permissions, dependency concerns, secret exposure, and other findings that need human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A low risk score or clean scan can be mistaken for proof that a skill is safe. <br>
Mitigation: Use this as a lightweight first-pass scanner only, then manually review the skill and investigate material findings before installation. <br>
Risk: Scanning a broad local path may expose more files than intended to the scanner process. <br>
Mitigation: Run the skill on a copied or narrowly scoped skill directory. <br>
Risk: The CLI depends on the click Python package when run directly. <br>
Mitigation: Install or provide the click dependency in the execution environment before using the CLI. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evezart/evez-skill-vetter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Shell commands] <br>
**Output Format:** [Plain text CLI report and JSON-like scan report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a 0-100 risk score and findings with severity, category, file, and line when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
