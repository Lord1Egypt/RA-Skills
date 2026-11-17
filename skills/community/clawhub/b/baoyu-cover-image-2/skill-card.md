## Description:

Generates article cover images by combining configurable cover type, palette, rendering style, text density, mood, font, aspect ratio, language, watermark, and reference-image options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nengnengz](https://clawhub.ai/user/nengnengz)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, and developers use this skill to turn article content or direct input into reusable cover-image prompts, generation guidance, saved source/reference files, and final cover images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The image prompt includes unconditional language to avoid refusal on sensitive or copyrighted-figure requests.

Mitigation: Review or edit the base prompt before installation to remove unconditional refusal override language and make safety and provider rules explicit.

Risk: Article content, reference images, generated prompts, and prompt notes can be saved locally, which can expose private or rights-sensitive material if used casually.

Mitigation: Avoid quick mode for sensitive inputs, confirm rights and consent for reference images or real people, and review saved source, reference, and prompt files before generation or sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nengnengz/skills/baoyu-cover-image-2)
- [OpenClaw homepage](https://github.com/JimLiu/baoyu-skills#baoyu-cover-image)
- [Auto-selection rules](references/auto-selection.md)
- [Base prompt](references/base-prompt.md)
- [Compatibility matrices](references/compatibility.md)
- [Preference schema](references/config/preferences-schema.md)
- [Reference image handling](references/workflow/reference-images.md)
- [Prompt template](references/workflow/prompt-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, generated prompt files, saved source/reference assets, completion reports, and cover image file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save local source files, reference-image descriptions, prompt markdown, and a cover.png output under the configured output directory.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence; artifact frontmatter reports 1.56.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
