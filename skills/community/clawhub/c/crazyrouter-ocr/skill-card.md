## Description: <br>
Image-to-text and OCR via Crazyrouter API using vision models (GPT-4o, Gemini, Claude). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xujfcn](https://clawhub.ai/user/xujfcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract text from images, describe visual content, and analyze screenshots through Crazyrouter-hosted vision models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images and prompts are uploaded to Crazyrouter or the endpoint configured by CRAZYROUTER_BASE_URL for processing. <br>
Mitigation: Use the skill only for images and prompts that are acceptable for external processing, and avoid confidential screenshots, IDs, secrets, or regulated documents unless that processing is approved. <br>
Risk: The skill requires a Crazyrouter API key for requests. <br>
Mitigation: Use a dedicated API key with appropriate limits and avoid exposing it in prompts, screenshots, logs, or shared output. <br>


## Reference(s): <br>
- [Crazyrouter](https://crazyrouter.com) <br>
- [Crazyrouter API base](https://crazyrouter.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown written to stdout or an optional output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CRAZYROUTER_API_KEY and sends the selected image and prompt to Crazyrouter or the CRAZYROUTER_BASE_URL endpoint.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
