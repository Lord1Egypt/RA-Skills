## Description:

A multi-platform article publishing skill for Zhihu, Bilibili, Baijiahao, Toutiao, and Xiaohongshu that uses Playwright browser automation, QR-code login, and persistent cookies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phoenix1630](https://clawhub.ai/user/phoenix1630)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to log in to supported creator platforms, check account status, and publish prepared article content to one or more platforms from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content publicly across logged-in accounts, including through publish_to_all.

Mitigation: Use testMode first, manually confirm every target platform and article, and avoid publish_to_all for sensitive or brand accounts.

Risk: Reusable login cookies are stored locally and can act as bearer credentials if exposed.

Mitigation: Keep the working directory private, do not sync or commit cookie files, and use logout to clear saved cookies when finished.

Risk: Dependency and browser setup guidance may use mirror or npx install commands.

Mitigation: Prefer official registries, trusted download sources, and pinned dependency installs where possible.

## Reference(s):

- [ClawHub Article Publisher skill page](https://clawhub.ai/phoenix1630/skills/article-publisher)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text with structured result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open a browser session, save local cookies, and return platform status, publish results, URLs, errors, or test-mode confirmations.]

## Skill Version(s):

1.5.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
