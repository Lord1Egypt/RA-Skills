## Description:

Guides agents through Ark CLI image and video generation, including resource and parameter checks, image generation, and asynchronous video task handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create images or videos with Ark through arkcli. It guides resource and model capability checks, request planning, and result handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review had partial coverage and flagged account or quota lookups and task deletion as possible purpose mismatches; task deletion bypasses confirmation.

Mitigation: Before installing, confirm those operations fit your needs; verify the task ID and intent before deleting a task.

## Reference(s):

- [Arkcli Gen workflow and options](references/arkcli-gen.md)
- [Intent and output validation](references/intent-and-validation.md)
- [Generation task management](references/gen-meta.md)
- [Image streaming](references/image-stream.md)
- [ClawHub skill release](https://clawhub.ai/jasonstarlight/skills/arkcli-gen)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Files]

**Output Format:** [Markdown guidance, shell commands, JSON task results, and generated image or video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video tasks may complete asynchronously; generated media depends on the selected Ark model and its supported parameters.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
