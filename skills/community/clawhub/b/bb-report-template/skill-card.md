## Description:

Generate professional bug bounty reports for HackerOne, Bugcrowd, and other platforms with pre-filled templates, CWE mapping, reproduction steps, and severity assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hostilespider](https://clawhub.ai/user/hostilespider)

### License/Terms of Use:

MIT-0

## Use Case:

Security researchers and developers use this skill to generate structured bug bounty report drafts for HackerOne, Bugcrowd, or generic submission workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-specified output path may overwrite an existing file.

Mitigation: Choose a new report path or confirm the destination before using --output.

Risk: Generated reports contain placeholders and severity guidance that may be incomplete for a real finding.

Mitigation: Review and customize reproduction steps, impact, evidence, remediation, CWE, and severity before submission.

## Reference(s):

- [Bug Bounty Report Template on ClawHub](https://clawhub.ai/hostilespider/skills/bb-report-template)
- [Publisher profile: hostilespider](https://clawhub.ai/user/hostilespider)
- [MITRE CWE](https://cwe.mitre.org/)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown report text written to stdout or a user-specified file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; generated reports include editable placeholders for evidence, impact, remediation, and submission checklists.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
