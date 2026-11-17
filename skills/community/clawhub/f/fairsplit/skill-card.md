## Description:

Split group expenses and settle up in the fewest payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[himadriganguly](https://clawhub.ai/user/himadriganguly)

### License/Terms of Use:

MIT-0

## Use Case:

People sharing expenses on trips, in households, or at events use FairSplit to record contributions, see balances, and plan settlement payments without moving money.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared expense records are stored as local JSON files.

Mitigation: Choose a suitable data directory and limit access to the stored records.

Risk: Undo removes an expense and init --force resets a group's history.

Mitigation: Confirm the intended change before either operation and review balances afterward.

Risk: Exports can write financial details to a chosen file, and live exchange-rate lookups require network access.

Mitigation: Choose export paths deliberately; request live rates only when needed and check the rate used for conversion.

## Reference(s):

- [FairSplit release](https://clawhub.ai/himadriganguly/skills/fairsplit)
- [FairSplit CLI reference](references/cli-reference.md)
- [Settlement algorithm](references/settlement-algorithm.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Plain-text balances and settlement plans; optional CSV or Markdown exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores expense records as local JSON files; does not transfer money.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
