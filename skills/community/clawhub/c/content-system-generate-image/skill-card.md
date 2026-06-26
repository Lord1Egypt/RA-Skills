## Description: <br>
Generate article companion images for the content factory pipeline from article markdown drafts, with remote image generation and a local infographic fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abigale-cyber](https://clawhub.ai/user/abigale-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to turn article markdown drafts into a companion PNG image for publishing workflows. It can use a remote image backend when available and fall back to a local infographic card when external generation fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Article draft content and inherited local image credentials may be sent to a remote image API, and article frontmatter can override the provider, API base, and model. <br>
Mitigation: Use trusted drafts, remove unexpected image_provider, image_api_base, and image_model frontmatter, run with a limited IMAGE_API_KEY, and review the configured endpoint before execution. <br>
Risk: The image workflow depends on md2wechat and external network or API availability, so remote generation may fail or return unusable image URLs. <br>
Mitigation: Verify the md2wechat dependency separately and review the generated PNG before publishing; use the local infographic fallback when the external backend is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abigale-cyber/content-system-generate-image) <br>
- [Default image API base](https://new.suxi.ai/v1) <br>
- [Banana image login](https://job.suxi.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, API Calls, Configuration] <br>
**Output Format:** [PNG image file with runtime image-generation metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes content-production/ready/<slug>-img-1.png; per-article frontmatter may override the image provider, API base, and model.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
