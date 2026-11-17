## Description:

AI Prompt Optimizer helps users turn creative ideas into structured bilingual prompts for Seedance 2.0 video, Seedream 4.0 image, and Kling O1 video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoxty](https://clawhub.ai/user/xiaoxty)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creative developers use this skill to convert brief image or video ideas into clear prompts, parameter suggestions, and optimization notes for supported AI generation tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill defaults to Chinese responses, which may not match every user's preferred response language.

Mitigation: Override the response language in the calling prompt when another language is required.

Risk: Generated prompts and parameter suggestions may need review before use in downstream image or video generation tools.

Mitigation: Review the optimized prompt, target tool selection, and suggested parameters before submitting them to a generation service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaoxty/skills/ai-prompt-optimizer)
- [Seedance 2.0 Prompt Guide](artifact/seedance-guide.md)
- [Seedream 4.0 Prompt Guide](artifact/seedream-guide.md)
- [Kling O1 Prompt Guide](artifact/kling-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with bilingual prompt text, parameter recommendations, and optimization notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese responses while providing optimized prompts in Chinese and English.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
