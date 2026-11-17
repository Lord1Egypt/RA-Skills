## Description:

Generate structured wedding-photo prompt packages for couples using either predefined wedding-style templates or custom user ideas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garkinchu](https://clawhub.ai/user/garkinchu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creative agents use this skill to plan cohesive AI wedding-photo or couple-portrait sets from templates, custom concepts, or reference images. It can produce direct images when the runtime supports image generation, or a reusable multi-shot prompt package when prompt-only output is required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled templates may apply default Chinese ethnicity or facial-trait wording to subjects even when that does not match the user's real couple photos.

Mitigation: Review and edit template subject profile and base prompt fields, or override them at use time, so the output preserves the actual subjects rather than a default ethnicity.

Risk: Identity-based wedding image generation can be misused with unauthorized photos or presented as real documentary evidence.

Mitigation: Use only authorized photos of the actual couple and avoid requests intended to deceive viewers about whether generated wedding images are real.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/garkinchu/skills/ai-wedding-studio)
- [Workflow](references/workflow.md)
- [Package Schema](references/package-schema.md)
- [Quality Rules](references/quality-rules.md)
- [Chinese Studio Xiuhe Wedding template](assets/packages/chinese-xiuhe-studio.yml)
- [Dali Sunrise Wedding template](assets/packages/dali-sunrise.yml)
- [Maldives Sunset Wedding template](assets/packages/maldives-sunset.yml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text prompt packages with package summary, base prompt, negative prompt, 8-shot prompt set, and usage notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include direct image outputs when the active runtime supports image generation; otherwise produces prompt packages for use in image tools.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
