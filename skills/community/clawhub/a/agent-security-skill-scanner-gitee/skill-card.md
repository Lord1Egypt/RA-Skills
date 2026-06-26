## Description: <br>
Scans AI agent skills and source files for suspicious code patterns across multiple languages and can report risk findings through CLI or JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caidongyun](https://clawhub.ai/user/caidongyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to screen AI agent skills, files, and repositories for suspicious patterns, risky metadata, and optional LLM-assisted findings before installation or marketplace review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Advertised detection-rate and scanner claims may not match real-world performance. <br>
Mitigation: Independently test the scanner on representative safe and malicious samples before relying on its verdicts. <br>
Risk: Optional LLM, webhook, and email integrations may transmit sensitive code or findings to configured endpoints. <br>
Mitigation: Use controlled endpoints, isolated credentials, and avoid enabling these integrations for sensitive code unless the data flow is approved. <br>
Risk: Optional daemon, cron, or systemd-style operation can create persistent scanning processes. <br>
Mitigation: Review the exact command and removal path before enabling persistence, and keep the feature disabled unless continuous scanning is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caidongyun/agent-security-skill-scanner-gitee) <br>
- [Publisher profile](https://clawhub.ai/user/caidongyun) <br>
- [Project homepage from ClawHub metadata](https://gitee.com/caidongyun/agent-security-skill-scanner) <br>
- [User guide](docs/USER_GUIDE.md) <br>
- [Capabilities](docs/CAPABILITIES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and optional JSON scanner reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scanner output can use default, advanced, or JSON modes; optional LLM, webhook, and email features depend on user configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
