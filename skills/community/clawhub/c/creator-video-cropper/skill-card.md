## Description:

Crop videos to focus on the most important area for social, ecommerce, ads, and storefront use without making the result look clumsy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and ecommerce teams use this skill to plan tighter video crops that preserve the important subject for social, storefront, ads, and product placement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A proposed video editing command could write to the wrong path or overwrite an original video.

Mitigation: Review any command or output path before execution and prefer writing cropped exports to a new file.

Risk: A static crop can fail when the subject moves outside the selected area.

Mitigation: Flag motion-heavy footage and choose a conservative crop or a motion-tracking workflow when static framing is likely to break.

## Reference(s):

- [Video Cropper Output Template](references/output-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown crop plan with input summary, crop rationale, motion risk notes, and recommended next step]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable files are packaged; output should warn when static cropping may fail on motion-heavy footage.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
