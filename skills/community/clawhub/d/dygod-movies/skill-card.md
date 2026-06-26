## Description: <br>
Dygod Movies helps an agent fetch DYGod movie and TV listings, search recent or high-scoring titles, and optionally add selected download links to a Synology DownloadStation NAS. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[anlinxi](https://clawhub.ai/user/anlinxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using a local media workflow can ask an agent to find recent or high-rated DYGod movies and TV shows, inspect metadata and download links, and create Synology DownloadStation tasks after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports hardcoded Synology NAS credentials and HTTP-based NAS authentication. <br>
Mitigation: Replace and rotate the embedded credentials before use, move NAS configuration to user-supplied secrets, and use HTTPS or a trusted private network where available. <br>
Risk: The artifact can create and delete Synology DownloadStation tasks. <br>
Mitigation: Require explicit user confirmation before each download or deletion and restrict allowed URI schemes and destination folders. <br>
Risk: The FastAPI service exposes download functionality without artifact-provided authentication and uses permissive CORS settings. <br>
Mitigation: Add authentication, bind the service to trusted interfaces, and narrow allowed origins before deployment. <br>
Risk: The release evidence advises dependency pinning. <br>
Mitigation: Pin and review Python dependencies before installing or running the service. <br>


## Reference(s): <br>
- [ClawHub Dygod Movies release page](https://clawhub.ai/anlinxi/dygod-movies) <br>
- [ClawHub publisher profile for anlinxi](https://clawhub.ai/user/anlinxi) <br>
- [DYGod movie listing source](https://dygod.net/html/gndy/dyzz/) <br>
- [DYGod site](https://dygod.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, API calls] <br>
**Output Format:** [Markdown summaries, JSON records, shell command examples, and FastAPI JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include external download URIs such as magnet, ftp, ed2k, and torrent links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
