## Description:

Court Prep helps agents provide court preparation guidance, including document preparation, evidence organization, litigation timelines, fee estimates, and small-claims support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to get command-line court-preparation assistance, including checklists, complaint templates, evidence guidance, litigation timeline estimates, and fee calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A bundled script can store legal entries and command history on local disk, which may expose case details, names, financial amounts, or legal strategy.

Mitigation: Use non-sensitive placeholders unless storage location, logging behavior, and deletion controls are documented and acceptable for the deployment environment.

Risk: The generated court materials and fee or timeline estimates may be jurisdiction-specific, incomplete, or unsuitable for a real case.

Mitigation: Treat outputs as preparation aids only and have a licensed legal professional or qualified reviewer verify filings, deadlines, fees, and strategy before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/court-prep)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and terminal-oriented plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces checklists, complaint templates, evidence guidance, timeline estimates, fee estimates, and command usage guidance.]

## Skill Version(s):

2.3.5 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
