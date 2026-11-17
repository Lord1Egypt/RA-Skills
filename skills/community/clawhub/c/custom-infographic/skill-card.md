## Description:

Generate a professional infographic from an article, document, URL, or topic, using the baoyu layout x style system (21 layouts x 21 styles). Original author 宝玉 (JimLiu); ported & customized by j3ffyang. Use when the user asks to create an infographic, 信息图, visual summary, 可视化, or a high-density information image, or wants an article turned into a visual poster.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT

## Use Case:

Developers and other agents use this skill to turn supplied articles, documents, URLs, or topics into infographics. It structures the content and prepares a visual prompt, then generates an image when the configured image service is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may send source content to an external image service without a privacy warning.

Mitigation: Review what content the service receives and confirm the provider is approved before sending sensitive material.

Risk: The security analysis was marked partial because some referenced paths were missing.

Mitigation: Review and scan the complete skill contents before installation, since the available scanner evidence is incomplete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/custom-infographic)
- [Upstream project listed in skill metadata](https://github.com/JimLiu/baoyu-skills#baoyu-infographic)
- [Content analysis framework](artifact/references/analysis-framework.md)
- [Structured content template](artifact/references/structured-content-template.md)
- [Base image prompt](artifact/references/base-prompt.md)

## Skill Output:

**Output Type(s):** [Image files, Markdown]

**Output Format:** [PNG infographic with Markdown source, analysis, structured content, and image prompt files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Layout, style, aspect ratio, and language can be selected; supporting Markdown files are saved with the infographic workflow.]

## Skill Version(s):

1.56.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
