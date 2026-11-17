## Description:

服装平铺图一键上身试穿。服装平铺图 + 姿势参考图 → 模特上身商拍图，款式、颜色、织法、版型保持不变。当用户说「平铺图转模特图」「衣服上身」「虚拟试穿」「AI 试衣」「让模特穿上」时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

电商商家和内容团队可将服装平铺图与姿势或场景参考图合成为模特上身商品图，也可为多件服装生成统一造型。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with medium confidence; only 5 of 9 components were fully inspected. Image inputs are sent to the selected external generation provider.

Mitigation: Review the partially inspected components and confirm the selected provider's privacy terms before uploading garment or model images.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dlazyai/skills/flat-lay)
- [Provider CLI and data flow](references/provider-cli.md)
- [Image model flags](references/model-flags.md)

## Skill Output:

**Output Type(s):** [Image files, Shell commands]

**Output Format:** [JPEG product images, typically 1024×1536, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review generated images for garment color, texture, fit, print placement, anatomy, and background before use.]

## Skill Version(s):

1.0.33 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
