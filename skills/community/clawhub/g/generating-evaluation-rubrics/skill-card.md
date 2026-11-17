## Description:

Generates structured classroom evaluation rubrics from lesson plans, including learning-process star ratings and scored learning-outcome criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyboat403](https://clawhub.ai/user/flyboat403)

### License/Terms of Use:

MIT-0

## Use Case:

Educators and instructional designers use this skill to turn lesson-plan content into structured classroom assessment rubrics. It is intended for primary, secondary, and vocational education contexts where users need observable criteria, star-rated process measures, scored outcomes, and editable preview output before spreadsheet generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact references local files for examples and Excel generation that are not included in the submitted artifact.

Mitigation: Verify that required reference and script files are bundled before installation; otherwise use the Markdown preview path or add the missing files before spreadsheet generation.

Risk: The skill may ask the agent to install a mutable Python dependency in the local environment.

Mitigation: Review dependency changes before execution, prefer an isolated environment, and pin package versions for release use.

Risk: The skill may ask the agent to run a relative script path that writes output files.

Mitigation: Inspect the referenced script before execution and confirm the intended output path before writing files.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/flyboat403/generating-evaluation-rubrics)
- [ClawHub skill page](https://clawhub.ai/flyboat403/skills/generating-evaluation-rubrics)
- [ClawHub publisher profile](https://clawhub.ai/user/flyboat403)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown previews, JSON-like rubric data, shell commands, and generated spreadsheet files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rubric guidance expects process criteria with star ratings and outcome criteria with scores totaling 100.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
