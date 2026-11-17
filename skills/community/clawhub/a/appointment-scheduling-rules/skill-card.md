## Description:

Creates drafts of appointment policies, cancellation rules, and reminder copy for U.S. service businesses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

External U.S. service businesses use the skill to draft appointment and cancellation policies and email or text reminders. Treat the results as drafts, and have the business owner or qualified counsel review legal, consent, privacy, and state-specific requirements before use.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The included checker may miss warning phrases it is intended to detect, so its results may not reliably flag problematic reminder copy.

Mitigation: Correct and test the checker before relying on its results, and review the copy independently.

Risk: Draft policies and reminders may not satisfy applicable privacy, consent, legal, or state-specific requirements.

Mitigation: Have the business owner and qualified counsel independently review requirements before sending or adopting the drafts.

Risk: Real customer details in shared templates could expose private information.

Mitigation: Keep real customer details out of shared templates.

Risk: The optional Windows app is unsigned and is not needed for the bundled workflow.

Mitigation: Assess it separately before use; the bundled workflow runs with Python and does not require the app.

## Reference(s):

- [US appointment, reminder and cancellation rules](artifact/references/appointment-and-reminder-rules.md)
- [ClawHub release](https://clawhub.ai/rapidworker1/skills/appointment-scheduling-rules)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Appointment policy and reminder drafts, typically in Markdown or YAML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft content requires review; do not include real customer details in shared templates.]

## Skill Version(s):

1.0.6 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
