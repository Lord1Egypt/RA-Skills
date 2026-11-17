## Description:

A tool to manage Baidu Wangpan (Baidu Netdisk) files using the official Baidu Open API, including quota checks, file listing, search, download link generation, and file management actions such as mkdir, rename, move, delete, and upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyi-3](https://clawhub.ai/user/zhangyi-3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to authenticate with a user-provided Baidu developer app and manage Baidu Wangpan files. It supports storage inspection, file discovery, download-link generation, and basic cloud-file operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AppKey, SecretKey, authorization codes, access tokens, refresh tokens, and token-bearing download URLs.

Mitigation: Treat credentials and generated URLs as sensitive, keep them out of shared chat or logs, and rotate or revoke Baidu credentials if exposed.

Risk: The skill can modify cloud storage through upload, delete, move, rename, and mkdir operations.

Mitigation: Confirm the target path and intended operation before execution, especially for delete, move, rename, and recursive upload requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangyi-3/skills/baidu-disk-helper)
- [Baidu Netdisk Open Platform](https://pan.baidu.com/union)
- [Baidu OAuth authorize endpoint](https://openapi.baidu.com/oauth/2.0/authorize)
- [Baidu OAuth token endpoint](https://openapi.baidu.com/oauth/2.0/token)
- [Baidu Wangpan Xpan API endpoint](https://pan.baidu.com/rest/2.0/xpan)
- [Baidu Netdisk quota API endpoint](https://pan.baidu.com/api/quota)
- [Baidu PCS API endpoint](https://d.pcs.baidu.com/rest/2.0/pcs)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper may print sensitive authorization, token-bearing download, and curl URLs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
