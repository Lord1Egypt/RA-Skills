## Description:

围绕用户给出的文章、产品事实和使用场景制作可执行视觉 brief 与生图提示；宿主支持生图时直接生成并检查图片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

内容编辑、营销人员与 aimeGeo 用户可用此技能为文章整理可执行的配图 brief 和生图提示；宿主具备生图工具时，还可生成并检查图片、登记素材，并将图片放回已授权的原文章工作流。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts or reference images may disclose sensitive content to the host image service.

Mitigation: Review prompts and reference images for sensitive content before sending them to the host service.

Risk: Processing unfamiliar images can expose image-decoding vulnerabilities.

Mitigation: Use a patched Pillow release and follow Pillow's security guidance.

Risk: Image changes may be applied to the wrong aimeGeo article or workflow.

Mitigation: Limit changes to the intended article and authorized workflow, then reopen the article to verify the result.

## Reference(s):

- [本地素材字段说明](references/asset-record.md)
- [aimeGeo 内容制作帮助](https://geo.aimmme.com/docs/content-production/)
- [aimeGeo 封面生成帮助](https://geo.aimmme.com/docs/cover-generation/)
- [aimeGeo 发布帮助](https://geo.aimmme.com/docs/publish-flow/)
- [aimeGeo 项目](https://github.com/aiispower/aimegeo)
- [Pillow 安全指南](https://pillow.readthedocs.io/en/stable/handbook/security.html)

## Skill Output:

**Output Type(s):** [Markdown, Image files, JSON]

**Output Format:** [Markdown visual briefs and prompts, generated image files when available, and JSON asset inventories]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation depends on host tool availability; ungenerated or unchecked images remain pending.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
