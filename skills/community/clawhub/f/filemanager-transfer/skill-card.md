## Description: <br>
Provides FileManager-based file upload, password-protected sharing, and download workflows between an agent environment and a user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrknow001](https://clawhub.ai/user/mrknow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to move files between a remote agent environment and a user by uploading files to a FileManager service, creating password-protected share links, or downloading files by FileManager file ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release packages a FileManager AppKey. <br>
Mitigation: Replace and rotate the packaged AppKey before use, and avoid printing real AppKeys in chat, logs, or final responses. <br>
Risk: The skill supports network-exposed file sharing. <br>
Mitigation: Bind the service to localhost unless remote exposure is intentional, and use firewall rules, TLS, or a trusted tunnel for remote access. <br>
Risk: Shared or downloaded files may be sensitive or untrusted. <br>
Mitigation: Use password-protected, short-lived shares, avoid putting real share passwords in shell commands, and inspect downloaded files before trusting them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrknow001/filemanager-transfer) <br>
- [FileManager releases](https://github.com/mrknow001/FileManager/releases) <br>
- [API reference](references/api.md) <br>
- [Install and start](references/install-and-start.md) <br>
- [Transfer script](references/transfer-script.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output from the transfer script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include share URLs, share passwords, FileManager file IDs, and local save paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
