## Description: <br>
Security-focused code review for hardcoded secrets, dangerous calls, and common vulnerabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itsnishi](https://clawhub.ai/user/itsnishi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan project repositories before commits, pull request reviews, periodic audits, or after AI-assisted code generation. It reports hardcoded secrets, dangerous calls, SQL injection patterns, dependency risks, sensitive files, permissive file modes, and exfiltration patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads selected project files, including .env-like files, and may print matched snippets in its report. <br>
Mitigation: Run it only on repositories whose contents can be reviewed in the agent session, and handle generated reports as potentially sensitive. <br>
Risk: Detected pip and npm package names may be checked against public package registries. <br>
Mitigation: Avoid or network-restrict the skill for confidential repositories where private package names must not be sent to PyPI or npm. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/itsnishi/audit-code) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with severity-ranked findings, file locations, matched patterns, and remediation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scans local source files up to 1 MB each and may verify detected pip or npm package names against public registries.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
