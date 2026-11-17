## Description:

从任意图提取干净商品平铺图。真人图 / 街拍图 → 白底平铺商品图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

服装电商运营者和设计人员可将上身照、街拍或买家秀转换为白底服装平铺图，用作商品素材或后续图像流程的输入。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source photos may be uploaded to an external image provider without a clear disclosure, creating privacy concerns for customer or other people's images.

Mitigation: Before processing real photos, disclose the external upload and confirm that the images are authorized for that use.

Risk: Details hidden by arms, bags, hair, or other obstructions are inferred rather than recovered from the source.

Mitigation: Review inferred areas against the original and manually confirm important design details; use a less-obstructed image when possible.

## Reference(s):

- [ClawHub release](https://clawhub.ai/dlazyai/skills/clothing-extraction)
- [Provider CLI and data flow reference](references/provider-cli.md)
- [Image model flags reference](references/model-flags.md)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Image files, Shell commands, Guidance]

**Output Format:** [JPEG or PNG clothing flat-lay images, with command examples and guidance in Markdown]

**Output Parameters:** [1D; one source image per extraction]

**Other Properties Related to Output:** [Square 1024×1024 output on a white background. Occluded garment details may be inferred and should be checked against the source.]

## Skill Version(s):

1.0.34 (source: frontmatter; server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
