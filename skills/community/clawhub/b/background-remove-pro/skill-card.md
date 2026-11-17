## Description:

Removes image backgrounds using AI models and writes transparent PNG outputs for single images or batches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to remove backgrounds from product, portrait, ID, and other image files, including batch workflows that need transparent PNG assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes local image files and writes output files, so an incorrect input or output path could expose or overwrite unintended files.

Mitigation: Run it with limited filesystem access, review input and output paths before execution, and use overwrite mode only when replacement is intended.

Risk: The skill depends on third-party Python packages and may download model artifacts on first use.

Mitigation: Pin and verify dependency versions and model artifacts before using it in stricter or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxliuyu/skills/background-remove-pro)
- [Publisher profile](https://clawhub.ai/user/sxliuyu)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Transparent PNG files with command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs default to PNG files with a _nobg suffix unless an output path or keep-name option is supplied.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
