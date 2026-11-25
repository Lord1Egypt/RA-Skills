## Description:

Generates Seedance 2.5 videos from prompts, with optional image, video, or audio references and first/last-frame controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use the skill to generate videos from text prompts, optionally guided by reference media or first and last frames.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and supplied reference media are sent to dLazy hosted services; local media paths are uploaded to its media storage.

Mitigation: Send only content you are authorized to share and review the service terms before use.

Risk: The security verdict is benign with medium confidence, but the scan was partial and did not verify the advertised video-generation capability.

Mitigation: Review the documented CLI sources and confirm the generation workflow before relying on it.

Risk: The CLI stores the dLazy API key in the user's local configuration.

Mitigation: Protect the configuration file and rotate or revoke the key if it may have been exposed.

## Reference(s):

- [dLazy CLI source repository](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)
- [dLazy API key dashboard](https://dlazy.com/dashboard/organization/api-key)

## Skill Output:

**Output Type(s):** [Generated video assets, JSON metadata and asset URLs, Shell commands, Configuration guidance]

**Output Format:** [Generated media files or hosted asset URLs in a JSON result; usage and setup guidance in Markdown with shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video duration, resolution, aspect ratio, audio generation, and optional image, video, audio, or first/last-frame references are configurable.]

## Skill Version(s):

1.2.40 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
