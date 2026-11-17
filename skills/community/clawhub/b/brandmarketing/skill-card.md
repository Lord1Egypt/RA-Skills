## Description:

AI 智能品牌营销工具：输入品牌名称，自动采集全网数据、分析当日热点、生成一篇小红书图文内容，支持一键自动发布

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongxiaoke](https://clawhub.ai/user/dongxiaoke)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and marketing operators use this skill to generate Xiaohongshu-ready brand marketing posts from a brand name, current hot-topic analysis, generated copy, tags, and image links. It can guide manual posting or, after explicit user confirmation, attempt browser-assisted publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend paid Zeelin credits when content generation succeeds.

Mitigation: Confirm the user's balance and cost before generation, avoid duplicate requests during the five-minute timeout window, and stop when balance is insufficient.

Risk: The skill stores a reusable App-Key locally for later use.

Mitigation: Tell users where the key is stored, limit local file access, support key replacement, and recommend deleting or rotating the key when no longer needed.

Risk: One content-generation API example uses plain HTTP while carrying the App-Key.

Mitigation: Prefer an HTTPS endpoint when available and rotate any key that may have been transmitted over an insecure channel.

Risk: Automated Xiaohongshu publishing can violate platform rules and may lead to account penalties.

Mitigation: Default to manual posting, display the explicit automation risk warning, and require affirmative user confirmation before any browser-assisted publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dongxiaoke/skills/brandmarketing)
- [Publisher Profile](https://clawhub.ai/user/dongxiaoke)
- [Zeelin Skill Platform](https://skills.zeelin.cn)
- [Xiaohongshu Creator Center](https://creator.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown and plain text with JSON API payloads, curl examples, credential setup guidance, generated titles, body copy, tags, image links, and optional publishing steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated posts target Xiaohongshu limits: titles up to 20 Chinese characters, body text up to 1000 Chinese characters, and up to 9 jpg/png images.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
