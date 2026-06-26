## Description: <br>
API Key Guardian scans repositories and files for leaked API keys, passwords, tokens, private keys, database URLs, and generic hardcoded secrets, with optional git-history scanning and AI risk analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaohuaishu](https://clawhub.ai/user/xiaohuaishu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to check projects for exposed credentials before committing, sharing, or releasing code. It can scan a directory, a single file, or recent git history and can optionally ask a local OpenClaw-compatible gateway for risk and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional AI mode includes an embedded API-key-like value. <br>
Mitigation: Remove the embedded value and require users to supply their own credential through a trusted local configuration or environment variable before enabling AI analysis. <br>
Risk: Optional AI mode sends finding metadata such as file paths and line numbers to a local HTTP service. <br>
Mitigation: Use --ai only with a trusted local OpenClaw/model gateway and review what metadata will be sent before running it on sensitive repositories. <br>
Risk: Secret-scanning results can include sensitive matches, even when masked in terminal output. <br>
Mitigation: Review findings locally, avoid sharing raw scan output externally, and rotate any credential that may have been exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaohuaishu/api-key-guardian) <br>
- [Publisher Profile](https://clawhub.ai/user/xiaohuaishu) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, analysis, guidance] <br>
**Output Format:** [Terminal text report with masked findings and optional AI-generated risk guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings include pattern name, severity, source path, line number, and masked matched value.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
