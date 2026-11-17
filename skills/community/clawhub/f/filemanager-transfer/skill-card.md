## Description:

Provides an agent workflow for transferring files through a FileManager service, including upload, password-protected sharing, and download by file ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrknow001](https://clawhub.ai/user/mrknow001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to move files between a remote agent environment and a user when normal chat or IM channels cannot transfer files. It guides setup of the FileManager service, then uses the included Python helper or documented API calls to upload, share, and download files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a real-looking FileManager bearer credential in scripts/.env.

Mitigation: Replace scripts/.env with a local least-privileged AppKey before installation, rotate the exposed key if it was ever valid, and avoid printing AppKeys in chat, logs, or final replies.

Risk: File transfer over an HTTP or broadly bound endpoint can expose files or credentials when used outside a local environment.

Mitigation: Use HTTPS for non-local endpoints, bind the service to localhost unless remote access is intentionally hardened, and prefer short-lived password-protected shares.

Risk: The setup flow depends on downloading an external FileManager binary.

Mitigation: Install only a pinned FileManager release after verifying its checksum or other trusted integrity signal.

Risk: Downloads can write files to implicit or unsafe local paths.

Mitigation: Choose explicit output paths in writable directories and confirm the FileManager file ID points to the intended file before downloading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrknow001/skills/filemanager-transfer)
- [FileManager releases](https://github.com/mrknow001/FileManager/releases)
- [Install and start guide](references/install-and-start.md)
- [Transfer script guide](references/transfer-script.md)
- [API reference](references/api.md)
- [Troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON transfer results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include FileManager share URLs, share passwords, file IDs, expiration times, and local save paths; AppKeys should not be exposed.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
