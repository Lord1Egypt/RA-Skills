## Description: <br>
Generate AI images from prompts using CivitAI's JavaScript SDK with configurable models, samplers, seeds, steps, LoRA networks, and output paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shinnpuru](https://clawhub.ai/user/shinnpuru) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to request CivitAI image generations from an agent, tune generation settings, and save the resulting image locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a CivitAI API token and sends prompts and generation settings to CivitAI. <br>
Mitigation: Use a dedicated CivitAI token, store it in the CIVITAI_API_TOKEN environment variable, and avoid submitting sensitive prompts or settings. <br>
Risk: Generated images are written to a user-selected local output path. <br>
Mitigation: Use a dedicated output directory or explicit image filename, and avoid pointing --output at important existing files. <br>
Risk: Generation may depend on the civitai npm package and may consume CivitAI credits or subscription resources. <br>
Mitigation: Install only if you trust the civitai package and confirm account costs or permissions before running large generations. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and local image file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, the civitai npm package, and CIVITAI_API_TOKEN; generated images are saved to the configured output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
