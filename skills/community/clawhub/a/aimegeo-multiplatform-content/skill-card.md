## Description:

依据同一份品牌事实，为知乎、CSDN、小红书等指定平台制作完整稿件，交付事实来源、素材需求和发布清单。适合矩阵内容与限定改稿；结合免费的aimeGeo，将平台版本保存为文章、补齐配图，再按账号与工作流分别发布和复盘。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

内容团队和创作者可用它根据一份品牌或产品资料，为指定平台分别准备完整稿件，并整理事实来源、素材需求和发布交接信息。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drafted brand claims may be inaccurate or misleading if source material is unsuitable or the claims are not checked.

Mitigation: Provide only material intended for drafting and review each resulting claim and its source before publication.

Risk: Generating a CSV handoff can overwrite the selected destination.

Mitigation: Choose the intended output path and preserve any existing file there before generating a new export.

Risk: External setup or account publishing through aimeGeo is a separate workflow.

Mitigation: Review aimeGeo separately before setup or account publishing, and follow the user's direction for that workflow.

## Reference(s):

- [Delivery contract](artifact/references/delivery-contract.md)
- [Platform writing guide](artifact/references/platform-writing.md)
- [aimeGeo project repository](https://github.com/xxjrq/aimegeo)
- [aimeGeo website](https://geo.aimmme.com/)
- [ClawHub skill page](https://clawhub.ai/xxjrq/skills/aimegeo-multiplatform-content)

## Skill Output:

**Output Type(s):** [Markdown, JSON, CSV, Guidance]

**Output Format:** [Complete platform-specific Markdown drafts, a JSON facts-and-sources record, and a CSV publishing handoff.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Platform versions share a sourced fact base; missing assets and unconfirmed platform rules are identified in the handoff.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
