## Description:

Converts Feishu Docs or Wiki pages into Xiaohongshu-style posts by rendering 1242x1660 image cards, preparing summary, title, and hashtag copy, and packaging the output into a Feishu document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaohuaishu](https://clawhub.ai/user/xiaohuaishu)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and technical writers use this skill to convert Feishu source documents into Xiaohongshu-ready image posts with accompanying publishing copy and a Feishu staging document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled Feishu credentials are present and may allow access under unclear account control.

Mitigation: Remove and rotate the exposed secret before installation, then configure least-privilege Feishu app credentials through environment variables.

Risk: The skill can upload user-generated images and markdown to Feishu documents.

Mitigation: Review generated content and confirm the destination account and document ownership before running uploads.

Risk: The image renderer loads generated HTML in Chromium.

Mitigation: Render only trusted HTML, disable JavaScript and outbound network access where practical, and pin Playwright/browser dependency versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaohuaishu/skills/feishu-xhs-publisher)
- [Publisher profile](https://clawhub.ai/user/xiaohuaishu)
- [Design styles reference](artifact/references/design-styles.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands, generated HTML/PNG assets, publishing copy, and a Feishu document link.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Renders 1242x1660 image cards and can upload generated content to Feishu when credentials are configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
