## Description:

Baidunetdisk Skill lets an agent manage Baidu Netdisk files, including listing, searching, extracting share links, transferring shared files, creating folders, renaming, moving, and deleting files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilei0311](https://clawhub.ai/user/lilei0311)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to operate a Baidu Netdisk account from OpenClaw workflows. It is intended for file discovery, share-link extraction, transfers into the user's netdisk, folder creation, and file management actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires BDUSS and STOKEN credentials that can provide full Baidu Netdisk account access.

Mitigation: Use environment variables or a protected secret store instead of committing credentials to config.json, and prefer a low-value or test account when possible.

Risk: The skill can delete, move, rename, transfer, and create files or directories without built-in confirmation safeguards.

Mitigation: Require explicit user approval before destructive or account-changing actions, especially delete, move, rename, transfer, and directory creation.

Risk: Broad invocation triggers could cause unintended account operations from general netdisk-related prompts.

Mitigation: Narrow invocation triggers and review planned file operations before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilei0311/skills/baidunetdisk)
- [Baidu Netdisk web service](https://pan.baidu.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON command results and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Baidu Netdisk BDUSS and STOKEN credentials; command results include success flags, file metadata, messages, and error strings.]

## Skill Version(s):

1.0.2 (source: release metadata, skill.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
