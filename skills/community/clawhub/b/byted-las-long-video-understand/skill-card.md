## Description:

Extracts audio tracks from video files and splits long audio into timed segments using Volcengine LAS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media workflow operators use this skill to extract audio from supported video files and split long audio into fixed-duration segments with indexed output paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The initialization script can install or upgrade a remote SDK wheel without hash verification.

Mitigation: Review the script before use, run it only in a trusted workspace, and pin or verify SDK artifacts when operating in controlled environments.

Risk: The skill handles Volcengine API keys and may ask users to store credentials locally.

Mitigation: Use narrowly scoped temporary credentials and avoid storing long-lived secrets in env.sh, .env, chat transcripts, or version-controlled directories.

Risk: Processing local media can upload inputs to TOS and generate billable cloud work.

Mitigation: Confirm region, bucket access, input paths, duration, unit price, and estimated cost with the user before uploading or submitting processing jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-las-long-video-understand)
- [Publisher profile](https://clawhub.ai/user/volcengine-skills)
- [LAS audio extraction and split API reference](artifact/references/api.md)
- [Volcengine LAS pricing](https://www.volcengine.com/docs/6492/1544808)
- [Local pricing reference](artifact/references/prices.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, API calls, Files, Guidance]

**Output Format:** [Markdown with inline bash commands, JSON request examples, and result tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces TOS output paths for extracted audio segments and includes estimated billing information when presenting results.]

## Skill Version(s):

1.0.1 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
