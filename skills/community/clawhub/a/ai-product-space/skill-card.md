## Description: <br>
Upload a single product photo and generate ecommerce assets including main images, scene shots, feature posters, marketing copy, and 8-second showcase videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[corinbtc](https://clawhub.ai/user/corinbtc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketers, and ecommerce teams use this skill to create product image sets, marketing copy, and short product videos from a supplied product photo. Developers can also use it inside OpenClaw workflows that call AI Product Space tools for upload, generation, status, and asset listing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad OAuth authorization for an AI Product Space account. <br>
Mitigation: Install only for trusted accounts and review the requested authorization before connecting. <br>
Risk: The skill can upload local files or URL contents to a remote service. <br>
Mitigation: Provide only explicit product-image paths or public image URLs intended for upload, and avoid confidential or regulated product assets unless permitted by provider terms. <br>
Risk: Generation workflows may consume account credits and may reuse an existing workspace. <br>
Mitigation: Confirm the workspace and generation request before starting credit-consuming image, copy, or video generation. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/corinbtc/ai-product-space) <br>
- [Publisher profile](https://clawhub.ai/user/corinbtc) <br>
- [AI Product Space homepage](https://renshevy.com) <br>
- [Project repository](https://github.com/renshevy/ai-product-space) <br>
- [Support issues](https://github.com/renshevy/ai-product-space/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown and text summaries with links or inline generated assets returned by the remote service] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product image URLs, grouped generated asset summaries, marketing copy, workspace status, or video links depending on the selected tool.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence, package.json, claw.json, clawhub.json, CHANGELOG released 2026-03-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
