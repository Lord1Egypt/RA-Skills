## Description:

Downloads public Douyin videos without watermarks, saves them locally, uploads them to cloud storage, and returns a share link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexliu9921](https://clawhub.ai/user/alexliu9921)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to parse a Douyin video link, download the corresponding watermark-free public video, upload it to cloud storage, and return a temporary sharing link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested Douyin videos are downloaded to /tmp and uploaded to cloud storage for about 30 days.

Mitigation: Use the skill only for public or non-sensitive videos and confirm the user is comfortable with temporary cloud storage.

Risk: Unvalidated or unexpectedly large video downloads can create privacy, storage, or reliability issues.

Mitigation: Maintainers should consider explicit confirmation, URL allowlisting, and file-size limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexliu9921/skills/alexliutkdownload)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Markdown-style status text with shell command execution and a downloaded MP4 file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads requested videos to /tmp and returns a cloud-storage share link when upload succeeds.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
