## Description:

Generate a professional infographic from an article, document, URL, or topic, using the baoyu layout x style system (21 layouts x 21 styles). Original author 宝玉 (JimLiu); ported & customized by j3ffyang. Use when the user asks to create an infographic, 信息图, visual summary, 可视化, or a high-density information image, or wants an article turned into a visual poster.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and developers use it to turn supplied articles, documents, URLs, or topics into structured visual summaries and infographic images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source-derived content may reach external services.

Mitigation: Check for private or sensitive material and confirm it can be sent to the chosen image service before generating.

Risk: ClawScan reports privacy and scope concerns and an unsafe boundary when processing images returned by an external service; scanning was partial.

Mitigation: Review the trigger and image-processing flow, keep inputs within the requested scope, and inspect returned images before using them.

## Reference(s):

- [Infographic workflow and design references](artifact/SKILL.md)
- [Analysis framework](artifact/references/analysis-framework.md)
- [Project reference linked in skill metadata](https://github.com/JimLiu/baoyu-skills#baoyu-infographic)

## Skill Output:

**Output Type(s):** [Images, Markdown, Text prompts]

**Output Format:** [PNG infographic plus Markdown planning files and a Markdown image-generation prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation uses an external image service and requires an API key and an image-capable model.]

## Skill Version(s):

1.56.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
