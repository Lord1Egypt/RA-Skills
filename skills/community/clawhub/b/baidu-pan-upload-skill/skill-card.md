## Description:

Uploads local files to Baidu Netdisk with chunked uploads, resumable transfer state, progress monitoring, and remote directory creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugpoor](https://clawhub.ai/user/ugpoor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to upload selected local files to Baidu Netdisk directories, including large files that need chunking, retry handling, and resumable progress after interruption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Baidu Netdisk access tokens and may expose the token in the curl command line while uploads run.

Mitigation: Run it only in trusted local environments and avoid shared machines or process listings where other users can inspect command-line arguments.

Risk: The resumable upload state file is written beside the selected source file.

Mitigation: Avoid running uploads from shared or sensitive directories, and remove stale .upload_state.json files if an upload is abandoned.

Risk: The skill uploads selected local files to Baidu Netdisk.

Mitigation: Confirm file selection, destination path, and token scope before execution, especially for confidential or regulated data.

## Reference(s):

- [Baidu Netdisk Open Platform App Console](https://pan.baidu.com/union/console/applist)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces upload commands and status guidance; the bundled script writes resumable upload state beside the selected source file while uploads are in progress.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
