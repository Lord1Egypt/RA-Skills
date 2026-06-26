## Description: <br>
Performs proactive security audits for OpenClaw deployments, checking SQL injection, sandbox configuration, session-secret persistence, rate limiting, and Matrix E2EE documentation gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, DevOps engineers, and security reviewers use this skill before OpenClaw deployments or public exposure to run audit checks and apply reviewed remediation guidance for critical and high findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Critical audit results may be sent to Slack with sensitive details. <br>
Mitigation: Require manual approval before external notifications and redact secrets, hostnames, internal paths, and exploit details. <br>
Risk: The required MCP extension may access deployment files or Slack. <br>
Mitigation: Verify the extension before installation and grant only the file and Slack permissions needed for the intended audit channel. <br>
Risk: Remediation snippets may affect production deployment configuration. <br>
Mitigation: Treat snippets as reviewable changes, keep backups, and prepare rollback plans before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/firm-security-audit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON tool-call examples, YAML and Nginx configuration snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Slack alert guidance for critical findings and requires expert review before production remediation.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
