## Description:

Generates detailed parametric 3D models from text descriptions using Python and Trimesh, with STL export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vonzellu](https://clawhub.ai/user/vonzellu)

### License/Terms of Use:


## Use Case:

Developers and makers use this skill to convert textual 3D model descriptions into Python/Trimesh generation workflows and STL assets for prototyping or 3D-print preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run user-influenced Python code without adequate safeguards.

Mitigation: Use trusted prompts and simple output names, review generated Python before execution, and run generation in a constrained sandbox with strict output-path validation.

Risk: Scheduled or automated generation may execute unsafe generated code without review.

Mitigation: Avoid scheduled or automated use until review and sandbox controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vonzellu/skills/ai-3d-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workflows may create Python scripts and STL files in a local export directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
