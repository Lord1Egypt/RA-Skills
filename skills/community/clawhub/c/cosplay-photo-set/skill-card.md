## Description:

将角色名称或参考图转化为真人 cosplay 套图流程，包含角色设定、分镜提示词、图像质检、腿脚肤色统一和发布文案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang-shuanglin](https://clawhub.ai/user/wang-shuanglin)

### License/Terms of Use:

MIT-0

## Use Case:

希望在本机制作角色 cosplay 图集的创作者，可从角色名称或参考图生成角色卡、真人基准图提示词和 4–6 镜头的成片脚本，并整理成竖版图集及配套发布文案。流程包含用户确认节点和成片质检。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 安全证据指出，故障排查内容建议绕过 PowerShell 安全措施，且扫描覆盖不完整，五个本地路径引用未能匹配到随包文件。

Mitigation: 安装前检查相关 PowerShell 建议和确切脚本；除非已检查脚本并信任其来源，否则不要通过绕过策略或 Invoke-Expression 运行。确认本地路径引用指向的内容后再使用。

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wang-shuanglin/skills/cosplay-photo-set)

## Skill Output:

**Output Type(s):** [Guidance, Text, Images, Code]

**Output Format:** [角色设定与生成提示词、分镜脚本、竖版 JPEG 图集、发布文案及图像处理脚本]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [通常为 4–6 张 9:16 图像，并附标题、正文和标签。]

## Skill Version(s):

2.1.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
