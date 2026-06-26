## Description: <br>
Best quality AI image generation (~$0.12-0.20/image). Text-to-image, image-to-image, and image editing via the EvoLink API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvoLinkAI](https://clawhub.ai/user/EvoLinkAI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to generate, edit, and save AI images through the EvoLink API using text prompts and optional reference image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference image URLs are sent to EvoLink for generation. <br>
Mitigation: Avoid submitting secrets, private content, or private/internal URLs unless the user has approved sharing that data with EvoLink. <br>
Risk: Trigger phrases can submit a paid generation request immediately and may spend API credits. <br>
Mitigation: Confirm the prompt, quality setting, and expected cost before generation when cost or intent is unclear; use a dedicated API key with spending limits where available. <br>
Risk: The skill depends on an EvoLink API key and external network access. <br>
Mitigation: Store EVOLINK_API_KEY securely, do not echo it in logs, and handle API or polling failures without exposing credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EvoLinkAI/best-image-generation) <br>
- [EvoLink homepage](https://evolink.ai) <br>
- [Python reference](references/python.md) <br>
- [PowerShell reference](references/powershell.md) <br>
- [curl and bash reference](references/curl_heredoc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, API request examples, and MEDIA:<absolute_path> output for generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVOLINK_API_KEY; supports text-to-image, image-to-image, image editing, selectable size and quality, and local image download.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
