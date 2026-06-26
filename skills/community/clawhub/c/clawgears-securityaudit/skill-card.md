## Description: <br>
Conducts macOS security audits for OpenClaw-based AI assistants to detect exposure risks, weak tokens, sensitive commands, permissions issues, and IP leaks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JinHanAI](https://clawhub.ai/user/JinHanAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to audit local macOS assistant security, inspect exposed gateway configurations, check token strength, review sensitive command protections, and optionally apply configuration fixes with consent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect local OpenClaw configuration, macOS security state, logs, and permission databases. <br>
Mitigation: Review the shell scripts before use and run the read-only quick check before enabling any fix workflow. <br>
Risk: Public IP and exposure checks contact external services and may send the user's public IP address. <br>
Mitigation: Use the IP leak check only when that network disclosure is acceptable for the environment being audited. <br>
Risk: Token rotation and audit output can expose token fragments or sensitive local security findings in terminal output and generated files. <br>
Mitigation: Treat terminal output, reports, and backups as sensitive and avoid sharing them without redaction. <br>
Risk: Interactive fixes may modify OpenClaw configuration, restart services, or require elevated firewall changes. <br>
Mitigation: Require explicit user consent for fix actions, keep backups, and manually verify hardening results after changes. <br>


## Reference(s): <br>
- [ClawGears ClawHub Skill Page](https://clawhub.ai/JinHanAI/clawgears-securityaudit) <br>
- [Publisher Profile](https://clawhub.ai/user/JinHanAI) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, terminal output, and local JSON or HTML audit reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local OpenClaw and macOS security state, contact public-IP and exposure-check services, and write local reports or configuration backups.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
