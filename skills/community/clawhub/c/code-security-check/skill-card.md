## Description: <br>
Audits the current project for sensitive information leaks before pushing to public repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mate-matt](https://clawhub.ai/user/mate-matt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to assess whether a project is at risk of exposing credentials, tokens, private keys, or incomplete .gitignore coverage before public release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects repository files for secrets and may encounter sensitive credentials during an audit. <br>
Mitigation: Keep credentials redacted in outputs, review findings before approving fixes, and rotate any credential that was already committed or exposed. <br>
Risk: Remediation guidance can affect repository tracking or ignore rules if applied incorrectly. <br>
Mitigation: Review proposed changes before execution and require explicit user confirmation before modifying project files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mate-matt/code-security-check) <br>
- [Publisher profile](https://clawhub.ai/user/mate-matt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with redacted findings and optional shell commands for remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should redact full secrets and ask for explicit user confirmation before modifying files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
