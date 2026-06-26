## Description: <br>
Use when users need DesignKit image editing, ecommerce product-image generation, or A+ detail-page planning and rendering, with runtime guidance defaulting to Simplified Chinese. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meituskills](https://clawhub.ai/user/meituskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to remove image backgrounds, restore low-quality images, generate ecommerce listing assets, and plan or render A+ detail-page image sets from user-provided product images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a DesignKit/OpenClaw API key and sends selected product images to a remote processing service. <br>
Mitigation: Use only images explicitly provided for the requested task, avoid sensitive images, keep credentials private, and tell users when local files will be uploaded. <br>
Risk: Request logging may expose operational details if enabled during debugging. <br>
Mitigation: Keep request logging disabled unless debugging and rely on the bundled redaction behavior for credentials and signed upload fields. <br>
Risk: Generated ecommerce and A+ detail images are downloaded to a local output directory. <br>
Mitigation: Review custom output directories and API-base overrides before use, and avoid saving outputs inside the skill repository. <br>


## Reference(s): <br>
- [DesignKit OpenClaw](https://www.designkit.cn/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/meituskills/designkit-skills) <br>
- [Publisher Profile](https://clawhub.ai/user/meituskills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files, markdown] <br>
**Output Format:** [Markdown user guidance with generated image URLs and local saved image paths when workflows complete] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DESIGNKIT_OPENCLAW_AK; accepts user-provided image URLs or local image paths and may save generated outputs to a configured local output directory.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
