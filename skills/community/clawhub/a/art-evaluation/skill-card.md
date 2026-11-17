## Description:

Evaluates uploaded artwork, provides critique and improvement suggestions, can produce a simulated optimized image, and lists representative artists and works for the selected art category.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickliu54](https://clawhub.ai/user/nickliu54)

### License/Terms of Use:

MIT-0

## Use Case:

Artists, educators, and developers can use this skill to assess uploaded artwork across categories such as sketch, comics, calligraphy, landscape, figure, and oil painting, then receive critique, improvement guidance, optional optimized-image output, and representative artist references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The image-output script can overwrite any writable file if given an arbitrary output path.

Mitigation: Run the skill in a sandbox or with a fixed output directory, and do not allow arbitrary output paths.

Risk: Future external image-service integrations could expose proprietary artwork or retain generated outputs outside the user's environment.

Mitigation: Do not use proprietary artwork with external image services unless the user explicitly approves where the image is sent and how outputs are retained.

Risk: The release is an incomplete placeholder skill and should not be trusted as production-ready automation without review.

Mitigation: Review before installing and scan the skill before deployment.

## Reference(s):

- [Evaluation Criteria](references/evaluation_criteria.md)
- [Representative Artists and Works](references/representative_artists.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance, Files]

**Output Format:** [Markdown prose and JSON, with optional generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read an uploaded image path and category, and may write optimized image files to a configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
