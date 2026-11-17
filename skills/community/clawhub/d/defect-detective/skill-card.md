## Description:

Provides read-only defect triage by normalizing bug signals, checking for duplicate tickets, correlating relevant recent code changes, and identifying a likely owning team.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yumingtao](https://clawhub.ai/user/yumingtao)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill before fixing or filing a bug to check whether it is already tracked, identify a likely owner, and review relevant recent changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic details used as search terms may disclose sensitive information to the configured issue tracker; the security review was incomplete.

Mitigation: Review and redact sensitive diagnostic content before searching, and confirm that the configured tracker is approved to receive it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/yumingtao/skills/defect-detective)
- [Triage examples](references/triage-examples.en.md)
- [Verification record](references/verification-record.en.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured triage report with search evidence and an optional ticket draft]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only; does not create tickets or modify code]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
