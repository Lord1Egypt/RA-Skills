## Description:

Provides access to HeyGen Lipsync Speed for fast lip-sync generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use the skill to submit video and audio for rapid lip synchronization, with optional captions, speech enhancement, and duration adjustment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan verdict is benign with medium confidence; Skillspector reported a mismatch between the advertised lip-sync purpose and visible authentication-focused content, and its inspection was partial.

Mitigation: Confirm the installed CLI and lip-sync command match the intended use before relying on the skill.

Risk: Video and audio supplied as local paths are uploaded to dLazy media storage, and authentication stores an API key in the user's CLI configuration.

Mitigation: Use media you are authorized to upload, protect the API key, and rotate or revoke it if exposed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-heygen-lipsync-speed)
- [dLazy](https://dlazy.com)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Generated media, JSON]

**Output Format:** [JSON containing generated media URLs or asynchronous task status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media can be downloaded to a local path; asynchronous requests may first return a task ID.]

## Skill Version(s):

1.3.44 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
