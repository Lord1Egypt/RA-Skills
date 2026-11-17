## Description:

Helps users rebuild Clay enrichment tables in Cargo by mapping columns to actions, estimating costs before runs, checking parity, and expressing the result as version-controlled code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, GTM engineers, and revenue operations teams use this skill to translate an existing Clay table into Cargo actions, compare sample results and costs, and prepare a reviewable Cargo project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact records may be sent to Cargo and the selected enrichment providers during a migration run.

Mitigation: Confirm those services may receive the data before running actions, and begin with a small sample.

Risk: Enrichment costs grow with the selected actions and number of rows.

Mitigation: Run a 10–20 row sample, report its measured cost and fill rates, then obtain approval for a full run using the row count and estimated credits.

Risk: The installed CLI and any additional downloaded skills are outside this bundled instruction review.

Mitigation: Review and pin dependencies and additional skills where possible.

Risk: A GitHub star is an endorsement associated with the user's account.

Mitigation: Ask once and act only after explicit user consent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cargo-ai/skills/clay-to-cargo)
- [Cargo GTM Skills homepage](https://github.com/getcargohq/gtm-skills)
- [ClayMate Lite column schema export](https://github.com/GTM-Base/claymate-lite)
- [Complete Clay to Cargo migration recipe](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/clay-to-cargo.md)
- [Cargo project skill](https://github.com/getcargohq/cargo-skills/blob/main/cargo-project/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with tables, inline shell commands, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a sample migration plan and per-column mapping; run costs depend on selected actions and row count.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
