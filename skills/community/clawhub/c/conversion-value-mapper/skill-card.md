## Description:

Conversion Value Mapper helps paid media teams define and QA conversion value models for value-based bidding, including margin-adjusted purchase values, proxy values for non-revenue actions, value-rule choices, and value-vs-count checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing practitioners, analysts, and ad account operators use this skill before launching or scaling tROAS, max-conversion-value, or similar value-based bidding. It turns user-provided revenue, margin, COGS, and lead-quality inputs into a launch-readiness-oriented value-model spec and QA sheet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive advertising economics such as revenue, margins, COGS, and proxy lead values.

Mitigation: Use only appropriate business data for the session and approve memory persistence only when those assumptions are suitable for reuse.

Risk: A value model can mislead bidding decisions when margin, COGS, close-rate, or value-vs-count inputs are missing or stale.

Mitigation: Label values as measured, user-provided, estimated, or needs-input, and do not treat the model as launch-ready until unresolved inputs and reconciliation gaps are addressed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/conversion-value-mapper)
- [Publisher profile](https://clawhub.ai/user/aaron-he-zhu)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration, Files]

**Output Format:** [Markdown guidance with value-model tables, QA findings, formulas, and handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a value-model spec and QA sheet to memory only after user confirmation.]

## Skill Version(s):

19.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
