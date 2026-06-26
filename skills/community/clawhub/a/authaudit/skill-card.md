## Description: <br>
Authentication and authorization pattern analyzer that scans codebases for missing auth checks, insecure sessions, broken access control, CSRF gaps, and token handling vulnerabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use AuthAudit to run local authentication and authorization checks across application source code before commits, releases, or security reviews. It reports findings, scores auth posture, and can generate JSON, Markdown, or HTML reports depending on tier and options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted license key can trigger local code execution through the current license-token parser. <br>
Mitigation: Use license keys only from a trusted source, do not test untrusted license or JWT strings, and review the license parser before installing in sensitive environments. <br>
Risk: Installed git hooks cause AuthAudit to run automatically during future repository commit or push workflows. <br>
Mitigation: Install hooks only in repositories where automatic auth scanning is intended, and review the generated lefthook configuration before enabling it. <br>
Risk: The skill may handle sensitive authentication code and license credentials during local scans. <br>
Mitigation: Run it in a trusted local environment, avoid exposing scan output publicly, and store AUTHAUDIT_LICENSE_KEY through approved local configuration or secret-management practices. <br>


## Reference(s): <br>
- [ClawHub AuthAudit release page](https://clawhub.ai/suhteevah/authaudit) <br>
- [AuthAudit website](https://authaudit.dev) <br>
- [AuthAudit pricing](https://authaudit.dev/#pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, JSON, Markdown reports, HTML reports, and shell commands for scans or git-hook setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local scanner output may include file paths, line numbers, severities, recommendations, auth posture scores, and process exit codes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
