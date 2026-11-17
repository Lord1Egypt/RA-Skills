## Description:

Scan web applications for accessibility issues including WCAG 2.2 compliance, screen reader compatibility, keyboard navigation, color contrast, and ARIA usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and accessibility reviewers use this skill to audit web applications for WCAG 2.2 issues across static code, ARIA usage, keyboard navigation, focus management, color contrast, and testing-tool integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Accessibility findings may be incomplete or misleading if treated as a final compliance determination.

Mitigation: Have qualified reviewers confirm WCAG findings with manual testing, assistive technology checks, and project-specific acceptance criteria.

Risk: Suggested audit commands and tools may read web application source files.

Mitigation: Run review commands only in the intended workspace and inspect suggested tool integrations before adding them to CI or local workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/accessibility-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown audit report with optional inline shell commands and testing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; security evidence reports no hidden execution, persistence, credential access, or automatic changes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
