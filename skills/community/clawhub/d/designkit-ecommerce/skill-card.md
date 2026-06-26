## Description: <br>
Use when users need AI design assets for ecommerce images: background removal, transparent or white background output, blurry photo restoration, or listing image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaorenaishu](https://clawhub.ai/user/xiaorenaishu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and ecommerce teams use this skill to turn product photos into marketplace-ready assets, including cutouts, enhanced images, and listing image sets. Agents route the request, collect required inputs, run the Designkit/OpenClaw workflow, and return result images or actionable error guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected product images, image URLs, and listing details are sent to remote Designkit/OpenClaw/Meitu services. <br>
Mitigation: Use only non-sensitive assets, confirm each upload or download with the user, and use a dedicated revocable API key. <br>
Risk: The security evidence flags broad shell/API controls and unsafe input handling for review. <br>
Mitigation: Review command inputs and HTTPS endpoints before use, and avoid overriding endpoint settings unless they have been approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiaorenaishu/designkit-ecommerce) <br>
- [Designkit OpenClaw](https://www.designkit.com/openClaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with image links, JSON command results, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DESIGNKIT_OPENCLAW_AK and may upload selected local images or image URLs to remote Designkit/OpenClaw/Meitu services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
