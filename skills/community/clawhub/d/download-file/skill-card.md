## Description:

Download large files from HTTP/HTTPS URLs with resume support, progress monitoring, and timeout handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moony320](https://clawhub.ai/user/moony320)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to download HTTP/HTTPS files, especially large files such as installers, datasets, media, and documents, with resumable curl commands, progress monitoring, timeouts, and result checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloader commands may use untrusted URLs, filenames, or destination paths without enough validation or containment.

Mitigation: Use only trusted URLs and destination paths, avoid attacker-supplied filenames or paths, check before overwriting, and write downloads inside a dedicated downloads directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moony320/skills/download-file)
- [Publisher profile](https://clawhub.ai/user/moony320)

## Skill Output:

**Output Type(s):** [shell commands, guidance, configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume curl is available and a trusted URL and destination path are supplied.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
