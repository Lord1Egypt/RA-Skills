## Description:

Builds a US complaint escalation path with severity tiers, response deadlines, repeat issue flags and review request limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US customer service managers, e-commerce support leads, and shop owners use the skill to set complaint severity tiers, response targets, remedy approvals, repeat-issue handling, and record-keeping rules.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The reported duplicate-reporting behavior may not match the stated complaint-escalation purpose.

Mitigation: Review the skill's actual behavior against the intended complaint-escalation tasks before use.

Risk: The skill's file-writing scope is not declared.

Mitigation: Review where the script writes output and direct it only to an approved folder.

## Reference(s):

- [US complaint, refund and dispute rules](references/complaint-escalation-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured complaint-escalation guidance and a Markdown duplicate report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a CSV complaint log as input; the included script writes duplicates.md to the selected output directory.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
