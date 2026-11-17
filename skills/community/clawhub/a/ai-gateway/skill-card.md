## Description:

Access 340+ AI models via the Agnic AI Gateway for chat, image generation, model listing, delegation to another LLM, and second opinions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route agent requests through Agnic for model discovery, text chat, and image generation across supported AI providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes an unpinned network-fetched Agnic CLI for authentication, prompts, and paid model calls.

Mitigation: Use a pinned and reviewed Agnic CLI version or a controlled local install before relying on the skill in sensitive or production workflows.

Risk: Prompts and generated content may be sent to an external AI gateway and may incur billing through the user's wallet balance.

Mitigation: Use the skill only with approved data, confirm the selected model and account state, and avoid exposing broad environment secrets or sensitive prompts.

Risk: Command construction includes user-provided model IDs, prompts, output paths, and numeric options.

Mitigation: Validate model, prompt, temperature, aspect-ratio, and output path values according to the bundled models/options reference before execution.

## Reference(s):

- [AI Gateway Models & Options Reference](reference/models-and-options.md)
- [Agnic application](https://app.agnic.ai)
- [ClawHub skill page](https://clawhub.ai/agnicpay-prog/skills/ai-gateway)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown with shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce text responses, model listings, generated image files, and authentication or billing guidance depending on the selected Agnic command.]

## Skill Version(s):

2.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
