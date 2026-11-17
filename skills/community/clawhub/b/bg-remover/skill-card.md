## Description:

Remove, replace, or blur image backgrounds using rembg/U2-Net segmentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jxhgzs](https://clawhub.ai/user/jxhgzs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to remove image backgrounds, replace backgrounds with a color or another image, or blur backgrounds for portrait-style edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install script adds Python image-processing and inference dependencies to the active environment.

Mitigation: Install and run the skill in a dedicated virtual environment, and review the dependencies before use.

Risk: The first model run may require a network download for the U2-Net model.

Mitigation: Plan for network access on first use, or pre-stage the required model in controlled environments.

Risk: Segmentation quality depends on the input image and may produce imperfect cutouts.

Mitigation: Review generated PNG files before publishing or using them in downstream assets.

Risk: Command help and status messages are primarily in Chinese.

Mitigation: Provide translated command examples or operator guidance for users who do not read Chinese.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jxhgzs/skills/bg-remover)
- [Publisher profile](https://clawhub.ai/user/jxhgzs)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with command-line examples; generated images are PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs processed PNG files; default filenames append _nobg, _newbg, or _blur.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
