## Description:

EKB Decision Algorithm analyzes life decisions using Expected Value, Kelly Criterion, and Bayesian updating across career, investment, relationship, education, and lifestyle choices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[truenorth-lj](https://clawhub.ai/user/truenorth-lj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to structure major life decisions with a repeatable EKB framework. It supports quick judgment, deeper resource audits, and optional EV/Kelly calculations when the user provides quantitative assumptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be invoked by broad decision-making language and may research sensitive life, financial, relationship, or employment facts online.

Mitigation: Confirm with the user before external research and avoid private names, account details, exact holdings, medical details, or sensitive relationship and employment context unless necessary.

Risk: The skill requests broad Write and Bash permissions even though the normal quantitative workflow only needs the bundled calculator.

Mitigation: Prefer the ClawHub-reviewed install path, review proposed commands before execution, and limit Bash use to the bundled calculator when possible.

Risk: Decision guidance can be misleading if probabilities, payoffs, or current facts are uncertain or incomplete.

Mitigation: Treat outputs as advisory analysis, surface key assumptions and information gaps, and use professional review for regulated or high-stakes financial, legal, medical, or employment decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/truenorth-lj/skills/decision-algorithm)
- [Methodology](docs/methodology.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown decision analysis with optional calculator output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 for the bundled EV/Kelly calculator; fact-dependent decisions may require current research before analysis.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
