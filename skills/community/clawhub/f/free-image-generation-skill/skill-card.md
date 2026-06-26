## Description: <br>
Generates local image files from text prompts through a no-key Perchance workflow with retry/backoff handling, configurable shape, and structured success or error output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrilaikram](https://clawhub.ai/user/mrilaikram) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to generate local image files from text prompts through a no-key Perchance workflow, with retry handling and configurable output shape. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to an unofficial Perchance endpoint. <br>
Mitigation: Do not include secrets, confidential material, or sensitive personal data in prompts. <br>
Risk: The setup script installs a user-level Python dependency. <br>
Mitigation: Review the dependency before installation and use an isolated environment when appropriate. <br>
Risk: Generated files are written to a user-provided output path. <br>
Mitigation: Save outputs to a dedicated folder and choose filenames that will not overwrite important files. <br>


## Reference(s): <br>
- [Endpoint Notes](references/endpoints.md) <br>
- [Integration Notes](references/telegram-delivery.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/mrilaikram/free-image-generation-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output from the generator script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local image files and structured success or error output; supports prompt, output path, shape, negative prompt, guidance, retries, and timeout parameters.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
