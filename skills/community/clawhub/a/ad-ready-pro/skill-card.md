## Description: <br>
Ad-Ready Pro generates professional advertising images from product URLs using a brand-aware ComfyDeploy pipeline with optional brand profiles, funnel-stage targeting, talent references, and multi-format output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PauldeLavallaz](https://clawhub.ai/user/PauldeLavallaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External marketers, creators, and developers use this skill to generate product advertising images from product URLs, brand assets, optional reference imagery, and campaign funnel objectives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product URLs, product images, logos, reference ads, and optional model or talent images are sent to ComfyDeploy. <br>
Mitigation: Use only assets approved for third-party processing, avoid private or unreleased campaign materials unless that processing is acceptable, and prefer a dedicated or scoped ComfyDeploy API key. <br>
Risk: Auto-fetch mode downloads image assets and stores temporary files during preparation. <br>
Mitigation: Review fetched assets before generation and clean up /tmp/ad-ready after auto-fetch runs. <br>
Risk: Product scraping can be fragile or blocked by some websites, which can lead to missing or incorrect product context. <br>
Mitigation: Provide a product image explicitly when possible and review the generated ad before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PauldeLavallaz/ad-ready-pro) <br>
- [ComfyDeploy deployment queue API](https://api.comfydeploy.com/api/run/deployment/queue) <br>
- [Ad-Ready documentation](https://www.patreon.com/posts/from-product-to-149933468) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands; generated ad output is an image file such as PNG.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ComfyDeploy API key and may download, upload, and temporarily store product, logo, reference, or model images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
