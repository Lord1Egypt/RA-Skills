## Description:

简报转手机长图，将结构化文字简报转化为适合手机阅读的长图，支持自定义资讯内容、标题、出品方和底部通栏广告图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xieliuzhu888](https://clawhub.ai/user/xieliuzhu888)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and business operators use this skill to turn industry, market, company, or campaign briefings into 390px-wide mobile long images for sharing on WeChat, Moments, Xiaohongshu, and similar channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local renderer opens user-supplied HTML in Chrome with the browser sandbox disabled.

Mitigation: Use trusted or sanitized HTML, consider removing --no-sandbox or running the renderer in a hardened container, and review the generated output before sharing.

Risk: Briefing content and banner assets may include inaccurate, unauthorized, or third-party material.

Mitigation: Verify facts, sources, brand assets, and permissions before publishing generated images publicly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xieliuzhu888/skills/briefing-visualizer)
- [HTML template reference](references/html_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with HTML/CSS examples, shell command examples, and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates HTML briefing layouts and long image files; uses a local Chrome/Pillow workflow when the processing script is run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
