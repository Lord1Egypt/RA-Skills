## Description:

Searches public debt notices for collateral clues and summarizes disclosed collateral, related parties, and source links without asserting ownership or value.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninjaliang](https://clawhub.ai/user/ninjaliang)

### License/Terms of Use:

MIT-0

## Use Case:

People researching publicly disclosed debt notices can search by property, parcel, address, or asset type and review related debtors, sellers, guarantors, and collateral descriptions with links to the original notices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional guest access writes a short-lived credential and random device identifier locally and sends limited attribution metadata to agent.debtop.com.

Mitigation: Prefer an existing connector; explain the local files and metadata sharing, and obtain user consent before creating or rebuilding guest credentials.

Risk: Matches in public notices can be mistaken for proof of property rights, valuation, or current lien status.

Mitigation: Quote and link the original notice, flag location ambiguities, and avoid ownership, valuation, or legal conclusions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ninjaliang/skills/debtop-collateral-check)
- [Tool and field reference](artifact/references/tools-and-fields.md)
- [Guest access guidance](artifact/references/guest-access.md)
- [Error handling reference](artifact/references/errors.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown report with cited notice links and collateral excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports source and lookup time; distinguishes disclosed text from inferred or unverified property details.]

## Skill Version(s):

1.0.1 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
