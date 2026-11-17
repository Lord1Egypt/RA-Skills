## Description:

CinePrompt helps agents generate structured AI video prompts and storyboard scripts using a five-dimension ideation framework and a seven-element video-language toolkit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slfcys](https://clawhub.ai/user/slfcys)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and video prompt writers use this skill to turn a video idea into structured AI video prompts, storyboards, and segmented shot plans with role cards, style cards, keyframe anchors, and audio timing notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad prompt-writing or storyboard requests outside video prompting, or when another language is needed.

Mitigation: Confirm the task is video-prompt creation and the requested output language before using the skill.

Risk: Generated prompts may include visual, audio, timing, and post-production guidance that exceeds the target video model's limits.

Mitigation: Review segment length, model constraints, and content safety before submitting prompts to a video generator.

## Reference(s):

- [CinePrompt ClawHub page](https://clawhub.ai/slfcys/skills/five-seven-videoprompt)
- [Five Dimensions Framework](artifact/references/five-dimensions.md)
- [Video Spectrum - Seven Elements](artifact/references/video-spectrum.md)
- [Segmented Generation Rules](artifact/references/segmented-rules.md)
- [Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown video prompt, storyboard, role and style cards, keyframe anchors, and audio timing notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; supports single-segment and segmented video prompt structures.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
