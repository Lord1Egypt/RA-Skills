## Description: <br>
Searches 1lou for movie or TV resources, helps the user choose a result, downloads torrent files, and adds selected downloads to a qBittorrent instance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluepop1991-cloud](https://clawhub.ai/user/bluepop1991-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals managing a private media library use this skill to search 1lou for movies or TV shows, review filtered results, and add a selected torrent to qBittorrent on a Synology NAS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill evidence reports an embedded qBittorrent password. <br>
Mitigation: Remove and rotate the password, then provide credentials through a secret store or prompt-time input. <br>
Risk: The skill can add torrent downloads to a private qBittorrent server. <br>
Mitigation: Use only in a private, controlled environment; confirm each torrent and destination path before adding it. <br>
Risk: Downloaded torrent files and watchlist entries may persist on local storage. <br>
Mitigation: Restrict downloads to a dedicated temporary folder and provide clear controls to view and delete watchlist entries. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with result tables and inline shell/API commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before selecting a download; may update a local drama watchlist.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
