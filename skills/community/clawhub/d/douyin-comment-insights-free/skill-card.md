## Description:

读取用户指定抖音视频或图文作品页面当前真实可见的评论样本，提炼需求主题、用户问题、反对点、脱敏原话证据和谨慎的回复草稿。仅复用用户已授权的 Easy WebBridge 浏览器，不需要第三方内容 API Key；支持确定性 mock fixture 自测。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者和运营人员可用此技能查看一个抖音作品页面当前可见的评论样本，整理用户需求、问题和反对点，并生成经过脱敏、尚未发送的回复草稿。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A failed run removes earlier successful report files from the selected output directory.

Mitigation: Use a dedicated output directory and save reports that need to be retained before rerunning.

Risk: Visible comments can include personal or sensitive text, and the sample may lack context.

Mitigation: Review the generated redacted report before sharing it, and treat its findings as a limited sample rather than a representative view of all users.

Risk: Browser access may encounter a login, verification, or other access gate.

Mitigation: Use only a browser environment the user has authorized; stop for user action at access gates and do not bypass them.

## Reference(s):

- [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge)
- [EasyBR official download page](https://www.ebrower.com/down.html)
- [Easy WebBridge Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Text]

**Output Format:** [JSON and Markdown reports with visible comment samples, needs, questions, objections, redacted evidence, and unsent reply drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one work page; defaults to at most 20 visible comments (configurable from 1 to 50); omits author identities and redacts detected sensitive text.]

## Skill Version(s):

1.0.3 (source: package.json and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
