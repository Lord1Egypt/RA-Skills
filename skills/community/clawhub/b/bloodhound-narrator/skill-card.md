## Description:

Turns BloodHound attack path exports into dual-layer Markdown security reports with executive risk prose and technical remediation guidance, using local PowerShell without API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kurostrike](https://clawhub.ai/user/kurostrike)

### License/Terms of Use:

MIT-0

## Use Case:

Pentesters, blue teams, Active Directory security consultants, and security managers use this skill to turn BloodHound Cypher export JSON into client-ready attack path reports and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local PowerShell against BloodHound exports, which can contain sensitive Active Directory security data.

Mitigation: Run it only in a trusted local environment, treat exports and generated reports as sensitive, and use trusted input when possible.

Risk: Generated Markdown reports may include fields from the input export.

Mitigation: Open generated reports in a Markdown viewer that disables raw HTML and remote resource loading until untrusted fields are escaped by the project.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kurostrike/skills/bloodhound-narrator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with console summary text and optional PowerShell objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against BloodHound Cypher export JSON; default report file is BH-Narrator-Report-<timestamp>.md.]

## Skill Version(s):

1.0.2 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
