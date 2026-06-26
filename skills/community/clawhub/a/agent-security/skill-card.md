## Description: <br>
Security hardening for AI agents. Audit your workspace for leaked secrets, check file permissions, validate API key storage, scan for prompt injection risks, and monitor for unauthorized access patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to generate local security audit commands and checklist guidance for finding leaked credentials, reviewing credential file permissions, checking API key age, and identifying sensitive files tracked by git. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan verdict is suspicious because the skill includes unexplained onlyflies.buzz network and registration endpoints. <br>
Mitigation: Review the endpoint usage before installing, remove the onlyflies.buzz target and OADP comment unless that service is intentionally required, and restrict network checks to approved hosts. <br>
Risk: Secret-scan and credential audit commands may print sensitive file paths or credential-like values. <br>
Mitigation: Run scans only on known project paths and redact any secret-scan output before sharing it. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/imaflytok/agent-security) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are intended for review and editing before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
