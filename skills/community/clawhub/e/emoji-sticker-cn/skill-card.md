## Description:

Helps create and prepare emoji stickers for Chinese platforms, including platform-specific sizing, text checks, and emotion-matched animated GIFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonniegeng-max](https://clawhub.ai/user/bonniegeng-max)

### License/Terms of Use:

MIT

## Use Case:

External creators use the skill to develop sticker concepts and prepare image sets for WeChat, Xiaohongshu, and Douyin. It also helps check platform requirements, review promotional text, and create animated GIF variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release scan flags an unpinned installer and possible external text checking without clear disclosure; the scan was partial and its evidence is incomplete.

Mitigation: Use a known installer version and tell users before sending text to an external checking service; review the skill and its behavior because the partial scan is not a complete assessment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/bonniegeng-max/skills/emoji-sticker-cn)
- [WeChat sticker creation specifications](https://sticker.weixin.qq.com/cgi-bin/mmemoticon-bin/readtemplate?t=guide/index.html#/makingSpecifications#specifications_stickers)
- [WeChat sticker review standards](https://sticker.weixin.qq.com/cgi-bin/mmemoticon-bin/readtemplate?t=guide/index.html#/auditingStandards#auditingStandards_demand)
- [Chinese platform sticker size specifications](references/中文平台表情包尺寸规范.md)
- [Chinese platform prohibited-word reference](references/中文平台违禁词合规参考.md)
- [Animation matching rules](references/动效匹配规则.md)
- [Static pose and action library](references/静态姿势动作库.md)

## Skill Output:

**Output Type(s):** [Images, GIF files, Markdown, Shell commands, Code]

**Output Format:** [Sticker image assets and animated GIFs, with Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image dimensions, formats, and file limits depend on the selected platform and sticker type.]

## Skill Version(s):

3.3.0 (source: frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
