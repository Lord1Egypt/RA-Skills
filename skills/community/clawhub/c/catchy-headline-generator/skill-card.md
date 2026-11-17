## Description:

根据用户输入的内容主题生成5个不同风格的中文社交媒体爆款标题，并附带平台适配、预估点击率、推荐标题和发布建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hadderyes](https://clawhub.ai/user/hadderyes)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media operators, and marketing writers use this skill to turn a content topic into five Chinese headline options tailored for platforms such as Xiaohongshu, Douyin, WeChat Official Accounts, Bilibili, and Weibo.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad title-writing requests and return a prescriptive Chinese social-media format when another language or style is expected.

Mitigation: Invoke it explicitly for Chinese social media headline generation, or override language, platform, and output format in the user prompt.

Risk: Generated headlines and CTR estimates may encourage overly sensational framing or imply engagement certainty.

Mitigation: Review each title for accuracy, platform policy, brand fit, and audience expectations before publishing.

## Reference(s):

- [爆款标题公式库 - 完整参考](references/title-formulas.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style structured Chinese text with content analysis, five headline candidates, CTR estimates, one recommendation, and publishing suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, credential access, persistence, or external data flow identified by server security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
