## Description: <br>
Scan any OpenClaw skill for security issues before installing: malware, prompt injection, obfuscation, and supply chain attacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mackding](https://clawhub.ai/user/mackding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan OpenClaw skill directories for malware, prompt injection, obfuscation, supply-chain, and data-exfiltration signals before installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an external npm scanner package to inspect the target skill directory. <br>
Mitigation: Run it on a specific skill directory, avoid broad private folders, and pin or verify the @claws-shield package version before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mackding/claws-security-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON scan output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports a security grade, confidence score, severity breakdown, install recommendation, manual review flags, and remediation suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
