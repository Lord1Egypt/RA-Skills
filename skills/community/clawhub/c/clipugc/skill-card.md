## Description:

ClipUGC CLI - create AI-generated UGC-style marketing videos for mobile apps from the terminal. Use when the user wants to create an AI character or AI influencer, generate character looks or reference images, create a UGC video or video clip from a look or photo, animate a photo with a driver video, put an app screen recording and a hook into a clip to make the finished UGC video, suggest hook texts for UGC videos, check ClipUGC credits or balance, manage ClipUGC characters/images/videos (list, show, rename, publish, delete, retry, download), or log in to ClipUGC with an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clipugc](https://clawhub.ai/user/clipugc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketers use ClipUGC commands to create AI character looks and short UGC-style marketing videos, combine clips with app recordings and hooks, and manage related assets and credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review calls out account deletion as a broad capability.

Mitigation: Confirm the account and the user's intent before deleting it; avoid the --yes option unless explicitly requested.

Risk: The security review notes an unpinned package install and was partial with medium confidence.

Mitigation: Review the package source and use a trusted pinned version before installing or running the CLI.

## Reference(s):

- [ClipUGC](https://clipugc.com)
- [ClipUGC API keys and account dashboard](https://clipugc.com/dashboard)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media-generation actions consume service credits; generated images and videos can be saved as files in the user's workspace.]

## Skill Version(s):

1.4.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
