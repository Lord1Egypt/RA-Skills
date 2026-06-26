## Description: <br>
Security gatekeeper for skill installations that scans ClawHub, GitHub, and external skill sources for malicious patterns, credential access, data exfiltration, command injection, and other security risks before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amir-ag](https://clawhub.ai/user/amir-ag) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill as a pre-install security check for external agent skills. It helps review local skill folders and automation workflows before installation by producing risk scores, findings, and install-blocking exit codes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A SAFE result can be mistaken for a guarantee that a skill is safe to install. <br>
Mitigation: Treat scanner output as advisory and manually review findings before installing external or high-privilege skills. <br>
Risk: Line-based regex checks can miss malicious behavior or produce incomplete findings. <br>
Mitigation: Pair the scan with source review, especially for scripts that request broad filesystem, network, credential, or shell access. <br>
Risk: Automated install gating can block or allow installs based only on heuristic score thresholds. <br>
Mitigation: Use --install-if-safe as a guardrail, not as the only approval control for sensitive environments. <br>


## Reference(s): <br>
- [Threat Patterns Reference](references/threat-patterns.md) <br>
- [ClawHub Skill Scanner Listing](https://clawhub.ai/amir-ag/clawhub-skill-scanner) <br>
- [ClawHavoc campaign report](https://www.esecurityplanet.com/threats/hundreds-of-malicious-skills-found-in-openclaws-clawhub/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain-text audit report or JSON summary with risk score, risk level, recommendation, file counts, and findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return a nonzero exit code with --install-if-safe when the scanned skill is not SAFE.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
