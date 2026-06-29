## Description: <br>
Guides agents through Chinese-language creative image generation and editing workflows, routing requests for logos, IP characters, packaging, brand assets, ecommerce visuals, educational diagrams, and media graphics to the appropriate image-generation or image-editing path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gu2003li](https://clawhub.ai/user/gu2003li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creative teams use this skill to plan, prompt, and route commercial creative image tasks across brand, ecommerce, educational, and media-design outputs. It helps an agent decide when to ask clarifying questions, when to preserve a core asset with image editing, and which reference rules to apply for each visual deliverable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation may route many image-generation and image-editing requests, especially Chinese-language creative design workflows. <br>
Mitigation: Review activation scope, routing preferences, and locale expectations before deployment when narrower behavior is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gu2003li/doubao-creative-design) <br>
- [Logo 系统](artifact/references/brand-logo-system.md) <br>
- [品牌 IP 角色系统](artifact/references/brand-ip-character-system.md) <br>
- [包装系统](artifact/references/brand-packaging-system.md) <br>
- [应用系统](artifact/references/brand-application-system.md) <br>
- [电商主图与详情页设计生成器](artifact/references/ecommerce-design.md) <br>
- [知识教育视觉 Prompt 改写](artifact/references/knowledge-education-visual.md) <br>
- [全平台营销配图与文案生成器](artifact/references/media-creative.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, API calls] <br>
**Output Format:** [Chinese-language text or Markdown with image-generation or image-editing prompts and ratio parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May route requests to image_gen or image_edit when those tools are available; otherwise it should explain the capability gap.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
