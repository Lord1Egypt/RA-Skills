## Description:

Turn a topic into a Douyin-ready short video script with hook, storyboard, captions, and BGM suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, e-commerce sellers, and content teams use this skill to turn a topic or product brief into a Douyin-ready short video plan with timed scenes, voiceover, subtitles, BGM guidance, publish windows, and cover copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save prompt details, including confidential campaign plans or unreleased product information, to a predictable local file.

Mitigation: Review inputs before use, avoid confidential campaign or product details, or modify the skill to require explicit opt-in and a user-selected private path before saving prompts.

Risk: Outputs are oriented toward Chinese-language Douyin workflows and may not fit other platforms, regions, or audiences without review.

Mitigation: Review and adapt generated scripts, captions, music suggestions, and publish windows for the target platform, region, and audience before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/douyin-script-writer-v1)
- [BGM Examples](artifact/references/bgm-examples.json)
- [15s Template](artifact/references/templates/15s-template.json)
- [30s Template](artifact/references/templates/30s-template.json)
- [60s E-Commerce Template](artifact/references/templates/60s-ecommerce-template.json)
- [Input Schema](artifact/schemas/input.schema.json)
- [Output Schema](artifact/schemas/output.schema.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown or JSON short-video script package with timed storyboard fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports 15, 30, and 60 second scripts; JSON output includes scenes, subtitles, BGM, publish time, summary, and cover copy.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, artifact frontmatter, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
