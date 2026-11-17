## Description:

Pick the right dLazy image model and get it right on the first call, with guidance for prompt caps, size formats, reference-image support, credit costs, editing, and post-processing chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to choose among dLazy image-generation and image-editing tools, build valid CLI commands, avoid incompatible parameters, and plan credit usage. It is intended for image generation, reference-image editing, post-processing, and troubleshooting, not for video, voice, or pure text tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the third-party @dlazy/cli package and dLazy API requires trust in the publisher and remote service.

Mitigation: Install only when the user trusts dLazy, confirm the package source before use, and run `dlazy <model> -h` or `--dry-run` before building or executing commands.

Risk: DLAZY_API_KEY and the saved config at ~/.dlazy/config.json can expose account access if mishandled.

Mitigation: Treat the API key as a secret, prefer per-command environment use when practical, and avoid printing or committing the key or config file.

Risk: Local reference images are uploaded to files.dlazy.com, which may expose private, regulated, or proprietary content to a third-party service.

Mitigation: Do not send sensitive images unless the user is comfortable with remote upload and storage by dLazy.

Risk: Model prices, flags, and image-generation outputs can change, and invalid prompts or size parameters can waste credits.

Mitigation: Use `dlazy <model> -h` and `--dry-run` to confirm current parameters and estimated credits before execution, especially for batch jobs.

## Reference(s):

- [dLazy homepage](https://dlazy.com)
- [dLazy API key dashboard](https://dlazy.com/dashboard/organization/api-key)
- [dLazy credits dashboard](https://dlazy.com/dashboard/organization/settings?tab=credits)
- [models.md](artifact/models.md)
- [choosing.md](artifact/choosing.md)
- [prompting.md](artifact/prompting.md)
- [editing.md](artifact/editing.md)
- [troubleshooting.md](artifact/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and CLI parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance can include dLazy CLI commands, dry-run recommendations, image URLs, and parameter checks; local image inputs may be uploaded to files.dlazy.com by the CLI.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
