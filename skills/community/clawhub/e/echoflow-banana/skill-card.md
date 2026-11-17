## Description:

Generates, edits, and composes images through the EchoFlow API using Nano Banana Pro (Gemini 3 Pro Image).

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjx15296694073](https://clawhub.ai/user/zjx15296694073)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate images, edit a provided image, or compose up to 14 images through EchoFlow from agent-provided prompts and file paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected input images are sent to EchoFlow for processing.

Mitigation: Use the skill only when sending that content to EchoFlow is acceptable.

Risk: Passing an API key on the command line can expose it through shell history or process listings.

Mitigation: Set ECHOFLOW_API_KEY in the environment instead of using --api-key.

Risk: Changing --api-base can send the EchoFlow API key to a different endpoint.

Mitigation: Keep the default endpoint unless the replacement endpoint is fully trusted.

Risk: The documented curl|sh installer path can execute a downloaded script.

Mitigation: Install uv through a trusted package manager where possible, or inspect installer scripts before running them.

## Reference(s):

- [EchoFlow API Reference](references/echoflow_api.md)
- [EchoFlow API](https://api.echoflow.cn/)
- [ClawHub Skill Page](https://clawhub.ai/zjx15296694073/skills/echoflow-banana)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and ECHOFLOW_API_KEY; can use optional input images, model, resolution, and API base arguments.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
