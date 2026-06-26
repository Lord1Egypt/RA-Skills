## Description: <br>
AI Agent security scanner for multi-language detection, AST analysis, intent recognition, and optional LLM verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caidongyun](https://clawhub.ai/user/caidongyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and marketplace operators use this skill to scan AI agent skills or code for potentially malicious behavior, risky patterns, credential exposure, and supply-chain concerns before release or deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Detection metrics and reporting may be unreliable for security decisions. <br>
Mitigation: Validate scanner results on representative benign and malicious samples before using the output for allow, reject, or escalation decisions. <br>
Risk: Optional LLM, webhook, or email features may send code, paths, findings, or other sensitive context outside the local environment. <br>
Mitigation: Keep external analysis and alerting disabled until data flows are reviewed, secrets are protected, and sensitive content can be redacted. <br>
Risk: The release is flagged suspicious by the authoritative security evidence. <br>
Mitigation: Review source behavior and run the scanner in a controlled environment before installing it where proprietary code, secrets, or regulated data are present. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caidongyun/agent-security-scanner) <br>
- [Publisher profile](https://clawhub.ai/user/caidongyun) <br>
- [Homepage from ClawHub metadata](https://github.com/caidongyun/agent-security-skill-scanner#readme) <br>
- [Repository from artifact metadata](https://github.com/caidongyun/agent-security-skill-scanner) <br>
- [Architecture documentation](docs/ARCHITECTURE.md) <br>
- [Capabilities documentation](docs/CAPABILITIES.md) <br>
- [User guide](docs/USER_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Command-line scan results, Python result objects, and Markdown or JSON security reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include risk scores, risk levels, detected behaviors, and remediation guidance.] <br>

## Skill Version(s): <br>
4.1.6 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
