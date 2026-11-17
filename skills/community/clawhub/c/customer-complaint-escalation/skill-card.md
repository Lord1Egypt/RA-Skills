## Description:

Builds a US complaint escalation path with severity tiers, response deadlines, repeat issue flags and review request limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US customer service managers, e-commerce support leads, and shop owners use the skill to define complaint severity tiers, response and resolution targets, approved remedies, repeat-issue handling, and complaint-record practices.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The bundled script reports duplicate complaints but does not produce the complete escalation plan described by the skill.

Mitigation: Treat its report as one input and separately complete and review the tiers, remedies, deadlines, and record notes.

Risk: The CSV reader can misread the template header when its two leading comment lines remain.

Mitigation: Remove those comment lines before running the script and confirm that the expected columns were read.

Risk: Complaint reports may contain customer details.

Mitigation: Limit access to reports and store them using the organization's approved handling practices.

Risk: The optional Windows application is a separate unsigned download and is not part of the skill bundle.

Mitigation: Assess the application separately, verify its published SHA-256 before use, and avoid running it with elevated privileges unless necessary.

## Reference(s):

- [US complaint, refund and dispute rules](artifact/references/complaint-escalation-rules.md)
- [ClawHub skill release](https://clawhub.ai/rapidworker1/skills/customer-complaint-escalation)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Structured complaint escalation guidance and Markdown duplicate report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Human review is required before customer communication or remedy approval; the duplicate-report script does not generate a complete escalation plan.]

## Skill Version(s):

1.0.6 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
