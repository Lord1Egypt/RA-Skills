## Description:

使用用户指定的 Easy WebBridge browserId，只读检查本人已打开的 B站投稿草稿及当前可见栏目，整理封面、标题、简介、分区、素材的缺项和修改建议，并逐条保留页面可见来源。适合发布前快速核对；账号、稿件归属或页面不能确认时立即停止，不保存、不提交、不发布，缺料如实标注。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

B站创作者在发布前使用此技能检查自己已打开且归属可确认的投稿草稿，获取封面、标题、简介、分区和素材的缺项、修改建议及可见页面来源。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports an unpinned installer, a mutable source, and incomplete analysis of some script content; the benign verdict is not a guarantee that every component was fully assessed.

Mitigation: Before installing the separate external skill, verify the source and version and review the relevant script content; treat the scan verdict as limited evidence.

## Reference(s):

- [EasyBR 官方下载页](https://www.ebrower.com/down.html)
- [Easy WebBridge 项目](https://github.com/xxjrq/easy-webbridge)
- [Easy WebBridge Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)
- [EasyBR v1.7.8 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown checklist with observed values, missing fields, suggestions, and visible-page sources]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to 100 asset or table rows per run; each checked field retains a visible-page source.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
