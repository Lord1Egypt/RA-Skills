## Description: <br>
Generates an image from a user text prompt by sending the prompt to AutoGLM and returning the generated image URL for Markdown display. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyfujian](https://clawhub.ai/user/flyfujian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill when a user asks for image generation, text-to-image output, or AI drawing from a short prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts are sent to the external AutoGLM service. <br>
Mitigation: Avoid including secrets, private customer data, or proprietary text unless that data sharing is acceptable for the use case. <br>
Risk: The skill depends on a local token provider on port 53699. <br>
Mitigation: Install and run the skill only with a trusted local token provider and a trusted AutoGLM service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flyfujian/autoglm-generate-image) <br>
- [AutoGLM generate-image API endpoint](https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/generate-image) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [JSON response containing an image URL, typically presented as a Markdown image] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted local token provider on port 53699 and sends the prompt to the AutoGLM service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
