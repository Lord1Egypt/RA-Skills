## Description: <br>
Possibly the cheapest AI image generation (~$0.0036/image). Text-to-image via the EvoLink API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvoLinkAI](https://clawhub.ai/user/EvoLinkAI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users use this skill to generate images from text prompts through the EvoLink API. It provides reference implementations for Python, PowerShell, and curl workflows that submit a generation task, poll for completion, download the result, and emit a local media path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts are sent to EvoLink. <br>
Mitigation: Avoid including secrets or sensitive personal or business information in prompts. <br>
Risk: Trigger phrases can consume EvoLink API credits and create local image files. <br>
Mitigation: Use a controlled EVOLINK_API_KEY, monitor usage, and delete generated files that should not persist. <br>
Risk: Shell-based output filenames can be unsafe if user-controlled names are passed through unchanged. <br>
Mitigation: Use the artifact's filename sanitization pattern and restrict saved image extensions to webp, png, jpg, or jpeg. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EvoLinkAI/cheapest-image-generation) <br>
- [EvoLink homepage](https://evolink.ai) <br>
- [Python reference](references/python.md) <br>
- [PowerShell reference](references/powershell.md) <br>
- [curl + bash reference](references/curl_heredoc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with code examples, shell commands, and MEDIA:<absolute_path> output markers for locally saved image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVOLINK_API_KEY; generated images are saved locally and EvoLink API credits may be consumed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
