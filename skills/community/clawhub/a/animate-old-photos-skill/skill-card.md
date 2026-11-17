## Description:

Animate old photos into AI-generated videos using the Animate Old Photos API by uploading a photo, generating a 5-second animation video, and downloading the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shurshanx](https://clawhub.ai/user/shurshanx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent run a paid photo-to-video workflow: collect an API key and local JPEG or PNG image, submit an animation task, poll for completion, and download the MP4 result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected photos are uploaded to Animate Old Photos and its storage provider.

Mitigation: Use only photos the user is comfortable sending to the service, and review the service's privacy and retention behavior before processing sensitive images.

Risk: The workflow consumes paid credits and requires an API key.

Mitigation: Confirm the 3-credit cost before submitting a task and provide the key through AOP_API_KEY or another protected secret mechanism.

Risk: The skill relies on shell execution and writes to a user-selected MP4 output path.

Mitigation: Review commands before execution and choose an output path that will not overwrite important files.

## Reference(s):

- [Animate Old Photos API Reference](artifact/references/animate-old-photos-api.md)
- [Animate Old Photos Website](https://animateoldphotos.org/)
- [Animate Old Photos ClawHub Skill](https://clawhub.ai/shurshanx/skills/animate-old-photos-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Files]

**Output Format:** [Markdown guidance with bash command snippets and MP4 file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces progress messages, error guidance, and a local MP4 output path after successful completion.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
