## Description: <br>
Searches Gequhai for songs, rankings, and download links, then can send direct music downloads to a configured Synology NAS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anlinxi](https://clawhub.ai/user/anlinxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal media-library operators use this skill to search Gequhai, review song rankings, retrieve direct or netdisk download links, and queue supported downloads to a Synology NAS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports embedded Synology NAS credentials. <br>
Mitigation: Rotate or remove the embedded credentials before use and provide NAS access through user-controlled secrets or environment configuration. <br>
Risk: The security scan reports unauthenticated NAS workflows that can download, rename, or move files. <br>
Mitigation: Add authentication, restrict operations to an app-owned music folder, and require explicit confirmation before downloads or NAS file changes. <br>
Risk: The artifact includes background rename and move automation for downloaded files. <br>
Mitigation: Disable background automation unless it is explicitly needed and review pending rename or move queues before processing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anlinxi/gequhai-music) <br>
- [Publisher profile](https://clawhub.ai/user/anlinxi) <br>
- [Gequhai website](https://www.gequhai.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON responses with optional shell command examples and service API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include song metadata, rankings, direct download URLs, netdisk links, NAS task status, and rename queue status.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
