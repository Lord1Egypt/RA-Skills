## Description: <br>
Generates images from text prompts through NVIDIA's image generation API and saves the JSON response with base64 image data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[savior1987](https://clawhub.ai/user/savior1987) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn natural-language prompts into generated images through NVIDIA's API, with configurable image width and height. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts are sent to NVIDIA's API and may contain sensitive or confidential content. <br>
Mitigation: Avoid including secrets, private data, or confidential business information in prompts. <br>
Risk: The skill requires an NVIDIA_API_KEY loaded from the user's environment. <br>
Mitigation: Provide the key only in an environment you trust and avoid sharing logs or files that could expose credentials. <br>
Risk: Generated response JSON is saved under /tmp, which may persist temporarily on the local system. <br>
Mitigation: Review and remove saved response files when generated content should not remain on disk. <br>
Risk: The documented model naming is inconsistent between the skill description and script behavior. <br>
Mitigation: Confirm the intended NVIDIA model with the publisher before relying on exact model identity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/savior1987/cs-free-image-generator-nv) <br>
- [NVIDIA Flux.2 Klein 4B image generation API endpoint](https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.2-klein-4b) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, API Calls] <br>
**Output Format:** [JSON response containing base64-encoded image data, printed to stdout and saved under /tmp/cs-free-image-generator/nv/.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NVIDIA_API_KEY. Prompt, width, and height are required; width and height must be between 1 and 4096.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
