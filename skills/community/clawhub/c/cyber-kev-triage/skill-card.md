## Description:

Prioritize vulnerability remediation using KEV-style exploitation context plus asset criticality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x-professor](https://clawhub.ai/user/0x-professor)

### License/Terms of Use:


## Use Case:

Security teams, vulnerability managers, and remediation engineers use this skill to rank CVEs by exploitation status, severity, and asset criticality, then produce patch priority guidance and due windows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports can overwrite existing files, including when dry-run mode is supplied.

Mitigation: Choose output paths deliberately and avoid pointing the report output at existing files that should be preserved.

Risk: CSV reports can carry untrusted vulnerability or asset data into spreadsheet software.

Mitigation: Prefer JSON or Markdown output, or sanitize CSV content before opening it in a spreadsheet.

## Reference(s):

- [KEV Triage Method](references/triage-method.md)
- [Cyber KEV Triage on ClawHub](https://clawhub.ai/0x-professor/skills/cyber-kev-triage)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, CSV, Shell commands, Guidance]

**Output Format:** [JSON, Markdown, or CSV patch triage reports with ranked vulnerabilities, priority tiers, scores, and recommended due windows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script accepts JSON vulnerability and asset input up to 1048576 bytes and can emit json, md, or csv output.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
