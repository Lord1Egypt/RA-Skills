## Description:

Baidu Netdisk helps agents list, search, extract shared links, transfer shared files, create directories, and manage files in a Baidu Netdisk account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilei0311](https://clawhub.ai/user/lilei0311)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users can use this skill to let an OpenClaw agent operate Baidu Netdisk content, including browsing files, searching storage, extracting share links, transferring shared files, creating directories, and performing reviewed file-management actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses BDUSS and STOKEN session credentials that can provide broad access to a Baidu Netdisk account.

Mitigation: Install only in trusted environments, prefer a dedicated test account, treat the credentials like account passwords, avoid committing config.json, and restrict file permissions.

Risk: The skill can modify cloud files through delete, rename, move, transfer, and directory creation operations.

Mitigation: Review the exact path and action before allowing an agent to invoke file-changing commands, especially delete, rename, move, and transfer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilei0311/skills/baidunetdisk-skill)
- [Baidu Netdisk](https://pan.baidu.com)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON command results and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BDUSS and STOKEN credentials supplied through config.json or environment variables.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
