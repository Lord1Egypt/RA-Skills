## Description:

Generate, edit, or compose images via the EchoFlow API using Nano Banana Pro (Gemini 3 Pro Image), with support for up to 14 input images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjx15296694073](https://clawhub.ai/user/zjx15296694073)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate new images, edit an existing image, or combine multiple images through a third-party EchoFlow API endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, input images, and API credentials may be sent to an external EchoFlow endpoint.

Mitigation: Use only data approved for EchoFlow, and use a dedicated EchoFlow API key with limited scope.

Risk: The script can fall back to ambient OPENAI_API_KEY or GEMINI_API_KEY values.

Mitigation: Set ECHOFLOW_API_KEY explicitly for this skill and avoid exposing unrelated provider keys in the execution environment.

Risk: The --api-base option can redirect requests to a caller-chosen endpoint.

Mitigation: Use the default endpoint or another endpoint only after verifying that it is trusted for the prompts, images, and credentials being sent.

## Reference(s):

- [EchoFlow API Reference](references/echoflow_api.md)
- [EchoFlow API](https://api.echoflow.cn/)
- [ClawHub Skill Page](https://clawhub.ai/zjx15296694073/skills/echoflow-banana-gen)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Configuration]

**Output Format:** [PNG image files with plain-text saved-path and MEDIA lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an API key and can use 1K, 2K, or 4K output resolution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
