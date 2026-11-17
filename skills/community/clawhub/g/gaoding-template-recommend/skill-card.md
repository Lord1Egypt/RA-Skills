## Description:

搜索稿定设计模板。当用户想制作海报、名片、Banner、电商主图等设计，或搜索/推荐设计模板时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gezilinll](https://clawhub.ai/user/gezilinll)

### License/Terms of Use:

MIT

## Use Case:

Design and marketing users can ask an OpenClaw agent, in Chinese, to search Gaoding templates for posters, business cards, banners, e-commerce images, and similar design work. The skill returns template previews and lets the user choose, edit text, and export a design when configured with a Gaoding account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Gaoding username and password and stores session cookies locally.

Mitigation: Use a low-privilege Gaoding account, restrict access to the .env and cookie files, and rotate credentials if either file is exposed.

Risk: Browser automation may break or return incomplete results when Gaoding changes page structure.

Mitigation: Review the returned screenshot and template titles before recommending a template or exporting a design.

Risk: The artifact includes editing, export, and troubleshooting behavior that can affect local generated files or global OpenClaw session state.

Mitigation: Review generated design files before sharing them and avoid session-state troubleshooting workarounds unless the user backs up the affected file and understands the impact.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gezilinll/skills/gaoding-template-recommend)
- [Gaoding Design](https://www.gaoding.com)
- [OpenClaw](https://github.com/nicepkg/openclaw)
- [Troubleshooting Notes](docs/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, JSON, files, guidance]

**Output Format:** [JSON results with template metadata, screenshot file paths, user-facing text, and exported design file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, Playwright Chromium, a configured Gaoding account, and Chinese search keywords; browser automation depends on Gaoding page structure.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
