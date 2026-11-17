## Description:

Generates Chinese standard ID photos from user-provided portraits with standard sizes, white, blue, or red backgrounds, JPEG or PNG output, and OpenCV-based face detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert local portrait images into Chinese ID, passport, visa, and other standard document-photo formats with selected dimensions and background colors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may install Python image-processing dependencies and download the rembg model at first run.

Mitigation: Use a trusted environment, consider a virtual environment, and review or pin dependencies before running the skill.

Risk: The skill processes sensitive portrait or identity-photo inputs.

Mitigation: Process private images only in a trusted local workspace and avoid sharing generated output directories unintentionally.

Risk: Automatic face detection and background removal can produce document photos that fail official requirements.

Mitigation: Review the generated photo dimensions, crop, background, and face placement before submitting it for official use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tobewin/skills/china-id-photo)
- [Publisher Profile](https://clawhub.ai/user/tobewin)
- [Chinese ID Photo Size Reference](artifact/references/sizes.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, files]

**Output Format:** [Markdown guidance with inline bash and Python code blocks; generated image files are JPEG or PNG.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files are written to a local id_photo timestamped output directory.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact frontmatter says 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
