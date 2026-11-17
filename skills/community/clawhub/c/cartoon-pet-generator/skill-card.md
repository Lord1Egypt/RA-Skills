## Description:

Generate cute cartoon-style pet images such as dogs, cats, rabbits, and bears using local SVG generation and PNG conversion without an AI image API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juliantsaiii](https://clawhub.ai/user/juliantsaiii)

### License/Terms of Use:


## Use Case:

External users and developers use this skill when they need an agent to create simple cartoon pet avatars or animal illustrations by running a local Node.js script and returning the generated image path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-controlled output filename can lead to shell command execution during image conversion.

Mitigation: Use only trusted, fixed output paths until the conversion command uses shell-free argument arrays and validates output filenames.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juliantsaiii/skills/cartoon-pet-generator)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and generated PNG/SVG file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated file path may be returned to the user or embedded by the host agent as an image attachment.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
