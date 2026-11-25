## Description:

Generate visually unified image-based PPT/PPTX decks from articles, reports, papers, notes, or outlines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[notegpt-official](https://clawhub.ai/user/notegpt-official)

### License/Terms of Use:

MIT-0

## Use Case:

People preparing teaching, research, or business presentations can turn articles, reports, papers, notes, or outlines into visually consistent image-based PowerPoint decks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source text and images may be sent to the selected image service, which may be unsuitable for confidential material.

Mitigation: Identify the configured image provider and confirm its data handling is acceptable before supplying confidential content.

Risk: The security analysis was incomplete because some referenced local paths were absent, and dependency versions are not pinned.

Mitigation: Review the complete files needed for the workflow and check dependency versions before installing or running the skill.

Risk: The scanner reports broad tool capabilities.

Mitigation: Review the requested actions and limit file access and permissions to what the presentation task requires.

## Reference(s):

- [ClawHub release](https://clawhub.ai/notegpt-official/skills/creative-slides)
- [Source repository and skill directory](https://github.com/notegpt-official/notegpt-skills/tree/main/skills/ai-image-ppt)
- [Slide generation guidance](docs/slide-generation.md)
- [User-supplied assets guidance](docs/user-supplied-assets.md)

## Skill Output:

**Output Type(s):** [PowerPoint presentation, Image files, Markdown, JSON]

**Output Format:** [Image-based .pptx deck with supporting slide images, Markdown outline and speaker notes, and JSON deck specification and prompt files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Slides are full-slide images assembled into a .pptx; individual text, charts, and shapes are not separately editable.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
