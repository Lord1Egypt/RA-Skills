## Description: <br>
Generate images using Azure OpenAI DALL-E. Supports batch generation, custom prompts, and outputs a gallery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhibavishi](https://clawhub.ai/user/abhibavishi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content creators use this skill to generate Azure OpenAI DALL-E images from prompts, tune size, quality, and style, and save local PNG outputs with a manifest and HTML gallery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Azure OpenAI credentials could be over-privileged or exposed through local configuration. <br>
Mitigation: Use a least-privileged Azure OpenAI key, protect local environment files, and confirm the endpoint and deployment belong to the intended account before running the skill. <br>
Risk: Batch image generation can create unintended Azure usage or cost. <br>
Mitigation: Keep image counts small unless larger batches are intentional and reviewed. <br>
Risk: The generated HTML gallery includes prompt-derived values, which may be unsafe when prompts contain untrusted HTML or script-like text. <br>
Mitigation: Avoid opening galleries generated from untrusted prompt text unless the gallery generation is updated to HTML-escape prompt values. <br>
Risk: Generated files may be written to an unexpected local location. <br>
Mitigation: Choose an output directory controlled by the user before generating images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abhibavishi/azure-image-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated PNG files, manifest.json, and index.html gallery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Azure OpenAI endpoint, API key, and DALL-E deployment configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
