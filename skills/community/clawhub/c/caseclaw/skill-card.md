## Description:

caseclaw helps legal teams manage matters from the terminal by calculating filing deadlines from court rules, checking conflicts, and tracking billable time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jagadeeshmurali-coder](https://clawhub.ai/user/jagadeeshmurali-coder)

### License/Terms of Use:


## Use Case:

External legal practitioners and firm staff use caseclaw to coordinate matter intake, filing deadlines, court-rule checks, conflicts, timekeeping, and billing workflows from a terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unaudited third-party CLI that may process confidential legal data.

Mitigation: Review the Homebrew tap, source, release provenance, and privacy/security terms before installing; use an isolated environment or test data until the binary is trusted.

Risk: Pro/Firm features and email, Slack, or calendar alerts may disclose client or matter metadata to external services.

Mitigation: Enable external integrations only after approving the data flow, using firm-authorized accounts, and confirming that confidentiality obligations are satisfied.

Risk: Deadline, conflict, and court-rule outputs can be jurisdiction-dependent and may be incomplete or outdated.

Mitigation: Have qualified legal staff verify results against governing rules, docket calendars, and firm conflict procedures before relying on them.

## Reference(s):

- [caseclaw ClawHub skill page](https://clawhub.ai/jagadeeshmurali-coder/skills/caseclaw)
- [caseclaw homepage from artifact metadata](https://github.com/legal-tools/caseclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the caseclaw CLI from the configured Homebrew tap.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
