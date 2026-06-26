## Description: <br>
BT Download helps agents use aria2 RPC to download magnet links, torrent files, and standard URLs, then monitor and stop seeding tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n0nsense11](https://clawhub.ai/user/n0nsense11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to check or install aria2, start a local aria2 RPC service, add BT, magnet, or HTTP download tasks, monitor seeding status, and stop seeding when a target ratio is reached. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install system packages and start a persistent aria2 background service. <br>
Mitigation: Review the exact commands before use, require explicit confirmation for sudo package installation and daemon startup, and document how to stop the service. <br>
Risk: The aria2 RPC service can become network-facing if configured broadly. <br>
Mitigation: Bind RPC access to localhost where possible, require authentication, and verify exposed ports before using the downloader. <br>
Risk: Downloads, torrent activity, and logs can write files to local storage. <br>
Mitigation: Confirm the download directory before starting tasks and define a cleanup process for downloaded files and aria2 logs. <br>


## Reference(s): <br>
- [BT Download on ClawHub](https://clawhub.ai/n0nsense11/bt-download) <br>
- [aria2 project homepage](https://aria2.github.io) <br>
- [ngosang tracker list](https://raw.githubusercontent.com/ngosang/ngosang-trackerslist/master/trackers_best.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON tool results and human-readable status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include confirmation prompts for download directory selection and status summaries for active downloads and seeding tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
