## Description:

Fetches public WeChat articles with Playwright using a real system browser, extracts the title, author, and article body, and saves Markdown and HTML copies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucky-dreamer](https://clawhub.ai/user/lucky-dreamer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user provides an mp.weixin.qq.com article link and needs a public WeChat article captured as local Markdown and HTML with article metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser can open arbitrary URLs when the input is not restricted to intended WeChat article links.

Mitigation: Review before installing, use only in an isolated environment, and pass only intended mp.weixin.qq.com article URLs.

Risk: The browser launch weakens sandboxing by using a default --no-sandbox flag.

Mitigation: Avoid sensitive environments until the browser launch removes the weakened sandbox configuration.

Risk: Generated HTML may contain content derived from untrusted pages.

Mitigation: Avoid opening generated HTML from untrusted pages until output escaping or sanitization is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucky-dreamer/skills/fetch-wechat-article)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Shell commands, Guidance]

**Output Format:** [Markdown and HTML files with terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves one Markdown file and one HTML file per fetched article, plus a title, author, and content-length summary.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
