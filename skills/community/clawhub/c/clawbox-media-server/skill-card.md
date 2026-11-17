## Description:

Clawbox Media Server provides bidirectional LAN file sharing for AI agents through a local static file server and browser-based upload server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techthrasher](https://clawhub.ai/user/techthrasher)

### License/Terms of Use:


## Use Case:

Developers and AI agents use this skill to exchange files with users on a trusted LAN when inline media transfer is unavailable, including serving generated files and receiving uploads for processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated file-sharing services can allow anyone who can reach the configured ports to upload or download files.

Mitigation: Run only on trusted networks, bind to localhost or a specific trusted interface, and use firewall rules to limit access.

Risk: Shared directories and directory listings can expose sensitive filenames or file contents.

Mitigation: Avoid placing sensitive files in the shared directory and remove files when sharing is complete.

Risk: Auto-started services can keep file sharing available beyond the current session.

Mitigation: Disable or remove the systemd user services when the sharing workflow is finished.

Risk: Uploads can consume local disk space.

Mitigation: Monitor disk usage and clean the shared directory regularly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/techthrasher/skills/clawbox-media-server)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in local files, upload and download URLs, and optional systemd user services when the provided scripts are run.]

## Skill Version(s):

1.0.1 (source: server release metadata, CHANGELOG, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
