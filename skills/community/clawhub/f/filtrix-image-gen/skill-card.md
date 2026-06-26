## Description: <br>
Filtrix Image Gen helps agents generate and edit images through Filtrix Remote MCP using gpt-image-1, nano-banana, and nano-banana-2 modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lumenclaw-cloud](https://clawhub.ai/user/lumenclaw-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create new images from text prompts, refine existing images, and check Filtrix account credits through a remote MCP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and edited images are sent to Filtrix for remote processing. <br>
Mitigation: Use the skill only when remote Filtrix processing is acceptable, and avoid submitting sensitive or regulated prompts or images. <br>
Risk: Generation and edit calls can consume Filtrix account credits. <br>
Mitigation: Use idempotency keys for retries, check account credits when needed, and monitor credit usage after calls. <br>
Risk: The skill requires an API key for the remote MCP service. <br>
Mitigation: Use a Filtrix-specific API key and rotate or revoke it if it is exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lumenclaw-cloud/filtrix-image-gen) <br>
- [MCP Tools Reference](references/mcp-tools.md) <br>
- [gpt-image-1 Mode](references/gpt-image-1.md) <br>
- [nano-banana Mode](references/nano-banana.md) <br>
- [nano-banana-2 Mode](references/nano-banana-2.md) <br>
- [Prompt Guide](references/prompts.md) <br>
- [Filtrix prompt library](https://www.filtrix.ai/prompts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and local image file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated and edited images are downloaded from Filtrix and written to a user-provided path or a timestamped PNG file under /tmp.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
