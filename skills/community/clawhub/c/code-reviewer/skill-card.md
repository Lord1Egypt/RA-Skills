## Description: <br>
Code Reviewer helps review code changes, pull requests, or repositories across major programming languages for security, performance, code quality, error handling, testing, and documentation issues, with optional local HTML reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nameused](https://clawhub.ai/user/nameused) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review diffs, pull requests, single files, or repositories before merge and to triage security, quality, performance, testing, documentation, and error-handling issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated review reports may include source snippets or exposed secrets from the reviewed project. <br>
Mitigation: Scope reviews to intended files or directories and keep generated reports private. <br>
Risk: Automated scans and AI review can produce false positives or miss context-dependent issues. <br>
Mitigation: Confirm findings against the actual code context before acting on them or blocking a release. <br>


## Reference(s): <br>
- [Code Reviewer Skill Page](https://clawhub.ai/nameused/code-reviewer) <br>
- [Code Review Checklist](references/checklist.md) <br>
- [Security Vulnerability Detection Rules](references/security-rules.md) <br>
- [Language-Specific Best Practices](references/best-practices.md) <br>
- [Severity Classification Guide](references/severity-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown findings and recommendations, optional JSON analysis results, and optional local HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are severity-ranked and may include file paths, line numbers, snippets, and remediation guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
