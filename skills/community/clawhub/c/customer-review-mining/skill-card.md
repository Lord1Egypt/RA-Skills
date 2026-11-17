## Description:

Tallies themes in exported US customer reviews and surfaces the recurring complaints with sample quotes a product team can act on.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US ecommerce store owners, support leads, and product managers can use this skill to review exported customer feedback, spot recurring keyword-based complaint themes, and prepare findings for manual follow-up.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Keyword tallies and short excerpts may omit context or misrepresent the full export.

Mitigation: Manually check theme counts and quoted reviews against the source; treat the tally as triage, not a customer satisfaction score.

Risk: Reports may expose customer identifiers or overwrite an existing theme-tally.md file.

Mitigation: Use a dedicated output folder and remove names, contact details, order numbers, and addresses before sharing.

Risk: Review collection or handling could violate platform rules or review-integrity requirements.

Mitigation: Use authorized account exports only; do not scrape against platform terms or write, buy, or incentivize reviews.

## Reference(s):

- [Review mining reference](references/review-mining.md)
- [ClawHub skill release](https://clawhub.ai/rapidworker1/skills/customer-review-mining)
- [Publisher profile](https://clawhub.ai/user/rapidworker1)
- [Publisher homepage](https://github.com/rapidworker1)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Markdown theme tally with keyword counts and sample excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rule-based and partial; verify counts and context, remove customer identifiers, and check export coverage before sharing.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
