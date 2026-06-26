## Description: <br>
Use when users need ecommerce image help such as background removal, transparent or white background output, blurry photo restoration, or listing image generation from a product photo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[designkit](https://clawhub.ai/user/designkit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Ecommerce sellers, marketplace operators, creative operations teams, merchandising teams, and agencies use this skill to remove product backgrounds, restore blurry product photos, and generate marketplace-ready listing image sets from provided product images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided image URLs, local image files, and ecommerce listing details are sent to Designkit/OpenClaw for remote processing. <br>
Mitigation: Use the skill only when remote processing is acceptable, and avoid sensitive personal images unless that transfer is appropriate. <br>
Risk: The skill requires a Designkit/OpenClaw API key for authenticated processing. <br>
Mitigation: Provide the API key only through the configured DESIGNKIT_OPENCLAW_AK environment variable and avoid exposing it in normal user-facing replies or logs. <br>


## Reference(s): <br>
- [Designkit OpenClaw](https://www.designkit.com/openClaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/designkit/ecommerce-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with result image links, progress updates, and concise user guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns remote result URLs and may render previews in clients that support image display.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
