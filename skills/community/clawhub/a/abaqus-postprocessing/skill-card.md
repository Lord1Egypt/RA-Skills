## Description:

Provides Chinese-language guidance for Abaqus postprocessing workflows, including result visualization, output data types, data processing, graphics display, data export, and explicit-analysis checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jijinbao-code](https://clawhub.ai/user/jijinbao-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and structural engineers use this skill to review Abaqus/CAE postprocessing steps, select relevant output variables, export plots and tabular data, and sanity-check explicit-analysis energy histories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example Abaqus snippets and export workflows can create local report, image, animation, or data files and may consume significant disk space when used with large ODB files.

Mitigation: Review snippets before execution, run them against intended ODB files only, and confirm output paths and available disk space before exporting reports or animations.

Risk: Postprocessing conclusions depend on the quality and setup of the underlying Abaqus analysis.

Mitigation: Validate model setup, units, output frequency, and energy-history checks before relying on exported plots or reports.

## Reference(s):

- [Abaqus documentation](https://help.3ds.com)
- [ClawHub skill page](https://clawhub.ai/jijinbao-code/skills/abaqus-postprocessing)
- [ClawHub publisher profile](https://clawhub.ai/user/jijinbao-code)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown guidance with Abaqus Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested Abaqus/CAE menu actions, output variable names, export steps, and postprocessing checks.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
