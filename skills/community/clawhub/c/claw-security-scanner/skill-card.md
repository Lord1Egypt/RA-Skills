## Description: <br>
Claw Security Scanner scans OpenClaw skill directories for potential credential leaks, suspicious code patterns, dependency risks, and insecure configuration, then reports findings with remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BetsyMalthus](https://clawhub.ai/user/BetsyMalthus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, security reviewers, and teams use this skill to scan local OpenClaw skill folders before installation, release, or periodic review. It helps identify credentials, suspicious code behavior, dependency concerns, and configuration issues, then produces reports that support manual remediation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may include real secrets or sensitive snippets found in scanned skills. <br>
Mitigation: Treat JSON, Markdown, and console reports as sensitive artifacts; redact findings before sharing or uploading them. <br>
Risk: The tool reads the skill directories it is pointed at, and broad or automatic scan modes can expand the amount of local code inspected. <br>
Mitigation: Prefer targeted local scans, run with least necessary file access, and avoid enabling broad auto-scan behavior unless scope and retention are clear. <br>
Risk: Documentation advertises URL scanning, dynamic analysis, and auto-fix style workflows that require stronger isolation and rollback guarantees than the server evidence confirms. <br>
Mitigation: Use static local scanning by default and require human review before enabling URL-scan, dynamic-analysis, or auto-fix behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BetsyMalthus/claw-security-scanner) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact installation guide](artifact/INSTALLATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Console text, JSON reports, Markdown reports, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include matched evidence from scanned files and should be handled as sensitive when secrets are detected.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
