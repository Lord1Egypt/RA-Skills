## Description:

Generates structured prompts for AI video and image generation models, adapting natural-language creative requests to model-specific prompt formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creative teams, and developers use this skill to turn natural-language media ideas into model-adapted prompts for video, image, product image, poster, and multi-shot generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional preference memory could preserve user prompt style or model preferences without clear user intent.

Mitigation: Keep preference saving opt-in, reviewable, and clearable through the host agent's normal memory controls.

Risk: Generated media prompts may contain incorrect model adaptation, language choice, or physically implausible scene details.

Mitigation: Use the skill's self-check and acceptance criteria before copying prompts into downstream media-generation systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-video-prompt-architect)
- [Generation Modes](references/generation-modes.md)
- [Prompt Templates Library](references/prompt-templates.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Usage Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured analysis tables and copy-ready prompt code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include model metadata, notes, video parameters, positive prompts, negative prompts, and multi-shot prompt sections.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
