## Description:

Flux Kontext Pro - Pro Pack on RunComfy helps agents prepare and run precise single-image edit requests against Flux 1 Kontext Pro through the RunComfy CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to route explicit Flux Kontext image-edit requests, supply a single public source image and prompt, and receive guidance for invoking RunComfy with suitable parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and image URLs to RunComfy as an external image-editing service.

Mitigation: Use it only when that external processing is acceptable, and confirm ambiguous requests before sending image URLs or prompts.

Risk: RunComfy authentication can rely on stored local credentials or an environment token.

Mitigation: Use a revocable RunComfy token, prefer an isolated or pinned CLI install, and avoid exposing unrelated secrets to the CLI process.

Risk: The broad trigger word can route unintended image-editing requests to this skill.

Mitigation: Confirm user intent before invoking the RunComfy workflow when the request is ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/flux-kontext)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=flux-kontext)
- [Flux 1 Kontext Pro model page](https://www.runcomfy.com/models/blackforestlabs/flux-1-kontext-pro/image-to-image?utm_source=clawhub&utm_medium=skill&utm_campaign=flux-kontext)
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=flux-kontext)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and JSON input snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local RunComfy CLI configuration or RUNCOMFY_TOKEN and a public HTTPS source image URL.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
