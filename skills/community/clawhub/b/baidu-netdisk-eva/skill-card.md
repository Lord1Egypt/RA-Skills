## Description:

Manages Baidu Netdisk files by listing directories, searching files, and creating folders using user-configured Baidu AppID and OAuth access token credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[382108113](https://clawhub.ai/user/382108113)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Baidu Netdisk accounts from an agent workflow, including listing files, searching by keyword, and creating remote directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a user-supplied OAuth token to access a Baidu Netdisk account.

Mitigation: Install and configure it only for accounts where agent access is intended, and keep BAIDU_NETDISK_TOKEN scoped and stored as an environment variable.

Risk: List and search results can reveal private file and directory metadata.

Mitigation: Treat command output as private account metadata and avoid sharing it in public logs or transcripts.

Risk: The mkdir command creates remote directories in the connected account.

Mitigation: Confirm directory paths before execution and review remote account changes after use.

## Reference(s):

- [Baidu Netdisk Open Platform documentation](https://pan.baidu.com/union/doc/)

## Skill Output:

**Output Type(s):** [text, configuration]

**Output Format:** [Plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include private file names, directory names, sizes, and remote directory creation status from the user's Baidu Netdisk account.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact/skill.json, artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
