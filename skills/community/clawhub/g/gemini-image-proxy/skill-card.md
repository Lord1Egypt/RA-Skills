## Description: <br>
Generate and edit images with Gemini API using the OpenAI Python SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YspCoder](https://clawhub.ai/user/YspCoder) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to generate new images or edit existing images through an OpenAI-compatible Gemini image endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and optional source images are sent to the configured image API endpoint. <br>
Mitigation: Do not send confidential prompts, regulated data, or private images unless the endpoint's logging, retention, and data-handling policies are acceptable. <br>
Risk: The skill depends on the configured GOOGLE_PROXY_BASE_URL endpoint and the OpenAI Python package source. <br>
Mitigation: Install only from a trusted package source, verify the endpoint before use, and use a limited API key where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YspCoder/gemini-image-proxy) <br>
- [Publisher profile](https://clawhub.ai/user/YspCoder) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOOGLE_PROXY_API_KEY and GOOGLE_PROXY_BASE_URL; saves returned images to a local output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
