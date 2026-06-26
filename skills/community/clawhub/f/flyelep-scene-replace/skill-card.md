## Description: <br>
Scene Replace guides an agent to call the Flyelep AI Tool API to replace an image background using a public source image URL, scene reference image URL, and prompt text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyelepai](https://clawhub.ai/user/flyelepai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to replace the background scene of an image, such as changing a product display environment while preserving the subject. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected image URLs, reference image URLs, prompt text, and a Flyelep API key to Flyelep. <br>
Mitigation: Use it only with images and prompts suitable for that provider, and keep the secretKey private. <br>
Risk: The API requires publicly reachable image URLs, so private or expiring links may fail or expose content to a third-party service. <br>
Mitigation: Provide only intended public image links and avoid sensitive images unless the provider's handling is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flyelepai/flyelep-scene-replace) <br>
- [Flyelep scene replacement API endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/sceneReplace) <br>
- [Flyelep controlboard](https://www.flyelep.cn/controlboard) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the generated image URL from the Flyelep API response.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
