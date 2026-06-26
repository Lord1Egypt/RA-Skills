## Description: <br>
This skill helps agents optimize 1688 product materials by routing Chinese user requests for product image generation, background cutouts, title optimization, and selling-point copy generation through CLI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and operators working with 1688 product listings use this skill to turn a product ID or image URL into optimized product visuals, white-background cutouts, titles, or selling-point copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a 1688 AK and may send product prompts, IDs, and image URLs to 1688 gateway services. <br>
Mitigation: Configure credentials through a secure OpenClaw or ClawHub secret mechanism, avoid pasting AKs into chat, and review what product data is sent before use. <br>
Risk: ISV token commands are broader than the normal material-optimization workflow. <br>
Mitigation: Use ISV token commands only when specifically needed and limit their use to trusted operators. <br>
Risk: Image-editing and watermark-removal flows can affect images the user may not own or be authorized to modify. <br>
Mitigation: Use image modification flows only for images the user owns or is authorized to change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/1688-distribution-material-newton) <br>
- [1688 AK portal](https://clawhub.1688.com) <br>
- [AK configuration](references/10_ak_configure.md) <br>
- [Product information query](references/20_product_info.md) <br>
- [Product image query](references/30_product_image.md) <br>
- [Image editing](references/40_image_edit.md) <br>
- [Background cutout](references/50_cutout_image.md) <br>
- [Title optimization](references/60_title_optimize.md) <br>
- [Selling point generation](references/70_selling_point.md) <br>
- [Image optimization workflow](references/80_image_optimize.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese Markdown guidance and JSON CLI results with a markdown field] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated image URLs, product title text, selling-point copy, and credential setup guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
