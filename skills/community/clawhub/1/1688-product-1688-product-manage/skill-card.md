## Description:

将商品图片、文字、文档或参考商品链接整理为逐商品素材包，生成类目、SKU 和商品发布信息，并保存 1688 新商品草稿供用户编辑；收到素材但未明确发品意图时先询问用途。

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

1688 sellers and their agents use this skill to organize product images, text, documents, and reference listings into per-product material packages, prepare listing fields, and save editable product drafts. The seller reviews and publishes each draft in 1688.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product details or generated listing content may need correction before publication.

Mitigation: Review generated prices, inventory, specifications, and claims before publishing.

Risk: Product materials may be shared with 1688 services without authorization.

Mitigation: Use an authorized 1688 store and provide only materials you may share with its services.

Risk: Local source copies and task records remain in the workspace after processing.

Mitigation: Remove local source copies and task records when they are no longer needed.

## Reference(s):

- [1688 AI 发品 skill](https://clawhub.ai/1688aiinfra/skills/1688-product-1688-product-manage)
- [Tool boundaries and store authorization](artifact/references/00-01-tools.md)
- [Product intake and material packages](artifact/references/01-00-intake.md)
- [Category and SKU handling](artifact/references/02-01-category.md)
- [Draft assembly and delivery](artifact/references/04-00-draft.md)

## Skill Output:

**Output Type(s):** [Files, Text, Markdown]

**Output Format:** [Per-product material files and an editable 1688 product draft, with a concise Markdown status and draft link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts remain unpublished until the user reviews and publishes them in 1688.]

## Skill Version(s):

0.1.0 (source: frontmatter; server release 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
