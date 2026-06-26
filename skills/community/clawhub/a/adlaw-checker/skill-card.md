## Description: <br>
Checks Chinese advertising copy for prohibited advertising-law terms, false-advertising language, platform-specific rule concerns, risk levels, and suggested revisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eric060](https://clawhub.ai/user/eric060) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and content operators use this skill to review Chinese advertising copy for risky claims before publication. It returns detected terms, risk assessment, compliance scores, suggested replacements, and revised copy drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compliance output may be mistaken for legal advice. <br>
Mitigation: Treat results as review assistance and have important commercial copy reviewed by qualified legal or compliance staff. <br>
Risk: Advertising rules, platform policies, and forbidden-word lists can become stale. <br>
Mitigation: Update the word lists and platform-specific rules regularly before relying on the skill for publication workflows. <br>
Risk: CLI use with file inputs can expose unintended local files if paths are chosen carelessly. <br>
Mitigation: Use normal caution with file paths passed to the command-line checker and review generated reports before sharing them. <br>


## Reference(s): <br>
- [Adlaw Checker on ClawHub](https://clawhub.ai/eric060/adlaw-checker) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.zh-CN.md](artifact/README.zh-CN.md) <br>
- [中华人民共和国广告法](http://www.gov.cn/gongbao/content/2015/content_2893774.htm) <br>
- [小红书社区规范](https://www.xiaohongshu.com/community_guidelines) <br>
- [微信公众号运营规范](https://mp.weixin.qq.com/cgi-bin/announce?action=getannouncement) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Markdown guidance and JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes violation lists, risk levels, compliance scores, suggested replacements, and compliant copy drafts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
