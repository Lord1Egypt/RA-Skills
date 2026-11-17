## Description:

Helps growth teams plan and document ad or landing-page A/B tests, including sample size, run length, decision rules, and results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US growth teams and media buyers use this skill to plan ad and landing-page conversion tests, estimate sample sizes, set run and decision rules, and record results.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The sample-size calculator is incomplete, and the template's baseline field does not match the calculator's expected field.

Mitigation: Check rate units and field names, then independently calculate sample sizes before committing advertising spend.

Risk: The script overwrites calculation.md in the selected output folder.

Mitigation: Choose a folder where replacing calculation.md is acceptable or preserve any existing report before running the script.

Risk: The optional Windows app is a separate executable decision; the clean verdict does not validate that executable.

Mitigation: Assess the Windows app separately and run it only if its trust and safety have been independently established.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rapidworker1/skills/ab-test-plan-designer)
- [Experiment rules](references/experiment-rules.md)
- [Publisher homepage (metadata link; not provenance)](https://github.com/rapidworker1)

## Skill Output:

**Output Type(s):** [Markdown, YAML, Guidance]

**Output Format:** [Markdown calculation report and YAML test-plan template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report is written as calculation.md in the selected output folder and may overwrite an existing file with that name.]

## Skill Version(s):

1.0.7 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
