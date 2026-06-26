## Description: <br>
跨境电商图片生成工具 helps agents generate ecommerce main images, detail-page composites, and lifestyle scenes for Amazon, Shopee, TikTok Shop, Lazada, AliExpress, Temu, and SHEIN using platform specs, style routing, and compliance checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[howtimeschange](https://clawhub.ai/user/howtimeschange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, ecommerce operators, and design agents use this skill to turn product images and marketplace requirements into generated product imagery, prompts, output files, and compliance reports for cross-border listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product images, prompts, and brand context are sent to 1xm.ai for generation. <br>
Mitigation: Use the skill only with material approved for third-party processing, avoid sensitive product or brand data when policy requires it, and review generated assets before publication. <br>
Risk: ClawScan reports under-disclosed local credential fallback behavior. <br>
Mitigation: Set the 1XM_API_KEY environment variable deliberately and check or remove the fixed local .env fallback before use. <br>
Risk: Generated listing images can still contain marketplace, IP, cultural, or factual product issues. <br>
Mitigation: Manually verify final images and compliance reports against platform rules, product facts, brand authorization, and regional market requirements before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/howtimeschange/ecommerce-img-gen) <br>
- [Platform specifications](references/platform_specs.md) <br>
- [Compliance engine](references/compliance_engine.md) <br>
- [Cultural compliance](references/cultural_compliance.md) <br>
- [Main image workflow](references/main_image_workflow.md) <br>
- [Detail page workflow](references/detail_page_workflow.md) <br>
- [Styles and routing](references/styles_and_routing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, PNG image files, and YAML compliance reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-image and batch workflows, marketplace-specific sizing, model selection, and resolution tiers.] <br>

## Skill Version(s): <br>
2.6.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
