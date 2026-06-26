## Description: <br>
AgentImgHost REST API for uploading, listing, and deleting images, returning direct public CDN URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JacobMaldonado](https://clawhub.ai/user/JacobMaldonado) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, bots, and scripts use this skill to upload images to AgentImgHost, receive public CDN URLs, manage hosted image IDs, and delete images when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded images are returned as direct public CDN URLs and may expose sensitive visual content. <br>
Mitigation: Upload only selected images intended for public sharing and review files before upload. <br>
Risk: The AgentImgHost API key can authorize image-hosting operations if exposed. <br>
Mitigation: Keep AGENTIMGHOST_API_KEY private and avoid embedding the bearer token in shared logs, prompts, or public artifacts. <br>
Risk: Deleting the wrong image ID or relying on circular overwrite can remove hosted images unexpectedly. <br>
Mitigation: Confirm the exact image ID before deletion and disable circular overwrite when preserving older hosted images matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/JacobMaldonado/agent-image-hosting) <br>
- [AgentImgHost Homepage](https://agent-img.com) <br>
- [AgentImgHost Account Dashboard](https://agent-img.com/account) <br>
- [AgentImgHost Settings](https://agent-img.com/config) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with REST API endpoints, curl commands, JSON response examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTIMGHOST_API_KEY; uploaded images return public CDN URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
