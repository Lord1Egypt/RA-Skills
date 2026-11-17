## Description:

Uploads and manages Aliyun Drive files using refresh-token authentication, including large-file uploads, folder creation, file search, share links, deletion, download links, and user information lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjcly](https://clawhub.ai/user/wjcly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to upload, list, search, share, delete, and retrieve download links for Aliyun Drive files through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe command execution in the Aliyun Drive action path.

Mitigation: Fix the execution path to use argument-vector subprocess execution before installation.

Risk: Aliyun refresh token exposure through command-line handling or shared environment files.

Mitigation: Do not pass the token on the command line; treat it like a password and avoid committing or sharing the .env file.

Risk: Destructive delete actions can modify cloud storage.

Mitigation: Require explicit user confirmation before running delete actions.

Risk: Unpinned dependencies can change runtime behavior.

Mitigation: Pin the required dependencies before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wjcly/skills/claw-aliyun-drive-uploader)
- [Aliyun Drive token endpoint](https://auth.aliyundrive.com/v2/account/token)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Files]

**Output Format:** [JSON action result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Aliyun Drive refresh token and can modify cloud files, including creating folders, sharing files, and deleting files.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
