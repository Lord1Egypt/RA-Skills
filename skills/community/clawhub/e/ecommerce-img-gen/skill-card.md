## Description:

跨境电商图片生成工具根据产品图生成 Amazon、Shopee、TikTok Shop、Lazada、AliExpress、Temu 和 SHEIN 的主图、详情页长图和生活场景图，并提供风格路由与合规审查建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtimeschange](https://clawhub.ai/user/howtimeschange)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace operators, and e-commerce creative teams use this skill to turn product images into platform-specific listing visuals and detail-page layouts with cross-border marketplace compliance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and optional local product reference images to a third-party image API.

Mitigation: Use only non-sensitive product images and provide a scoped 1XM_API_KEY explicitly for the session.

Risk: Untrusted prompts could influence which local reference image paths are used.

Mitigation: Do not allow untrusted prompts to choose reference file paths; select or review local file paths before execution.

Risk: The skill's compliance changes are automated suggestions and may not be sufficient for marketplace publication.

Mitigation: Have a human reviewer confirm compliance reports, platform rules, brand rights, image rights, and listing claims before publishing.

## Reference(s):

- [Platform image specifications](references/platform_specs.md)
- [Styles and routing](references/styles_and_routing.md)
- [Compliance engine](references/compliance_engine.md)
- [Cultural compliance](references/cultural_compliance.md)
- [Main image workflow](references/main_image_workflow.md)
- [Detail page workflow](references/detail_page_workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, generated image files, and YAML compliance reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a scoped 1XM_API_KEY and may use product reference images as inputs.]

## Skill Version(s):

2.6.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
