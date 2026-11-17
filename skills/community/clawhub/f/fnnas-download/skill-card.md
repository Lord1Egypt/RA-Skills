## Description:

Manage qBittorrent download tasks on FeiNiu NAS, including listing torrents and adding magnet links or torrent files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geniusfox](https://clawhub.ai/user/geniusfox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and NAS operators use this skill to manage qBittorrent downloads on a FeiNiu NAS through SSH, including reviewing active torrents and adding new magnet or torrent-file tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The qBittorrent password is handled in the shell script.

Mitigation: Move the qBittorrent password out of the script and avoid using admin credentials.

Risk: Remote SSH and curl calls can treat untrusted magnet-link text as shell syntax.

Mitigation: Quote inputs rigorously or redesign the calls so magnet links are passed as data, not shell-interpreted command text.

Risk: Temporary qBittorrent cookie and torrent files are written to shared paths.

Mitigation: Use private temporary files with cleanup for cookies and copied torrent files.

Risk: The script can add downloads or copy torrent files to the NAS without a separate confirmation step.

Mitigation: Require explicit confirmation before adding downloads or copying torrent files to the NAS.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/geniusfox/skills/fnnas-download)
- [ClawHub publisher profile](https://clawhub.ai/user/geniusfox)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for running a Bash helper script that calls SSH, scp, curl, and Python to inspect or add qBittorrent tasks.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
