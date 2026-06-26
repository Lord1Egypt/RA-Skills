## Description: <br>
Extends one or more image canvases through the Flyelep AI Tool API and returns generated image URLs for requested aspect ratios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyelepai](https://clawhub.ai/user/flyelepai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to prepare HTTP API calls that expand image edges, complete canvases, or adapt one or more image URLs to supported aspect ratios such as 16:9, 1:1, and 9:16. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided image URLs and the Flyelep API key to Flyelep. <br>
Mitigation: Use a dedicated or revocable API key, avoid sensitive or private image URLs unless Flyelep's handling is acceptable, and provide the key only at runtime. <br>
Risk: Ambiguous or unsupported target ratios can produce failed requests or results that do not match the user's intent. <br>
Mitigation: Use only the documented ratio values and ask the user to confirm the target ratio when context is insufficient. <br>


## Reference(s): <br>
- [Flyelep Intelligent Extension API endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/intelligentExtension) <br>
- [Flyelep Open Platform control board](https://www.flyelep.cn/controlboard) <br>
- [ClawHub skill page](https://clawhub.ai/flyelepai/flyelep-intelligent-extension) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request bodies and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns result image URLs in the same order as the input image URL list.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
