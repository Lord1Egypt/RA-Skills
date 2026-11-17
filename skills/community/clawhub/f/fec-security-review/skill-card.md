## Description:

Reviews frontend code for XSS, CSRF, sensitive-data exposure, unsafe DOM usage, authentication risks, and third-party dependency risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Frontend developers and security reviewers use this skill to assess changes, selected files, or a project for browser-side security risks and receive prioritized findings with repair suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unscoped review may inspect the entire frontend project and save a report under reports/.

Mitigation: Specify files or directories for a narrower review and check the report before sharing it.

## Reference(s):

- [Security review checklist](references/security-checklist.md)
- [Security review report template](references/report-template.md)
- [Frontend Craft project homepage (package metadata)](https://github.com/bovinphang/frontend-craft)
- [ClawHub skill listing](https://clawhub.ai/bovinphang/skills/fec-security-review)

## Skill Output:

**Output Type(s):** [Markdown, Security review guidance]

**Output Format:** [Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Severity-ranked findings with file and line references, repair suggestions, review scope, and completion status; saved under reports/.]

## Skill Version(s):

2.9.0 (source: ClawHub release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
