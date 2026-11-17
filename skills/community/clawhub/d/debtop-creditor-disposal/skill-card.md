## Description:

Summarizes publicly announced debt-transfer and disposal notices for a named creditor, including amounts, debtors, timelines, and links to individual notices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninjaliang](https://clawhub.ai/user/ninjaliang)

### License/Terms of Use:

MIT-0

## Use Case:

Creditors, asset managers, and other users can review a named bank's or seller's public debt-disposal notices to identify available assets and compare notice types, amounts, and debtors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Guest access contacts agent.debtop.com and stores a guest token and device identifier locally.

Mitigation: Review the guest-access helper before use and protect the token cache at ~/.cache/debtop as sensitive data.

Risk: Repeated or concurrent guest-helper runs may create unnecessary credentials or trigger shared rate limits.

Mitigation: Reuse or refresh an existing guest token and avoid repeated or concurrent helper runs.

Risk: Public notices may be incomplete or outdated and do not establish a debtor's creditworthiness.

Mitigation: Show the query time and original notice links; do not infer undisclosed debts or credit ratings.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ninjaliang/skills/debtop-creditor-disposal)
- [Notice tools and fields](references/tools-and-fields.md)
- [Guest access guide](references/guest-access.md)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown report with notice tables and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes query time, public-notice caveats, type and amount summaries, and unaltered notice links.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
