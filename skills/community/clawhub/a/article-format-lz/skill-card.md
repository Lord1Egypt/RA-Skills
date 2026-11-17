## Description:

Formats Chinese self-media articles for WeChat Official Account and Toutiao publishing, generating editor-compatible HTML with selectable platform styles and reusable article components.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuzheng60](https://clawhub.ai/user/liuzheng60)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, editors, and publishing teams use this skill to turn article drafts into polished HTML for WeChat Official Account or semantic HTML for Toutiao. It helps select platform-specific structure, style palettes, and components such as titles, lists, quotes, tables, data cards, code blocks, and key-value layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may not match publisher expectations when used for non-Chinese content or pasted from untrusted user-supplied HTML.

Mitigation: Preview and review the generated HTML before publishing, especially outside zh-CN WeChat or Toutiao workflows.

Risk: Platform-specific editor behavior may strip or alter formatting.

Mitigation: Use inline CSS output for WeChat and semantic HTML output for Toutiao, then verify the pasted result in the target editor.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuzheng60/skills/article-format-lz)
- [Publisher profile](https://clawhub.ai/user/liuzheng60)
- [Design system reference](references/design-system.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [HTML and Markdown-style guidance for article formatting workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces WeChat inline-CSS HTML or Toutiao semantic HTML; users should preview generated HTML before publishing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
