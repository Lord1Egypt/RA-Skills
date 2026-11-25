## Description:

Turn scripts or scene breakdowns into a storyboarded, shot-by-shot video by breaking down scenes, generating shots, assembling, and validating the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to turn a script or scene breakdown into a multi-shot video, including storyboard shots, consistent character references, audio, subtitles, and assembled output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial, and the reported CLI login and organization project-list behavior may not clearly match the video's stated purpose.

Mitigation: Review the skill and CLI behavior, and confirm the requested login and project access fit your expectations before installing.

Risk: Files attached to a request are uploaded to the service's media storage.

Mitigation: Attach only files you are comfortable sharing with the service.

Risk: The CLI stores an organization API key in local configuration.

Mitigation: Protect the local configuration and rotate or revoke the key if it may have been exposed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-script-to-video)
- [dLazy homepage](https://dlazy.com)
- [dLazy CLI repository (listed in skill metadata)](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Video files, Text, Shell commands, Guidance]

**Output Format:** [Generated video assets and text responses through a project-scoped CLI conversation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the user's prompt, project context, and service response.]

## Skill Version(s):

1.0.41 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
