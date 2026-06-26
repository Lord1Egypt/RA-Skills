## Description: <br>
Use a text model such as gpt-5.4 with the image_generation tool over an OpenAI-compatible /v1/responses endpoint, matching the CPA blog example. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shiftshen](https://clawhub.ai/user/shiftshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate image files through an OpenAI-compatible Responses API by calling a text model with the image_generation tool. It is useful when a gateway expects the CPA blog request pattern instead of direct gpt-image-2 model calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and API credentials are sent to the configured image-generation endpoint. <br>
Mitigation: Use only trusted endpoints, prefer explicit IMAGE_GEN_BASE_URL and IMAGE_GEN_KEY values, and use scoped or disposable API keys where possible. <br>
Risk: Generated images are written to the requested local output path. <br>
Mitigation: Choose an output path where directory creation and file overwriting are acceptable. <br>
Risk: Prompt content may be sensitive when sent to the configured provider. <br>
Mitigation: Avoid including secrets, personal data, or confidential material in image prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shiftshen/cpa-gpt-image-2) <br>
- [Publisher profile](https://clawhub.ai/user/shiftshen) <br>


## Skill Output: <br>
**Output Type(s):** [Files, API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [PNG, JPEG, or WebP image files plus Markdown guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads endpoint, model, and credential settings from environment variables; writes the first base64 image returned by the configured Responses API endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
