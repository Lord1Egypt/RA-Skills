## Description:

Uses fal.ai sync-lipsync v3 to align a speaker’s lip movements in an input video with supplied audio, for dubbing, localization, and virtual presenters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and developers can align a speaker’s mouth movements in a video with supplied audio for dubbing, localization, or virtual presenters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local video and audio files supplied to the skill are uploaded to dLazy media storage, and request details are sent to its hosted API.

Mitigation: Check your organization’s privacy requirements and use only media approved for external processing.

Risk: The security scan had medium confidence and left some CLI behavior and referenced details unverified.

Mitigation: Review the CLI’s authentication and command behavior before installing it or providing credentials.

## Reference(s):

- [CLI project page (listed in skill metadata)](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Video, JSON]

**Output Format:** [Generated video asset with a JSON result containing its URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The input video and audio are aligned; the result can be saved locally.]

## Skill Version(s):

1.3.41 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
