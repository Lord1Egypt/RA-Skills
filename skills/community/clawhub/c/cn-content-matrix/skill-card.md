## Description: <br>
Chinese multi-platform content matrix generator that creates platform-native drafts and compliance reviews for Xiaohongshu, WeChat Official Account, Douyin, and Bilibili from a topic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fullstackcrew-alpha](https://clawhub.ai/user/fullstackcrew-alpha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content marketers, creators, and social-media teams use this skill to turn a topic into Chinese platform-native content variants and review drafts for format, tone, sensitive terms, SEO, and publishability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Topic research may send campaign ideas, customer details, unreleased product names, or sensitive draft themes to web search. <br>
Mitigation: Use non-confidential topics or sanitized briefs when invoking research-backed generation. <br>
Risk: Generated drafts are saved locally under ~/content-output and may include sensitive campaign context supplied by the user. <br>
Mitigation: Avoid sensitive inputs unless local persistence is acceptable, and review generated files before sharing or publishing. <br>


## Reference(s): <br>
- [CN Content Matrix ClawHub page](https://clawhub.ai/fullstackcrew-alpha/cn-content-matrix) <br>
- [Bilibili content guide](references/bilibili.md) <br>
- [Content core template](references/content-core-template.md) <br>
- [Douyin script guide](references/douyin.md) <br>
- [Sensitive words guide](references/sensitive-words.md) <br>
- [WeChat Official Account guide](references/wechat-mp.md) <br>
- [Xiaohongshu content guide](references/xiaohongshu.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown files with YAML frontmatter, plus console review reports and optional fix suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written under ~/content-output by date and topic when generation commands are used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
