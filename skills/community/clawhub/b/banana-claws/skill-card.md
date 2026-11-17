## Description:

Generates images through OpenRouter text-to-image models with local scripts for single-image requests, batched variants, queued processing, and structured success or failure records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ironystock](https://clawhub.ai/user/ironystock)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Banana Claws to turn image-generation requests into OpenRouter API calls, queue multi-image batches, and return generated files with consolidated status records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and baseline images are transmitted to OpenRouter, and generated provider responses may be retained in local queue files.

Mitigation: Do not submit sensitive prompts or private images without explicit approval, and periodically clear queue and provider-response files when retention is not needed.

Risk: The server security review flagged the background queue because it can write outside intended paths and terminate local processes based on weak queue metadata.

Mitigation: Install and run the skill only in a dedicated workspace under an unprivileged account, avoid shared or attacker-writable queue directories, and keep request IDs to simple letters, numbers, and dashes.

Risk: Local baseline image uploads can disclose local file contents to the external provider.

Mitigation: Use the deny-by-default local upload behavior and pass the upload confirmation option only after the user approves external transmission.

## Reference(s):

- [Banana Claws on ClawHub](https://clawhub.ai/ironystock/skills/banana-claws)
- [Skill homepage](https://github.com/ironystock/banana-claws)
- [OpenRouter](https://openrouter.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON status records, and generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY, python3, and requests; queue workflows may write result and provider-response JSON files.]

## Skill Version(s):

0.1.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
