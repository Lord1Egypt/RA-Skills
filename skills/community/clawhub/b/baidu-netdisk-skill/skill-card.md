## Description: <br>
Baidu Netdisk file management for OpenClaw, including file listing, search, download-link retrieval, upload, and OAuth 2.0 authorization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niukesi](https://clawhub.ai/user/niukesi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to Baidu Netdisk, list and search cloud files, retrieve download links, and upload selected local files through OAuth or configured API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles long-lived Baidu Netdisk access and refresh tokens. <br>
Mitigation: Prefer the OAuth flow or environment variables over command-line secrets, set a unique ENCRYPTION_KEY before use, and protect the local config file. <br>
Risk: Upload behavior can write to remote Baidu Netdisk paths and may overwrite existing remote files. <br>
Mitigation: Review upload targets carefully before execution and use least-privilege Baidu API credentials where available. <br>
Risk: The release security verdict is suspicious because security details are overstated or under-disclosed. <br>
Mitigation: Review the published security guidance and scan results before deployment, especially credential storage and remote file-write behavior. <br>
Risk: Local test or configuration commands may expose secrets in shared logs. <br>
Mitigation: Avoid running test or setup commands with visible secrets in shared terminals, CI logs, or shell history. <br>


## Reference(s): <br>
- [Baidu Netdisk Skill on ClawHub](https://clawhub.ai/niukesi/baidu-netdisk-skill) <br>
- [Quick Start Guide](docs/QUICKSTART.md) <br>
- [Security Notes](SECURITY.md) <br>
- [Baidu Open Platform Console](https://pan.baidu.com/union/console) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text with file metadata, status messages, configuration prompts, and download URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local files for upload and may write encrypted OAuth tokens to local config storage.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
