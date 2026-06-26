## Description: <br>
Manage qBittorrent download tasks on FeiNiu NAS by listing torrents and adding magnet links or torrent files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geniusfox](https://clawhub.ai/user/geniusfox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
NAS users and operators use this skill to inspect qBittorrent download status and add new download tasks on a FeiNiu NAS over SSH. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The add-download flow can expose NAS control to unsafe remote shell execution when given crafted magnet links or unsafe credential values. <br>
Mitigation: Avoid untrusted magnet links and fix shell quoting and form encoding before using the add command against a real NAS. <br>
Risk: The qBittorrent WebUI password is stored directly in the shell script configuration. <br>
Mitigation: Move the password to a local secret source or protected environment variable and restrict file permissions. <br>
Risk: The skill performs NAS operations over SSH and can affect qBittorrent downloads on the target system. <br>
Mitigation: Use a restricted NAS account and SSH key, verify the host and Unix socket settings, and review commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/geniusfox/fnnas-download) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-configured NAS host, SSH key access, qBittorrent Unix socket path, and WebUI password.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
